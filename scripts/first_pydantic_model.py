from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

user = User(name = "Priyanka", age="27", email="priya@example.com")

print("User Name:", user.name)

# Validating data
try:
    user2 = User(name="John", age="twenty-five", email="ramdom")
except ValueError as e:
    print("Error creating user2:", e)