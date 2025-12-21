import os
from dataclasses import dataclass

from dotenv import load_dotenv


class AuthConfigurationError(Exception):
    pass


@dataclass
class SenderConfig:
    max_retries: int = 3
    next_retry_delay: int = 2
    timeout: int = 10


@dataclass
class AuthConfig:
    client_id: str
    tenant: str
    email: str
    scopes: list[str]
    auth_method: str


def load_auth_config(env_path: str | None = None) -> AuthConfig:
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
    return os.getenv(key, fallback)


def validate(cfg: AuthConfig):
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
