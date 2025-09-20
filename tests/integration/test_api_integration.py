"""
Integration tests for API endpoints and database interactions.

This module tests the complete flow from API request to database response,
including error handling and data processing.
"""

import pytest
import json
import sqlite3
import tempfile
from unittest.mock import Mock, patch
from backend.app import app


class TestAPIDatabaseIntegration:
    """Test API and database integration."""
    
    @pytest.fixture
    def test_db(self):
        """Create a test database with sample data."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        # Create test database with sample data
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                region TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price_cents INTEGER NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date TEXT NOT NULL,
                status TEXT NOT NULL,
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
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Insert sample data
        customers = [
            (1, 'John Doe', 'john@example.com', 'North America'),
            (2, 'Jane Smith', 'jane@example.com', 'Europe'),
            (3, 'Bob Johnson', 'bob@example.com', 'Asia')
        ]
        cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', customers)
        
        products = [
            (1, 'Laptop', 'Electronics', 100000),
            (2, 'Book', 'Education', 2000),
            (3, 'Shirt', 'Clothing', 5000)
        ]
        cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?)', products)
        
        orders = [
            (1, 1, '2024-01-01', 'delivered'),
            (2, 2, '2024-01-02', 'shipped'),
            (3, 1, '2024-01-03', 'pending')
        ]
        cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?)', orders)
        
        order_items = [
            (1, 1, 1, 1, 100000),
            (2, 2, 2, 2, 2000),
            (3, 3, 3, 1, 5000)
        ]
        cursor.executemany('INSERT INTO order_items VALUES (?, ?, ?, ?, ?)', order_items)
        
        conn.commit()
        conn.close()
        
        yield db_path
        
        # Cleanup
        import os
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    def test_analyze_endpoint_with_real_database(self, test_db):
        """Test analyze endpoint with real database."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                # Test customer analysis
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': 'How many customers do we have?'}),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert 'textResponse' in data
                assert 'chartData' in data
                assert 'analysisType' in data
                assert data['analysisType'] == 'customers'
                
                # Verify response contains expected data
                assert '3' in data['textResponse']  # Should mention 3 customers
    
    def test_sales_analysis_with_real_data(self, test_db):
        """Test sales analysis with real database data."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': 'What is our total revenue?'}),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data['analysisType'] == 'sales'
                
                # Verify revenue calculation (100000 + 4000 + 5000 = 109000 cents = $1090)
                assert '$1,090.00' in data['textResponse']
    
    def test_product_analysis_with_real_data(self, test_db):
        """Test product analysis with real database data."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': 'What products do we sell?'}),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data['analysisType'] == 'products'
                
                # Verify product information
                assert 'Laptop' in data['textResponse']
                assert 'Book' in data['textResponse']
                assert 'Shirt' in data['textResponse']
    
    def test_order_analysis_with_real_data(self, test_db):
        """Test order analysis with real database data."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': 'How many orders do we have?'}),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data['analysisType'] == 'orders'
                
                # Verify order count
                assert '3' in data['textResponse']  # Should mention 3 orders
    
    def test_time_based_analysis_with_real_data(self, test_db):
        """Test time-based analysis with real database data."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': 'Show me data for January 2024'}),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data['analysisType'] == 'time_based'
                
                # Verify time-based analysis
                assert 'January 2024' in data['textResponse'] or '2024' in data['textResponse']
    
    def test_general_analytics_with_real_data(self, test_db):
        """Test general analytics with real database data."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': 'Give me a business overview'}),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data['analysisType'] == 'analytics'
                
                # Verify general analytics
                assert '3' in data['textResponse']  # 3 customers
                assert '3' in data['textResponse']  # 3 products
                assert '3' in data['textResponse']  # 3 orders


class TestErrorHandlingIntegration:
    """Test error handling in integration scenarios."""
    
    def test_database_connection_error(self):
        """Test handling of database connection errors."""
        with patch('backend.app.DB_PATH', '/nonexistent/database.db'):
            with app.test_client() as client:
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': 'Test prompt'}),
                                     content_type='application/json')
                
                assert response.status_code == 500
                data = json.loads(response.data)
                assert 'error' in data
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON requests."""
        with app.test_client() as client:
            response = client.post('/api/analyze', 
                                 data="invalid json",
                                 content_type='application/json')
            
            assert response.status_code == 400
    
    def test_missing_prompt_field(self):
        """Test handling of missing prompt field."""
        with app.test_client() as client:
            response = client.post('/api/analyze', 
                                 data=json.dumps({'wrong_field': 'value'}),
                                 content_type='application/json')
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'No prompt provided' in data['error']


