import sys
import asyncio

if sys.platform == "darwin":  # Проверка на macOS
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from app.config import load_settings, Settings
from app.handlers.start import start_handler_command, start_handler_button  # Добавлен импорт start_handler_button
from app.handlers.voice import handle_voice
from app.keyboards.commands import setup_bot_commands

def create_bot(settings: Settings) -> Bot:
    return Bot(token=settings.token)

def create_dispatcher() -> Dispatcher:
    return Dispatcher()

async def main():
    settings = load_settings()
    bot = create_bot(settings)
    dp = create_dispatcher()

    # Регистрация обработчиков
    dp.message.register(start_handler_command, CommandStart())
    dp.message.register(handle_voice, lambda message: message.voice is not None)
    dp.message.register(start_handler_button, lambda message: message.text == "Запустить")  # Регистрация обработчика кнопки

    await setup_bot_commands(bot)
    print("Бот запущен и готов к работе!")  # Сообщение о запуске бота

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
