from aiogram import Router, types
from aiogram.filters import CommandStart
from app.keyboards.reply import START_KB

router = Router(name="start")

@router.message(CommandStart())  # Обработчик для команды /start
async def start_handler_command(message: types.Message):
    await message.answer(
        "Привет! Пришли мне голосовое сообщение — добавлю расшифровку в Obsidian.",
        reply_markup=START_KB
    )

@router.message(lambda message: message.text == "Запустить")  # Обработчик для текста кнопки "Запустить"
async def start_handler_button(message: types.Message):
    await message.answer(
        "Привет! Пришли мне голосовое сообщение — добавлю расшифровку в Obsidian.",
        reply_markup=START_KB
    )
