"""Configuration for Phase 6 Backend API."""

from __future__ import annotations

import os
from typing import Any


class Settings:
    """Application settings."""
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    TITLE: str = "Restaurant Recommendation API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered restaurant recommendation system backend"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
    
    # Redis Configuration (for rate limiting)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Data Paths
    DATA_ROOT: str = os.getenv("DATA_ROOT", "c:/Projects/Milestone1")
    PHASE2_OUTPUT: str = f"{DATA_ROOT}/phase2_user_preferences/data/validated_profile.json"
    PHASE3_OUTPUT: str = f"{DATA_ROOT}/phase3_candidate_retrieval/data/candidates.json"
    PHASE4_OUTPUT: str = f"{DATA_ROOT}/phase4_llm_recommendation/data/recommendations.json"
    PHASE5_OUTPUT: str = f"{DATA_ROOT}/phase5_presentation_delivery/data/presentation.json"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Observability
    ENABLE_TRACING: bool = os.getenv("ENABLE_TRACING", "false").lower() == "true"
    OTEL_EXPORTER_OTLP_ENDPOINT: str = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"
    )
    
    @classmethod
    def as_dict(cls) -> dict[str, Any]:
        """Return settings as dictionary."""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith("_") and not callable(getattr(cls, key))
        }


settings = Settings()
