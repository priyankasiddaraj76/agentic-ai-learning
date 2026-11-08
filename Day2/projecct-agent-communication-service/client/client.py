import httpx
import asyncio
import json

BASE_URL = "http://127.0.0.1:8000"

# Call health endpoint
async def check_health(client: httpx.AsyncClient):
    response = await client.get("/health")
    response.raise_for_status()
    return response.json()

# call echo endpoint
async def send_echo(client: httpx.AsyncClient, message: str, agent_name: str):
    payload = {"message": message, "agent_name": agent_name}
    response = await client.post("/echo", json=payload)
    response.raise_for_status()
    return response.json()

# Call process endpoint
async def process_message(client: httpx.AsyncClient, message: str, agent_name: str):
    payload = {"message": message, "agent_name": agent_name}
    response = await client.post("/process", json=payload)
    response.raise_for_status()
    return response.json()

# Main async function to run all tasks concurrently
async def main():
    async with httpx.AsyncClient(
        base_url=BASE_URL,
        timeout=10.0
    ) as client:
        
        # Run all tasks concurrently
        health_result = await check_health(client)

        # Send 3 echo requests concurrently
        messages = [
            "Explain Python's asyncio library.",
            "What is FastAPI and how does it work?",
            "How to use httpx for asynchronous HTTP requests?"
        ]

        echo_tasks = [
            send_echo(client, message, "learning-agent") for message in messages
        ]

        echo_results = await asyncio.gather(*echo_tasks)

        process_result = await process_message(client, "Process this message", "ClientAgent")

        final_result = {
            "health": health_result,
            "echo_responses": echo_results,
            "process_responses": process_result
        }

        print(json.dumps(final_result, indent=4))


if __name__ == "__main__":
    asyncio.run(main())