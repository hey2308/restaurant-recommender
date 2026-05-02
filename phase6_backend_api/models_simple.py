"""Simplified Pydantic models for API requests and responses."""

from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Field


class UserPreferenceRequest(BaseModel):
    """Request model for user preferences."""
    
    location: str = Field(..., description="City or area for restaurant search")
    budget: str = Field(..., description="Budget category: low, medium, high")
    cuisine: str = Field(..., description="Preferred cuisine type")
    min_rating: float = Field(..., ge=0, le=5, description="Minimum rating requirement")
    optional_tags: Optional[List[str]] = Field(default=None, description="Additional preference tags")


class RestaurantCard(BaseModel):
    """Restaurant card representation."""
    
    title: str
    subtitle: str
    rating: Optional[float]
    estimated_cost: Optional[float]
    cuisine: Optional[str]
    location: Optional[str]
    explanation: Optional[str]


class RecommendationResponse(BaseModel):
    """Response model for recommendations."""
    
    profile: Dict[str, Any]
    summary: str
    cards: List[RestaurantCard]
    table_rows: List[Dict[str, Any]]
    explanation_lines: List[str]
    meta: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = "healthy"
    version: str
    timestamp: str
    components: Dict[str, str]


class FeedbackRequest(BaseModel):
    """Feedback submission model."""
    
    restaurant_name: str = Field(..., description="Name of the restaurant")
    feedback_type: str = Field(..., description="Type of feedback: like, dislike, selected")
    user_profile: Dict[str, Any] = Field(..., description="User preferences context")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Optional user rating")
    comments: Optional[str] = Field(None, description="Optional user comments")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    timestamp: str = Field(..., description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request tracking ID")
