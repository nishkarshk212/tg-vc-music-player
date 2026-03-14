#!/usr/bin/env python3
"""
Test script to verify NexGenBots API functionality
"""
import asyncio
import aiohttp
from config import API_KEY

async def test_nexgen_api():
    """Test the NexGenBots API directly"""
    
    api_key = API_KEY or "NxGBNexGenBots448436"
    search_url = "https://api.nexgenbots.xyz/search"
    song_url = "https://api.nexgenbots.xyz/api/song"
    
    print("🔍 Testing NexGenBots API...")
    print(f"📌 Search Endpoint: {search_url}")
    print(f"📌 Song Endpoint: {song_url}")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-5:]}")
    print()
    
    async with aiohttp.ClientSession(
        headers={
            "User-Agent": "AnnieXMusic/1.0"
        }
    ) as session:
        # Test search query
        test_query = "Shape of You Ed Sheeran"
        params = {
            "query": test_query,
            "limit": 5,
            "apikey": api_key
        }
        
        try:
            print(f"🎵 Test 1: Searching for '{test_query}'...")
            async with session.get(search_url, params=params, timeout=15) as response:
                print(f"\n📊 Response Status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Search API: SUCCESS")
                    print(f"📦 Response keys: {list(data.keys())}")
                    
                    results = data.get("results", []) or data.get("data", []) or data.get("videos", [])
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
                        
                        # Test song endpoint with this video ID
                        if video_id:
                            print(f"\n🎵 Test 2: Getting song download for ID '{video_id}'...")
                            song_params = {
                                "query": video_id,
                                "apikey": api_key
                            }
                            async with session.get(song_url, params=song_params, timeout=20) as song_response:
                                print(f"📊 Song API Status: {song_response.status}")
                                if song_response.status == 200:
                                    song_data = await song_response.json()
                                    print(f"✅ Song API: SUCCESS")
                                    print(f"📦 Song Data Keys: {list(song_data.keys())}")
                                    print(f"📄 Sample Data: {str(song_data)[:300]}...")
                                else:
                                    print(f"❌ Song API Error: {song_response.status}")
                                    error_text = await song_response.text()
                                    print(f"   Response: {error_text[:200]}")
                    else:
                        print("⚠️ No results returned")
                        
                elif response.status == 401:
                    print("❌ API Error: Invalid API Key (401)")
                elif response.status == 429:
                    print("⚠️ API Error: Rate Limit Exceeded (429)")
                else:
                    print(f"❌ API Error: HTTP {response.status}")
                    error_text = await response.text()
                    print(f"   Response: {error_text[:200]}")
                    
        except asyncio.TimeoutError:
            print("❌ Request Timeout - API took too long to respond")
        except Exception as e:
            print(f"❌ Test Failed: {e}")
            
    print("\n" + "="*60)
    print("Test completed!")


if __name__ == "__main__":
    asyncio.run(test_nexgen_api())
