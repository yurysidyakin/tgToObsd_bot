from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove
from app.keyboards.reply import START_KB

router = Router(name="start")

@router.message(CommandStart())  # Обработчик для команды /start
async def start_handler_command(message: types.Message):
    await message.answer(
        "Привет! Я бот для расшифровки голосовых сообщений. "
        "Просто отправьте мне голосовое сообщение, и я добавлю текст в вашу заметку Obsidian. "
        "Если у вас есть вопросы, просто напишите!",
        reply_markup=ReplyKeyboardRemove()  # Удаление старой клавиатуры
    )

@router.message(lambda message: message.text == "Запустить")  # Обработчик для текста кнопки "Запустить"
async def start_handler_button(message: types.Message):
    await message.answer(
        "Привет! Пришли мне голосовое сообщение — добавлю расшифровку в Obsidian.",
        reply_markup=START_KB
    )
