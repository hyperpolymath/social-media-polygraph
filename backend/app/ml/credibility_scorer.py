from typing import Dict, Any, List
import numpy as np
from datetime import datetime, timedelta
from loguru import logger


class CredibilityScorer:
    """Algorithm for scoring source and claim credibility."""

    def __init__(self) -> None:
        # Weights for different credibility factors
        self.weights = {
            "historical_accuracy": 0.35,
            "source_reputation": 0.25,
            "claim_complexity": 0.15,
            "corroboration": 0.15,
            "recency": 0.10,
        }

    def score_source(
        self,
        fact_check_record: Dict[str, int],
        verification_count: int,
        age_days: int,
        category: str = "unknown",
    ) -> float:
        """
        Calculate credibility score for a source.

        Args:
            fact_check_record: Historical fact-check verdicts
            verification_count: Total number of verifications
            age_days: Age of source in days
            category: Source category

        Returns:
            Credibility score (0-1)
        """
        if verification_count == 0:
            return 0.5  # Neutral score for new sources

        # Calculate accuracy rate
        total_checks = sum(fact_check_record.values())
        if total_checks == 0:
            accuracy_score = 0.5
        else:
            # Weight different verdicts
            weighted_score = (
                fact_check_record.get("true", 0) * 1.0
                + fact_check_record.get("mixed", 0) * 0.5
                + fact_check_record.get("unverifiable", 0) * 0.3
                + fact_check_record.get("false", 0) * 0.0
            )
            accuracy_score = weighted_score / total_checks

        # Category-based reputation
        category_scores = {
            "academic": 0.9,
            "government": 0.85,
            "mainstream_news": 0.7,
            "fact_checker": 0.95,
            "blog": 0.4,
            "social_media": 0.3,
            "unknown": 0.5,
        }
        reputation_score = category_scores.get(category, 0.5)

        # Recency bonus (established sources get bonus)
        if age_days > 365:
            recency_multiplier = 1.1
        elif age_days > 180:
            recency_multiplier = 1.0
        else:
            recency_multiplier = 0.9

        # Verification count confidence (more data = higher confidence)
        confidence_multiplier = min(1.0, np.log10(verification_count + 1) / 2)

        # Combine scores
        base_score = (
            accuracy_score * self.weights["historical_accuracy"]
            + reputation_score * self.weights["source_reputation"]
        )

        final_score = base_score * recency_multiplier * (0.5 + 0.5 * confidence_multiplier)

        return np.clip(final_score, 0.0, 1.0)

    def score_claim(
        self,
        source_credibility: float,
        fact_check_results: List[Dict[str, Any]],
        corroborating_sources: int,
        claim_complexity: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate credibility score for a claim.

        Args:
            source_credibility: Credibility of the claim source
            fact_check_results: Results from fact-checking services
            corroborating_sources: Number of sources corroborating the claim
            claim_complexity: Text complexity metrics

        Returns:
            Credibility assessment with score and breakdown
        """
        # Source credibility component
        source_score = source_credibility

        # Fact-check results component
        if fact_check_results:
            verdicts = [result.get("verdict", "unverifiable") for result in fact_check_results]
            verdict_scores = {
                "true": 1.0,
                "mostly_true": 0.8,
                "mixed": 0.5,
                "mostly_false": 0.2,
                "false": 0.0,
                "unverifiable": 0.5,
            }

            fact_check_score = np.mean(
                [verdict_scores.get(v, 0.5) for v in verdicts]
            )
        else:
            fact_check_score = 0.5

        # Corroboration component
        # More independent sources = higher credibility
        corroboration_score = min(1.0, corroborating_sources / 5.0)

        # Complexity component (simpler claims are easier to verify)
        complexity_score = self._score_complexity(claim_complexity)

        # Recency component (claims about recent events)
        recency_score = 0.8  # Default, would need timestamp to calculate

        # Weighted combination
        overall_score = (
            source_score * self.weights["source_reputation"]
            + fact_check_score * self.weights["historical_accuracy"]
            + corroboration_score * self.weights["corroboration"]
            + complexity_score * self.weights["claim_complexity"]
            + recency_score * self.weights["recency"]
        )

        # Normalize to 0-1 range
        overall_score = np.clip(overall_score, 0.0, 1.0)

        return {
            "overall_score": round(float(overall_score), 3),
            "confidence": self._calculate_confidence(fact_check_results, corroborating_sources),
            "breakdown": {
                "source_credibility": round(float(source_score), 3),
                "fact_check_consensus": round(float(fact_check_score), 3),
                "corroboration": round(float(corroboration_score), 3),
                "complexity": round(float(complexity_score), 3),
                "recency": round(float(recency_score), 3),
            },
            "recommendation": self._get_recommendation(overall_score),
        }

    def _score_complexity(self, complexity: Dict[str, Any]) -> float:
        """
        Score based on text complexity.

        Lower complexity = easier to verify = slightly higher initial credibility
        """
        if not complexity:
            return 0.5

        # Inverse relationship with complexity
        diversity = complexity.get("lexical_diversity", 0.5)
        avg_sentence_length = complexity.get("avg_sentence_length", 15)

        # Normalize
        diversity_score = 1.0 - min(1.0, diversity)
        length_score = 1.0 - min(1.0, avg_sentence_length / 30.0)

        return (diversity_score + length_score) / 2

    def _calculate_confidence(
        self,
        fact_check_results: List[Dict[str, Any]],
        corroborating_sources: int,
    ) -> float:
        """
        Calculate confidence in the credibility score.

        More data sources = higher confidence
        """
        data_points = len(fact_check_results) + corroborating_sources

        if data_points == 0:
            return 0.1  # Very low confidence
        elif data_points <= 2:
            return 0.4
        elif data_points <= 5:
            return 0.7
        else:
            return 0.9

    def _get_recommendation(self, score: float) -> str:
        """
        Get recommendation based on credibility score.

        Args:
            score: Credibility score (0-1)

        Returns:
            Recommendation string
        """
        if score >= 0.8:
            return "highly_credible"
        elif score >= 0.6:
            return "likely_credible"
        elif score >= 0.4:
            return "uncertain"
        elif score >= 0.2:
            return "likely_not_credible"
        else:
            return "not_credible"

    def calculate_bias_score(
        self,
        sentiment: Dict[str, Any],
        entity_sentiment: List[Dict[str, Any]],
        language_patterns: Dict[str, Any],
    ) -> float:
        """
        Calculate potential bias in content.

        Args:
            sentiment: Overall sentiment analysis
            entity_sentiment: Sentiment toward specific entities
            language_patterns: Patterns indicating bias

        Returns:
            Bias score (-1 to 1, where 0 is neutral)
        """
        # This is a simplified bias detection
        # In production, would use more sophisticated ML models

        polarity = sentiment.get("polarity", 0.0)
        subjectivity = sentiment.get("subjectivity", 0.5)

        # High subjectivity with strong polarity suggests bias
        bias_magnitude = abs(polarity) * subjectivity

        # Return with original polarity direction
        return np.clip(polarity * bias_magnitude, -1.0, 1.0)


# Global instance
credibility_scorer = CredibilityScorer()
