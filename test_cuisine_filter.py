#!/usr/bin/env python3
"""Test cuisine filtering"""
import sys
sys.path.insert(0, '.')

from phase2_user_preferences.validation import validate_preferences
from phase2_user_preferences.normalizer import normalize_preferences
from phase3_candidate_retrieval.pipeline import run_phase3

# Test Italian preferences
payload = {
    'location': 'Indiranagar',
    'budget': 'medium', 
    'cuisine': 'Italian',
    'min_rating': 3.8,
    'optional_tags': []
}

print('Testing Italian cuisine filter...')
profile, errors = validate_preferences(payload)
if errors:
    print(f"Validation errors: {errors}")
else:
    print(f"Cuisine requested: {profile.cuisine}")
    
    phase3 = run_phase3(profile)
    print(f"\nPhase 3 filtered: {phase3['filtered_candidates']} candidates")
    print(f"Phase 3 selected: {phase3['selected_candidates']} candidates")
    
    print("\nTop 5 results:")
    for i, c in enumerate(phase3['candidates'][:5]):
        print(f"{i+1}. {c['name']} - {c['cuisine']}")
