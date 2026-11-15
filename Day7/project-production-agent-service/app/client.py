
from google import genai
from google.genai import types

from app.config import get_settings

settings = get_settings()

client = genai.Client(
    api_key=settings.gemini_api_key.get_secret_value(),
    http_options=types.HttpOptions(
        timeout=settings.request_timeout_seconds * 1000
    ),
)
