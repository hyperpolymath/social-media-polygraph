import pytest
from app.ml.credibility_scorer import CredibilityScorer


@pytest.fixture
def scorer():
    """Credibility scorer instance."""
    return CredibilityScorer()


def test_score_source_new_source(scorer):
    """Test scoring for a new source with no history."""
    score = scorer.score_source(
        fact_check_record={},
        verification_count=0,
        age_days=0,
        category="unknown"
    )

    assert 0.0 <= score <= 1.0
    assert score == 0.5  # New sources get neutral score


def test_score_source_high_accuracy(scorer):
    """Test scoring for a source with high accuracy."""
    score = scorer.score_source(
        fact_check_record={"true": 90, "false": 10},
        verification_count=100,
        age_days=400,
        category="mainstream_news"
    )

    assert 0.0 <= score <= 1.0
    assert score > 0.7  # Should be high


def test_score_source_low_accuracy(scorer):
    """Test scoring for a source with low accuracy."""
    score = scorer.score_source(
        fact_check_record={"true": 10, "false": 90},
        verification_count=100,
        age_days=400,
        category="blog"
    )

    assert 0.0 <= score <= 1.0
    assert score < 0.5  # Should be low


def test_score_claim(scorer):
    """Test claim credibility scoring."""
    result = scorer.score_claim(
        source_credibility=0.8,
        fact_check_results=[
            {"verdict": "true", "rating": 0.9},
            {"verdict": "true", "rating": 0.85}
        ],
        corroborating_sources=3,
        claim_complexity={
            "lexical_diversity": 0.5,
            "avg_sentence_length": 15
        }
    )

    assert "overall_score" in result
    assert "confidence" in result
    assert "breakdown" in result
    assert "recommendation" in result

    assert 0.0 <= result["overall_score"] <= 1.0
    assert 0.0 <= result["confidence"] <= 1.0


def test_get_recommendation(scorer):
    """Test recommendation based on score."""
    assert scorer._get_recommendation(0.9) == "highly_credible"
    assert scorer._get_recommendation(0.7) == "likely_credible"
    assert scorer._get_recommendation(0.5) == "uncertain"
    assert scorer._get_recommendation(0.3) == "likely_not_credible"
    assert scorer._get_recommendation(0.1) == "not_credible"


def test_calculate_bias_score(scorer):
    """Test bias score calculation."""
    # Neutral sentiment
    neutral_bias = scorer.calculate_bias_score(
        sentiment={"polarity": 0.0, "subjectivity": 0.5},
        entity_sentiment=[],
        language_patterns={}
    )
    assert -1.0 <= neutral_bias <= 1.0
    assert abs(neutral_bias) < 0.2  # Should be near zero

    # Positive and subjective
    positive_bias = scorer.calculate_bias_score(
        sentiment={"polarity": 0.8, "subjectivity": 0.9},
        entity_sentiment=[],
        language_patterns={}
    )
    assert positive_bias > 0  # Should be positive

    # Negative and subjective
    negative_bias = scorer.calculate_bias_score(
        sentiment={"polarity": -0.8, "subjectivity": 0.9},
        entity_sentiment=[],
        language_patterns={}
    )
    assert negative_bias < 0  # Should be negative
