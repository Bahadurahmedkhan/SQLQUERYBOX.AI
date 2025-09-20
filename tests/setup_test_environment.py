#!/usr/bin/env python3
"""
Test environment setup script.

This script sets up the test environment for the Interactive Prompt Responder project.
It creates test databases, installs dependencies, and prepares the environment for testing.
"""

import os
import sys
import subprocess
import sqlite3
import tempfile
from pathlib import Path


def setup_test_database():
    """Create a test database with sample data."""
    print("🗄️  Setting up test database...")
    
    # Create test database
    test_db_path = Path("tests/test_data/test.db")
    test_db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(test_db_path))
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            region TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price_cents INTEGER NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            total_cents INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            unit_price_cents INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            amount_cents INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE refunds (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            amount_cents INTEGER NOT NULL,
            reason TEXT,
            status TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders (id)
        )
    ''')
    
    # Insert sample data
    customers = [
        (1, 'John Doe', 'john.doe@example.com', 'North America'),
        (2, 'Jane Smith', 'jane.smith@example.com', 'Europe'),
        (3, 'Bob Johnson', 'bob.johnson@example.com', 'Asia'),
        (4, 'Alice Brown', 'alice.brown@example.com', 'North America'),
        (5, 'Charlie Wilson', 'charlie.wilson@example.com', 'Europe'),
        (6, 'Diana Davis', 'diana.davis@example.com', 'Asia'),
        (7, 'Eve Miller', 'eve.miller@example.com', 'North America'),
        (8, 'Frank Garcia', 'frank.garcia@example.com', 'Europe'),
        (9, 'Grace Lee', 'grace.lee@example.com', 'Asia'),
        (10, 'Henry Taylor', 'henry.taylor@example.com', 'North America')
    ]
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)', customers)
    
    products = [
        (1, 'Laptop Pro', 'Electronics', 150000, 'High-performance laptop'),
        (2, 'Wireless Mouse', 'Electronics', 5000, 'Ergonomic wireless mouse'),
        (3, 'Programming Book', 'Books', 3000, 'Learn Python programming'),
        (4, 'Coffee Mug', 'Accessories', 1500, 'Ceramic coffee mug'),
        (5, 'Desk Lamp', 'Furniture', 8000, 'LED desk lamp'),
        (6, 'Notebook', 'Stationery', 800, 'Spiral-bound notebook'),
        (7, 'USB Cable', 'Electronics', 1200, 'USB-C to USB-A cable'),
        (8, 'Water Bottle', 'Accessories', 2000, 'Insulated water bottle'),
        (9, 'Keyboard', 'Electronics', 12000, 'Mechanical keyboard'),
        (10, 'Monitor Stand', 'Furniture', 6000, 'Adjustable monitor stand')
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)', products)
    
    orders = [
        (1, 1, '2024-01-15', 'delivered', 155000),
        (2, 2, '2024-01-16', 'shipped', 8000),
        (3, 3, '2024-01-17', 'pending', 3000),
        (4, 1, '2024-01-18', 'delivered', 12000),
        (5, 4, '2024-01-19', 'shipped', 1500),
        (6, 5, '2024-01-20', 'delivered', 2000),
        (7, 2, '2024-01-21', 'pending', 6000),
        (8, 6, '2024-01-22', 'shipped', 800),
        (9, 3, '2024-01-23', 'delivered', 1200),
        (10, 7, '2024-01-24', 'shipped', 2000)
    ]
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)', orders)
    
    order_items = [
        (1, 1, 1, 1, 150000),
        (2, 1, 2, 1, 5000),
        (3, 2, 5, 1, 8000),
        (4, 3, 3, 1, 3000),
        (5, 4, 9, 1, 12000),
        (6, 5, 4, 1, 1500),
        (7, 6, 8, 1, 2000),
        (8, 7, 10, 1, 6000),
        (9, 8, 6, 1, 800),
        (10, 9, 7, 1, 1200),
        (11, 10, 8, 1, 2000)
    ]
    cursor.executemany('INSERT INTO order_items VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)', order_items)
    
    payments = [
        (1, 1, 155000, 'credit_card', 'completed'),
        (2, 2, 8000, 'paypal', 'completed'),
        (3, 4, 12000, 'credit_card', 'completed'),
        (4, 5, 1500, 'debit_card', 'completed'),
        (5, 6, 2000, 'credit_card', 'completed'),
        (6, 8, 800, 'paypal', 'completed'),
        (7, 9, 1200, 'credit_card', 'completed'),
        (8, 10, 2000, 'debit_card', 'completed')
    ]
    cursor.executemany('INSERT INTO payments VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)', payments)
    
    refunds = [
        (1, 3, 3000, 'Customer requested cancellation', 'completed'),
        (2, 7, 6000, 'Product defect', 'pending')
    ]
    cursor.executemany('INSERT INTO refunds VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)', refunds)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Test database created at {test_db_path}")
    return str(test_db_path)


def install_test_dependencies():
    """Install test dependencies."""
    print("📦 Installing test dependencies...")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'tests/requirements.txt'
        ], check=True, capture_output=True, text=True)
        print("✅ Test dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install test dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False
    
    return True


def create_test_environment_file():
    """Create test environment file."""
    print("🔧 Creating test environment file...")
    
    test_env_path = Path("tests/.env.test")
    test_env_content = """# Test environment variables
GOOGLE_API_KEY=test-api-key-for-testing
DATABASE_URL=sqlite:///tests/test_data/test.db
LLM_MODEL=gemini-1.5-flash
LLM_TEMPERATURE=0
LLM_MAX_TOKENS=1000
LLM_TIMEOUT=60
MAX_QUERY_LIMIT=200
ENABLE_QUERY_LOGGING=true
LOG_LEVEL=DEBUG
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE=tests/test.log
"""
    
    with open(test_env_path, 'w') as f:
        f.write(test_env_content)
    
    print(f"✅ Test environment file created at {test_env_path}")


def setup_test_directories():
    """Create necessary test directories."""
    print("📁 Setting up test directories...")
    
    test_dirs = [
        "tests/test_data",
        "tests/test_logs",
        "tests/test_output",
        "tests/coverage",
        "tests/reports"
    ]
    
    for test_dir in test_dirs:
        Path(test_dir).mkdir(parents=True, exist_ok=True)
        print(f"  📂 Created directory: {test_dir}")
    
    print("✅ Test directories created")


def create_test_config():
    """Create test configuration file."""
    print("⚙️  Creating test configuration...")
    
    test_config_path = Path("tests/test_config.py")
    test_config_content = '''"""
Test configuration for the Interactive Prompt Responder project.
"""

