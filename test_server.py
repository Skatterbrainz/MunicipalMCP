#!/usr/bin/env python3
"""
Test script for the MunicipalMCP server
Tests basic functionality without requiring full MCP client setup.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List
import httpx

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Municode API base URL
MUNICODE_API_BASE = "https://api.municode.com"

class MunicodeClient:
    """HTTP client for interacting with Municode API."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "MCP-Municode-Server/1.0",
                "Accept": "application/json",
            }
        )
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def get_states(self, state_abbr: str) -> Dict[str, Any]:
        """Get state information by abbreviation."""
        url = f"{MUNICODE_API_BASE}/States/abbr"
        params = {"stateAbbr": state_abbr}
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_clients_by_state(self, state_abbr: str) -> List[Dict[str, Any]]:
        """Get all Municode clients in a state."""
        url = f"{MUNICODE_API_BASE}/Clients/stateAbbr"
        params = {"stateAbbr": state_abbr}
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_client_by_name(self, client_name: str, state_abbr: str) -> Dict[str, Any]:
        """Get client information by name and state."""
        url = f"{MUNICODE_API_BASE}/Clients/name"
        params = {"clientName": client_name, "stateAbbr": state_abbr}
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def search_munidocs(
        self,
        client_id: int,
        search_text: str,
        page_num: int = 1,
        page_size: int = 10,
        titles_only: bool = False
    ) -> Dict[str, Any]:
        """Search MuniDocs for a word or phrase."""
        url = f"{MUNICODE_API_BASE}/search"
        params = {
            "clientId": client_id,
            "searchText": search_text,
            "pageNum": page_num,
            "pageSize": page_size,
            "titlesOnly": titles_only,
            "isAdvanced": False,
            "isAutocomplete": False,
            "mode": "standard",
            "sort": 0,
            "fragmentSize": 200,
            "contentTypeId": "",
            "stateId": 0
        }
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()


async def test_municode_client():
    """Test the Municode API client directly."""
    client = MunicodeClient()
    
    try:
        print("🏛️  Testing Municode API Client\n")
        
        # Test 1: Get Virginia state info
        print("1. Getting Virginia state information...")
        try:
            va_info = await client.get_states("VA")
            print(f"   ✅ Found: {va_info.get('StateName', 'Unknown')} (ID: {va_info.get('StateId', 'Unknown')})")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Test 2: Get Norfolk information
        print("\n2. Getting Norfolk, VA information...")
        try:
            norfolk_info = await client.get_client_by_name("Norfolk", "VA")
            client_id = norfolk_info.get("ClientID")
            
            if client_id:
                print(f"   ✅ Found Norfolk (ID: {client_id})")
                print(f"      Website: {norfolk_info.get('Website', 'Not available')}")
            else:
                print("   ❌ Norfolk not found or no ClientID returned")
                return
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Test 3: Search for crawl space ventilation
        print("\n3. Searching Norfolk codes for 'crawl space ventilation'...")
        try:
            search_results = await client.search_munidocs(
                client_id=client_id,
                search_text="crawl space ventilation",
                page_size=5
            )
            
            num_hits = search_results.get("NumberOfHits", 0)
            print(f"   ✅ Found {num_hits} results for 'crawl space ventilation'")
            
            hits = search_results.get("Hits", [])
            if hits:
                print("   Top results:")
                for i, hit in enumerate(hits[:3]):  # Show first 3 results
                    title = hit.get("Title", "Unknown")
                    snippet = hit.get("ContentSnippet", "")
                    print(f"      {i+1}. {title}")
                    if snippet:
                        # Clean up snippet
                        clean_snippet = snippet.replace("<em>", "").replace("</em>", "").strip()[:150]
                        print(f"         {clean_snippet}...")
                        
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 4: Search for building codes
        print("\n4. Searching Norfolk codes for 'foundation vent'...")
        try:
            search_results = await client.search_munidocs(
                client_id=client_id,
                search_text="foundation vent",
                page_size=3
            )
            
            num_hits = search_results.get("NumberOfHits", 0)
            print(f"   ✅ Found {num_hits} results for 'foundation vent'")
            
            hits = search_results.get("Hits", [])
            if hits:
                print("   Top results:")
                for i, hit in enumerate(hits):
                    title = hit.get("Title", "Unknown")
                    snippet = hit.get("ContentSnippet", "")
                    print(f"      {i+1}. {title}")
                    if snippet:
                        clean_snippet = snippet.replace("<em>", "").replace("</em>", "").strip()[:150]
                        print(f"         {clean_snippet}...")
                        
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("\n🎉 Test completed!")
        
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(test_municode_client())