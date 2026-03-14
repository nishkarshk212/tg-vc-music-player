#!/usr/bin/env python3
"""
Test NexGen API Video Playback
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from AnnieXMedia.platforms.NexGenBots import get_nexgen_client


async def test_video_api():
    """Test video download with NexGen API"""
    print("=" * 60)
    print("Testing NexGen API Video Download")
    print("=" * 60)
    
    # Test video ID (Rick Astley - Never Gonna Give You Up)
    test_video_id = "dQw4w9WgXcQ"
    
    client = get_nexgen_client()
    
    print(f"\n🎬 Testing video ID: {test_video_id}")
    print("\n📡 Calling NexGen API...")
    
    try:
        result = await client.get_video_download(test_video_id)
        
        if result:
            print(f"\n✅ API Response received!")
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   Link: {result.get('link', 'N/A')[:80]}...")
            print(f"   Format: {result.get('format', 'N/A')}")
            
            if result.get('status') == 'done' and result.get('link'):
                print("\n✅ SUCCESS! Video download URL obtained!")
                return True
            else:
                print("\n⚠️  API returned data but status is not 'done' or link is missing")
                return False
        else:
            print("\n❌ API returned None")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await client.close()


async def main():
    success = await test_video_api()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ NexGen API is working correctly for video playback!")
        print("\nNext steps:")
        print("1. Restart your bot: python3 -m AnnieXMedia")
        print("2. Try playing a video in voice chat")
    else:
        print("❌ NexGen API test failed")
        print("\nTroubleshooting:")
        print("1. Check if API_KEY is correct in .env")
        print("2. Verify API endpoint is accessible")
        print("3. Check server internet connection")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
