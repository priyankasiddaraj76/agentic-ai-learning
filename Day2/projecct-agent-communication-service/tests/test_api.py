
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "service": "Agent Communication Service"
    }


def test_echo_endpoint():

    payload = {
        "message": "Explain Python async",
        "agent_name": "learning-agent"
    }

    response = client.post(
        "/echo",
        json=payload
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Explain Python async",
        "agent_name": "learning-agent",
        "status": "received",
        "message_length": 20
    }


def test_process_endpoint():

    payload = {
        "message": "I need help with my account",
        "agent_name": "support-agent"
    }

    response = client.post(
        "/process",
        json=payload
    )

    assert response.status_code == 200

    assert response.json() == {
        "original_message": "I need help with my account",
        "processed_message": "i need help with my account",
        "word_count": 6,
        "agent_name": "support-agent"
    }


def test_invalid_echo_request():

    payload = {
        "message": "",
        "agent_name": "learning-agent"
    }

    response = client.post(
        "/echo",
        json=payload
    )

    assert response.status_code == 422


def test_extra_field_rejected():

    payload = {
        "message": "Hello there",
        "agent_name": "learning-agent",
        "unexpected": "value"
    }

    response = client.post(
        "/echo",
        json=payload
    )

    assert response.status_code == 422
