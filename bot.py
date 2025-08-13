import os
import datetime
import tempfile
import asyncio
import warnings
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiofiles
import whisper
from dotenv import load_dotenv, find_dotenv

from keyboards import MAIN_KB, setup_bot_commands

# Загружаем переменные из .env
load_dotenv(find_dotenv())

# === Настройки ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
VAULT_PATH = os.getenv("VAULT_PATH")
NOTE_FILENAME = os.getenv("NOTE_FILENAME")

# Проверки конфигурации
if not TELEGRAM_TOKEN or ":" not in TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN не задан или некорректен. Установите его в .env или окружении.")

if not VAULT_PATH:
    raise RuntimeError("VAULT_PATH не задан. Пропишите VAULT_PATH в .env или окружении.")

VAULT_DIR = Path(VAULT_PATH).expanduser()
VAULT_DIR.mkdir(parents=True, exist_ok=True)
NOTE_FILE = VAULT_DIR / NOTE_FILENAME

# Подавляем предупреждение про FP16 на CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU.*")

# --- Инициализация Whisper ---
model = whisper.load_model("small", device="cpu")  # small/base/tiny и т.д.

async def save_to_obsidian(text: str):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    async with aiofiles.open(NOTE_FILE, 'a', encoding='utf-8') as f:
        await f.write(f'\n---\n**{now}**\n{text}\n')

async def handle_voice(message: types.Message, bot: Bot):
    if not message.voice:
        return

    user = message.from_user.full_name or message.from_user.first_name or str(message.from_user.id)

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            ogg_path = os.path.join(tmpdir, f'{message.voice.file_unique_id}.ogg')

            # 1) Скачиваем voice OGG (Opus)
            file_info = await bot.get_file(message.voice.file_id)
            await bot.download_file(file_info.file_path, ogg_path)

            # 2) Транскрибируем .ogg напрямую
            loop = asyncio.get_running_loop()

            def _transcribe():
                result = model.transcribe(
                    ogg_path,
                    language="ru",
                    fp16=False,
                    temperature=0.0,
                    task="transcribe",
                )
                return (result.get("text") or "").strip()

            text = await loop.run_in_executor(None, _transcribe)

            if not text:
                await message.answer("Не удалось распознать речь.", reply_markup=MAIN_KB)
                return

            # 3) Сохраняем в Obsidian
            note = f'- **{user}**: {text}'
            await save_to_obsidian(note)

        await message.answer("Готово! Текст добавлен в вашу заметку Obsidian.", reply_markup=MAIN_KB)
    except FileNotFoundError as e:
        await message.answer("Ошибка при обработке аудио. Проверьте, что установлен ffmpeg.", reply_markup=MAIN_KB)
        print("ffmpeg/File error:", e)
    except Exception as e:
        await message.answer("Произошла ошибка при распознавании. Подробности в логах.", reply_markup=MAIN_KB)
        print("Transcribe error:", e)

async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Пришли мне голосовое сообщение — добавлю расшифровку в Obsidian.",
        reply_markup=MAIN_KB
    )

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    # Хендлеры
    dp.message(Command("start"))(start_handler)
    dp.message(lambda msg: msg.voice is not None)(handle_voice)

    # Настраиваем меню команд
    await setup_bot_commands(bot)

    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
