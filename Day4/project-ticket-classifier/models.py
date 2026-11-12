
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class TicketCategory(str, Enum):
    ACCOUNT = "account"
    BILLING = "billing"
    TECHNICAL = "technical"
    GENERAL = "general"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TicketClassification(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    category: TicketCategory = Field(description="The category of the ticket.")
    priority: TicketPriority = Field(description="The priority of the ticket.")
    summary: str = Field(description="A concise summary of the customer's issue.")