from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from bs_nats_updater import NatsConfig

if TYPE_CHECKING:
    from bs_config import Env


@dataclass
class SentryConfig:
    dsn: str | None
    release: str

    @classmethod
    def from_env(cls, env: Env) -> Self:
        return cls(
            dsn=env.get_string("SENTRY_DSN"),
            release=env.get_string("APP_VERSION", default="debug"),
        )


@dataclass
class TelegramConfig:
    token: str

    @classmethod
    def from_env(cls, env: Env) -> Self:
        return cls(
            token=env.get_string("TOKEN", required=True),
        )


@dataclass
class Config:
    nats: NatsConfig
    sentry: SentryConfig
    telegram: TelegramConfig

    @classmethod
    def from_env(cls, env: Env) -> Self:
        return cls(
            nats=NatsConfig.from_env(env.scoped("NATS_")),
            sentry=SentryConfig.from_env(env),
            telegram=TelegramConfig.from_env(env.scoped("TELEGRAM_")),
        )
