from aiogram import Dispatcher
from app.config import Settings
from .start import router as start_router
from .voice import get_voice_router

def setup_routers(dp: Dispatcher, settings: Settings):
    dp.include_router(start_router)
    dp.include_router(get_voice_router(settings))