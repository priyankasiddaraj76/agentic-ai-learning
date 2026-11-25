from src.retriever import vector_search
from src.hybrid_retriever import hybrid_search
from src.advanced_retriever import advanced_search
from src.reranker import rerank_chunks
from src.config import FINAL_TOP_K


QUESTIONS = [
    "What is DNA sequencing?",
    "How does PCR amplify DNA?",
    "What is the role of BRCA1 in cancer?",
    "Explain next-generation sequencing.",
    "What is genome assembly?",
    "How does CRISPR-Cas9 edit genes?",
    "What is RNA sequencing?",
    "Explain the difference between DNA and RNA.",
    "What are single nucleotide polymorphisms?",
    "What is the Human Genome Project?"
]

def evaluate():

    for question in QUESTIONS:
        print("\n" + "=" * 60)

        print("QUESTION:", question)

        # A: Vector-only
        vector_results = vector_search(question)

        # B: Hybrid
        hybrid_results = hybrid_search(question)

        # C: Hybrid + reranking
        reranked_results = rerank_chunks(question, hybrid_results, top_k=FINAL_TOP_K)

        # D: Query rewriting + hybrid + reranking
        advanced_results = advanced_search(question)

        configurations = {
            "A - Vector": vector_results[:FINAL_TOP_K],
            "B - Hybrid": hybrid_results[:FINAL_TOP_K],
            "C - Hybrid + Rerank": reranked_results,
            "D - Full Day 12": advanced_results
        }

        for name, results in configurations.items():
            print(f"\n{name}")

            for rank, chunk in enumerate(results, start=1):
                score = chunk.get("rerank_score", chunk.get("rrf_score", 0))
                print(
                    rank,
                    chunk["chunk_id"],
                    round(float(score), 4)
                )

if __name__ == "__main__":
    evaluate()