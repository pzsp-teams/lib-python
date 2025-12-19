import json
import pathlib
import platform
import subprocess
import threading
from typing import Any

from teams_lib_pzsp2_z1 import config
from teams_lib_pzsp2_z1.services.channels import ChannelsService


class TeamsClient:
    def __init__(
        self,
        auto_init: bool = True,
        env_path: str | None = None,
        cache_enabled: bool = False,
        cache_path: str | None = None,
    ):
        self._lock = threading.Lock()

        self.proc = subprocess.Popen(  # noqa: S603
            [str(self._binary())],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )

        self.env_path = env_path
        self.channels = ChannelsService(self)

        if auto_init:
            self.init_client(cache_enabled, cache_path)

    def _binary(self):
        base = pathlib.Path(__file__).parent / "bin"
        osname = platform.system()

        if osname == "Windows":
            return base / "teamsClientLib_windows.exe"
        elif osname == "Linux":
            return base / "teamsClientLib_linux"
        else:
            raise RuntimeError("Unsupported OS")

    def init_client(
        self, cache_enabled: bool = False, cache_path: str | None = None
    ) -> Any:
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
                "cacheEnabled": cache_enabled,
                "cachePath": cache_path,
            },
        )

    def init_fake_client(self, mock_server_url: str) -> Any:
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
        payload = {"type": cmd_type}
        if method:
            payload["method"] = method
        if params:
            payload["params"] = params
        if config:
            payload["config"] = config

        json_payload = json.dumps(payload)

        # Critical section to avoid interleaving requests/responses
        with self._lock:
            try:
                self.proc.stdin.write(json_payload + "\n")
                self.proc.stdin.flush()

                raw_response = self.proc.stdout.readline()
            except BrokenPipeError:
                raise RuntimeError("Go process crashed or closed connection")  # noqa: B904

            if not raw_response:
                raise RuntimeError("Go process returned empty response")

            res = json.loads(raw_response)

        if "error" in res and res["error"]:
            raise RuntimeError(f"Go Error: {res['error']}")

        return res.get("result")

    def close(self):
        self.proc.terminate()
