import random
from typing import Any

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
    def __init__(self, config: TelegramConfig) -> None:
        self.telegram_token = config.token

    def run(self) -> None:
        app = (
            Application.builder()
            .get_updates_read_timeout(5)
            .token(self.telegram_token)
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
