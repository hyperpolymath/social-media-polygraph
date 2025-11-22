import pytest
from app.ml.nlp_processor import NLPProcessor


@pytest.fixture
def nlp():
    """NLP processor instance."""
    processor = NLPProcessor()
    # Mock initialization to avoid downloading models in tests
    processor._initialized = True
    processor.nlp = None  # Would be mocked or use small test model
    return processor


def test_compute_text_hash():
    """Test text hash computation."""
    processor = NLPProcessor()
    text1 = "This is a test claim."
    text2 = "This   is   a   test   claim."  # Extra spaces
    text3 = "THIS IS A TEST CLAIM."  # Different case

    hash1 = processor.compute_text_hash(text1)
    hash2 = processor.compute_text_hash(text2)
    hash3 = processor.compute_text_hash(text3)

    # All should produce the same hash (normalized)
    assert hash1 == hash2 == hash3
    assert len(hash1) == 64  # SHA256 hash length


def test_analyze_sentiment():
    """Test sentiment analysis."""
    processor = NLPProcessor()

    # Positive text
    positive = processor.analyze_sentiment("This is wonderful and amazing!")
    assert positive["classification"] in ["positive", "neutral"]
    assert -1.0 <= positive["polarity"] <= 1.0
    assert 0.0 <= positive["subjectivity"] <= 1.0

    # Negative text
    negative = processor.analyze_sentiment("This is terrible and horrible!")
    assert negative["classification"] in ["negative", "neutral"]
    assert -1.0 <= negative["polarity"] <= 1.0

    # Neutral text
    neutral = processor.analyze_sentiment("The meeting is at 3pm.")
    assert neutral["classification"] in ["neutral", "positive", "negative"]


def test_detect_language():
    """Test language detection."""
    processor = NLPProcessor()

    assert processor.detect_language("This is an English sentence.") == "en"
    assert processor.detect_language("Esto es una frase en español.") == "es"
    # Very short text may fail
    assert processor.detect_language("a") is None or isinstance(
        processor.detect_language("a"), str
    )