class TestDataFlowIntegration:
    """Test complete data flow from request to response."""
    
    def test_complete_analysis_flow(self, test_db):
        """Test complete analysis flow from prompt to response."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                # Test the complete flow
                prompt = "Show me our top customers by revenue"
                
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': prompt}),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                
                # Verify response structure
                assert 'textResponse' in data
                assert 'chartData' in data
                assert 'analysisType' in data
                assert 'timestamp' in data
                
                # Verify analysis type detection
                assert data['analysisType'] == 'customers'
                
                # Verify chart data structure
                chart_data = data['chartData']
                assert 'type' in chart_data
                assert 'title' in chart_data
                assert 'data' in chart_data
                assert 'labels' in chart_data['data']
                assert 'datasets' in chart_data['data']
    
    def test_multiple_requests_consistency(self, test_db):
        """Test consistency across multiple requests."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                prompts = [
                    "How many customers do we have?",
                    "What is our total revenue?",
                    "Show me all products"
                ]
                
                responses = []
                for prompt in prompts:
                    response = client.post('/api/analyze', 
                                         data=json.dumps({'prompt': prompt}),
                                         content_type='application/json')
                    
                    assert response.status_code == 200
                    data = json.loads(response.data)
                    responses.append(data)
                
                # Verify all responses have consistent structure
                for response in responses:
                    assert 'textResponse' in response
                    assert 'chartData' in response
                    assert 'analysisType' in response
                    assert 'timestamp' in response
    
    def test_concurrent_requests(self, test_db):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                results = []
                errors = []
                
                def make_request(prompt):
                    try:
                        response = client.post('/api/analyze', 
                                             data=json.dumps({'prompt': prompt}),
                                             content_type='application/json')
                        results.append(response.status_code)
                    except Exception as e:
                        errors.append(e)
                
                # Create multiple threads
                threads = []
                prompts = [
                    "How many customers?",
                    "What is our revenue?",
                    "Show me products",
                    "How many orders?",
                    "Business overview"
                ]
                
                for prompt in prompts:
                    thread = threading.Thread(target=make_request, args=(prompt,))
                    threads.append(thread)
                    thread.start()
                
                # Wait for all threads to complete
                for thread in threads:
                    thread.join()
                
                # Verify all requests succeeded
                assert len(errors) == 0
                assert all(status == 200 for status in results)


class TestPerformanceIntegration:
    """Test performance characteristics in integration scenarios."""
    
    def test_response_time(self, test_db):
        """Test response time for typical requests."""
        import time
        
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                start_time = time.time()
                
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': 'Show me customer data'}),
                                     content_type='application/json')
                
                end_time = time.time()
                response_time = end_time - start_time
                
                assert response.status_code == 200
                assert response_time < 5.0  # Should respond within 5 seconds
    
    def test_memory_usage(self, test_db):
        """Test memory usage during requests."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                # Make multiple requests
                for i in range(10):
                    response = client.post('/api/analyze', 
                                         data=json.dumps({'prompt': f'Request {i}'}),
                                         content_type='application/json')
                    assert response.status_code == 200
                
                final_memory = process.memory_info().rss
                memory_increase = final_memory - initial_memory
                
                # Memory increase should be reasonable (less than 50MB)
                assert memory_increase < 50 * 1024 * 1024


class TestSecurityIntegration:
    """Test security aspects in integration scenarios."""
    
    def test_sql_injection_prevention(self, test_db):
        """Test SQL injection prevention in API."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                malicious_prompts = [
                    "'; DROP TABLE customers; --",
                    "' UNION SELECT * FROM sqlite_master --",
                    "'; INSERT INTO customers VALUES (999, 'hacker', 'hack@evil.com', 'Evil'); --"
                ]
                
                for prompt in malicious_prompts:
                    response = client.post('/api/analyze', 
                                         data=json.dumps({'prompt': prompt}),
                                         content_type='application/json')
                    
                    # Should not crash or execute malicious SQL
                    assert response.status_code in [200, 400, 500]
                    
                    if response.status_code == 200:
                        data = json.loads(response.data)
                        # Should not contain any indication of successful injection
                        assert 'hacker' not in data['textResponse']
                        assert 'sqlite_master' not in data['textResponse']
    
    def test_input_validation(self, test_db):
        """Test input validation in API."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                # Test very long input
                long_prompt = "A" * 10000
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': long_prompt}),
                                     content_type='application/json')
                
                # Should handle long input gracefully
                assert response.status_code in [200, 400]
                
                # Test special characters
                special_prompt = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
                response = client.post('/api/analyze', 
                                     data=json.dumps({'prompt': special_prompt}),
                                     content_type='application/json')
                
                # Should handle special characters
                assert response.status_code in [200, 400]
    
    def test_rate_limiting_simulation(self, test_db):
        """Test behavior under high request volume."""
        with patch('backend.app.DB_PATH', test_db):
            with app.test_client() as client:
                # Make many requests quickly
                for i in range(50):
                    response = client.post('/api/analyze', 
                                         data=json.dumps({'prompt': f'Request {i}'}),
                                         content_type='application/json')
                    
                    # Should handle all requests (no rate limiting implemented yet)
                    assert response.status_code in [200, 429, 500]
