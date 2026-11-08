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

try:
    response = client.chat.completions.create(
        model="gemini-3.5-flash-lite",
        messages=[
            {"role": "user", "content": "Explain the concept of asynchronous programming in Python."}
        ],
    )
    print(response.choices[0].message.content)
except openai.AuthenticationError:
    print("Authentication failed. Please check your GEMINI_API_KEY.")
except openai.RateLimitError:
    print("Rate limit exceeded. Please try again later.")
except openai.APITimeoutError:
    print("The request timed out. Please try again.")
except openai.APIConnectionError:
    print("Failed to connect to the API. Please check your network connection.")
except openai.APIStatusError as e:
    print(f"API error: {e.status_code} - {e.message}")
except openapi.ApiError as e:
    print(f"An unexpected error occurred: {e}")
