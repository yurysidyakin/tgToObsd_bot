from aiogram import Bot
from aiogram.types import BotCommand

async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="help", description="Получить помощь")
    ])

