import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, InlineKeyboardButton, Message

from settings import settings

logger = logging.getLogger(__name__)


bot = Bot(token=settings.TOKEN)
dp = Dispatcher(storage=MemoryStorage())
commands = [BotCommand(command="start", description="Start the bot")]


@dp.message(CommandStart())
async def command_start_handler(msg: Message) -> None:
    try:
        text = (
            "🎉 Welcome, *popcorn138*! 🎉\n\n"
            "🔑 Твой ID: *5312665858*\n"
            "Используй этот номер при регистрации на сайте.\n\n"
            "📩 После этого бот сможет оповещать тебя о непрочитанных сообщениях."
)
        button = InlineKeyboardButton(
            text="Зарегистрироваться",
            url=settings.APP_URL,
        )
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[button]])
        await msg.answer(text, parse_mode="Markdown")

    except Exception:
        logger.exception("Ошибка при отправке сообщения")


async def main():
    try:
        await bot.set_my_commands(commands)
        await dp.start_polling(bot, close_bot_session=True)
    except Exception:
        logger.exception("Ошибка при запуске бота")


if __name__ == "__main__":
    asyncio.run(main())
