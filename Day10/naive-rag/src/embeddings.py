from google import genai
from src.config import (GEMINI_API_KEY, EMBEDDING_MODEL)

client = genai.Client(api_key = GEMINI_API_KEY)

def generate_embedding(text: str, task_type: str = "RETRIEVAL_QUERY") -> list[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config={
            "task_type": task_type,
            "output_dimensionality": 768
        })

    return response.embeddings[0].values
