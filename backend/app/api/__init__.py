from fastapi import APIRouter
from app.api.endpoints import claims, auth

api_router = APIRouter()

api_router.include_router(claims.router, prefix="/claims", tags=["claims"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

__all__ = ["api_router"]
