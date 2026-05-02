"""Simplified FastAPI application for Phase 6 Backend API."""

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Configuration
class Config:
    API_V1_PREFIX = "/api/v1"
    TITLE = "Restaurant Recommendation API"
    VERSION = "1.0.0"
    DESCRIPTION = "AI-powered restaurant recommendation system backend"
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    DATA_ROOT = "c:/Projects/Milestone1"

# Pydantic Models
class UserPreferenceRequest(BaseModel):
    location: str = Field(..., description="City or area for restaurant search")
    budget: str = Field(..., description="Budget category: low, medium, high")
    cuisine: str = Field(..., description="Preferred cuisine type")
    min_rating: float = Field(..., ge=0, le=5, description="Minimum rating requirement")
    optional_tags: Optional[List[str]] = Field(default=None, description="Additional preference tags")

class RestaurantCard(BaseModel):
    title: str
    subtitle: str
    rating: Optional[float]
    estimated_cost: Optional[float]
    cuisine: Optional[str]
    location: Optional[str]
    explanation: Optional[str]

class RecommendationResponse(BaseModel):
    profile: Dict[str, Any]
    summary: str
    cards: List[RestaurantCard]
    table_rows: List[Dict[str, Any]]
    explanation_lines: List[str]
    meta: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str
    timestamp: str
    components: Dict[str, str]

class FeedbackRequest(BaseModel):
    restaurant_name: str = Field(..., description="Name of the restaurant")
    feedback_type: str = Field(..., description="Type of feedback: like, dislike, selected")
    user_profile: Dict[str, Any] = Field(..., description="User preferences context")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Optional user rating")
    comments: Optional[str] = Field(None, description="Optional user comments")

class ErrorResponse(BaseModel):
    error: str
    error_code: str
    timestamp: str
    request_id: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(
    title=Config.TITLE,
    version=Config.VERSION,
    description=Config.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple in-memory storage for feedback
feedback_storage = []

# Middleware for request tracking
@app.middleware("http")
async def request_tracking_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    
    logger.info(f"Request started: {request.method} {request.url} - ID: {request_id}")
    
    response = await call_next(request)
    
    duration = (datetime.utcnow() - start_time).total_seconds()
    logger.info(f"Request completed: {response.status_code} - Duration: {duration}s - ID: {request_id}")
    
    response.headers["X-Request-ID"] = request_id
    return response

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
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
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            error_code="INTERNAL_ERROR",
            timestamp=datetime.utcnow().isoformat(),
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )

# Helper functions
def load_phase4_data() -> Dict[str, Any]:
    """Load Phase 4 recommendations data."""
    try:
        with open(f"{Config.DATA_ROOT}/phase4_llm_recommendation/data/recommendations.json", "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load Phase 4 data: {str(e)}")
        return {}

def load_phase5_data() -> Dict[str, Any]:
    """Load Phase 5 presentation data."""
    try:
        with open(f"{Config.DATA_ROOT}/phase5_presentation_delivery/data/presentation.json", "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load Phase 5 data: {str(e)}")
        return {}

# API Endpoints

