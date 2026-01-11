import json
import pathlib
import platform
import subprocess
import sys
import threading
from typing import Any

from teams_lib_pzsp2_z1 import config
from teams_lib_pzsp2_z1.services.channels import ChannelsService
from teams_lib_pzsp2_z1.services.chats import ChatsService
from teams_lib_pzsp2_z1.services.teams import TeamsService


class TeamsClient:
    """The main entry point for interacting with the Microsoft Teams library.

    This class manages the lifecycle of the underlying Go subprocess, handles
    Inter-Process Communication (IPC) via JSON over stdin/stdout, and exposes
    high-level services for Teams, Channels, and Chats.

    **Architecture:**
    The Python library acts as a frontend wrapper. It spawns a compiled Go binary
    (`teamsClientLib`) as a subprocess. Commands are serialized to JSON and sent
    to the Go process, which executes the actual Microsoft Graph API calls and
    returns the results.

    Attributes:
        channels (ChannelsService): Service for managing channels.
        teams (TeamsService): Service for managing teams.
        chats (ChatsService): Service for managing chats and messages.
    """


    def __init__(
        self,
        auto_init: bool = True,
        env_path: str | None = None,
        cache_mode: config.CacheMode = config.CacheMode.DISABLED,
        cache_path: str | None = None,
    ):
        """Initializes the TeamsClient and spawns the Go subprocess.

        Args:
            auto_init (bool, optional): If True, automatically calls `init_client`
                using configuration loaded from the environment. Defaults to True.
            env_path (str | None, optional): Path to the `.env` file containing
                credentials (CLIENT_ID, TENANT_ID, etc.). If None, defaults are used.
            cache_mode (config.CacheMode, optional): The caching strategy to use
                (e.g., DISABLED, IN_MEMORY, DISK). Defaults to DISABLED.
            cache_path (str | None, optional): File path for the cache (required if
                cache_mode is DISK). Defaults to None.

        Raises:
            RuntimeError: If the operating system is not supported (only Windows/Linux).
        """

        self._lock = threading.Lock()

        # Spawn the Go binary in a subprocess with piped IO
        self.proc = subprocess.Popen(  # noqa: S603
            [str(self._binary())],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stderr, # Pass Go logs directly to stderr
            text=True,
            bufsize=1,
        )

        self.env_path = env_path

        # Initialize services with a reference to self (to access .execute())
        self.channels = ChannelsService(self)
        self.teams = TeamsService(self)
        self.chats = ChatsService(self)

        self.is_cache_enabled = cache_mode != config.CacheMode.DISABLED

        if auto_init:
            self.init_client(cache_mode, cache_path)

    def _binary(self):
        """Resolves the path to the correct Go binary for the current OS.

        Returns:
            pathlib.Path: The absolute path to the executable.

        Raises:
            RuntimeError: If the OS is not Windows or Linux.
        """

        base = pathlib.Path(__file__).parent / "bin"
        osname = platform.system()

        if osname == "Windows":
            return base / "teamsClientLib_windows.exe"
        elif osname == "Linux":
            return base / "teamsClientLib_linux"
        else:
            raise RuntimeError("Unsupported OS")

    def init_client(
        self,
        cache_mode: config.CacheMode = config.CacheMode.DISABLED,
        cache_path: str | None = None,
    ) -> Any:
        """Initializes the Go backend with authentication and cache configuration.

        This method sends the 'init' command to the Go process, which sets up the
        MSAL token provider and the Graph Service Client.

        Args:
            cache_mode (config.CacheMode): The caching strategy.
            cache_path (str | None): Path to the cache file (if applicable).

        Returns:
            Any: The initialization result from the Go process.

        Raises:
            RuntimeError: If the Go process reports an initialization error.
        """

        sender_config = config.SenderConfig()
        auth_config = config.load_auth_config(self.env_path)
        return self.execute(
            cmd_type="init",
            config={
                "senderConfig": {
                    "maxRetries": sender_config.max_retries,
                    "nextRetryDelay": sender_config.next_retry_delay,
                    "timeout": sender_config.timeout,
                },
                "authConfig": {
                    "clientID": auth_config.client_id,
                    "tenant": auth_config.tenant,
                    "email": auth_config.email,
                    "scopes": auth_config.scopes,
                    "authMethod": auth_config.auth_method,
                },
                "cacheMode": cache_mode.value,
                "cachePath": cache_path,
            },
        )

    def init_fake_client(self, mock_server_url: str) -> Any:
        """Initializes the Go backend in test mode using a mock server.

        This bypasses real MSAL authentication and directs Graph API calls to
        the provided local URL. [For testing purposes only]

        Args:
            mock_server_url (str): The URL of the mock HTTP server.

        Returns:
            Any: The result of the initialization.
        """

        return self.execute(
            cmd_type="init",
            params={
                "mockServerUrl": mock_server_url,
            },
        )

    def execute(
        self,
        cmd_type: str,
        method: str | None = None,
        config: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Executes a command on the Go subprocess via JSON-IPC.

        This is the low-level bridge method used by services to communicate with the backend.
        It handles serialization, thread-safe writing to stdin, reading from stdout,
        and error propagation.

        Args:
            cmd_type (str): The type of command (e.g., "init", "request").
            method (str | None): The specific API method to call (e.g., "listChannels").
                Required if cmd_type is "request".
            config (dict | None): Configuration payload (used primarily for initialization).
            params (dict | None): Parameters for the method call (e.g., teamRef, body).

        Returns:
            Any: The 'result' field from the Go response.

        Raises:
            RuntimeError: If the Go process crashes, closes the pipe, returns an empty response,
                or explicitly reports an error in the "error" field.
        """

        payload = {"type": cmd_type}
        if method:
            payload["method"] = method
        if params:
            payload["params"] = params
        if config:
            payload["config"] = config

        json_payload = json.dumps(payload)

        # Critical section to avoid interleaving requests/responses#
        # (e.g., thread A writes request A, thread B writes request B,
        # then thread A reads response B).
        with self._lock:
            try:
                self.proc.stdin.write(json_payload + "\n")
                self.proc.stdin.flush()

                print("Sent to Go process:", json_payload)  # Debug print

                raw_response = self.proc.stdout.readline()

                print("Received from Go process:", raw_response.strip())  # Debug print
            except BrokenPipeError:
                raise RuntimeError("Go process crashed or closed connection")  # noqa: B904

            if not raw_response:
                raise RuntimeError("Go process returned empty response")

            res = json.loads(raw_response)

        if "error" in res and res["error"]:
            raise RuntimeError(f"Go Error: {res['error']}")

        return res.get("result")

    def close(self):
        """Gracefully closes the Go backend, ensuring cache is synced.

        Sends a 'close' command to the Go process, which triggers `lib.Close()`
        to wait for background cache operations. Then terminates the process.
        """

        if self.is_cache_enabled:
            with self._lock:
                if self.proc.poll() is None:
                    try:
                        payload = json.dumps({"type": "close"}) + "\n"
                        self.proc.stdin.write(payload)
                        self.proc.stdin.flush()
                    except (BrokenPipeError, OSError):
                        pass

            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()

            try:
                if self.proc.stdin:
                    self.proc.stdin.close()
                if self.proc.stdout:
                    self.proc.stdout.close()
            except (OSError, ValueError):
                pass
        else:
            self.proc.terminate()
            self.proc.wait()
