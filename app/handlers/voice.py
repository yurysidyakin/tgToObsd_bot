import os
import tempfile
from aiogram import Router, F, Bot, types
from app.keyboards.reply import START_KB
from app.config import load_settings  # Заменён импорт Settings на load_settings
from app.services.transcribe import transcribe_file
from app.services.obsidian import append_note

def get_voice_router(settings=None) -> Router:
    if settings is None:
        settings = load_settings()  # Используем load_settings для загрузки настроек

    router = Router(name="voice")

    @router.message(F.voice)
    async def handle_voice(message: types.Message, bot: Bot):
        user = message.from_user.full_name or message.from_user.first_name or str(message.from_user.id)

        await message.answer("Ваше сообщение обрабатывается, пожалуйста, подождите...")  # Уведомление об обработке

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                ogg_path = os.path.join(tmpdir, f"{message.voice.file_unique_id}.ogg")

                file_info = await bot.get_file(message.voice.file_id)
                await bot.download_file(file_info.file_path, ogg_path)

                text = await transcribe_file(
                    ogg_path,
                    language="ru",
                    model_name=settings.whisper_model,
                    device=settings.whisper_device,
                )

                if not text:
                    await message.answer("Не удалось распознать речь.", reply_markup=START_KB)
                    return

                note_line = f"- **{user}**: {text}"
                await append_note(
                    vault_dir=settings.vault_dir,
                    note_filename=settings.note_filename,
                    time_format=settings.time_format,
                    content=note_line,
                )

            await message.answer("Готово! Текст добавлен в вашу заметку Obsidian.", reply_markup=START_KB)
        except FileNotFoundError as e:
            await message.answer("Ошибка при обработке аудио. Проверьте, что установлен ffmpeg.", reply_markup=START_KB)
            print("ffmpeg/File error:", e)
        except Exception as e:
            await message.answer("Произошла ошибка при распознавании. Подробности в логах.", reply_markup=START_KB)
            print("Transcribe error:", e)

    return router

# Экспортируем handle_voice для использования в других модулях
handle_voice = get_voice_router().message.handlers[0].callback
