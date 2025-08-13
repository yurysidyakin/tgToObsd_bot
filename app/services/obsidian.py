import datetime
from pathlib import Path
import aiofiles
from app.config import Settings  # Заменён импорт VAULT_PATH и NOTE_FILENAME на Settings

async def save_to_obsidian(text: str):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    note_file = Path(Settings.VAULT_PATH) / Settings.NOTE_FILENAME
    async with aiofiles.open(note_file, 'a', encoding='utf-8') as f:
        await f.write(f'\n---\n**{now}**\n{text}\n')

async def append_note(vault_dir: Path, note_filename: str, time_format: str, content: str):
    note_path = vault_dir / note_filename
    now = datetime.datetime.now().strftime(time_format)
    async with aiofiles.open(note_path, "a", encoding="utf-8") as f:
        await f.write(f"\n---\n**{now}**\n{content}\n")
