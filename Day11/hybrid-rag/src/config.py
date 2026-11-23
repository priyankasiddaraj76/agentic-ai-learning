import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
DATABASE_URL=os.getenv("DATABASE_URL")
EMBEDDING_MODEL = "gemini-embedding-001"

LLM_MODEL = "gemini-3.5-flash-lite"

# Number of final chunks returned to the LLM
TOP_K = 3

# Number of candidates fetched by each search method
VECTOR_CANDIDATES = 20

FULLTEXT_CANDIDATES = 20

# RRF smoothing constant
RRF_K = 60