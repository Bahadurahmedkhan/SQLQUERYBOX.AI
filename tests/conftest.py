"""
Pytest configuration and shared fixtures for the test suite.

This module provides common fixtures and configuration for all tests
in the project.
"""

import pytest
import tempfile
import os
import sys
from unittest.mock import Mock, patch
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "lectures" / "week_10" / "SQLAgent"))

@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        'GOOGLE_API_KEY': 'test-api-key',
        'DATABASE_URL': 'sqlite:///test.db',
        'LLM_MODEL': 'gemini-1.5-flash',
        'LLM_TEMPERATURE': '0',
        'LOG_LEVEL': 'DEBUG'
    }):
        yield

@pytest.fixture
def mock_flask_app():
    """Mock Flask app for testing."""
    from backend.app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_prompt_data():
    """Sample prompt data for testing."""
    return {
        'prompt': 'Show me sales data for January 2024'
    }

@pytest.fixture
def sample_response_data():
    """Sample response data for testing."""
    return {
        'textResponse': 'Sample text response',
        'chartData': {
            'type': 'bar',
            'title': 'Sample Chart',
            'data': {
                'labels': ['Jan', 'Feb', 'Mar'],
                'datasets': [{
                    'label': 'Sales',
                    'data': [100, 200, 150]
                }]
            }
        },
        'analysisType': 'sales',
        'timestamp': '2024-01-01T00:00:00'
    }

@pytest.fixture
def mock_database_connection():
    """Mock database connection for testing."""
    mock_conn = Mock()
    mock_conn.execute.return_value.fetchone.return_value = {
        'customer_count': 10,
        'order_count': 25,
        'total_revenue': 50000
    }
    mock_conn.execute.return_value.fetchall.return_value = [
        {'region': 'North America', 'revenue': 30000},
        {'region': 'Europe', 'revenue': 20000}
    ]
    return mock_conn

@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    return {
        'output': 'This is a mock LLM response for testing purposes.'
    }

@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing."""
    return [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'region': 'North America'},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'region': 'Europe'},
        {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com', 'region': 'Asia'}
    ]

@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return [
        {'id': 1, 'name': 'Product A', 'category': 'Electronics', 'price_cents': 10000},
        {'id': 2, 'name': 'Product B', 'category': 'Books', 'price_cents': 2000},
        {'id': 3, 'name': 'Product C', 'category': 'Clothing', 'price_cents': 5000}
    ]

@pytest.fixture
def sample_order_data():
    """Sample order data for testing."""
    return [
        {'id': 1, 'customer_id': 1, 'order_date': '2024-01-01', 'status': 'delivered'},
        {'id': 2, 'customer_id': 2, 'order_date': '2024-01-02', 'status': 'shipped'},
        {'id': 3, 'customer_id': 1, 'order_date': '2024-01-03', 'status': 'pending'}
    ]

# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "api: mark test as requiring API access"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add unit marker to tests in unit test directories
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to tests in integration test directories
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add slow marker to tests that might be slow
        if any(keyword in item.name.lower() for keyword in ['slow', 'database', 'api']):
            item.add_marker(pytest.mark.slow)
