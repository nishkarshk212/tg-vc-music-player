#!/usr/bin/env python3
"""
Test NexGenBots API with the correct endpoint
"""
import requests

API_KEY = "NxGBNexGenBots448436"

print("="*60)
print("Testing NexGenBots API - v1/music/search")
print("="*60)

# Test search endpoint
print("\n🔍 Testing: /v1/music/search")
url = "https://api.nexgenbots.xyz/v1/music/search"
params = {
    "query": "Shape of You Ed Sheeran",
    "apikey": API_KEY,
    "limit": 5
}

try:
    r = requests.get(url, params=params, timeout=15)
    print(f"\n📊 Status Code: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ SUCCESS!")
        print(f"📦 Response keys: {list(data.keys())}")
        
        results = data.get("results", []) or data.get("data", []) or data.get("videos", []) or data.get("items", [])
        print(f"🎶 Results found: {len(results)}")
        
        if results:
            print(f"\n✨ First Result:")
            first = results[0]
            video_id = first.get('id') or first.get('videoId')
            print(f"   • ID: {video_id}")
            print(f"   • Title: {first.get('title')}")
            print(f"   • Duration: {first.get('duration') or first.get('durationText', 'N/A')}")
            print(f"   • Channel: {first.get('channel') or first.get('author')}")
            print(f"   • Views: {first.get('views') or first.get('viewCount', 'N/A')}")
            print(f"   • Link: https://www.youtube.com/watch?v={video_id}")
    else:
        print(f"❌ Failed with status {r.status_code}")
        print(f"Response: {r.text[:500]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("Test completed!")
