import psycopg

from src.config import (DATABASE_URL, FULLTEXT_CANDIDATES, TOP_K)
from src.retriever import vector_search
from src.rrf import reciprocal_rank_fusion

def fulltext_search(question: str) -> list[dict]:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, content,
                ts_rank_cd(search_vector, websearch_to_tsquery('english', %s)) as RELEVANCE
                FROM document_chunks
                WHERE search_vector @@ websearch_to_tsquery('english', %s)
                ORDER BY RELEVANCE desc
                LIMIT %s
                """,
                (question, question, FULLTEXT_CANDIDATES)
            )

            rows = cur.fetchall()

    results = []

    for rank, row in enumerate(rows, start=1):
        results.append({
            "chunk_id": row[0],
            "content": row[1],
            "relevance": float(row[2]),
            "rank": rank
        })

    return results

def hybrid_search(question: str) -> list[dict]:
    # Search 1: Semantic Vector Search
    vector_results = vector_search(question)

    # Search 2: Keyword full-text search
    fulltext_results = fulltext_search(question)

    # Merge using Reciprocal Rank Fusion (RRF)
    hybrid_results = reciprocal_rank_fusion(vector_results, fulltext_results, top_k=TOP_K)

    return hybrid_results