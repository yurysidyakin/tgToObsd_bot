import asyncio
from typing import Optional
from .whisper_model import get_model

async def transcribe_file(path: str, language: str = "ru", model_name: str = "small", device: str = "cpu") -> Optional[str]:
    loop = asyncio.get_running_loop()
    model = get_model(model_name, device)

    def _run():
        segments, _ = model.transcribe(
            path,
            language=language,
            beam_size=5,  # Настройка для улучшения качества
            temperature=0.0,
        )
        return " ".join(segment.text.strip() for segment in segments)

    return await loop.run_in_executor(None, _run)
