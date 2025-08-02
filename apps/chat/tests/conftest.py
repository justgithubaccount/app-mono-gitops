# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)

@pytest.fixture
def sample_message():
    from app.schemas import Message
    return Message(role="user", content="test")