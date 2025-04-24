from dataclasses import dataclass


@dataclass(frozen=True)
class Secrets:
    SECRET_KEY: str
    DB_PASSWORD: str
    EMAIL_HOST_PASSWORD: str
    SENTRY_DSN: str
