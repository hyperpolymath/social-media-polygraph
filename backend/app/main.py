from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger
import sys

from app.core.config import settings
from app.api import api_router
from app.db import arango_manager, xtdb_client, cache_manager
from app.ml import nlp_processor
from app.services import fact_check_service


# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.log_level,
)


# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting Social Media Polygraph API...")

    try:
        # Initialize databases
        await arango_manager.connect()
        await xtdb_client.connect()
        await cache_manager.connect()

        # Initialize ML models
        nlp_processor.initialize()

        # Initialize services
        await fact_check_service.initialize()

        logger.info("All services initialized successfully")

    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down...")

    await arango_manager.disconnect()
    await xtdb_client.disconnect()
    await cache_manager.disconnect()
    await fact_check_service.shutdown()

    logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered social media fact-checking and misinformation detection system",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
if settings.environment == "production":
    Instrumentator().instrument(app).expose(app)

# Include API routes
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns service health status and dependencies.
    """
    health_status = {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment,
        "services": {
            "arango": arango_manager.is_connected,
            "xtdb": xtdb_client.is_connected,
            "cache": cache_manager.is_connected,
            "nlp": nlp_processor.is_initialized,
        },
    }

    # Check if any service is down
    if not all(health_status["services"].values()):
        health_status["status"] = "degraded"

    return health_status


@app.get("/info")
async def info():
    """
    Get API information and capabilities.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "features": {
            "fact_checking": settings.enable_fact_checking,
            "sentiment_analysis": settings.enable_sentiment_analysis,
            "source_credibility": settings.enable_source_credibility,
            "temporal_tracking": settings.enable_temporal_tracking,
        },
        "endpoints": {
            "verify_claim": f"{settings.api_v1_prefix}/claims/verify",
            "get_claim": f"{settings.api_v1_prefix}/claims/{{claim_id}}",
            "claim_history": f"{settings.api_v1_prefix}/claims/{{claim_id}}/history",
            "register": f"{settings.api_v1_prefix}/auth/register",
            "login": f"{settings.api_v1_prefix}/auth/login",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.workers,
    )
