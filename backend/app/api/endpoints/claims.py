from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from loguru import logger
import time

from app.models import ClaimCreate, ClaimResponse, ClaimAnalysis, Claim
from app.services import claim_service
from app.api.dependencies import get_current_user_optional

router = APIRouter()


@router.post("/verify", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def verify_claim(
    claim_data: ClaimCreate,
    user_id: Optional[str] = Depends(get_current_user_optional),
) -> ClaimResponse:
    """
    Submit a claim for verification.

    This endpoint:
    1. Creates a new claim in the database
    2. Extracts entities and analyzes sentiment
    3. Queries fact-checking services
    4. Calculates credibility scores
    5. Returns comprehensive analysis

    Args:
        claim_data: Claim submission data
        user_id: Optional authenticated user ID

    Returns:
        Complete claim analysis with verification results
    """
    start_time = time.time()

    try:
        # Create claim
        claim = await claim_service.create_claim(claim_data)

        # Verify claim
        analysis = await claim_service.verify_claim(claim.id)

        processing_time = time.time() - start_time

        return ClaimResponse(
            success=True,
            claim_id=claim.id,
            analysis=analysis,
            processing_time=round(processing_time, 3),
        )

    except Exception as e:
        logger.error(f"Error verifying claim: {e}")
        processing_time = time.time() - start_time

        return ClaimResponse(
            success=False,
            claim_id="",
            error=str(e),
            processing_time=round(processing_time, 3),
        )


@router.get("/{claim_id}", response_model=ClaimAnalysis)
async def get_claim_analysis(
    claim_id: str,
    user_id: Optional[str] = Depends(get_current_user_optional),
) -> ClaimAnalysis:
    """
    Get analysis for a previously verified claim.

    Args:
        claim_id: Claim identifier
        user_id: Optional authenticated user ID

    Returns:
        Complete claim analysis

    Raises:
        HTTPException: If claim not found
    """
    try:
        analysis = await claim_service.verify_claim(claim_id)
        return analysis
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error getting claim analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/", response_model=List[Claim])
async def list_claims(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    status: Optional[str] = Query(None, description="Filter by status"),
    user_id: Optional[str] = Depends(get_current_user_optional),
) -> List[Claim]:
    """
    List claims with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        status: Optional status filter
        user_id: Optional authenticated user ID

    Returns:
        List of claims
    """
    try:
        claims = await claim_service.list_claims(skip=skip, limit=limit, status=status)
        return claims
    except Exception as e:
        logger.error(f"Error listing claims: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{claim_id}/history")
async def get_claim_history(
    claim_id: str,
    user_id: Optional[str] = Depends(get_current_user_optional),
) -> List[dict]:
    """
    Get temporal history of a claim's verifications.

    Uses XTDB to show how the verification of this claim has changed over time.

    Args:
        claim_id: Claim identifier
        user_id: Optional authenticated user ID

    Returns:
        List of historical verification records
    """
    from app.db import xtdb_client

    try:
        history = await xtdb_client.get_claim_history(claim_id)
        return history
    except Exception as e:
        logger.error(f"Error getting claim history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
