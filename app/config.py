import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv, find_dotenv



@dataclass
class Settings:
    token: str
    vault_dir: Path
    note_filename: str = "tgToObsd.md"
    whisper_model: str = "small"
    whisper_device: str = "cpu"
    time_format: str = "%Y-%m-%d %H:%M"

def load_settings() -> Settings:
    load_dotenv(find_dotenv())

    token = os.getenv("TELEGRAM_TOKEN")
    if not token or ":" not in token:
        raise RuntimeError("TELEGRAM_TOKEN не задан или некорректен (.env).")

    vault_path = os.getenv("VAULT_PATH")
    if not vault_path:
        raise RuntimeError("VAULT_PATH не задан (.env).")

    settings = Settings(
        token=token,
        vault_dir=Path(vault_path).expanduser(),
        note_filename=os.getenv("NOTE_FILENAME", "tgToObsd.md"),
        whisper_model=os.getenv("WHISPER_MODEL", "small"),
        whisper_device=os.getenv("WHISPER_DEVICE", "cpu"),
        time_format=os.getenv("TIME_FORMAT", "%Y-%m-%d %H:%M"),
    )

    settings.vault_dir.mkdir(parents=True, exist_ok=True)
    return settings