import os
from pathlib import Path

# Test database configuration
TEST_DATABASE_URL = "sqlite:///tests/test_data/test.db"
TEST_DATABASE_PATH = Path("tests/test_data/test.db")

# Test API configuration
TEST_API_BASE_URL = "http://localhost:5000"
TEST_FRONTEND_URL = "http://localhost:3000"

# Test data configuration
TEST_DATA_DIR = Path("tests/test_data")
TEST_LOGS_DIR = Path("tests/test_logs")
TEST_OUTPUT_DIR = Path("tests/test_output")

# Test timeout configuration
TEST_TIMEOUT = 30
TEST_LONG_TIMEOUT = 60

# Test file paths
TEST_ENV_FILE = Path("tests/.env.test")
TEST_LOG_FILE = Path("tests/test_logs/test.log")

# Test markers
TEST_MARKERS = {
    'unit': 'Unit tests',
    'integration': 'Integration tests',
    'slow': 'Slow running tests',
    'api': 'Tests requiring API access',
    'database': 'Tests requiring database access'
}

# Test coverage configuration
COVERAGE_THRESHOLD = 80
COVERAGE_REPORT_DIR = Path("tests/coverage")
COVERAGE_HTML_DIR = Path("tests/coverage/html")

# Performance test configuration
PERFORMANCE_THRESHOLD_MS = 1000
MEMORY_THRESHOLD_MB = 100
'''
    
    with open(test_config_path, 'w') as f:
        f.write(test_config_content)
    
    print(f"✅ Test configuration created at {test_config_path}")


def run_basic_tests():
    """Run basic tests to verify setup."""
    print("🧪 Running basic tests to verify setup...")
    
    try:
        # Run a simple test to verify pytest is working
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 'tests/unit/test_utilities.py::TestPackageConfiguration::test_package_json_structure', 
            '-v', '--tb=short'
        ], check=True, capture_output=True, text=True)
        
        print("✅ Basic tests passed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Basic tests failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up test environment for Interactive Prompt Responder...")
    print("=" * 60)
    
    # Setup steps
    steps = [
        ("Setting up test directories", setup_test_directories),
        ("Creating test database", setup_test_database),
        ("Installing test dependencies", install_test_dependencies),
        ("Creating test environment file", create_test_environment_file),
        ("Creating test configuration", create_test_config),
        ("Running basic tests", run_basic_tests)
    ]
    
    success_count = 0
    
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}...")
        try:
            if step_function():
                success_count += 1
            else:
                print(f"⚠️  {step_name} completed with warnings")
                success_count += 1
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎉 Test environment setup completed!")
    print(f"✅ {success_count}/{len(steps)} steps completed successfully")
    
    if success_count == len(steps):
        print("\n🎯 You can now run tests with:")
        print("  pytest tests/                    # Run all tests")
        print("  pytest tests/unit/               # Run unit tests only")
        print("  pytest tests/integration/        # Run integration tests only")
        print("  pytest -m unit                   # Run tests marked as unit")
        print("  pytest -m integration            # Run tests marked as integration")
        print("  pytest --cov=backend tests/      # Run tests with coverage")
        print("  pytest -v                        # Run tests with verbose output")
    else:
        print("\n⚠️  Some steps failed. Please check the errors above and try again.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
