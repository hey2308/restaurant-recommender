"""Main FastAPI application for Phase 6 Backend API."""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import settings
from models_simple import (
    UserPreferenceRequest, 
    RecommendationResponse, 
    HealthResponse, 
    FeedbackRequest,
    ErrorResponse
)
from orchestration import OrchestrationService
from data_access import DataAccessLayer
from auth import auth, rate_limiter
from logging_config import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Initialize services
orchestration_service = OrchestrationService()
data_access = DataAccessLayer()


# Middleware for request tracking
@app.middleware("http")
async def request_tracking_middleware(request: Request, call_next):
    """Add request tracking and logging."""
    request_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    
    # Log request
    logger.info(
        "request_started",
        method=request.method,
        url=str(request.url),
        request_id=request_id,
        client_ip=request.client.host if request.client else None
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = (datetime.utcnow() - start_time).total_seconds()
    
    # Log response
    logger.info(
        "request_completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        duration_seconds=duration,
        request_id=request_id
    )
    
    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id
    return response


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with structured error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            error_code=f"HTTP_{exc.status_code}",
            timestamp=datetime.utcnow().isoformat(),
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with structured error response."""
    logger.error(
        "unhandled_exception",
        error=str(exc),
        request_id=request.headers.get("X-Request-ID"),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            error_code="INTERNAL_ERROR",
            timestamp=datetime.utcnow().isoformat(),
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )


# API Endpoints

@app.get(f"{settings.API_V1_PREFIX}/health", response_model=HealthResponse)
@limiter.limit("10/minute")
async def health_check(request: Request):
    """Health check endpoint."""
    try:
        components = await orchestration_service.health_check()
        
        return HealthResponse(
            status="healthy",
            version=settings.VERSION,
            timestamp=datetime.utcnow().isoformat(),
            components=components
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        )


@app.post(f"{settings.API_V1_PREFIX}/recommendations", response_model=RecommendationResponse)
@limiter.limit("5/minute")
async def get_recommendations(
    request: Request,
    preferences: UserPreferenceRequest,
    api_key: str = None
):
    """Get restaurant recommendations based on user preferences."""
    request_id = request.headers.get("X-Request-ID", "unknown")
    
    try:
        # Simple API key validation (optional for demo)
        if api_key and not auth.validate_api_key(api_key):
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        
        # Rate limiting check
        client_id = get_remote_address(request)
        if not rate_limiter.is_allowed(client_id):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
        
        logger.info(
            "recommendation_request",
            preferences=preferences.dict(),
            request_id=request_id
        )
        
        # Run recommendation pipeline
        result = await orchestration_service.run_recommendation_pipeline(
            preferences.dict()
        )
        
        logger.info(
            "recommendation_completed",
            recommendations_count=len(result.get("cards", [])),
            request_id=request_id
        )
        
        return RecommendationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "recommendation_failed",
            error=str(e),
            request_id=request_id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to generate recommendations"
        )


@app.post(f"{settings.API_V1_PREFIX}/feedback")
@limiter.limit("10/minute")
async def submit_feedback(
    request: Request,
    feedback: FeedbackRequest,
    api_key: str = None
):
    """Submit user feedback for recommendations."""
    request_id = request.headers.get("X-Request-ID", "unknown")
    
    try:
        # Simple API key validation (optional for demo)
        if api_key and not auth.validate_api_key(api_key):
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        
        logger.info(
            "feedback_submission",
            feedback_type=feedback.feedback_type,
            restaurant=feedback.restaurant_name,
            request_id=request_id
        )
        
        # Save feedback
        success = await data_access.save_feedback(feedback.dict())
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to save feedback"
            )
        
        logger.info(
            "feedback_saved",
            feedback_type=feedback.feedback_type,
            restaurant=feedback.restaurant_name,
            request_id=request_id
        )
        
        return {"status": "success", "message": "Feedback saved successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "feedback_failed",
            error=str(e),
            request_id=request_id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to process feedback"
        )


@app.get(f"{settings.API_V1_PREFIX}/feedback/stats")
@limiter.limit("5/minute")
async def get_feedback_stats(request: Request):
    """Get feedback statistics."""
    try:
        stats = await data_access.get_feedback_stats()
        return stats
    except Exception as e:
        logger.error(f"Failed to get feedback stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve feedback statistics"
        )


@app.get(f"{settings.API_V1_PREFIX}/data/status")
@limiter.limit("10/minute")
async def get_data_status(request: Request):
    """Get data availability status."""
    try:
        availability = data_access.check_data_availability()
        return {"data_availability": availability}
    except Exception as e:
        logger.error(f"Failed to check data status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to check data status"
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    logger.info(
        "application_startup",
        version=settings.VERSION,
        environment="development" if settings.DEBUG else "production"
    )
    
    # Check data availability
    availability = data_access.check_data_availability()
    logger.info("data_availability_check", **availability)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    logger.info("application_shutdown")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
