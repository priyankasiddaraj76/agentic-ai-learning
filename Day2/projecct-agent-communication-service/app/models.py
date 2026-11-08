from pydantic import BaseModel, Field, ConfigDict

# Incoming request model
class AgentMessage(BaseModel):
    message: str = Field(min_length=1, max_length=100)
    agent_name: str = Field(min_length=1, max_length=50)

    model_config = ConfigDict(strict=True, extra="forbid")  # Forbid extra fields in the request

# Response model for /echo
class EchoResponse(BaseModel):
    message: str
    agent_name: str
    status: str
    message_length: int

# Response model for /process
class ProcessResponse(BaseModel):
    original_message: str
    processed_message: str
    agent_name: str
    word_count: int

# Response model for /health
class HealthResponse(BaseModel):
    status: str
    service: str
