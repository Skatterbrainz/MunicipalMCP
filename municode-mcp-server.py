#!/usr/bin/env python3
"""
Municode MCP Server

Model Context Protocol server for accessing municipal code libraries from Municode.
Provides tools to search, retrieve, and navigate municipal ordinances and codes.

Based on the unofficial Municode API documentation at:
https://sr.ht/~partytax/unofficial-municode-api-documentation/
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import quote, urljoin

import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Municode API base URL
MUNICODE_API_BASE = "https://api.municode.com"
MUNICODE_LIBRARY_BASE = "https://library.municode.com"


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
    
    async def get_client_content(self, client_id: int) -> Dict[str, Any]:
        """Get all products a client subscribes to."""
        url = f"{MUNICODE_API_BASE}/ClientContent/{client_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    async def get_product_by_name(self, client_id: int, product_name: str) -> Dict[str, Any]:
        """Get product information by client and product name."""
        url = f"{MUNICODE_API_BASE}/Products/name"
        params = {"clientId": client_id, "productName": product_name}
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_latest_job(self, job_id: int) -> Dict[str, Any]:
        """Get the latest job information."""
        url = f"{MUNICODE_API_BASE}/Jobs/latest/{job_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    async def get_toc_children(self, job_id: int, product_id: int, node_id: str = "10121") -> List[Dict[str, Any]]:
        """Get children of a node in the document tree."""
        url = f"{MUNICODE_API_BASE}/codesToc/children"
        params = {
            "jobId": job_id,
            "productId": product_id,
            "nodeId": node_id
        }
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_codes_content(self, job_id: int, product_id: int, node_id: str) -> Dict[str, Any]:
        """Get content of a specific node in the document tree."""
        url = f"{MUNICODE_API_BASE}/CodesContent"
        params = {
            "jobId": job_id,
            "productId": product_id,
            "nodeId": node_id
        }
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def search_munidocs(
        self,
        client_id: int,
        search_text: str,
        page_num: int = 1,
        page_size: int = 10,
        titles_only: bool = False,
        is_advanced: bool = False
    ) -> Dict[str, Any]:
        """Search MuniDocs for a word or phrase."""
        url = f"{MUNICODE_API_BASE}/search"
        params = {
            "clientId": client_id,
            "searchText": search_text,
            "pageNum": page_num,
            "pageSize": page_size,
            "titlesOnly": titles_only,
            "isAdvanced": is_advanced,
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


# Initialize the MCP server
server = Server("municode")
municode_client = MunicodeClient()


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_states_info",
            description="Get information about a US state by its abbreviation",
            inputSchema={
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": "Two-character US state abbreviation (e.g., 'VA', 'TX', 'CA')"
                    }
                },
                "required": ["state_abbr"]
            }
        ),
        Tool(
            name="list_municipalities",
            description="List all municipalities in a state that use Municode",
            inputSchema={
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": "Two-character US state abbreviation (e.g., 'VA', 'TX', 'CA')"
                    }
                },
                "required": ["state_abbr"]
            }
        ),
        Tool(
            name="get_municipality_info",
            description="Get detailed information about a specific municipality",
            inputSchema={
                "type": "object",
                "properties": {
                    "municipality_name": {
                        "type": "string",
                        "description": "Name of the city, county, or municipality"
                    },
                    "state_abbr": {
                        "type": "string",
                        "description": "Two-character US state abbreviation"
                    }
                },
                "required": ["municipality_name", "state_abbr"]
            }
        ),
        Tool(
            name="get_code_structure",
            description="Get the table of contents structure for a municipality's code",
            inputSchema={
                "type": "object",
                "properties": {
                    "municipality_name": {
                        "type": "string",
                        "description": "Name of the city, county, or municipality"
                    },
                    "state_abbr": {
                        "type": "string",
                        "description": "Two-character US state abbreviation"
                    },
                    "node_id": {
                        "type": "string",
                        "description": "Optional specific node ID to get children for (defaults to root)",
                        "default": "10121"
                    }
                },
                "required": ["municipality_name", "state_abbr"]
            }
        ),
        Tool(
            name="get_code_section",
            description="Get the content of a specific section of municipal code",
            inputSchema={
                "type": "object",
                "properties": {
                    "municipality_name": {
                        "type": "string",
                        "description": "Name of the city, county, or municipality"
                    },
                    "state_abbr": {
                        "type": "string",
                        "description": "Two-character US state abbreviation"
                    },
                    "node_id": {
                        "type": "string",
                        "description": "Node ID of the specific code section to retrieve"
                    }
                },
                "required": ["municipality_name", "state_abbr", "node_id"]
            }
        ),
        Tool(
            name="search_municipal_codes",
            description="Search through municipal codes and ordinances",
            inputSchema={
                "type": "object",
                "properties": {
                    "municipality_name": {
                        "type": "string",
                        "description": "Name of the city, county, or municipality"
                    },
                    "state_abbr": {
                        "type": "string",
                        "description": "Two-character US state abbreviation"
                    },
                    "search_query": {
                        "type": "string",
                        "description": "Text to search for in the municipal codes"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results per page (default: 10)",
                        "default": 10
                    },
                    "page_number": {
                        "type": "integer",
                        "description": "Page number to retrieve (default: 1)",
                        "default": 1
                    },
                    "titles_only": {
                        "type": "boolean",
                        "description": "Search only in titles (default: false)",
                        "default": False
                    }
                },
                "required": ["municipality_name", "state_abbr", "search_query"]
            }
        ),
        Tool(
            name="get_municipality_url",
            description="Get the URL for a municipality's code library page",
            inputSchema={
                "type": "object",
                "properties": {
                    "municipality_name": {
                        "type": "string",
                        "description": "Name of the city, county, or municipality"
                    },
                    "state_abbr": {
                        "type": "string",
                        "description": "Two-character US state abbreviation"
                    }
                },
                "required": ["municipality_name", "state_abbr"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        if name == "get_states_info":
            state_abbr = arguments["state_abbr"].upper()
            result = await municode_client.get_states(state_abbr)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "list_municipalities":
            state_abbr = arguments["state_abbr"].upper()
            clients = await municode_client.get_clients_by_state(state_abbr)
            
            # Format the output for better readability
            formatted_clients = []
            for client in clients:
                formatted_clients.append({
                    "name": client.get("ClientName", "Unknown"),
                    "id": client.get("ClientID"),
                    "population_range": client.get("PopRangeId"),
                    "classification": client.get("ClassificationId"),
                    "website": client.get("Website"),
                    "city": client.get("City"),
                    "zip_code": client.get("ZipCode")
                })
            
            return [TextContent(
                type="text", 
                text=f"Found {len(formatted_clients)} municipalities in {state_abbr}:\n\n" + 
                     json.dumps(formatted_clients, indent=2)
            )]
        
        elif name == "get_municipality_info":
            municipality_name = arguments["municipality_name"]
            state_abbr = arguments["state_abbr"].upper()
            
            client_info = await municode_client.get_client_by_name(municipality_name, state_abbr)
            client_id = client_info.get("ClientID")
            
            if client_id:
                client_content = await municode_client.get_client_content(client_id)
                
                result = {
                    "client_info": client_info,
                    "available_products": client_content
                }
            else:
                result = {"client_info": client_info}
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_code_structure":
            municipality_name = arguments["municipality_name"]
            state_abbr = arguments["state_abbr"].upper()
            node_id = arguments.get("node_id", "10121")
            
            # First get client info
            client_info = await municode_client.get_client_by_name(municipality_name, state_abbr)
            client_id = client_info.get("ClientID")
            
            if not client_id:
                return [TextContent(type="text", text=f"Municipality '{municipality_name}' not found in {state_abbr}")]
            
            # Get available products
            client_content = await municode_client.get_client_content(client_id)
            
            # Find the code of ordinances product
            code_product = None
            for product in client_content:
                if "code" in product.get("ProductName", "").lower():
                    code_product = product
                    break
            
            if not code_product:
                return [TextContent(type="text", text="No code of ordinances found for this municipality")]
            
            job_id = code_product.get("Id")
            product_id = code_product.get("ProductID")
            
            # Get table of contents
            toc = await municode_client.get_toc_children(job_id, product_id, node_id)
            
            return [TextContent(
                type="text",
                text=f"Code structure for {municipality_name}, {state_abbr}:\n\n" +
                     json.dumps(toc, indent=2)
            )]
        
        elif name == "get_code_section":
            municipality_name = arguments["municipality_name"]
            state_abbr = arguments["state_abbr"].upper()
            node_id = arguments["node_id"]
            
            # Get client and product info
            client_info = await municode_client.get_client_by_name(municipality_name, state_abbr)
            client_id = client_info.get("ClientID")
            
            if not client_id:
                return [TextContent(type="text", text=f"Municipality '{municipality_name}' not found in {state_abbr}")]
            
            client_content = await municode_client.get_client_content(client_id)
            code_product = None
            for product in client_content:
                if "code" in product.get("ProductName", "").lower():
                    code_product = product
                    break
            
            if not code_product:
                return [TextContent(type="text", text="No code of ordinances found for this municipality")]
            
            job_id = code_product.get("Id")
            product_id = code_product.get("ProductID")
            
            # Get the content
            content = await municode_client.get_codes_content(job_id, product_id, node_id)
            
            return [TextContent(
                type="text",
                text=f"Content for node {node_id} in {municipality_name}, {state_abbr}:\n\n" +
                     json.dumps(content, indent=2)
            )]
        
        elif name == "search_municipal_codes":
            municipality_name = arguments["municipality_name"]
            state_abbr = arguments["state_abbr"].upper()
            search_query = arguments["search_query"]
            page_size = arguments.get("page_size", 10)
            page_number = arguments.get("page_number", 1)
            titles_only = arguments.get("titles_only", False)
            
            # Get client info
            client_info = await municode_client.get_client_by_name(municipality_name, state_abbr)
            client_id = client_info.get("ClientID")
            
            if not client_id:
                return [TextContent(type="text", text=f"Municipality '{municipality_name}' not found in {state_abbr}")]
            
            # Perform search
            search_results = await municode_client.search_munidocs(
                client_id=client_id,
                search_text=search_query,
                page_num=page_number,
                page_size=page_size,
                titles_only=titles_only
            )
            
            return [TextContent(
                type="text",
                text=f"Search results for '{search_query}' in {municipality_name}, {state_abbr}:\n\n" +
                     json.dumps(search_results, indent=2)
            )]
        
        elif name == "get_municipality_url":
            municipality_name = arguments["municipality_name"]
            state_abbr = arguments["state_abbr"].lower()
            
            # Format the municipality name for URL (spaces to underscores, lowercase)
            formatted_name = municipality_name.lower().replace(" ", "_").replace(",", "")
            
            url = f"{MUNICODE_LIBRARY_BASE}/{state_abbr}/{formatted_name}/codes/code_of_ordinances"
            
            return [TextContent(
                type="text",
                text=f"Municode Library URL for {municipality_name}, {state_abbr.upper()}:\n{url}"
            )]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="municode://help",
            name="Municode MCP Server Help",
            description="Documentation for using the Municode MCP server",
            mimeType="text/plain"
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Handle resource reads."""
    if uri == "municode://help":
        return """
# Municode MCP Server

This server provides access to municipal codes and ordinances through the Municode digital library.

## Available Tools:

1. **get_states_info** - Get information about a US state by abbreviation
2. **list_municipalities** - List all municipalities in a state that use Municode
3. **get_municipality_info** - Get detailed information about a specific municipality
4. **get_code_structure** - Get the table of contents structure for a municipality's code
5. **get_code_section** - Get the content of a specific section of municipal code
6. **search_municipal_codes** - Search through municipal codes and ordinances
7. **get_municipality_url** - Get the URL for a municipality's code library page

## Example Usage:

1. First, list municipalities in your state:
   - Tool: list_municipalities
   - Args: {"state_abbr": "VA"}

2. Get detailed info about a municipality:
   - Tool: get_municipality_info
   - Args: {"municipality_name": "Norfolk", "state_abbr": "VA"}

3. Browse the code structure:
   - Tool: get_code_structure
   - Args: {"municipality_name": "Norfolk", "state_abbr": "VA"}

4. Search for specific topics:
   - Tool: search_municipal_codes
   - Args: {"municipality_name": "Norfolk", "state_abbr": "VA", "search_query": "zoning"}

## Notes:

- State abbreviations should be 2-letter codes (VA, TX, CA, etc.)
- Municipality names should match exactly as they appear in Municode
- Some municipalities may not have all products/features available
- The API uses unofficial endpoints that may change

Based on the unofficial Municode API documentation.
        """
    
    raise ValueError(f"Unknown resource: {uri}")


async def main():
    """Run the server."""
    # Import here to avoid issues if mcp package is not available
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream, 
            InitializationOptions(
                server_name="municode",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None
                )
            )
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped")
    finally:
        asyncio.run(municode_client.close())