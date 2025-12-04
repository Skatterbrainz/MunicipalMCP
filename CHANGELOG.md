# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-04

### Added
- Initial release of MunicipalMCP server
- 7 MCP tools for accessing municipal codes:
  - `get_states_info` - Get US state information
  - `list_municipalities` - List municipalities by state
  - `get_municipality_info` - Get municipality details
  - `get_code_structure` - Browse code structure
  - `get_code_section` - Get specific code content
  - `search_municipal_codes` - Search municipal codes
  - `get_municipality_url` - Generate direct URLs
- Support for thousands of municipalities across the US
- Full-text search capabilities
- MCP resource for help documentation
- Comprehensive test suite
- MIT License

### Technical Details
- Built on Model Context Protocol (MCP) standard
- Uses unofficial Municode API endpoints
- Supports Python 3.8+
- Dependencies: httpx, mcp, pydantic
- Robust error handling and logging
- JSON-based configuration

### Documentation
- Complete README with installation and usage instructions
- Example MCP configurations for various clients
- Comprehensive tool documentation
- Use case examples and workflows
- Technical implementation details