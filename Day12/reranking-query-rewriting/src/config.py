import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
DATABASE_URL=os.getenv("DATABASE_URL")
EMBEDDING_MODEL = "gemini-embedding-001"

LLM_MODEL = "gemini-3.5-flash-lite"

# Day 11 retrieval configuration
VECTOR_CANDIDATES = 20
FULLTEXT_CANDIDATES = 20
RRF_K = 60

# Day 12 reranking configuration
RERANKER_MODEL = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

RERANK_CANDIDATES = 20

FINAL_TOP_K = 5