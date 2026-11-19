import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
DATABASE_URL=os.getenv("DATABASE_URL")
EMBEDDING_MODEL = "gemini-embedding-001"

LLM_MODEL = "gemini-3.5-flash-lite"

TOP_K = 3