from src.query_rewriter import rewrite_query
from src.hybrid_retriever import (vector_search, fulltext_search)
from src.rrf import reciprocal_rank_fusion
from src.reranker import rerank_chunks
from src.config import (RERANK_CANDIDATES, FINAL_TOP_K)

def advanced_search(question: str) -> list[dict]:
    # Step1: Rewrite original question
    rewritten_query=rewrite_query(question)

    print("\nOriginal question:", question)
    print("Rewritten query:", rewritten_query)

    # Step 2: Vector search using rewritten query
    vector_results = vector_search(rewritten_query)

    # Step 3: Full-text search using rewritten query
    fulltext_results = fulltext_search(rewritten_query)

    # Step 4: Combine results using RRF
    hybrid_results = reciprocal_rank_fusion(vector_results, fulltext_results, top_k=RERANK_CANDIDATES)

    # Step 5: Rerank using original question
    reranked_results = rerank_chunks(question, hybrid_results, top_k=FINAL_TOP_K)

    return reranked_results