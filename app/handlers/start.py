from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router(name="start")

@router.message(CommandStart())  # Обработчик для команды /start
async def start_handler_command(message: types.Message):
    start_text = ("<b>Привет!\n</b> Я бот для расшифровки голосовых сообщений.\n" "Просто отправьте мне голосовое сообщение, и я добавлю текст в вашу заметку <b>Obsidian</b>.\n" "Если у вас есть вопросы — просто напишите!") 
    await message.answer(
        start_text
    )

