from src.retriever import vector_search
from src.hybrid_retriever import hybrid_search
from src.config import TOP_K


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


# Replace these with actual relevant chunk IDs.
GROUND_TRUTH = {
    "What is DNA sequencing?": {2, 6},
    "How does PCR amplify DNA?": {"39", "15"},
    "What is the role of BRCA1 in cancer?": {"20"},
    "Explain next-generation sequencing.": {"15"},
    "What is genome assembly?": {"30"},
    "How does CRISPR-Cas9 edit genes?": {"45", "60"},
    "What is RNA sequencing?": {"65", "40"},
    "Explain the difference between DNA and RNA.": {"39", "46"},
    "What are single nucleotide polymorphisms?": {"80", "76"},
    "What is the Human Genome Project?": {"88", "44"}
}


def calculate_metrics(
    retrieved: list[dict],
    relevant_ids: set[str]
) -> dict:

    retrieved_ids = [
        chunk["chunk_id"]
        for chunk in retrieved[:TOP_K]
    ]

    relevant_retrieved = (
        set(retrieved_ids) & relevant_ids
    )

    hit = int(len(relevant_retrieved) > 0)

    recall = (
        len(relevant_retrieved) / len(relevant_ids)
        if relevant_ids else 0.0
    )

    reciprocal_rank = 0.0

    for rank, chunk_id in enumerate(
        retrieved_ids,
        start=1
    ):
        if chunk_id in relevant_ids:
            reciprocal_rank = 1 / rank
            break

    return {
        "hit": hit,
        "recall": recall,
        "mrr": reciprocal_rank
    }


def evaluate():

    vector_metrics = []
    hybrid_metrics = []

    for question in QUESTIONS:

        relevant_ids = GROUND_TRUTH.get(
            question,
            set()
        )

        if not relevant_ids:
            print(
                f"Skipping {question}: "
                "ground truth not configured"
            )
            continue

        # Vector-only retrieval
        vector_results = vector_search(question)

        # Hybrid retrieval
        hybrid_results = hybrid_search(question)

        vector_score = calculate_metrics(
            vector_results,
            relevant_ids
        )

        hybrid_score = calculate_metrics(
            hybrid_results,
            relevant_ids
        )

        vector_metrics.append(vector_score)
        hybrid_metrics.append(hybrid_score)

        print("\nQuestion:", question)

        print(
            "Vector IDs:",
            [
                x["chunk_id"]
                for x in vector_results[:TOP_K]
            ]
        )

        print(
            "Hybrid IDs:",
            [
                x["chunk_id"]
                for x in hybrid_results
            ]
        )

        print("Vector metrics:", vector_score)
        print("Hybrid metrics:", hybrid_score)

    if not vector_metrics:
        print("\nNo questions evaluated.")
        return

    def average(metrics, key):
        return sum(
            item[key] for item in metrics
        ) / len(metrics)

    print("\n========== FINAL COMPARISON ==========")

    for name, metrics in [
        ("Vector-only", vector_metrics),
        ("Hybrid", hybrid_metrics)
    ]:

        print(f"\n{name}")

        print(
            "Hit Rate@3:",
            round(average(metrics, "hit"), 3)
        )

        print(
            "Recall@3:",
            round(average(metrics, "recall"), 3)
        )

        print(
            "MRR:",
            round(average(metrics, "mrr"), 3)
        )


if __name__ == "__main__":
    evaluate()