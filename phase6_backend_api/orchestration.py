"""Orchestration service for recommendation pipeline phases."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

from config import settings


logger = logging.getLogger(__name__)


class OrchestrationService:
    """Orchestrates the recommendation pipeline phases."""
    
    def __init__(self):
        self.data_root = Path(settings.DATA_ROOT)
    
    async def run_recommendation_pipeline(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Run the complete recommendation pipeline: Phase 2 -> 3 -> 4 -> 5."""
        logger.info(f"Starting recommendation pipeline for: {preferences}")
        
        try:
            # Phase 2: Validate and normalize preferences
            validated_profile = await self._run_phase2(preferences)
            logger.info("Phase 2 completed: User preferences validated")
            
            # Phase 3: Retrieve and filter candidates
            candidates = await self._run_phase3(validated_profile)
            logger.info(f"Phase 3 completed: Retrieved {len(candidates.get('candidates', []))} candidates")
            
            # Phase 4: Generate LLM recommendations
            recommendations = await self._run_phase4(validated_profile, candidates)
            logger.info(f"Phase 4 completed: Generated {len(recommendations.get('recommendations', []))} recommendations")
            
            # Phase 5: Format for presentation
            presentation = await self._run_phase5(recommendations)
            logger.info("Phase 5 completed: Presentation formatted")
            
            return presentation
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise
    
    async def _run_phase2(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Run Phase 2: User Preference Capture Layer."""
        try:
            # Import and run Phase 2 pipeline
            import sys
            sys.path.append(str(self.data_root / "phase2_user_preferences"))
            
            from phase2_user_preferences.pipeline import run_phase2
            
            result = run_phase2(preferences)
            
            # Save result for debugging
            output_path = Path(settings.PHASE2_OUTPUT)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            
            return result
            
        except Exception as e:
            logger.error(f"Phase 2 failed: {str(e)}")
            raise RuntimeError(f"Phase 2 execution failed: {str(e)}")
    
    async def _run_phase3(self, validated_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Run Phase 3: Candidate Retrieval and Filtering Layer."""
        try:
            # Import and run Phase 3 pipeline
            import sys
            sys.path.append(str(self.data_root / "phase3_candidate_retrieval"))
            
            from phase3_candidate_retrieval.pipeline import run_phase3
            
            result = run_phase3(validated_profile)
            
            # Save result for debugging
            output_path = Path(settings.PHASE3_OUTPUT)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            
            return result
            
        except Exception as e:
            logger.error(f"Phase 3 failed: {str(e)}")
            raise RuntimeError(f"Phase 3 execution failed: {str(e)}")
    
    async def _run_phase4(self, profile: Dict[str, Any], candidates: Dict[str, Any]) -> Dict[str, Any]:
        """Run Phase 4: LLM Recommendation Intelligence Layer."""
        try:
            # Import and run Phase 4 pipeline
            import sys
            sys.path.append(str(self.data_root / "phase4_llm_recommendation"))
            
            from phase4_llm_recommendation.pipeline import run_phase4
            
            result = run_phase4(profile, candidates)
            
            # Save result for debugging
            output_path = Path(settings.PHASE4_OUTPUT)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            
            return result
            
        except Exception as e:
            logger.error(f"Phase 4 failed: {str(e)}")
            raise RuntimeError(f"Phase 4 execution failed: {str(e)}")
    
    async def _run_phase5(self, recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Run Phase 5: Presentation and Delivery Layer."""
        try:
            # Import and run Phase 5 pipeline
            import sys
            sys.path.append(str(self.data_root / "phase5_presentation_delivery"))
            
            from phase5_presentation_delivery.pipeline import run_phase5
            
            result = run_phase5(recommendations)
            
            # Save result for debugging
            output_path = Path(settings.PHASE5_OUTPUT)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            
            return result
            
        except Exception as e:
            logger.error(f"Phase 5 failed: {str(e)}")
            raise RuntimeError(f"Phase 5 execution failed: {str(e)}")
    
    async def health_check(self) -> Dict[str, str]:
        """Check health of all pipeline components."""
        components = {}
        
        # Check data files exist
        phase1_data = self.data_root / "phase1_data_foundation" / "data" / "cleaned_restaurants.csv"
        components["phase1_data"] = "healthy" if phase1_data.exists() else "missing"
        
        # Check phase modules are importable
        try:
            import phase2_user_preferences
            components["phase2_module"] = "healthy"
        except ImportError:
            components["phase2_module"] = "unavailable"
            
        try:
            import phase3_candidate_retrieval
            components["phase3_module"] = "healthy"
        except ImportError:
            components["phase3_module"] = "unavailable"
            
        try:
            import phase4_llm_recommendation
            components["phase4_module"] = "healthy"
        except ImportError:
            components["phase4_module"] = "unavailable"
            
        try:
            import phase5_presentation_delivery
            components["phase5_module"] = "healthy"
        except ImportError:
            components["phase5_module"] = "unavailable"
        
        return components
