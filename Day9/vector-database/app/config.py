import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001",)
EMBEDDING_DIMENSIONS = int(
    os.getenv("EMBEDDING_DIMENSIONS", "768")
)

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing")

if EMBEDDING_DIMENSIONS != 768:
    raise RuntimeError(
        "This project's database expects 768 dimensions"
    )