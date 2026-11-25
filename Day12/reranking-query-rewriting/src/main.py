from src.advanced_retriever import advanced_search
from src.generator import generate_answer
from src.validators import validate_rag_response

def ask_question(question: str) -> dict:
    # Step1: Query Rewriting + hybrid retrieval + reranking
    chunks = advanced_search(question)

    if not chunks:

        return {
            "question": question,
            "answer": "No relevant information found.",
            "citations": [],
            "retrieved_chunks": []
        }

    # Step 2: Generate answer using original question
    response = generate_answer(question, chunks)

    # Step3: Validate citations
    validated = validate_rag_response(response, chunks)

    # Step 4: Return final response
    return {
        "question": question,
        "answer": validated.answer,
        "citations": validated.citations,
        "retrieved_chunks": chunks
    }

if __name__ == "__main__":

    question = input("Ask a question: ")

    result = ask_question(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nCitations:")
    print(result["citations"])

    print("\nRERANKED CHUNKS:")

    for chunk in result["retrieved_chunks"]:
        print(
            chunk["chunk_id"],
             round(chunk["rerank_score"], 4)
        )