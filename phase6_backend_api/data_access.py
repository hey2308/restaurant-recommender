"""Data Access Layer for restaurant data and feedback storage."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from config import settings


logger = logging.getLogger(__name__)


class DataAccessLayer:
    """Handles data access for restaurant data and user feedback."""
    
    def __init__(self):
        self.data_root = Path(settings.DATA_ROOT)
        self.feedback_file = self.data_root / "phase6_backend_api" / "data" / "feedback.json"
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
    
    def get_cleaned_restaurants(self) -> List[Dict[str, Any]]:
        """Load cleaned restaurant data from Phase 1."""
        try:
            restaurants_file = self.data_root / "phase1_data_foundation" / "data" / "cleaned_restaurants.csv"
            if not restaurants_file.exists():
                logger.warning(f"Cleaned restaurants file not found: {restaurants_file}")
                return []
            
            # For now, return empty list - CSV parsing would require pandas
            # In production, this would load and return the restaurant dataset
            logger.info(f"Restaurant data available at: {restaurants_file}")
            return []
            
        except Exception as e:
            logger.error(f"Failed to load restaurant data: {str(e)}")
            return []
    
    async def save_feedback(self, feedback: Dict[str, Any]) -> bool:
        """Save user feedback to storage."""
        try:
            # Load existing feedback
            feedback_data = []
            if self.feedback_file.exists():
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    feedback_data = json.load(f)
            
            # Add timestamp and ID
            feedback['timestamp'] = datetime.utcnow().isoformat()
            feedback['id'] = len(feedback_data) + 1
            
            # Append new feedback
            feedback_data.append(feedback)
            
            # Save back to file
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, indent=2)
            
            logger.info(f"Feedback saved: {feedback['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save feedback: {str(e)}")
            return False
    
    async def get_feedback(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve stored feedback."""
        try:
            if not self.feedback_file.exists():
                return []
            
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)
            
            # Return most recent feedback first
            return sorted(feedback_data, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]
            
        except Exception as e:
            logger.error(f"Failed to retrieve feedback: {str(e)}")
            return []
    
    async def get_feedback_stats(self) -> Dict[str, Any]:
        """Get feedback statistics."""
        try:
            feedback_data = await self.get_feedback(limit=1000)  # Get more for stats
            
            stats = {
                'total_feedback': len(feedback_data),
                'like_count': 0,
                'dislike_count': 0,
                'selected_count': 0,
                'average_rating': 0.0,
                'top_restaurants': {}
            }
            
            ratings = []
            restaurant_counts = {}
            
            for feedback in feedback_data:
                feedback_type = feedback.get('feedback_type', '')
                if feedback_type == 'like':
                    stats['like_count'] += 1
                elif feedback_type == 'dislike':
                    stats['dislike_count'] += 1
                elif feedback_type == 'selected':
                    stats['selected_count'] += 1
                
                # Track ratings
                rating = feedback.get('rating')
                if rating is not None:
                    ratings.append(rating)
                
                # Track restaurant popularity
                restaurant = feedback.get('restaurant_name', 'Unknown')
                restaurant_counts[restaurant] = restaurant_counts.get(restaurant, 0) + 1
            
            # Calculate average rating
            if ratings:
                stats['average_rating'] = sum(ratings) / len(ratings)
            
            # Get top restaurants
            stats['top_restaurants'] = dict(
                sorted(restaurant_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            )
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to calculate feedback stats: {str(e)}")
            return {'error': str(e)}
    
    def check_data_availability(self) -> Dict[str, bool]:
        """Check availability of required data files."""
        availability = {}
        
        # Check Phase 1 data
        cleaned_data = self.data_root / "phase1_data_foundation" / "data" / "cleaned_restaurants.csv"
        availability['cleaned_restaurants'] = cleaned_data.exists()
        
        # Check Phase outputs
        phase2_output = Path(settings.PHASE2_OUTPUT)
        phase3_output = Path(settings.PHASE3_OUTPUT)
        phase4_output = Path(settings.PHASE4_OUTPUT)
        phase5_output = Path(settings.PHASE5_OUTPUT)
        
        availability['phase2_output'] = phase2_output.exists()
        availability['phase3_output'] = phase3_output.exists()
        availability['phase4_output'] = phase4_output.exists()
        availability['phase5_output'] = phase5_output.exists()
        
        return availability
