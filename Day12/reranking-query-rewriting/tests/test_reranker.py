from src.reranker import rerank_chunks


question = "How does CRISPR edit genes?"

chunks = [
    {
        "chunk_id": "chunk_001",
        "content": (
            "CRISPR-Cas9 is a genome editing "
            "technology that targets DNA."
        )
    },
    {
        "chunk_id": "chunk_002",
        "content": (
            "RNA sequencing measures gene expression."
        )
    },
    {
        "chunk_id": "chunk_003",
        "content": (
            "Guide RNA directs Cas9 to a specific "
            "DNA sequence for gene editing."
        )
    }
]


results = rerank_chunks(
    question,
    chunks,
    top_k=3
)


for chunk in results:

    print(
        chunk["chunk_id"],
        chunk["rerank_score"],
        chunk["content"]
    )