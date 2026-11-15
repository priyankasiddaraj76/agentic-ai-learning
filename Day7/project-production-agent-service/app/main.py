# CREATING API ENDPOINT
import asyncio
import logging
import time
import uuid
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.client import client
from app.config import get_settings
from app.context import trim_history
from app.retry import retry_llm_call
from app.usage import calculate_cost

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title="Production Agent Service",
    version="1.0.0",
)


class ChatMessage(BaseModel):
    role: Literal["user", "model"]
    text: str


class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    history: list[ChatMessage] = Field(default_factory=list)


class AgentResponse(BaseModel):
    request_id: str
    answer: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    duration_ms: int


SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer clearly and accurately.
If you do not know something, say so.
"""


@retry_llm_call
def generate_answer(contents: list[dict]):
    return client.models.generate_content(
        model=settings.gemini_model,
        contents=contents,
        config={
            "system_instruction": SYSTEM_PROMPT,
        },
    )


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "production-agent-service",
    }


@app.post("/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    # Trim older conversation messages
    history = trim_history(
        [message.model_dump() for message in request.history]
    )

    contents = [
        {
            "role": message["role"],
            "parts": [{"text": message["text"]}],
        }
        for message in history
    ]

    contents.append({
        "role": "user",
        "parts": [{"text": request.message}],
    })

    try:
        # SDK call is synchronous, so run it outside the event loop.
        # asyncio.to_thread() prevents the synchronous SDK call from blocking FastAPI's event loop
        response = await asyncio.to_thread(
            generate_answer,
            contents,
        )

    except TimeoutError as exc:
        logger.exception("LLM timeout: %s", request_id)
        raise HTTPException(
            status_code=504,
            detail="LLM request timed out",
        ) from exc

    except Exception as exc:
        logger.exception("LLM request failed: %s", request_id)
        raise HTTPException(
            status_code=502,
            detail="LLM provider request failed",
        ) from exc

    usage = response.usage_metadata

    input_tokens = (
        usage.prompt_token_count if usage else 0
    )
    output_tokens = (
        usage.candidates_token_count if usage else 0
    )

    estimated_cost = calculate_cost(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        input_price_per_million=settings.input_price_per_million,
        output_price_per_million=settings.output_price_per_million,
    )

    duration_ms = int(
        (time.perf_counter() - start_time) * 1000
    )

    logger.info(
        "request_id=%s model=%s input_tokens=%s "
        "output_tokens=%s estimated_cost_usd=%s duration_ms=%s",
        request_id,
        settings.gemini_model,
        input_tokens,
        output_tokens,
        estimated_cost,
        duration_ms,
    )

    return AgentResponse(
        request_id=request_id,
        answer=response.text or "",
        model=settings.gemini_model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost_usd=estimated_cost,
        duration_ms=duration_ms,
    )
