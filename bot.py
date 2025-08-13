import os
import datetime
import tempfile
import asyncio
import warnings
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiofiles
import whisper
from dotenv import load_dotenv  # Импортируем загрузчик .env

# Загружаем переменные из .env файла
load_dotenv()

# === Настройки ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # замените/используйте .env
VAULT_PATH = os.getenv("VAULT_PATH")
NOTE_FILENAME = "tgToObsd.md"

# Подавляем предупреждение про FP16 на CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU.*")

# --- Инициализация Whisper ---
model = whisper.load_model("small", device="cpu")  # small/base/tiny и т.д.

async def save_to_obsidian(text: str):
    os.makedirs(VAULT_PATH, exist_ok=True)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    note_path = os.path.join(VAULT_PATH, NOTE_FILENAME)
    async with aiofiles.open(note_path, 'a', encoding='utf-8') as f:
        await f.write(f'\n---\n**{now}**\n{text}\n')

async def handle_voice(message: types.Message, bot: Bot):
    user = message.from_user.full_name or message.from_user.first_name or str(message.from_user.id)

    with tempfile.TemporaryDirectory() as tmpdir:
        ogg_path = os.path.join(tmpdir, f'{message.voice.file_unique_id}.ogg')

        # 1) Скачиваем voice OGG (Opus)
        file_info = await bot.get_file(message.voice.file_id)
        await bot.download_file(file_info.file_path, ogg_path)

        # 2) Транскрибируем .ogg напрямую (без pydub, без конвертации)
        loop = asyncio.get_running_loop()
        def _transcribe():
            result = model.transcribe(
                ogg_path,
                language="ru",
                fp16=False,          # важно для CPU
                temperature=0.0,     # детерминированнее
            )
            return (result.get("text") or "").strip()

        text = await loop.run_in_executor(None, _transcribe)

        if not text:
            await message.answer("Не удалось распознать речь.")
            return

        # 3) Сохраняем в Obsidian
        note = f'- **{user}**: {text}'
        await save_to_obsidian(note)

    await message.answer("Готово! Текст добавлен в вашу заметку Obsidian.")

async def start_handler(message: types.Message):
    await message.answer("Привет! Пришли мне голосовое сообщение — добавлю расшифровку в Obsidian.")

def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.message(Command("start"))(start_handler)
    dp.message(lambda msg: msg.voice is not None)(handle_voice)

    print("Бот запущен...")
    asyncio.run(dp.start_polling(bot))

if __name__ == "__main__":
    main()
