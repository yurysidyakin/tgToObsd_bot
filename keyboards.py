from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, BotCommand

# Основная клавиатура с кнопкой "/start"
MAIN_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/start")]],
    resize_keyboard=True,
    one_time_keyboard=False,
)

# Регистрация команд в меню Telegram (иконка с "/")
async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать работу"),
    ])
