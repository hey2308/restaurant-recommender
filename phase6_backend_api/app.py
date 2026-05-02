"""Flask API for Phase 6 Backend API and Orchestration Layer."""

import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS

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

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In-memory storage for feedback
feedback_storage = []

# Helper functions
def load_phase4_data() -> Dict[str, Any]:
    """Load Phase 4 recommendations data."""
    try:
        phase4_path = f"{Config.DATA_ROOT}/phase4_llm_recommendation/data/recommendations.json"
        if os.path.exists(phase4_path):
            with open(phase4_path, "r") as f:
                return json.load(f)
        else:
            logger.warning(f"Phase 4 data not found at {phase4_path}")
            return {}
    except Exception as e:
        logger.error(f"Failed to load Phase 4 data: {str(e)}")
        return {}

def load_phase5_data() -> Dict[str, Any]:
    """Load Phase 5 presentation data."""
    try:
        phase5_path = f"{Config.DATA_ROOT}/phase5_presentation_delivery/data/presentation.json"
        if os.path.exists(phase5_path):
            with open(phase5_path, "r") as f:
                return json.load(f)
        else:
            logger.warning(f"Phase 5 data not found at {phase5_path}")
            return {}
    except Exception as e:
        logger.error(f"Failed to load Phase 5 data: {str(e)}")
        return {}


def _debug_log(msg: str):
    """Write debug message to file."""
    with open("c:/Projects/Milestone1/debug_api.log", "a") as f:
        f.write(f"{msg}\n")

