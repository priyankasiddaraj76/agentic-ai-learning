from fastapi import FastAPI
from app.models import EchoRequest, EchoResponse

app = FastAPI(
    title="Day 2 FastAPI Example",
    description="A simple FastAPI application for echoing messages.",
    version="1.0.0"
)

# GET endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy",
            "message": "FastAPI is running!"}

# POST endpoint
@app.post("/echo", response_model=EchoResponse)
async def echo_message(request: EchoRequest):
    return EchoResponse(
        message=request.message,
        sender=request.sender,
        status="success"
    )


# Running the application using Uvicorn
# From the day2/fastapi root folder: uvicorn app.main:app --reload
# Explanation:
# - app.main: Python module path.
# - app: FastAPI application object.
# - --reload: Automatically reloads the application when code changes. Use for development, not production.
# Your API will be available at: http://127.0.0.1:8000