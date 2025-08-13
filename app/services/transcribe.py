import asyncio
from typing import Optional
from .whisper_model import get_model  # Удалён импорт model

async def transcribe_file(path: str, language: str = "ru", model_name: str = "small", device: str = "cpu") -> Optional[str]:
    loop = asyncio.get_running_loop()
    model = get_model(model_name, device)

    def _run():
        result = model.transcribe(
            path,
            language=language,
            fp16=False,
            temperature=0.0,
            task="transcribe",
        )
        return (result.get("text") or "").strip()

    return await loop.run_in_executor(None, _run)
