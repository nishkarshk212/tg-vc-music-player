#!/usr/bin/env python3
"""
Test NexGenBots API with pvtz.nexgenbots.xyz domain
"""
import requests

API_KEY = "NxGBNexGenBots448436"

print("="*60)
print("Testing NexGenBots API - pvtz.nexgenbots.xyz")
print("="*60)

# Test base URL first
print("\n🔍 Testing base URL...")
try:
    r = requests.get("https://pvtz.nexgenbots.xyz/", timeout=10)
    print(f"Base URL Status: {r.status_code}")
    print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"Base URL Error: {e}")

# Test search endpoint
print("\n\n🔍 Testing: /v1/music/search")
url = "https://pvtz.nexgenbots.xyz/v1/music/search"
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
            print(f"\n🎉 NEXGENBOTS API IS WORKING!")
        else:
            print("⚠️ No results returned")
    else:
        print(f"❌ Failed with status {r.status_code}")
        print(f"Response: {r.text[:500]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("Test completed!")
