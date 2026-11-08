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

for temperature in [0.1, 0.7, 1.2]:
    response = client.chat.completions.create(
    model="gemini-3.5-flash-lite",
    messages=[
        {"role": "user", "content": "Give me a creative name for an AI startup."}
    ],
    temperature=temperature,
    max_tokens=50
    )
    print(f"Temperature: {temperature}")
    print(response.choices[0].message.content)
