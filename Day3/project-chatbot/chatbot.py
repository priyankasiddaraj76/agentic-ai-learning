import asyncio
import os

import openai
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    max_retries=2,
)

SYSTEM_PROMPT = """
You are a helpful AI coding assistant.

The user is learning Python and Agentic AI.
They come from a Java background.

Follow these rules:
1. Explain concepts in simple language.
2. Compare Python concepts with Java.
3. Give practical code examples.
4. Explain errors and debugging approaches.
5. Keep answers structured.
"""

# Stores conversation history
messages = []

async def get_response(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})
    assistant_response = ""

    try:
        stream = await client.chat.completions.create(
            model="gemini-3.5-flash-lite",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            stream=True,
            max_tokens=1000,
            timeout=30,
        )

        print("\nAI: ", end="", flush=True)

        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                assistant_response += content
                print(content, end="", flush=True)

        print("\n")

        # Save assistant response for future context
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })

    except openai.AuthenticationError:
        messages.pop()
        print("\nInvalid API key. Check your .env file.")

    except openai.RateLimitError:
        messages.pop()
        print("\nRate limit reached. Try again later.")

    except openai.APITimeoutError:
        messages.pop()
        print("\nRequest timed out.")

    except openai.APIConnectionError:
        messages.pop()
        print("\nUnable to connect to OpenAI.")

    except openai.APIStatusError as error:
        messages.pop()
        print(f"\nAPI error: {error.status_code}")
        print(f"Request ID: {error.request_id}")

    except openai.APIError as error:
        messages.pop()
        print(f"\nOpenAI error: {error}")

async def main():

    print("=" * 50)
    print("       PYTHON AI CHATBOT")
    print("=" * 50)

    print("Commands: /exit, /reset")

    while True:

        user_message = input("\nYou: ").strip()

        if not user_message:
            continue

        if user_message.lower() == "/exit":
            print("Goodbye!")
            break

        if user_message.lower() == "/reset":
            messages.clear()
            print("Conversation history cleared.")
            continue

        await get_response(user_message)


if __name__ == "__main__":

    asyncio.run(main())
