from app.models import EchoResponse, AgentMessage, ProcessResponse, HealthResponse
from fastapi import FastAPI
from app.services import create_echo_response, process_message

app = FastAPI(
    title="Agent Communication Service",
    description="A FastAPI application for agent communication, echoing messages, and processing them.",
    version="1.0.0")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", service="Agent Communication Service")

@app.post("/echo", response_model=EchoResponse)
async def echo_message(request: AgentMessage):
    return create_echo_response(request)

@app.post("/process", response_model=ProcessResponse)
async def process_agent_message(request: AgentMessage):
    return process_message(request)