# Contributing to MunicipalMCP

Thank you for your interest in contributing to MunicipalMCP! This project aims to provide accessible, programmatic access to municipal legal information across the United States.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub Issues tab to report bugs or suggest features
- Provide clear, detailed descriptions of the issue
- Include steps to reproduce bugs
- Mention your operating system and Python version

### Feature Requests
- Check existing issues to avoid duplicates
- Clearly describe the desired functionality
- Explain how it would benefit users
- Consider providing a use case example

### Code Contributions

#### Getting Started
1. Fork the repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/MunicipalMCP.git
   cd MunicipalMCP
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run tests to ensure everything works:
   ```bash
   python test_server.py
   ```

#### Making Changes
1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Test your changes thoroughly
4. Update documentation if needed
5. Update CHANGELOG.md with your changes

#### Code Style
- Follow PEP 8 Python style guidelines
- Use clear, descriptive variable and function names
- Include docstrings for all functions and classes
- Keep functions focused and modular
- Add type hints where appropriate

#### Testing
- Test your changes with `python test_server.py`
- Ensure the MCP server starts without errors
- Test with real Municode API endpoints when possible
- Add new tests for new functionality

#### Submitting Changes
1. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Create a Pull Request from your fork to the main repository
3. Provide a clear description of your changes
4. Link to any related issues
5. Be responsive to feedback and questions

## 🛠️ Development Guidelines

### Project Structure
```
MunicipalMCP/
├── municode-mcp-server.py     # Main MCP server implementation
├── test_server.py             # Test suite
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── CHANGELOG.md               # Version history
└── mcp-config-example.json    # Example configuration
```

### Adding New Tools
When adding new MCP tools:
1. Add the tool definition to `handle_list_tools()`
2. Implement the tool logic in `handle_call_tool()`
3. Add proper error handling
4. Update the README with tool documentation
5. Add tests for the new functionality

### API Guidelines
- Use consistent parameter naming across tools
- Provide helpful error messages
- Follow the existing patterns for API calls
- Handle rate limiting gracefully
- Validate input parameters

### Documentation
- Keep README.md up to date
- Document all public functions and classes
- Provide usage examples for new features
- Update CHANGELOG.md with all changes

## 🚀 Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality (backwards compatible)
- PATCH version for backwards compatible bug fixes

### Creating Releases
1. Update version numbers in relevant files
2. Update CHANGELOG.md with all changes
3. Create a release tag
4. Update documentation as needed

## 📝 Commit Guidelines

### Commit Message Format
```
type(scope): brief description

Longer explanation if needed

Closes #issue-number
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(search): add pagination support for search results

Added page_size and page_number parameters to search_municipal_codes
tool to handle large result sets more efficiently.

Closes #15
```

```
fix(api): handle network timeout errors gracefully

Improved error handling for API timeouts and connection issues.
Now provides more helpful error messages to users.

Fixes #23
```

## 🎯 Areas for Contribution

### High Priority
- Improved error handling and user feedback
- Performance optimizations for API calls
- Additional search filters and options
- Better documentation and examples

### Medium Priority
- Support for additional document types
- Caching mechanisms for frequently accessed data
- Batch operations for multiple municipalities
- Enhanced logging and debugging features

### Low Priority
- Alternative API backends
- GUI tools for configuration
- Integration with other civic data sources
- Advanced search algorithms

## ❓ Questions?

If you have questions about contributing:
1. Check existing issues and documentation
2. Create a GitHub issue with the "question" label
3. Provide as much context as possible

## 🙏 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- CHANGELOG.md for specific contributions
- GitHub contributors list

Thank you for helping make municipal legal information more accessible to everyone!