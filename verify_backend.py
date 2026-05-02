#!/usr/bin/env python3
"""Verify backend returns different results for different cuisines"""
import requests
import json

base_url = "http://localhost:8000/api/v1"

def test_recommendations(location, cuisine, budget="medium", min_rating=3.8):
    """Test recommendations endpoint"""
    payload = {
        "location": location,
        "budget": budget,
        "cuisine": cuisine,
        "min_rating": min_rating
    }
    
    try:
        resp = requests.post(f"{base_url}/recommendations", json=payload, timeout=60)
        data = resp.json()
        
        restaurants = [card["title"] for card in data.get("cards", [])[:3]]
        cuisines = [card["cuisine"] for card in data.get("cards", [])[:3]]
        
        return {
            "restaurants": restaurants,
            "cuisines": cuisines,
            "summary": data.get("summary", "N/A")
        }
    except Exception as e:
        return {"error": str(e)}

# Test 1: Chinese in Koramangala
print("=== TEST 1: Chinese in Koramangala ===")
result1 = test_recommendations("Koramangala", "Chinese")
print(f"Restaurants: {result1.get('restaurants', [])}")
print(f"Cuisines: {result1.get('cuisines', [])}")

# Test 2: Italian in Indiranagar
print("\n=== TEST 2: Italian in Indiranagar ===")
result2 = test_recommendations("Indiranagar", "Italian")
print(f"Restaurants: {result2.get('restaurants', [])}")
print(f"Cuisines: {result2.get('cuisines', [])}")

# Test 3: Compare
print("\n=== COMPARISON ===")
if result1.get("restaurants") == result2.get("restaurants"):
    print("❌ FAIL: Same restaurants for different cuisines!")
    print("   The backend is NOT running the dynamic pipeline.")
else:
    print("✅ PASS: Different restaurants for different cuisines!")
    print(f"   Chinese: {result1.get('restaurants', [])[:2]}")
    print(f"   Italian: {result2.get('restaurants', [])[:2]}")
