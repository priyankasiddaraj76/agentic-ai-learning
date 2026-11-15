# CONTEXT TRIMMING
from app.config import get_settings

settings = get_settings()


def trim_history(messages: list[dict]) -> list[dict]:
    limit = settings.max_history_messages
    return messages[-limit:]
