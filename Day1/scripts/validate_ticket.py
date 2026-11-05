from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

class Customer(StrictModel):
    customer_id: int
    name: str

class Ticket(StrictModel):
    ticket_id: int
    customer: Customer
    category: Literal["billing", "technical", "general"]
    priority: Literal["low", "medium", "high"]
    decscription: str = Field(min_length=10, max_length=500)
    tags: list[str] = Field(min_items=1, max_items=5)

def main() -> None:
    json_data = """{
        "ticket_id": 123,
        "customer": {
            "customer_id": 456,
            "name": "John Doe"
        },
        "category": "technical",
        "priority": "high",
        "decscription": "The system is not responding when I try to log in.",
        "tags": ["login", "urgent"]
    }"""

    try:
        ticket = Ticket.model_validate_json(json_data)
        print("Ticket data is valid:")
        print("Ticket ID:", ticket.ticket_id)
        print("Customer Name:", ticket.customer.name)
        print("Category:", ticket.category)
        print("Priority:", ticket.priority)
        print("Tags:", ticket.tags)
    except ValidationError as e:
        print("Validation error:", e)

if __name__ == "__main__":
    main()