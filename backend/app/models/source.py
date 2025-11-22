from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class SourceBase(BaseModel):
    """Base model for sources."""

    domain: str = Field(..., description="Domain name of the source")
    name: str = Field(..., description="Human-readable name")
    url: HttpUrl = Field(..., description="Base URL")
    category: Optional[str] = Field(None, description="Source category (news, blog, academic, etc.)")
    country: Optional[str] = Field(None, description="Country of origin")


class SourceCreate(SourceBase):
    """Model for creating a new source."""

    pass


class Source(SourceBase):
    """Full source model with credibility scoring."""

    id: str = Field(..., description="Unique source identifier")
    credibility_score: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Overall credibility score"
    )
    bias_score: Optional[float] = Field(
        None, ge=-1.0, le=1.0, description="Political bias (-1 left, 1 right)"
    )
    fact_check_record: Dict[str, int] = Field(
        default_factory=lambda: {"true": 0, "false": 0, "mixed": 0, "unverifiable": 0},
        description="Historical fact-check record",
    )
    verification_count: int = Field(default=0, description="Number of claims verified")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class SourceCredibilityUpdate(BaseModel):
    """Model for updating source credibility."""

    credibility_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    bias_score: Optional[float] = Field(None, ge=-1.0, le=1.0)
    fact_check_record: Optional[Dict[str, int]] = None


class SourceAnalysis(BaseModel):
    """Detailed source analysis."""

    source: Source
    recent_claims: List[Dict[str, Any]] = Field(
        default_factory=list, description="Recent claims from this source"
    )
    related_sources: List[Source] = Field(
        default_factory=list, description="Related or similar sources"
    )
    credibility_breakdown: Dict[str, Any] = Field(
        default_factory=dict, description="Detailed credibility metrics"
    )
