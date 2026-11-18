from google import genai
from google.genai import types

from app.config import (GEMINI_API_KEY,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSIONS,)

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_document_embeddings(texts: list[str]) -> list[list[float]]:
    response = client.models.embed_content(
        model = EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )

    return [embedding.values for embedding in response.embeddings]

def generate_query_embedding(query: str) -> list[float]:
    response = client.models.embed_content(
        model = EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )

    return response.embeddings[0].values