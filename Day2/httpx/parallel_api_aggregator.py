# Requirement:
# Build a script that fetches:
# - User details from /users/1
# - Posts from /posts?userId=1
# - Albums from /albums?userId=1
# Use asyncio.gather() to fetch all three concurrently.

# Combine the results into:
# {    "user": {...},    "posts": [...],    "albums": [...]}


import asyncio
import httpx
import json


BASE_URL = "https://jsonplaceholder.typicode.com"

# STEP 1: Create a reusable asynchronous API function
async def fetch_data(client: httpx.AsyncClient, endpoint: str, params: dict | None = None):
    url = f"{BASE_URL}/{endpoint}"
    response = await client.get(url, params=params)
    response.raise_for_status()
    return response.json()

# STEP 2: Fetch all three resources concurrently
async def aggregate_user_data(user_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        user_task = fetch_data(client, f"users/{user_id}")
        posts_task = fetch_data(client, "posts", params={"userId": user_id})
        albums_task = fetch_data(client, "albums", params={"userId": user_id})

        user, posts, albums = await asyncio.gather(user_task, posts_task, albums_task)

        # STEP 3: Combine all API responses
        result = {
            "user": user,
            "posts": posts,
            "albums": albums
        }

    return result

# STEP 4: Main function
async def main():

    try:

        result = await aggregate_user_data(1)

        print("Aggregated API Response:\n")

        print(json.dumps(result, indent=4))

        print("\nSummary:")
        print("User:", result["user"]["name"])
        print("Total Posts:", len(result["posts"]))
        print("Total Albums:", len(result["albums"]))

    except httpx.HTTPError as error:

        print("API request failed:", error)


# STEP 5: Execute the async program

if __name__ == "__main__":
    asyncio.run(main())


