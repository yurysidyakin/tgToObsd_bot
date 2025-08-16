import asyncio
from app.config import load_settings
from app.bot import create_bot, create_dispatcher
from app.handlers import setup_routers
from app.keyboards.commands import setup_bot_commands

async def main():
    
    settings = load_settings()
    bot = create_bot(settings)
    dp = create_dispatcher()

    # Роутеры (хендлеры)
    setup_routers(dp, settings)

    # Команды в меню Telegram
    await setup_bot_commands(bot)

    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
