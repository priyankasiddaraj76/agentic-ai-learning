import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def main():
    async with httpx.AsyncClient() as client:
        # Make a GET request to the /health endpoint
        health_response = await client.get(f"{BASE_URL}/health")
        print("Health Check Response:", health_response.json())

        # Make a POST request to the /echo endpoint
        echo_payload = {"message": "Hello, FastAPI!", "sender": "httpx Client"}
        echo_response = await client.post(f"{BASE_URL}/echo", json=echo_payload)
        print("Echo Response:", echo_response.json())  


if __name__ == "__main__":
    asyncio.run(main())