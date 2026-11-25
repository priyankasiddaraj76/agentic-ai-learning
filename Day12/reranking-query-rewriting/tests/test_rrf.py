from src.rrf import reciprocal_rank_fusion


vector_results = [
    {"chunk_id": "chunk_001", "content": "DNA sequencing"},
    {"chunk_id": "chunk_004", "content": "PCR"},
    {"chunk_id": "chunk_003", "content": "Genome assembly"}
]

fulltext_results = [
    {"chunk_id": "chunk_003", "content": "Genome assembly"},
    {"chunk_id": "chunk_002", "content": "RNA sequencing"},
    {"chunk_id": "chunk_001", "content": "DNA sequencing"}
]


results = reciprocal_rank_fusion(
    vector_results,
    fulltext_results,
    top_k=4
)

for result in results:

    print(
        result["chunk_id"],
        round(result["rrf_score"], 5),
        result["vector_rank"],
        result["fulltext_rank"]
    )