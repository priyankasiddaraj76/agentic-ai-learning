# To generate the answer using gemini model
import json
from google import genai
from google.genai import types

from src.config import (GEMINI_API_KEY, LLM_MODEL)

from src.prompt import build_prompt

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_answer(question:str, chunks:list[dict]) -> dict:
    promt = build_prompt(question, chunks)
    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=promt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        ) )

    result = response.text
    return json.loads(result)