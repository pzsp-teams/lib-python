"""
Package config holds configuration structures used across the application.

This module defines data classes for authentication, request sending, and caching,
as well as utility functions to load and validate these configurations from
environment variables.
"""

import os
from dataclasses import dataclass
from enum import Enum

from dotenv import load_dotenv


class AuthConfigurationError(Exception):
    """Raised when the authentication configuration is missing or invalid."""
    pass


@dataclass
class SenderConfig:
    """Defines configuration for the HTTP request sender connecting to Microsoft Graph API.

    Attributes:
        max_retries (int): The maximum number of retry attempts for failed requests.
            Defaults to 3.
        next_retry_delay (int): The delay between retry attempts in **seconds**.
            Defaults to 2.
        timeout (int): The maximum time to wait for a request to complete in **seconds**.
            Defaults to 10.
    """

    max_retries: int = 3
    next_retry_delay: int = 2
    timeout: int = 10


@dataclass
class AuthConfig:
    """Holds configuration required for authentication via MSAL.

    All fields are required to successfully acquire tokens.

    Attributes:
        client_id (str): The Application (client) ID assigned by the Azure portal.
        tenant (str): The Directory (tenant) ID or domain.
        email (str): The email address of the user to authenticate.
        scopes (list[str]): A list of Graph API permission scopes (e.g., "User.Read").
        auth_method (str): The flow used to acquire tokens.
            Valid values are:
            * **"DEVICE_CODE"**: Prints a code to console; user visits a URL.
            * **"INTERACTIVE"**: Opens a local browser window.
    """

    client_id: str
    tenant: str
    email: str
    scopes: list[str]
    auth_method: str


class CacheMode(Enum):
    """Defines the caching strategy used by the application.

    Attributes:
        DISABLED: Caching is turned off completely.
        SYNC: Cache operations (read/write) are performed synchronously.
            Safe but may block the main thread.
        ASYNC: Cache operations are performed asynchronously in the background.
            Faster for the main thread but requires `close()` to ensure data consistency.
    """

    DISABLED = "DISABLED"
    SYNC = "SYNC"
    ASYNC = "ASYNC"

@dataclass
class CacheConfig:
    """Holds configuration for the caching layer.

    Attributes:
        mode (CacheMode): The caching strategy to use.
        path (str | None): The file path for the cache storage (e.g., JSON file).
            Required if mode is not DISABLED. Defaults to None.
    """

    mode: CacheMode
    path: str | None = None

def load_auth_config(env_path: str | None = None) -> AuthConfig:
    """Loads authentication configuration from environment variables or a .env file.

    It looks for the following environment variables:
    * `CLIENT_ID`
    * `TENANT_ID`
    * `EMAIL`
    * `SCOPES` (comma-separated, defaults to "https://graph.microsoft.com/.default")
    * `AUTH_METHOD` (defaults to "DEVICE_CODE")

    Args:
        env_path (str | None, optional): Path to the .env file. If None,
            loads from the current directory.

    Returns:
        AuthConfig: A populated and validated configuration object.

    Raises:
        AuthConfigurationError: If required variables are missing or values are invalid.
    """

    load_dotenv(env_path)

    cfg = AuthConfig(
        client_id=get_env("CLIENT_ID", ""),
        tenant=get_env("TENANT_ID", ""),
        email=get_env("EMAIL", ""),
        scopes=get_env("SCOPES", "https://graph.microsoft.com/.default").split(","),
        auth_method=get_env("AUTH_METHOD", "DEVICE_CODE"),
    )

    validate(cfg)
    return cfg


def get_env(key: str, fallback: str) -> str:
    """Retrieves an environment variable with a fallback value."""

    return os.getenv(key, fallback)


def validate(cfg: AuthConfig):
    """Validates the authentication configuration object.

    Checks for the presence of required fields and the validity of the auth method.

    Args:
        cfg (AuthConfig): The configuration object to validate.

    Raises:
        AuthConfigurationError: If `client_id`, `tenant`, or `email` are empty,
            or if `auth_method` is not supported.
    """

    missing = []
    if not cfg.client_id:
        missing.append("CLIENT_ID")
    if not cfg.tenant:
        missing.append("TENANT_ID")
    if not cfg.email:
        missing.append("EMAIL")

    if missing:
        raise AuthConfigurationError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    if cfg.auth_method not in ("DEVICE_CODE", "INTERACTIVE"):
        raise AuthConfigurationError(
            f"Invalid AUTH_METHOD: {cfg.auth_method}. Must be DEVICE_CODE or INTERACTIVE"
        )
