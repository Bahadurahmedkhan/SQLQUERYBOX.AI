# SQL Agent Development Guide

This guide provides comprehensive information for developers working on the SQL Agent project, including code quality standards, architecture decisions, and development workflows.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Code Quality Standards](#code-quality-standards)
3. [Development Workflow](#development-workflow)
4. [Testing Guidelines](#testing-guidelines)
5. [Configuration Management](#configuration-management)
6. [Security Considerations](#security-considerations)
7. [Performance Guidelines](#performance-guidelines)
8. [Troubleshooting](#troubleshooting)

## Architecture Overview

### Core Components

The SQL Agent system is built with a modular architecture that promotes maintainability and extensibility:

#### 1. Configuration Management (`config.py`)
- **Purpose**: Centralized configuration management
- **Key Features**:
  - Environment variable handling
  - Type-safe configuration classes
  - Validation of required settings
  - Support for different environments

#### 2. Shared Components (`shared_components.py`)
- **Purpose**: Reusable components and utilities
- **Key Features**:
  - `SafeSQLTool`: Secure SQL execution with validation
  - `DatabaseManager`: Database connection management
  - `LLMManager`: Language model management
  - `ErrorHandler`: Centralized error handling

#### 3. Base CLI (`base_cli.py`)
- **Purpose**: Common CLI functionality
- **Key Features**:
  - Abstract base class for all CLI implementations
  - Consistent user interface patterns
  - Resource management and cleanup
  - Error handling and logging

#### 4. Agent Implementations
- **Simple Agent**: Basic SQL querying (educational)
- **Secure Agent**: Production-ready with safety guardrails
- **Analytics Agent**: Advanced business intelligence

### Design Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **DRY (Don't Repeat Yourself)**: Shared functionality is centralized
3. **Type Safety**: Comprehensive type hints throughout
4. **Error Handling**: Consistent error handling patterns
5. **Security First**: Security considerations built into every component
6. **Testability**: All components are designed for easy testing

## Code Quality Standards

### Code Style

We use the following tools to maintain consistent code quality:

- **Black**: Code formatting
- **Flake8**: Linting and style checking
- **MyPy**: Static type checking
- **Pytest**: Testing framework

### Type Hints

All functions and methods must include comprehensive type hints:

```python
def process_query(self, query: str) -> Dict[str, Any]:
    """
    Process user query and return agent response.
    
    Args:
        query: User's question
        
    Returns:
        Dictionary containing query results
        
    Raises:
        ValueError: If query is invalid
    """
    # Implementation here
```

### Documentation

All public methods and classes must include docstrings following Google style:

```python
class ExampleClass:
    """
    Brief description of the class.
    
    Longer description if needed, explaining the purpose,
    usage, and any important implementation details.
    
    Attributes:
        attribute1: Description of attribute1
        attribute2: Description of attribute2
    """
    
    def example_method(self, param: str) -> bool:
        """
        Brief description of the method.
        
        Args:
            param: Description of the parameter
            
        Returns:
            Description of the return value
            
        Raises:
            ValueError: When param is invalid
        """
        # Implementation here
```

### Error Handling

Use the centralized error handling system:

```python
from shared_components import error_handler

try:
    # Risky operation
    result = risky_operation()
except DatabaseError as e:
    error_msg = error_handler.handle_database_error(e)
    logger.error(f"Database operation failed: {error_msg}")
    raise
```

## Development Workflow

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"

# Copy environment template
cp env.example .env
# Edit .env with your configuration
```

### 2. Code Quality Checks

Before committing, run all quality checks:

```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .

# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html
```

### 3. Pre-commit Hooks

Set up pre-commit hooks to automatically run quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

## Testing Guidelines

### Test Structure

Tests are organized in the `tests/` directory with the following structure:

```
tests/
├── __init__.py
├── test_config.py
├── test_shared_components.py
├── test_cli.py
└── fixtures/
    ├── sample_data.json
    └── test_database.db
```

### Test Categories

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows

### Test Naming

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example Test

```python
import pytest
from unittest.mock import patch, MagicMock
from shared_components import SafeSQLTool

class TestSafeSQLTool:
    """Test cases for the SafeSQLTool class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        with patch('shared_components.sqlalchemy.create_engine'):
            self.tool = SafeSQLTool()
    
    def test_valid_select_query(self):
        """Test that valid SELECT queries are executed."""
        with patch.object(self.tool, '_execute_sql_safely') as mock_execute:
            mock_execute.return_value = {"columns": ["id"], "rows": [[1]], "row_count": 1}
            
            result = self.tool._run("SELECT * FROM customers LIMIT 10")
            
            assert isinstance(result, dict)
            assert "columns" in result
```

## Configuration Management

### Environment Variables

All configuration is managed through environment variables:

```bash
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional (with defaults)
DATABASE_URL=sqlite:///sql_agent_class.db
LLM_MODEL=gemini-1.5-flash
MAX_QUERY_LIMIT=200
LOG_LEVEL=INFO
```

### Configuration Classes

Use the configuration classes for type-safe access:

```python
from config import config

# Access configuration
db_url = config.database.url
model_name = config.llm.model
max_limit = config.security.max_query_limit
```

## Security Considerations

### SQL Injection Prevention

The `SafeSQLTool` implements multiple layers of protection:

1. **Input Validation**: Regex-based pattern matching
2. **Whitelist Approach**: Only SELECT statements allowed
3. **Multiple Statement Prevention**: Blocks statement chaining
4. **Performance Limits**: Automatic LIMIT injection

### API Key Security

- Never commit API keys to version control
- Use environment variables for all sensitive data
- Validate API keys on startup
- Provide clear error messages for missing keys

### Database Security

- Use read-only database users in production
- Implement connection pooling with limits
- Log all database operations
- Validate all SQL queries before execution

## Performance Guidelines

### Database Connections

- Use connection pooling
- Implement proper connection cleanup
- Set appropriate timeouts
- Monitor connection usage

### Query Optimization

- Automatic LIMIT injection for large result sets
- Query result caching where appropriate
- Efficient error handling to avoid resource leaks

### Memory Management

- Use context managers for resource cleanup
- Implement proper object lifecycle management
- Monitor memory usage in long-running processes

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: Module not found errors
**Solution**: Ensure the parent directory is in the Python path:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

#### 2. Configuration Errors

**Problem**: Missing environment variables
**Solution**: Check that all required variables are set:

```bash
# Check environment variables
python -c "from config import config; print(config.to_dict())"
```

#### 3. Database Connection Issues

**Problem**: Database connection failures
**Solution**: Verify database file exists and is accessible:

```python
from shared_components import db_manager
if db_manager.test_connection():
    print("Database connection successful")
else:
    print("Database connection failed")
```

#### 4. API Key Issues

**Problem**: LLM API calls failing
**Solution**: Verify API key is valid and has proper permissions:

```python
from config import config
try:
    api_key = config.get_api_key('google')
    print("API key found")
except ValueError as e:
    print(f"API key error: {e}")
```

### Debug Mode

Enable debug logging for troubleshooting:

```bash
export LOG_LEVEL=DEBUG
python your_script.py
```

### Log Files

Check log files for detailed error information:

```bash
tail -f sql_agent.log
```

## Contributing

### Pull Request Process

1. Create a feature branch from `main`
2. Implement changes with tests
3. Run all quality checks
4. Update documentation if needed
5. Submit pull request with clear description

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Type hints are comprehensive
- [ ] Documentation is updated
- [ ] Security considerations addressed
- [ ] Performance impact assessed

### Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release tag
4. Build and publish package

## Support

For questions or issues:

1. Check this documentation
2. Review existing issues
3. Create a new issue with detailed information
4. Contact the development team

---

This guide is living documentation that should be updated as the project evolves. Please contribute improvements and corrections as needed.
