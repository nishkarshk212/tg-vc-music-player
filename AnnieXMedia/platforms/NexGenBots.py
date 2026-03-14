# Authored By Certified Coders © 2025
"""
NexGenBots API Integration for YouTube Search
API Documentation: https://console.nexgenbots.xyz/dashboard
"""
import aiohttp
from typing import List, Dict, Optional
from AnnieXMedia import LOGGER
from config import API_KEY


class NexGenBotsSearch:
    """NexGenBots API Client for searching songs"""
    
    def __init__(self):
        self.base_url = "https://api.nexgenbots.xyz/api/search"
        self.api_key = API_KEY or "30DxNexGenBotsf57c86"
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "AnnieXMusic/1.0"
                }
            )
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for songs using NexGenBots API
        
        Args:
            query: Search query (song name, artist, etc.)
            limit: Maximum number of results
            
        Returns:
            List of search results with video information
        """
        if not self.api_key:
            LOGGER("NexGenBots").warning("API_KEY not configured, falling back to default")
        
        try:
            session = await self._get_session()
            
            # Use specific endpoint: https://api.nexgenbots.xyz/api/search
            params = {
                "query": query,
                "limit": limit,
                "key": self.api_key
            }
            
            async with session.get(self.base_url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results", []) or data.get("data", []) or data.get("videos", [])
                    
                    if results:
                        LOGGER("NexGenBots").info(f"Found {len(results)} results for '{query}'")
                        return self._format_results(results)
                    else:
                        LOGGER("NexGenBots").debug(f"No results found for '{query}'")
                        return []
                        
                elif response.status == 401:
                    LOGGER("NexGenBots").error("Invalid API key!")
                    return []
                    
                elif response.status == 429:
                    LOGGER("NexGenBots").warning("Rate limit exceeded!")
                    return []
                    
                else:
                    LOGGER("NexGenBots").error(f"API error: {response.status}")
                    return []
                    
        except asyncio.TimeoutError:
            LOGGER("NexGenBots").error("Request timeout!")
            return []
        except Exception as e:
            LOGGER("NexGenBots").error(f"Search failed: {e}")
            return []
    
    def _format_results(self, results: List[Dict]) -> List[Dict]:
        """Format API results to match expected format"""
        formatted = []
        
        for item in results:
            try:
                formatted_item = {
                    "id": item.get("id") or item.get("videoId"),
                    "title": item.get("title"),
                    "duration": item.get("duration") or item.get("durationText", "0:00"),
                    "thumbnail": item.get("thumbnail") or item.get("thumbnails", [{}])[0].get("url"),
                    "channel": item.get("channel") or item.get("author") or item.get("channelTitle"),
                    "views": item.get("views") or item.get("viewCount", "0"),
                    "published": item.get("published") or item.get("publishedTime", ""),
                    "link": f"https://www.youtube.com/watch?v={item.get('id') or item.get('videoId')}"
                }
                
                # Validate required fields
                if formatted_item["id"] and formatted_item["title"]:
                    formatted.append(formatted_item)
                    
            except Exception as e:
                LOGGER("NexGenBots").debug(f"Failed to format result: {e}")
                continue
        
        return formatted


# Global instance
_nexgen_instance: Optional[NexGenBotsSearch] = None


def get_nexgen_client() -> NexGenBotsSearch:
    """Get singleton instance of NexGenBots client"""
    global _nexgen_instance
    if _nexgen_instance is None:
        _nexgen_instance = NexGenBotsSearch()
    return _nexgen_instance


async def nexgen_search(query: str, limit: int = 10) -> List[Dict]:
    """
    Convenience function for searching via NexGenBots API
    
    Args:
        query: Search query
        limit: Max results
        
    Returns:
        List of formatted results
    """
    client = get_nexgen_client()
    return await client.search(query, limit)
