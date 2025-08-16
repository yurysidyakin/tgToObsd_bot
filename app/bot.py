import sys
import asyncio

from aiogram.filters import Command
from aiogram import F

from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from app.config import load_settings, Settings
from app.handlers.start import start_handler_command 
from app.handlers.help import help_handler_command
from app.handlers.voice import handle_voice
from app.keyboards.commands import setup_bot_commands
from aiogram.enums import ParseMode 
from aiogram.client.default import DefaultBotProperties

def create_bot(settings: Settings) -> Bot: return Bot( token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

def create_dispatcher() -> Dispatcher:
    return Dispatcher()

async def main():
    settings = load_settings()
    bot = create_bot(settings)
    dp = create_dispatcher()

    # Регистрация обработчиков
    dp.message.register(start_handler_command, CommandStart())
    dp.message.register(help_handler_command, Command('help'))
    dp.message.register(handle_voice, F.voice)


    await setup_bot_commands(bot)
    print("Бот запущен и готов к работе!")  

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
