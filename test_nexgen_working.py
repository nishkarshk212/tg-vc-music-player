#!/usr/bin/env python3
"""
Test NexGenBots API - Download Only (pvtz.nexgenbots.xyz)
Based on actual OpenAPI spec from /docs
"""
import requests

API_KEY = "NxGBNexGenBots448436"

print("="*60)
print("Testing NexGenBots API - pvtz.nexgenbots.xyz")
print("API Type: Download Only (NO Search)")
print("="*60)

# Test base URL
print("\n🔍 Testing base URL...")
try:
    r = requests.get("https://pvtz.nexgenbots.xyz/", timeout=10)
    print(f"✅ Base URL Status: {r.status_code}")
    print(f"   Response: {r.text[:100]}")
except Exception as e:
    print(f"❌ Base URL Error: {e}")

# Test song endpoint with a known video ID
print("\n\n🎵 Testing: /song/{vidid}")
video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
url = f"https://pvtz.nexgenbots.xyz/song/{video_id}"
params = {"api": API_KEY}

try:
    r = requests.get(url, params=params, timeout=15)
    print(f"\n📊 Status Code: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ SUCCESS!")
        print(f"📦 Response keys: {list(data.keys())}")
        print(f"📄 Response preview: {str(data)[:300]}...")
        print(f"\n🎉 NEXGENBOTS SONG API IS WORKING!")
    else:
        print(f"❌ Failed with status {r.status_code}")
        try:
            error_data = r.json()
            print(f"Error response: {error_data}")
        except:
            print(f"Response: {r.text[:500]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("IMPORTANT: This API only provides downloads, NOT search!")
print("Use youtubesearchpython for search functionality.")
print("="*60)
