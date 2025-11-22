from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class ClaimBase(BaseModel):
    """Base model for claims."""

    text: str = Field(..., description="The claim text to be verified")
    url: Optional[HttpUrl] = Field(None, description="Source URL of the claim")
    platform: Optional[str] = Field(None, description="Social media platform")
    author: Optional[str] = Field(None, description="Author of the claim")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ClaimCreate(ClaimBase):
    """Model for creating a new claim."""

    pass


class ClaimUpdate(BaseModel):
    """Model for updating a claim."""

    text: Optional[str] = None
    url: Optional[HttpUrl] = None
    platform: Optional[str] = None
    author: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Claim(ClaimBase):
    """Full claim model with database fields."""

    id: str = Field(..., description="Unique claim identifier")
    text_hash: str = Field(..., description="Hash of the claim text")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending", description="Verification status")

    class Config:
        from_attributes = True


class VerificationResult(BaseModel):
    """Model for fact-check verification results."""

    verdict: str = Field(..., description="Verification verdict (true/false/mixed/unverifiable)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    explanation: str = Field(..., description="Detailed explanation of the verdict")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Supporting sources")
    fact_checks: List[Dict[str, Any]] = Field(
        default_factory=list, description="Related fact-checks"
    )
    entities: List[str] = Field(default_factory=list, description="Extracted entities")
    sentiment: Optional[Dict[str, Any]] = Field(None, description="Sentiment analysis")
    credibility_score: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Source credibility score"
    )
    checked_at: datetime = Field(default_factory=datetime.utcnow)


class ClaimAnalysis(BaseModel):
    """Complete claim analysis including verification."""

    claim: Claim
    verification: VerificationResult
    temporal_history: Optional[List[Dict[str, Any]]] = Field(
        None, description="Historical verifications from XTDB"
    )


class ClaimResponse(BaseModel):
    """Response model for claim verification."""

    success: bool = Field(..., description="Whether the verification was successful")
    claim_id: str = Field(..., description="Unique identifier for this claim")
    analysis: Optional[ClaimAnalysis] = Field(None, description="Full analysis if successful")
    error: Optional[str] = Field(None, description="Error message if failed")
    processing_time: float = Field(..., description="Time taken to process in seconds")
