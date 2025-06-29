import asyncio
import logging

import sentry_sdk
import uvloop
from bs_config import Env

from app.bot import Bot
from app.config import Config, SentryConfig

_logger = logging.getLogger(__package__)


def _setup_logging() -> None:
    logging.basicConfig()

    logging.root.level = logging.WARNING
    logging.getLogger(__package__).level = logging.DEBUG


def _setup_sentry(config: SentryConfig) -> None:
    dsn = config.dsn
    if not dsn:
        _logger.warning("Sentry DSN not found")
        return

    sentry_sdk.init(
        dsn=dsn,
        release=config.release,
    )


def main() -> None:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    _setup_logging()
    env = Env.load(include_default_dotenv=True)
    config = Config.from_env(env)
    _setup_sentry(config.sentry)

    bot = Bot(config.telegram, config.nats)
    bot.run()


if __name__ == "__main__":
    main()
