from src.retriever import retrieve_chunks
from src.generator import generate_answer
from src.validators import validate_rag_response

def ask_question(question: str) -> dict:
    # step1: Retreive relavant chunks
    chunks = retrieve_chunks(question)
    if not chunks:
        return {
            "question": question,
            "answer": "No relevant information found.",
            "citations": [],
            "retrieved_chunks": []
        }

    # Step2: generate answer using Gemini
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

    print("\nRAG RESPONSE")

    print("\nQuestion:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nCitations:")
    print(result["citations"])

    print("\nRetrieved chunks:")

    for chunk in result["retrieved_chunks"]:
        print(
            chunk["chunk_id"],
            chunk["similarity"]
        )