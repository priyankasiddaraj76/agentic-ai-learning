from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field, ValidationError

class User(BaseModel):
    user_id: int
    name: str = Field(min_length=2)
    age: int = Field(gt=17, lt=100)
    is_active: bool

    model_config = ConfigDict(strict=True,extra="forbid")


def main() -> None:
    file_path = Path("data/user.json")
    try:
        with file_path.open("r") as file:
            user_data = file.read()
        user = User.model_validate_json(user_data)
        print("User data is valid:", user)
        print(user.model_dump())
    except FileNotFoundError:
        print("File not found.")
    except ValidationError as e:
        print("Validation error:", e)

if __name__ == "__main__":
    main()