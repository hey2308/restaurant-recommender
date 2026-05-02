"""Authentication and authorization utilities."""

from __future__ import annotations

import secrets
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SimpleAuth:
    """Simple token-based authentication for demo purposes."""
    
    def __init__(self):
        self.api_keys = {
            "demo-key-123": {"name": "demo", "created": datetime.utcnow()},
            "test-key-456": {"name": "test", "created": datetime.utcnow()},
        }
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate an API key and return user info."""
        if api_key in self.api_keys:
            return self.api_keys[api_key]
        return None
    
    def generate_api_key(self, name: str) -> str:
        """Generate a new API key."""
        api_key = f"{name}-key-{secrets.token_urlsafe(16)}"
        self.api_keys[api_key] = {"name": name, "created": datetime.utcnow()}
        return api_key


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed based on rate limit."""
        now = datetime.utcnow()
        
        # Clean old entries
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if now - req_time < timedelta(seconds=self.window_seconds)
            ]
        else:
            self.requests[identifier] = []
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        
        return False
    
    def get_remaining_requests(self, identifier: str) -> int:
        """Get remaining requests for identifier."""
        if identifier not in self.requests:
            return self.max_requests
        
        now = datetime.utcnow()
        # Count recent requests
        recent_requests = sum(
            1 for req_time in self.requests[identifier]
            if now - req_time < timedelta(seconds=self.window_seconds)
        )
        
        return max(0, self.max_requests - recent_requests)


# Global instances
auth = SimpleAuth()
rate_limiter = RateLimiter(max_requests=10, window_seconds=60)
