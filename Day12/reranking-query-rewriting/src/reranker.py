from sentence_transformers import CrossEncoder
from src.config import RERANKER_MODEL

# Load model once when the module is imported
reranker = CrossEncoder(
    RERANKER_MODEL
)

def rerank_chunks(question: str, chunks: list[dict], top_k: int=5) -> list[dict]:
    if not chunks:
        return []

    # Create question-document pairs
    pairs = [
        (
            question,
            chunk["content"]
        )
        for chunk in chunks
    ]

    # Calculate relevance scores - the model scores each pair
    scores = reranker.predict(pairs)

    # Attach reranking scores
    ranked_chunks = []

    for chunk, score in zip(chunks, scores):
        result = chunk.copy()
        result["rerank_score"] = float(score)
        ranked_chunks.append(result)

    # Sort by descending relevance score
    ranked_chunks.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return ranked_chunks[:top_k]