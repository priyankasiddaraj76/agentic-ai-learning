import json

from google import genai
from google.genai import types

from src.config import(GEMINI_API_KEY, LLM_MODEL)

from pydantic import BaseModel, Field

client = genai.Client(api_key=GEMINI_API_KEY)

class RewrittenQuery(BaseModel):
    rewrittenQuery: str = Field(min_length=3)

def rewrite_query(question: str) -> str:
    prompt = f"""
    You are a search query optimization assistant
    for computational biology documents.

    Rewrite the user's question to improve document retrieval.

    Rules:
    1. Preserve the original meaning.
    2. Expand important scientific abbreviations.
    3. Include relevant technical terminology.
    4. Clarify ambiguity only when context supports it.
    5. Do not answer the question.
    6. Do not introduce unrelated topics.
    7. Return only the rewritten query.

    Original question:
    {question}

    Return JSON:
    {{
        "rewritten_query": "Improved search query"
    }}
    """

    try:
        response = client.models.generate_content(
            model=LLM_MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json", responseSchema=RewrittenQuery
            )
        )

        result = RewrittenQuery.model_validate_json(response.text)
        return result.rewrittenQuery
    except Exception as error:

        print("Query rewriting failed:", error)

        # Fallback: use original question
        return question