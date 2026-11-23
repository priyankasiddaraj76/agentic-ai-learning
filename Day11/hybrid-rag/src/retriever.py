import psycopg

from pgvector import Vector
from pgvector.psycopg import register_vector

from src.config import (DATABASE_URL, VECTOR_CANDIDATES)
from src.embeddings import generate_embedding

def vector_search(question: str) -> list[dict]:

    # Generate question embedding
    query_embedding = Vector(
        generate_embedding(question, task_type="RETRIEVAL_QUERY")
    )

    with psycopg.connect(DATABASE_URL) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    content,
                    1 - (embedding <=> %s) AS similarity
                FROM document_chunks
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (
                    query_embedding,
                    query_embedding,
                    VECTOR_CANDIDATES
                )
            )

            rows = cur.fetchall()

    results = []
    for rank, row in enumerate(rows, start=1):
        results.append({
            "chunk_id": row[0],
            "content": row[1],
            "similarity": float(row[2]),
            "rank": rank
        })

    return results
