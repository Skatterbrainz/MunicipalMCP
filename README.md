# MunicipalMCP

A Model Context Protocol (MCP) server for accessing municipal codes and ordinances from the Municode digital library. This server provides programmatic access to municipal legal documents including city ordinances, zoning codes, and other local regulations for thousands of municipalities across the United States.

## 🏛️ Overview

Municode hosts municipal codes for thousands of cities and counties across the United States. This MCP server leverages the unofficial Municode API to provide structured access to this valuable public information through a standardized MCP interface.

### Features

- 🏛️ **Municipal Discovery**: Find municipalities by state
- 📜 **Code Navigation**: Browse municipal code structures 
- 🔍 **Search Capabilities**: Search through ordinances and codes
- 📋 **Content Retrieval**: Get specific code sections and content
- 🌐 **URL Generation**: Generate direct links to municipal codes
- 🔗 **MCP Integration**: Works with any MCP-compatible client

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/MunicipalMCP.git
   cd MunicipalMCP
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the server:**
   ```bash
   python3 test_server.py
   ```

### Adding to MCP Clients

#### Warp Terminal
Create or update your MCP configuration file at `~/.config/mcp/mcp.json`:

```json
{
  "mcpServers": {
    "municode": {
      "command": "python3",
      "args": ["/path/to/MunicipalMCP/municode-mcp-server.py"],
      "description": "Access municipal codes and ordinances from Municode digital library"
    }
  }
}
```

#### Claude Desktop App
Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "municode": {
      "command": "python3",
      "args": ["/path/to/MunicipalMCP/municode-mcp-server.py"]
    }
  }
}
```

## 🛠️ Available Tools

### 1. `get_states_info`
Get information about a US state by its abbreviation.
- **Parameters**: `state_abbr` (string) - Two-character state abbreviation

### 2. `list_municipalities` 
List all municipalities in a state that use Municode.
- **Parameters**: `state_abbr` (string) - Two-character state abbreviation

### 3. `get_municipality_info`
Get detailed information about a specific municipality.
- **Parameters**: 
  - `municipality_name` (string) - Name of the municipality
  - `state_abbr` (string) - Two-character state abbreviation

### 4. `get_code_structure`
Get the table of contents structure for a municipality's code.
- **Parameters**: 
  - `municipality_name` (string) - Name of the municipality
  - `state_abbr` (string) - Two-character state abbreviation
  - `node_id` (string, optional) - Specific node ID (defaults to root)

### 5. `get_code_section`
Get the content of a specific section of municipal code.
- **Parameters**: 
  - `municipality_name` (string) - Name of the municipality
  - `state_abbr` (string) - Two-character state abbreviation
  - `node_id` (string) - Node ID of the specific code section

### 6. `search_municipal_codes`
Search through municipal codes and ordinances.
- **Parameters**: 
  - `municipality_name` (string) - Name of the municipality
  - `state_abbr` (string) - Two-character state abbreviation
  - `search_query` (string) - Text to search for
  - `page_size` (integer, optional) - Results per page (default: 10)
  - `page_number` (integer, optional) - Page number (default: 1)
  - `titles_only` (boolean, optional) - Search only titles (default: false)

### 7. `get_municipality_url`
Get the URL for a municipality's code library page.
- **Parameters**: 
  - `municipality_name` (string) - Name of the municipality
  - `state_abbr` (string) - Two-character state abbreviation

## 📝 Example Usage

### Basic Municipal Research
```
User: "List all municipalities in Virginia that use Municode"
Tool: list_municipalities({"state_abbr": "VA"})

User: "Get information about Norfolk, Virginia"
Tool: get_municipality_info({"municipality_name": "Norfolk", "state_abbr": "VA"})

User: "What's the structure of Norfolk's municipal code?"
Tool: get_code_structure({"municipality_name": "Norfolk", "state_abbr": "VA"})
```

### Searching Municipal Codes
```
User: "Search Norfolk VA municipal codes for zoning ordinances"
Tool: search_municipal_codes({
  "municipality_name": "Norfolk", 
  "state_abbr": "VA", 
  "search_query": "zoning"
})

User: "Find building code requirements for crawl space ventilation in Norfolk"
Tool: search_municipal_codes({
  "municipality_name": "Norfolk", 
  "state_abbr": "VA", 
  "search_query": "crawl space ventilation"
})
```

## 🏗️ Use Cases

### Urban Planning & Development
- Compare zoning ordinances across municipalities
- Research building code requirements
- Analyze development regulations and procedures

### Legal & Compliance Research
- Find relevant municipal ordinances for compliance
- Research local law requirements
- Cross-reference regulations across jurisdictions

### Academic & Policy Research
- Study municipal governance structures
- Analyze regulatory patterns across regions
- Research evolution of local laws

### Civic Engagement
- Understand local regulations affecting residents
- Prepare for city council meetings
- Research municipal procedures and policies

## ⚙️ Technical Details

### API Integration
This server uses the unofficial Municode API with endpoints including:
- State and municipality discovery
- Code structure navigation  
- Content retrieval
- Full-text search capabilities

### Data Structure
Municipal codes are organized hierarchically:
```
State → Municipality → Products → Sections → Content
```

Each municipality may have multiple products (Code of Ordinances, Zoning Ordinance, etc.), each with its own hierarchical structure.

## ⚠️ Limitations

- Uses unofficial API endpoints that may change
- Not all municipalities have all features available
- Some content may be in PDF format and not searchable via API
- Rate limiting may apply to API requests
- Municipality names must match Municode's exact formatting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Based on the [unofficial Municode API documentation](https://sr.ht/~partytax/unofficial-municode-api-documentation/) by ~partytax
- Municode and CivicPlus for providing public access to municipal code information
- The MCP community for developing the Model Context Protocol standard

## ⚖️ Legal Notice

This is an unofficial tool created to provide programmatic access to publicly available municipal code information. It is not affiliated with or endorsed by Municode or CivicPlus. Always verify critical legal information with official sources and respect Municode's terms of service.

---

**Made with ❤️ for civic transparency and accessibility**