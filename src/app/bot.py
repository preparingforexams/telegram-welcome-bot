import random
import signal
from typing import Any

from bs_nats_updater import NatsConfig, create_updater
from telegram import Update
from telegram.ext import Application, ChatMemberHandler

from app.config import TelegramConfig

_FILE_IDS = [
    # Saufen
    "CQACAgIAAxkDAAMGYAQ3hb7J8740ND6tbnwf9m7o7s8AAooKAAIVSiBITKyTWpm8keweBA",
    # Alkpause
    "CQACAgIAAxkDAAMHYAQ3qNopch3GK9ZgfFckciIikHAAAosKAAIVSiBICtvI62oH3_seBA",
    # Trinken
    "CQACAgIAAxkDAAMIYAQ-CYlzFAABOG5HIV4Z52M2pOpsAAKYCgACFUogSOiJTDCf_HlXHgQ",
    # Aktuelle Situation
    "CQACAgIAAxkDAAMnYBGy7xpSrNxeVGqU-hKkmvKVQVoAAlcLAAKJO4hIuBttZLzEECYeBA",
    # Komasaufen
    "CQACAgIAAxkBAANZYeaJDEyC6yYa1Qe8RYxfyawvb_IAAmoWAAItbjBLXvJA_jHnjIkjBA",
]


class Bot:
    def __init__(
        self,
        config: TelegramConfig,
        nats_config: NatsConfig,
    ) -> None:
        self.__nats_config = nats_config
        self.__telegram_token = config.token

    def run(self) -> None:
        app = (
            Application.builder()
            .updater(create_updater(self.__telegram_token, self.__nats_config))
            .build()
        )
        app.add_handler(
            ChatMemberHandler(
                self._handle_chat_member,
                ChatMemberHandler.CHAT_MEMBER,
            )
        )
        app.run_polling(
            allowed_updates=[Update.CHAT_MEMBER],
            stop_signals=[
                signal.SIGTERM,
                signal.SIGINT,
            ],
        )

    async def _handle_chat_member(self, update: Update, _: Any) -> None:
        chat_member = update.chat_member
        if chat_member is None:
            return

        new_member = chat_member.new_chat_member
        if new_member is None:
            return

        file_id = random.choice(_FILE_IDS)
        user = new_member.user
        username = user.first_name
        if user["id"] == 1365395775:
            username = "Katerine"

        await update.get_bot().send_audio(
            chat_id=chat_member.chat.id,
            audio=file_id,
            allow_sending_without_reply=True,
            caption=f"Willkommen, {username}",
        )
