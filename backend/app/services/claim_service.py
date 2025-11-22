from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
from loguru import logger

from app.db import arango_manager, xtdb_client, cache_manager
from app.ml import nlp_processor, credibility_scorer
from app.services.fact_checker import fact_check_service
from app.models import ClaimCreate, Claim, VerificationResult, ClaimAnalysis


class ClaimService:
    """Service for processing and verifying claims."""

    async def create_claim(self, claim_data: ClaimCreate) -> Claim:
        """
        Create a new claim in the database.

        Args:
            claim_data: Claim creation data

        Returns:
            Created claim
        """
        # Generate unique ID
        claim_id = str(uuid.uuid4())

        # Compute text hash for deduplication
        text_hash = nlp_processor.compute_text_hash(claim_data.text)

        # Check if claim already exists
        claims_collection = arango_manager.get_collection("claims")
        existing = claims_collection.find({"text_hash": text_hash}, limit=1)

        if existing.count() > 0:
            logger.info(f"Claim already exists with hash: {text_hash}")
            return Claim(**existing.next())

        # Create new claim
        claim_doc = {
            "_key": claim_id,
            "id": claim_id,
            "text": claim_data.text,
            "url": str(claim_data.url) if claim_data.url else None,
            "platform": claim_data.platform,
            "author": claim_data.author,
            "text_hash": text_hash,
            "metadata": claim_data.metadata,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "status": "pending",
        }

        claims_collection.insert(claim_doc)
        logger.info(f"Created claim: {claim_id}")

        return Claim(**claim_doc)

    async def verify_claim(self, claim_id: str) -> ClaimAnalysis:
        """
        Perform comprehensive verification of a claim.

        Args:
            claim_id: Claim identifier

        Returns:
            Complete claim analysis
        """
        # Check cache first
        cache_key = f"claim:verification:{claim_id}"
        cached = await cache_manager.get(cache_key)
        if cached:
            logger.info(f"Returning cached verification for claim: {claim_id}")
            return ClaimAnalysis(**cached)

        # Get claim from database
        claims_collection = arango_manager.get_collection("claims")
        claim_doc = claims_collection.get(claim_id)

        if not claim_doc:
            raise ValueError(f"Claim not found: {claim_id}")

        claim = Claim(**claim_doc)

        # Extract entities
        entities = nlp_processor.extract_entities(claim.text)

        # Analyze sentiment
        sentiment = nlp_processor.analyze_sentiment(claim.text)

        # Analyze complexity
        complexity = nlp_processor.analyze_complexity(claim.text)

        # Get fact-check results
        fact_checks = await fact_check_service.aggregate_fact_checks(claim.text)

        # Determine verdict from fact-checks
        if fact_checks:
            verdicts = [fc.get("verdict", "unverifiable") for fc in fact_checks]
            # Most common verdict
            verdict = max(set(verdicts), key=verdicts.count)
            avg_rating = sum(fc.get("rating", 0.5) for fc in fact_checks) / len(fact_checks)
        else:
            verdict = "unverifiable"
            avg_rating = 0.5

        # Calculate credibility score
        credibility = credibility_scorer.score_claim(
            source_credibility=0.7,  # Would get from source analysis
            fact_check_results=fact_checks,
            corroborating_sources=len(fact_checks),
            claim_complexity=complexity,
        )

        # Create verification result
        verification = VerificationResult(
            verdict=verdict,
            confidence=avg_rating,
            explanation=self._generate_explanation(verdict, fact_checks),
            sources=[],
            fact_checks=fact_checks,
            entities=[e["text"] for e in entities],
            sentiment=sentiment,
            credibility_score=credibility["overall_score"],
        )

        # Store in XTDB for temporal tracking
        if settings.enable_temporal_tracking:
            await xtdb_client.put_claim_verification(
                claim_id=claim_id,
                verification_data={
                    "verdict": verdict,
                    "confidence": avg_rating,
                    "credibility_score": credibility["overall_score"],
                    "fact_checks_count": len(fact_checks),
                },
            )

        # Get temporal history
        temporal_history = None
        if settings.enable_temporal_tracking:
            try:
                temporal_history = await xtdb_client.get_claim_history(claim_id)
            except Exception as e:
                logger.error(f"Error getting claim history: {e}")

        # Create analysis
        analysis = ClaimAnalysis(
            claim=claim,
            verification=verification,
            temporal_history=temporal_history,
        )

        # Cache result
        await cache_manager.set(cache_key, analysis.model_dump(), ttl=3600)

        # Update claim status
        claims_collection.update({
            "_key": claim_id,
            "status": "verified",
            "updated_at": datetime.utcnow().isoformat(),
        })

        return analysis

    def _generate_explanation(
        self,
        verdict: str,
        fact_checks: List[Dict[str, Any]],
    ) -> str:
        """
        Generate human-readable explanation of the verdict.

        Args:
            verdict: Verification verdict
            fact_checks: Fact-check results

        Returns:
            Explanation text
        """
        if not fact_checks:
            return (
                "This claim could not be verified due to insufficient information "
                "from fact-checking sources."
            )

        sources_text = ", ".join(set(fc.get("source", "Unknown") for fc in fact_checks))

        explanations = {
            "true": f"This claim has been verified as true by {sources_text}.",
            "mostly_true": f"This claim is mostly accurate according to {sources_text}, though some details may need context.",
            "mixed": f"This claim contains both accurate and inaccurate elements according to {sources_text}.",
            "mostly_false": f"This claim is mostly inaccurate according to {sources_text}.",
            "false": f"This claim has been fact-checked and found to be false by {sources_text}.",
            "unverifiable": f"This claim cannot be verified with available information from {sources_text}.",
        }

        return explanations.get(
            verdict,
            f"Verification status unclear. See fact-check sources for details.",
        )

    async def get_claim(self, claim_id: str) -> Optional[Claim]:
        """
        Get a claim by ID.

        Args:
            claim_id: Claim identifier

        Returns:
            Claim or None
        """
        claims_collection = arango_manager.get_collection("claims")
        claim_doc = claims_collection.get(claim_id)

        if not claim_doc:
            return None

        return Claim(**claim_doc)

    async def list_claims(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
    ) -> List[Claim]:
        """
        List claims with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            status: Filter by status

        Returns:
            List of claims
        """
        claims_collection = arango_manager.get_collection("claims")

        query = {}
        if status:
            query["status"] = status

        cursor = claims_collection.find(query, skip=skip, limit=limit)
        return [Claim(**doc) for doc in cursor]


# Global instance
claim_service = ClaimService()
