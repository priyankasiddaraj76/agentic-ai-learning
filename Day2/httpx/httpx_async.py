
import asyncio
import httpx

async def fetch_user(user_id: int):

    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    async with httpx.AsyncClient() as client:

        response = await client.get(url)

        response.raise_for_status()

        return response.json()


async def main():

    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3)
    )

    for user in users:
        print(user["name"])


asyncio.run(main())
