import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI


async def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY in the environment or .env file.")

    async with AsyncOpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    ) as client:
        stream = await client.chat.completions.create(
            model="gemini-3.5-flash-lite",
            messages=[
                {
                    "role": "user",
                    "content": "Explain the concept of asynchronous programming in Python.",
                }
            ],
            stream=True,
            max_tokens=100,
        )

        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())