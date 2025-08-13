import warnings
from functools import lru_cache
import whisper

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU.*")

@lru_cache(maxsize=4)
def get_model(model_name: str = "small", device: str = "cpu"):
    # Загружается один раз и кешируется
    return whisper.load_model(model_name, device=device)
