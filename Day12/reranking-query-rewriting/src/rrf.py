from src.config import RRF_K

def reciprocal_rank_fusion(vector_results: list[dict], fulltext_results: list[dict], top_k: int=5) -> list[dict]:
    fused_results = {}

    result_lists = [
        ("vector_rank", vector_results),
        ("fulltext_rank", fulltext_results)
    ]

    for rank_field, results in result_lists:
        for rank, result in enumerate(results, start=1):
            chunk_id = result["chunk_id"]

            if chunk_id not in fused_results:
                fused_results[chunk_id] = {
                    "chunk_id": chunk_id,
                    "content": result["content"],
                    "rrf_score": 0.0,
                    "vector_rank": None,
                    "fulltext_rank": None
                }
            fused_results[chunk_id]["rrf_score"] += (1 / (RRF_K + rank))

            fused_results[chunk_id][rank_field] = rank

    # Sort by combined RRF score
    ranked_results = sorted(fused_results.values(),
                            key=lambda x: (-x["rrf_score"], x["chunk_id"]))

    return ranked_results[:top_k]