import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock

from app.main import app
from app.db import arango_manager, xtdb_client, cache_manager
from app.ml import nlp_processor
from app.services import fact_check_service


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_arango():
    """Mock ArangoDB manager."""
    mock = MagicMock()
    mock.is_connected = True
    mock.get_collection = MagicMock()
    return mock


@pytest.fixture
def mock_xtdb():
    """Mock XTDB client."""
    mock = AsyncMock()
    mock.is_connected = True
    return mock


@pytest.fixture
def mock_cache():
    """Mock cache manager."""
    mock = AsyncMock()
    mock.is_connected = True
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mock_nlp():
    """Mock NLP processor."""
    mock = MagicMock()
    mock.is_initialized = True
    mock.extract_entities = MagicMock(return_value=[
        {"text": "Test Entity", "label": "ORG", "start": 0, "end": 11}
    ])
    mock.analyze_sentiment = MagicMock(return_value={
        "polarity": 0.0,
        "subjectivity": 0.5,
        "classification": "neutral"
    })
    mock.analyze_complexity = MagicMock(return_value={
        "num_sentences": 1,
        "num_words": 10,
        "num_unique_words": 10,
        "avg_word_length": 5.0,
        "avg_sentence_length": 10.0,
        "lexical_diversity": 1.0
    })
    mock.compute_text_hash = MagicMock(return_value="test_hash_123")
    return mock


@pytest.fixture
def sample_claim():
    """Sample claim data."""
    return {
        "text": "This is a test claim about climate change.",
        "url": "https://example.com/post",
        "platform": "twitter",
        "author": "@testuser"
    }


@pytest.fixture
def sample_claim_response():
    """Sample claim database response."""
    return {
        "_key": "test_claim_id",
        "id": "test_claim_id",
        "text": "This is a test claim about climate change.",
        "url": "https://example.com/post",
        "platform": "twitter",
        "author": "@testuser",
        "text_hash": "test_hash_123",
        "metadata": {},
        "created_at": "2024-01-15T12:00:00",
        "updated_at": "2024-01-15T12:00:00",
        "status": "pending"
    }


@pytest.fixture
def sample_verification_result():
    """Sample verification result."""
    return {
        "verdict": "true",
        "confidence": 0.85,
        "explanation": "This claim has been verified by multiple sources.",
        "sources": [],
        "fact_checks": [
            {
                "source": "Test Fact Checker",
                "verdict": "true",
                "rating": 0.9,
                "url": "https://example.com/factcheck"
            }
        ],
        "entities": ["climate change"],
        "sentiment": {
            "polarity": 0.0,
            "subjectivity": 0.5,
            "classification": "neutral"
        },
        "credibility_score": 0.8,
        "checked_at": "2024-01-15T12:00:00"
    }
