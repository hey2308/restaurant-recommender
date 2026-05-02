#!/usr/bin/env python3
"""Test API with different cuisines"""
import requests
import json

# Test 1: Italian
print("=== TEST 1: Italian in Indiranagar ===")
resp1 = requests.post("http://localhost:8000/api/v1/recommendations", 
    json={"location": "Indiranagar", "budget": "medium", "cuisine": "Italian", "min_rating": 3.8})
data1 = resp1.json()
print(f"Summary: {data1.get('summary', 'N/A')}")
for card in data1.get('cards', [])[:3]:
    print(f"  {card['subtitle']}: {card['title']} - {card['cuisine']}")

# Test 2: Chinese  
print("\n=== TEST 2: Chinese in Koramangala ===")
resp2 = requests.post("http://localhost:8000/api/v1/recommendations",
    json={"location": "Koramangala", "budget": "medium", "cuisine": "Chinese", "min_rating": 3.8})
data2 = resp2.json()
print(f"Summary: {data2.get('summary', 'N/A')}")
for card in data2.get('cards', [])[:3]:
    print(f"  {card['subtitle']}: {card['title']} - {card['cuisine']}")

# Compare
print("\n=== RESULT ===")
italian_names = [c['title'] for c in data1.get('cards', [])]
chinese_names = [c['title'] for c in data2.get('cards', [])]

if italian_names == chinese_names:
    print("❌ BUG: Same restaurants for different cuisines!")
else:
    print("✅ SUCCESS: Different restaurants for different cuisines!")
    print(f"Italian: {', '.join(italian_names[:3])}")
    print(f"Chinese: {', '.join(chinese_names[:3])}")
