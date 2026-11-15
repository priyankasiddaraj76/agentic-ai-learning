# Production Agent Service

A production-oriented AI agent API built using Python, FastAPI, Google Gemini, Pydantic, and Tenacity.

## Features

- FastAPI endpoint for AI requests
- Gemini model integration
- Exponential backoff and retry handling
- Configurable request timeouts
- Input and output token tracking
- Estimated API cost per request
- Environment-based API key management
- Conversation history trimming
- Structured request logging
- Pydantic request and response validation

## Tech Stack

- Python
- FastAPI
- Google Gen AI SDK
- Pydantic and Pydantic Settings
- Tenacity
- Uvicorn
- Pytest

## Project Structure

```text
app/
  main.py
  client.py
  config.py
  context.py
  retry.py
  usage.py
tests/
  test_usage.py
```

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd production-agent-service
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and add your Gemini API key.

Never commit `.env` or expose your API key.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

API documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

### GET /health

Checks service health.

### POST /agent

Accepts a user message and optional conversation history. Returns the model response, token usage, estimated cost, and request duration.

Example:

```json
{
  "message": "Explain how AI agents work",
  "history": []
}
```

## Reliability and Cost Management

The service includes configurable retry attempts, exponential backoff with jitter, provider request timeouts, token usage tracking, and estimated per-request costs.

## Running Tests

```bash
pytest -v
```

## Future Improvements

- Add token-budget-based context management
- Summarize older conversation history
- Persist usage records in PostgreSQL
- Add request authentication and rate limiting
- Add structured tracing and monitoring
- Add Docker support and deployment configuration

## Learning Objectives

This project demonstrates foundational production practices for LLM-powered applications: reliability, observability, cost control, secure configuration, and context management.
