# Test Suite for Interactive Prompt Responder

This directory contains comprehensive unit and integration tests for the Interactive Prompt Responder project.

## 📁 Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Pytest configuration and shared fixtures
├── pytest.ini                    # Pytest settings
├── requirements.txt               # Test dependencies
├── setup_test_environment.py     # Test environment setup script
├── run_tests.py                  # Test runner script
├── README.md                     # This file
├── unit/                         # Unit tests
│   ├── __init__.py
│   ├── test_backend.py           # Backend API tests
│   ├── test_frontend.py          # Frontend component tests
│   ├── test_sql_agent.py         # SQL Agent tests
│   └── test_utilities.py         # Utility script tests
├── integration/                  # Integration tests
│   ├── __init__.py
│   ├── test_api_integration.py   # API integration tests
│   └── test_sql_agent_integration.py # SQL Agent integration tests
├── test_data/                    # Test data files
├── test_logs/                    # Test log files
├── test_output/                  # Test output files
├── coverage/                     # Coverage reports
└── reports/                      # Test reports
```

## 🚀 Quick Start

### 1. Setup Test Environment

```bash
# Run the setup script to create test environment
python tests/setup_test_environment.py
```

### 2. Run Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test types
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration

# Run with coverage
python tests/run_tests.py --coverage

# Run with verbose output
python tests/run_tests.py --verbose
```

### 3. Using pytest directly

```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run tests with coverage
pytest tests/ --cov=backend --cov=src

# Run tests by marker
pytest tests/ -m unit
pytest tests/ -m integration
pytest tests/ -m slow
```

## 📋 Test Categories

### Unit Tests (`tests/unit/`)

Unit tests focus on testing individual components in isolation:

- **`test_backend.py`**: Tests for Flask backend API
  - Database connection functions
  - Utility functions (cents_to_dollars, analyze_prompt)
  - Analysis functions (sales, customer, product, order analysis)
  - API endpoints (/api/analyze, /api/health, /api/database/info)
  - Error handling scenarios

- **`test_frontend.py`**: Tests for React frontend components
  - App component initialization and state management
  - PromptInput component functionality
  - TextResponse component formatting
  - GraphicalResponse component chart handling
  - API integration and error handling

- **`test_sql_agent.py`**: Tests for SQL Agent components
  - Configuration management
  - Database operations and security
  - LLM integration
  - CLI interfaces
  - Error handling

- **`test_utilities.py`**: Tests for utility scripts and files
  - Startup scripts
  - Package configuration files
  - Database setup scripts
  - Build tools and documentation

### Integration Tests (`tests/integration/`)

Integration tests verify that different components work together correctly:

- **`test_api_integration.py`**: API and database integration
  - Complete request/response flow
  - Database operations with real data
  - Error handling in integration scenarios
  - Performance and security testing

- **`test_sql_agent_integration.py`**: SQL Agent component integration
  - Configuration with database integration
  - Database manager with real databases
  - SafeSQLTool with security validation
  - End-to-end SQL agent workflows

## 🏷️ Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Slow-running tests
- `@pytest.mark.api`: Tests requiring API access
- `@pytest.mark.database`: Tests requiring database access

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --color=yes
    --durations=10
```

### Shared Fixtures (`conftest.py`)

Common fixtures available to all tests:

- `temp_db`: Temporary database for testing
- `mock_env_vars`: Mocked environment variables
- `mock_flask_app`: Mock Flask application
- `sample_prompt_data`: Sample prompt data
- `sample_response_data`: Sample response data
- `mock_database_connection`: Mock database connection
- `mock_llm_response`: Mock LLM response
- `sample_customer_data`: Sample customer data
- `sample_product_data`: Sample product data
- `sample_order_data`: Sample order data

## 📊 Coverage Reports

### Generate Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov=backend --cov=src --cov-report=html

# Generate coverage report with missing lines
pytest tests/ --cov=backend --cov=src --cov-report=term-missing

# Generate XML coverage report
pytest tests/ --cov=backend --cov=src --cov-report=xml
```

### Coverage Thresholds

- **Backend**: 80% minimum coverage
- **Frontend**: 70% minimum coverage
- **SQL Agent**: 85% minimum coverage
- **Utilities**: 60% minimum coverage

## 🚨 Test Data

### Test Database

