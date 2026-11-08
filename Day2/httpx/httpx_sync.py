
import httpx

response = httpx.get(
    "https://jsonplaceholder.typicode.com/users/1"
)

print(response.status_code)
print(response.json())
