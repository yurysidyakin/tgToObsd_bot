from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

MAIN_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Команда 1"), KeyboardButton(text="Команда 2")],
    ],
    resize_keyboard=True
)

START_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Запустить")]],  # Изменён текст кнопки
    resize_keyboard=True,
    one_time_keyboard=False,
)