The test environment creates a sample database with:

- **Customers**: 10 sample customers with different regions
- **Products**: 10 sample products across different categories
- **Orders**: 10 sample orders with various statuses
- **Order Items**: Order line items with quantities and prices
- **Payments**: Payment records for completed orders
- **Refunds**: Refund records for cancelled orders

### Test Environment Variables

```bash
GOOGLE_API_KEY=test-api-key-for-testing
DATABASE_URL=sqlite:///tests/test_data/test.db
LLM_MODEL=gemini-1.5-flash
LLM_TEMPERATURE=0
MAX_QUERY_LIMIT=200
ENABLE_QUERY_LOGGING=true
LOG_LEVEL=DEBUG
```

## 🔍 Debugging Tests

### Running Specific Tests

```bash
# Run specific test file
pytest tests/unit/test_backend.py

# Run specific test function
pytest tests/unit/test_backend.py::TestAPIEndpoints::test_analyze_endpoint_success

# Run tests matching pattern
pytest tests/ -k "test_analyze"

# Run tests with specific marker
pytest tests/ -m "not slow"
```

### Verbose Output

```bash
# Verbose output with test names
pytest tests/ -v

# Extra verbose output
pytest tests/ -vv

# Show local variables on failure
pytest tests/ -l
```

### Debug Mode

```bash
# Drop into debugger on failure
pytest tests/ --pdb

# Drop into debugger on first failure
pytest tests/ --pdb -x
```

## 📈 Performance Testing

### Benchmark Tests

```bash
# Run performance tests
pytest tests/ -m slow --benchmark-only

# Compare with previous runs
pytest tests/ -m slow --benchmark-compare

# Save benchmark results
pytest tests/ -m slow --benchmark-save=performance
```

### Performance Thresholds

- **API Response Time**: < 1 second
- **Database Query Time**: < 500ms
- **Memory Usage**: < 100MB per test
- **Test Execution Time**: < 30 seconds total

## 🛡️ Security Testing

### SQL Injection Tests

Tests verify protection against:

- SQL injection attacks
- Cross-site scripting (XSS)
- Input validation bypass
- Authentication bypass attempts

### Security Test Examples

```python
def test_sql_injection_prevention(self):
    malicious_queries = [
        "'; DROP TABLE customers; --",
        "' UNION SELECT * FROM sqlite_master --",
        "'; INSERT INTO customers VALUES (999, 'hacker'); --"
    ]
    
    for query in malicious_queries:
        result = tool._validate_sql_security(query)
        assert result != "VALID"
```

## 🔄 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r tests/requirements.txt
    - name: Run tests
      run: |
        python tests/run_tests.py --coverage
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 📝 Writing New Tests

### Test File Structure

```python
"""
Test module description.
"""

import pytest
from unittest.mock import Mock, patch

class TestComponentName:
    """Test class for ComponentName."""
    
    def test_function_name(self):
        """Test function description."""
        # Arrange
        input_data = "test input"
        
        # Act
        result = function_under_test(input_data)
        
        # Assert
        assert result == expected_output
    
    @pytest.mark.parametrize("input,expected", [
        ("input1", "output1"),
        ("input2", "output2"),
    ])
    def test_parametrized_function(self, input, expected):
        """Test with multiple inputs."""
        result = function_under_test(input)
        assert result == expected
```

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Test descriptions: Clear and descriptive

### Best Practices

1. **Arrange-Act-Assert**: Structure tests clearly
2. **One assertion per test**: Focus on single behavior
3. **Descriptive names**: Make test purpose clear
4. **Use fixtures**: Reuse common setup code
5. **Mock external dependencies**: Isolate units under test
6. **Test edge cases**: Include boundary conditions
7. **Test error conditions**: Verify error handling

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Python path includes project root
2. **Database Errors**: Check test database setup
3. **Environment Variables**: Verify test environment configuration
4. **Dependencies**: Install all test requirements

### Getting Help

1. Check test output for specific error messages
2. Run tests with verbose output (`-v` flag)
3. Use debug mode (`--pdb`) for interactive debugging
4. Check test logs in `tests/test_logs/`

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python.org/3/library/unittest.html)
- [Flask Testing](https://flask.palletsprojects.com/en/2.0.x/testing/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [SQLite Testing](https://www.sqlite.org/testing.html)
