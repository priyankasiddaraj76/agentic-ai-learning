# To validate citations using pydantic
from pydantic import BaseModel, Field

class RAGResponse(BaseModel):
    answer: str = Field(min_length=1)
    citations: list[str] = Field(default_factory=list)

def validate_rag_response(response: dict, retrived_chunks:list[dict]) -> RAGResponse:
    # Validate JSON structure and datatypes
    validated = RAGResponse.model_validate(response)

    # Collect IDs of retrived chunks
    retrieved_ids = {str(chunk["chunk_id"])
                     for chunk in retrived_chunks}

    # Collect IDs cited by Gemini
    cited_ids = set(validated.citations)

    # Find invalid citations
    invalid_ids = cited_ids-retrieved_ids

    if invalid_ids:
        raise ValueError( f"Invalid citations: {invalid_ids}")

    return validated