def run_pipeline_with_preferences(preferences: Dict[str, Any]) -> Dict[str, Any]:
    """Run the complete pipeline dynamically with user preferences."""
    import sys
    import time
    sys.path.insert(0, Config.DATA_ROOT)
    
    _debug_log(f"\n{'='*50}")
    _debug_log(f"DEBUG: Starting pipeline at {time.strftime('%H:%M:%S')}")
    _debug_log(f"DEBUG: Preferences: {preferences}")
    
    try:
        # Phase 2: Validate preferences
        _debug_log("DEBUG: Phase 2 - Validating preferences...")
        from phase2_user_preferences.validation import validate_preferences
        from phase2_user_preferences.models import PreferenceProfile
        
        profile, errors = validate_preferences(preferences)
        if errors:
            _debug_log(f"DEBUG ERROR: Phase 2 validation failed: {errors}")
            return {}
        
        _debug_log(f"DEBUG: Phase 2 complete - cuisine={profile.cuisine}, location={profile.location}")
        
        # Phase 3: Retrieve candidates
        _debug_log("DEBUG: Phase 3 - Retrieving candidates...")
        from phase3_candidate_retrieval.pipeline import run_phase3
        phase3_result = run_phase3(profile)
        _debug_log(f"DEBUG: Phase 3 complete - {phase3_result['selected_candidates']} candidates")
        
        # Phase 4: Generate recommendations with LLM
        _debug_log("DEBUG: Phase 4 - Generating LLM recommendations...")
        from phase4_llm_recommendation.pipeline import run_phase4
        # Phase 4 expects phase3_payload as keyword argument
        phase4_result = run_phase4(phase3_payload=phase3_result)
        _debug_log(f"DEBUG: Phase 4 complete - {len(phase4_result.get('recommendations', []))} recs")
        
        # Phase 5: Format presentation
        _debug_log("DEBUG: Phase 5 - Formatting presentation...")
        from phase5_presentation_delivery.pipeline import run_phase5
        phase5_result = run_phase5(phase4_result)
        _debug_log(f"DEBUG: Phase 5 complete - {len(phase5_result.get('cards', []))} cards")
        
        return phase5_result
        
    except Exception as e:
        _debug_log(f"DEBUG ERROR: Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        # Fallback to static data if pipeline fails
        _debug_log("DEBUG: Falling back to static data")
        return load_phase5_data()

def create_error_response(error_message: str, error_code: str, status_code: int = 500) -> tuple:
    """Create standardized error response."""
    response = {
        "error": error_message,
        "error_code": error_code,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": getattr(request, 'request_id', None)
    }
    return jsonify(response), status_code

# Middleware for request tracking
@app.before_request
def before_request():
    """Set request ID and log request start."""
    request.request_id = str(uuid.uuid4())
    logger.info(f"Request started: {request.method} {request.url} - ID: {request.request_id}")

@app.after_request
def after_request(response):
    """Log request completion."""
    logger.info(f"Request completed: {response.status_code} - ID: {request.request_id}")
    response.headers["X-Request-ID"] = request.request_id
    return response

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return create_error_response("Endpoint not found", "NOT_FOUND", 404)

@app.errorhandler(500)
def internal_error(error):
    return create_error_response("Internal server error", "INTERNAL_ERROR", 500)

# API Routes

@app.route(f"{Config.API_V1_PREFIX}/health", methods=["GET"])
def health_check():
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
        phase1_data = f"{Config.DATA_ROOT}/phase1_data_foundation/data/cleaned_restaurants.csv"
        components["phase1_data"] = "healthy" if os.path.exists(phase1_data) else "missing"
        
        # Check if phase outputs exist
        phase2_output = f"{Config.DATA_ROOT}/phase2_user_preferences/data/validated_profile.json"
        phase3_output = f"{Config.DATA_ROOT}/phase3_candidate_retrieval/data/candidates.json"
        phase4_output = f"{Config.DATA_ROOT}/phase4_llm_recommendation/data/recommendations.json"
        phase5_output = f"{Config.DATA_ROOT}/phase5_presentation_delivery/data/presentation.json"
        
        components["phase2_output"] = "healthy" if os.path.exists(phase2_output) else "missing"
        components["phase3_output"] = "healthy" if os.path.exists(phase3_output) else "missing"
        components["phase4_output"] = "healthy" if os.path.exists(phase4_output) else "missing"
        components["phase5_output"] = "healthy" if os.path.exists(phase5_output) else "missing"
        
        response = {
            "status": "healthy",
            "version": Config.VERSION,
            "timestamp": datetime.utcnow().isoformat(),
            "components": components
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return create_error_response("Service unavailable", "SERVICE_UNAVAILABLE", 503)

@app.route(f"{Config.API_V1_PREFIX}/recommendations", methods=["POST"])
def get_recommendations():
    """Get restaurant recommendations based on user preferences."""
    try:
        if not request.is_json:
            return create_error_response("Request must be JSON", "INVALID_CONTENT_TYPE", 400)
        
        preferences = request.get_json()
        logger.info(f"Recommendation request: {preferences}")
        
        # Validate required fields
        required_fields = ["location", "budget", "cuisine", "min_rating"]
        for field in required_fields:
            if field not in preferences:
                return create_error_response(f"Missing required field: {field}", "VALIDATION_ERROR", 400)
        
        # Run the pipeline dynamically with user preferences
        presentation_data = run_pipeline_with_preferences(preferences)
        
        if not presentation_data:
            return create_error_response("Failed to generate recommendations", "PIPELINE_ERROR", 500)
        
        logger.info(f"Returning {len(presentation_data.get('cards', []))} recommendations")
        return jsonify(presentation_data)
        
    except Exception as e:
        logger.error(f"Recommendation failed: {str(e)}", exc_info=True)
        return create_error_response("Failed to generate recommendations", "RECOMMENDATION_ERROR", 500)

@app.route(f"{Config.API_V1_PREFIX}/feedback", methods=["POST"])
def submit_feedback():
    """Submit user feedback for recommendations."""
    try:
        if not request.is_json:
            return create_error_response("Request must be JSON", "INVALID_CONTENT_TYPE", 400)
        
        feedback = request.get_json()
        logger.info(f"Feedback submission: {feedback}")
        
        # Validate required fields
        required_fields = ["restaurant_name", "feedback_type", "user_profile"]
        for field in required_fields:
            if field not in feedback:
                return create_error_response(f"Missing required field: {field}", "VALIDATION_ERROR", 400)
        
        # Store feedback
        feedback_entry = {
            **feedback,
            "timestamp": datetime.utcnow().isoformat(),
            "id": len(feedback_storage) + 1
        }
        feedback_storage.append(feedback_entry)
        
        logger.info(f"Feedback saved: ID {feedback_entry['id']}")
        return jsonify({"status": "success", "message": "Feedback saved successfully"})
        
    except Exception as e:
        logger.error(f"Feedback failed: {str(e)}", exc_info=True)
        return create_error_response("Failed to process feedback", "FEEDBACK_ERROR", 500)

@app.route(f"{Config.API_V1_PREFIX}/feedback/stats", methods=["GET"])
def get_feedback_stats():
    """Get feedback statistics."""
    try:
        total = len(feedback_storage)
        likes = sum(1 for f in feedback_storage if f.get("feedback_type") == "like")
        dislikes = sum(1 for f in feedback_storage if f.get("feedback_type") == "dislike")
        selected = sum(1 for f in feedback_storage if f.get("feedback_type") == "selected")
        
        response = {
            "total_feedback": total,
            "like_count": likes,
            "dislike_count": dislikes,
            "selected_count": selected,
            "recent_feedback": feedback_storage[-10:]  # Last 10 feedbacks
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Failed to get feedback stats: {str(e)}")
        return create_error_response("Failed to retrieve feedback statistics", "STATS_ERROR", 500)

@app.route(f"{Config.API_V1_PREFIX}/data/status", methods=["GET"])
def get_data_status():
    """Get data availability status."""
    try:
        availability = {
            "cleaned_restaurants": os.path.exists(f"{Config.DATA_ROOT}/phase1_data_foundation/data/cleaned_restaurants.csv"),
            "phase2_output": os.path.exists(f"{Config.DATA_ROOT}/phase2_user_preferences/data/validated_profile.json"),
            "phase3_output": os.path.exists(f"{Config.DATA_ROOT}/phase3_candidate_retrieval/data/candidates.json"),
            "phase4_output": os.path.exists(f"{Config.DATA_ROOT}/phase4_llm_recommendation/data/recommendations.json"),
            "phase5_output": os.path.exists(f"{Config.DATA_ROOT}/phase5_presentation_delivery/data/presentation.json")
        }
        return jsonify({"data_availability": availability})
        
    except Exception as e:
        logger.error(f"Failed to check data status: {str(e)}")
        return create_error_response("Failed to check data status", "DATA_STATUS_ERROR", 500)

# Root endpoint
@app.route("/")
def index():
    """API information endpoint."""
    response = {
        "name": Config.TITLE,
        "version": Config.VERSION,
        "description": Config.DESCRIPTION,
        "endpoints": {
            "health": f"{Config.API_V1_PREFIX}/health",
            "recommendations": f"{Config.API_V1_PREFIX}/recommendations",
            "feedback": f"{Config.API_V1_PREFIX}/feedback",
            "feedback_stats": f"{Config.API_V1_PREFIX}/feedback/stats",
            "data_status": f"{Config.API_V1_PREFIX}/data/status"
        }
    }
    return jsonify(response)

if __name__ == "__main__":
    logger.info(f"Starting {Config.TITLE} v{Config.VERSION}")
    logger.info(f"Server will be available at http://{Config.HOST}:{Config.PORT}")
    logger.info(f"API documentation: http://{Config.HOST}:{Config.PORT}{Config.API_V1_PREFIX}/health")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
