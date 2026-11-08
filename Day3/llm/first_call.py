import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Set GEMINI_API_KEY in the environment or .env file.")

# Initialize the OpenAI client with the Gemini API key
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client.chat.completions.create(
    model="gemini-3.5-flash-lite",
    messages=[
        {"role": "user", "content": "Explain the concept of asynchronous programming in Python."}
    ],
)

print(response.choices[0].message.content)