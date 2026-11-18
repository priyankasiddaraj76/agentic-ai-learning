from app.db import get_connection
from app.embeddings import generate_query_embedding
from app.ingest import vector_to_string

def search_documents(query: str, top_k: int = 5):
    query_embedding = generate_query_embedding(query)
    query_vector = vector_to_string(query_embedding)

    sql = """
        SELECT
            id,
            source,
            page,
            section,
            content,
            1 - (embedding <=> %s::vector)
                AS similarity
        FROM document_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (query_vector, query_vector, top_k))

            results = cursor.fetchall()

    return results

def main():
    query = input("Enter your question: ")

    results = search_documents(query=query, top_k=5)

    print("\nMost relevant document chunks:\n")

    for result in results:
        (
            chunk_id,
            source,
            page,
            section,
            content,
            similarity,
        ) = result

        print("-" * 70)
        print(f"Chunk ID: {chunk_id}")
        print(f"Source: {source}")
        print(f"Page: {page}")
        print(f"Section: {section}")
        print(f"Similarity: {similarity:.4f}")
        print(f"Content:\n{content}")

if __name__ == "__main__":
    main()