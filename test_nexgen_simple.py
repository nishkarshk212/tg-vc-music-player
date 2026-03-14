#!/usr/bin/env python3
"""
Simple test using requests library as per user's example
"""
import requests

API_KEY = "NxGBNexGenBots448436"

print("="*60)
print("Testing NexGenBots API with requests")
print("="*60)

# Test 1: Search endpoint
print("\n🔍 Test 1: /v1/music/search endpoint")
url = "https://api.nexgenbots.xyz/v1/music/search"
params = {
    "query": "Shape of You Ed Sheeran",
    "apikey": API_KEY
}

try:
    r = requests.get(url, params=params, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ SUCCESS! Keys: {list(data.keys())}")
        results = data.get("results", []) or data.get("data", [])
        print(f"Results count: {len(results)}")
        if results and len(results) > 0:
            first = results[0]
            print(f"First result ID: {first.get('id') or first.get('videoId')}")
    else:
        print(f"❌ Failed with status {r.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Song endpoint
print("\n\n🎵 Test 2: /api/song endpoint")
url = "https://api.nexgenbots.xyz/api/song"
params = {
    "query": "faded",
    "apikey": API_KEY
}

try:
    r = requests.get(url, params=params, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ SUCCESS! Keys: {list(data.keys())}")
    else:
        print(f"❌ Failed with status {r.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
