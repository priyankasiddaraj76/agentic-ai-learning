from src.query_rewriter import rewrite_query

questions = [
    "What is PCR?",
    "How does CRISPR work?",
    "Explain NGS.",
    "What is BRCA1?",
    "How is genome assembly performed?"
]


for question in questions:

    rewritten = rewrite_query(question)

    print("\nOriginal:", question)

    print("Rewritten:", rewritten)