@app.get(f"{Config.API_V1_PREFIX}/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        components = {
            "phase1_data": "unknown",
            "phase2_module": "unknown",
            "phase3_module": "unknown",
            "phase4_module": "unknown",
            "phase5_module": "unknown"
        }
        
        # Check if data files exist
        import os
        phase1_data = f"{Config.DATA_ROOT}/phase1_data_foundation/data/cleaned_restaurants.csv"
        components["phase1_data"] = "healthy" if os.path.exists(phase1_data) else "missing"
        
        return HealthResponse(
            status="healthy",
            version=Config.VERSION,
            timestamp=datetime.utcnow().isoformat(),
            components=components
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.post(f"{Config.API_V1_PREFIX}/recommendations", response_model=RecommendationResponse)
async def get_recommendations(preferences: UserPreferenceRequest):
    """Get restaurant recommendations based on user preferences."""
    try:
        logger.info(f"Recommendation request: {preferences.dict()}")
        
        # For now, load existing Phase 5 data (in production, this would run the full pipeline)
        presentation_data = load_phase5_data()
        
        if not presentation_data:
            # Fallback: create mock response
            presentation_data = {
                "profile": preferences.dict(),
                "summary": "Recommendations generated based on your preferences.",
                "cards": [
                    {
                        "title": "Sample Restaurant",
                        "subtitle": "Rank #1",
                        "rating": 4.5,
                        "estimated_cost": 1200.0,
                        "cuisine": preferences.cuisine,
                        "location": preferences.location,
                        "explanation": "Matches your cuisine and budget preferences."
                    }
                ],
                "table_rows": [
                    {
                        "rank": 1,
                        "name": "Sample Restaurant",
                        "rating": 4.5,
                        "estimated_cost": 1200.0,
                        "cuisine": preferences.cuisine,
                        "location": preferences.location
                    }
                ],
                "explanation_lines": [
                    "Why these restaurants were recommended",
                    f"Preferences considered: location={preferences.location}, budget={preferences.budget}, cuisine={preferences.cuisine}, min_rating={preferences.min_rating}"
                ],
                "meta": {"mode": "demo", "pipeline_status": "simulated"}
            }
        
        return RecommendationResponse(**presentation_data)
        
    except Exception as e:
        logger.error(f"Recommendation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")

@app.post(f"{Config.API_V1_PREFIX}/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit user feedback for recommendations."""
    try:
        logger.info(f"Feedback submission: {feedback.dict()}")
        
        # Store feedback (in production, this would save to database)
        feedback_entry = {
            **feedback.dict(),
            "timestamp": datetime.utcnow().isoformat(),
            "id": len(feedback_storage) + 1
        }
        feedback_storage.append(feedback_entry)
        
        return {"status": "success", "message": "Feedback saved successfully"}
        
    except Exception as e:
        logger.error(f"Feedback failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process feedback")

@app.get(f"{Config.API_V1_PREFIX}/feedback/stats")
async def get_feedback_stats():
    """Get feedback statistics."""
    try:
        total = len(feedback_storage)
        likes = sum(1 for f in feedback_storage if f.get("feedback_type") == "like")
        dislikes = sum(1 for f in feedback_storage if f.get("feedback_type") == "dislike")
        selected = sum(1 for f in feedback_storage if f.get("feedback_type") == "selected")
        
        return {
            "total_feedback": total,
            "like_count": likes,
            "dislike_count": dislikes,
            "selected_count": selected,
            "feedback_data": feedback_storage[-10:]  # Last 10 feedbacks
        }
        
    except Exception as e:
        logger.error(f"Failed to get feedback stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve feedback statistics")

@app.get(f"{Config.API_V1_PREFIX}/data/status")
async def get_data_status():
    """Get data availability status."""
    try:
        import os
        availability = {
            "cleaned_restaurants": os.path.exists(f"{Config.DATA_ROOT}/phase1_data_foundation/data/cleaned_restaurants.csv"),
            "phase2_output": os.path.exists(f"{Config.DATA_ROOT}/phase2_user_preferences/data/validated_profile.json"),
            "phase3_output": os.path.exists(f"{Config.DATA_ROOT}/phase3_candidate_retrieval/data/candidates.json"),
            "phase4_output": os.path.exists(f"{Config.DATA_ROOT}/phase4_llm_recommendation/data/recommendations.json"),
            "phase5_output": os.path.exists(f"{Config.DATA_ROOT}/phase5_presentation_delivery/data/presentation.json")
        }
        return {"data_availability": availability}
        
    except Exception as e:
        logger.error(f"Failed to check data status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check data status")

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting {Config.TITLE} v{Config.VERSION}")
    uvicorn.run(
        "main_simple:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )
