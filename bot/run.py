import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import BotCommand, InlineKeyboardButton, Message

from settings import settings

logger = logging.getLogger(__name__)


bot = Bot(token=settings.TOKEN)
dp = Dispatcher(storage=MemoryStorage())
commands = [BotCommand(command="start", description="Start the bot")]


@dp.message(CommandStart())
async def command_start_handler(msg: Message) -> None:
    try:
        text = (f"Welcome, {msg.from_user.username}!\n"
                f"Твой id={msg.from_user.id}\n"
                "Использую этот номер при в приложении."
                )
        button = InlineKeyboardButton(
            text="Зарегистрироваться",
            url=settings.APP_URL,
        )
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[button]])
        await msg.answer(text=text, reply_markup=keyboard)

    except Exception:
        logger.exception("Ошибка при отправке сообщения")


async def main():
    try:
        await bot.set_my_commands(commands)
        await dp.start_polling(bot=bot, close_bot_session=True)
    except Exception:
        logger.exception("Ошибка при запуске бота")


if __name__ == "__main__":
    asyncio.run(main())
