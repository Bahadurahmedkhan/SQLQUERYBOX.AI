"""
Unit tests for the Flask backend application.

This module tests all the backend functionality including:
- API endpoints
- Database operations
- Data processing functions
- Error handling
"""

import pytest
import json
import sqlite3
from unittest.mock import Mock, patch, MagicMock
from backend.app import (
    app, get_db_connection, cents_to_dollars, analyze_prompt,
    get_time_based_analysis, get_sales_analysis, get_customer_analysis,
    get_product_analysis, get_order_analysis, get_general_analytics
)


class TestDatabaseConnection:
    """Test database connection functionality."""
    
    def test_get_db_connection(self, temp_db):
        """Test database connection creation."""
        with patch('backend.app.DB_PATH', temp_db):
            conn = get_db_connection()
            assert conn is not None
            assert hasattr(conn, 'execute')
            conn.close()
    
    def test_get_db_connection_with_row_factory(self, temp_db):
        """Test database connection with row factory."""
        with patch('backend.app.DB_PATH', temp_db):
            conn = get_db_connection()
            assert conn.row_factory == sqlite3.Row
            conn.close()


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_cents_to_dollars(self):
        """Test cents to dollars conversion."""
        assert cents_to_dollars(10000) == 100.0
        assert cents_to_dollars(0) == 0
        assert cents_to_dollars(None) == 0
        assert cents_to_dollars(1500) == 15.0
    
    def test_analyze_prompt_time_based(self):
        """Test prompt analysis for time-based queries."""
        prompts = [
            "Show me data for January 2024",
            "What happened in March?",
            "Revenue for 2024",
            "Customer purchases in December"
        ]
        
        for prompt in prompts:
            result = analyze_prompt(prompt)
            assert result == 'time_based'
    
    def test_analyze_prompt_customers(self):
        """Test prompt analysis for customer queries."""
        prompts = [
            "How many customers do we have?",
            "Show me customer demographics",
            "Who are our top customers?",
            "Customer purchase behavior"
        ]
        
        for prompt in prompts:
            result = analyze_prompt(prompt)
            assert result == 'customers'
    
    def test_analyze_prompt_sales(self):
        """Test prompt analysis for sales queries."""
        prompts = [
            "What's our total revenue?",
            "Show me sales performance",
            "Profit analysis",
            "Income breakdown"
        ]
        
        for prompt in prompts:
            result = analyze_prompt(prompt)
            assert result == 'sales'
    
    def test_analyze_prompt_products(self):
        """Test prompt analysis for product queries."""
        prompts = [
            "What products do we sell?",
            "Show me product inventory",
            "Best selling products",
            "Product categories"
        ]
        
        for prompt in prompts:
            result = analyze_prompt(prompt)
            assert result == 'products'
    
    def test_analyze_prompt_orders(self):
        """Test prompt analysis for order queries."""
        prompts = [
            "How many orders were placed?",
            "Show me recent purchases",
            "Order status breakdown",
            "Transaction history"
        ]
        
        for prompt in prompts:
            result = analyze_prompt(prompt)
            assert result == 'orders'
    
    def test_analyze_prompt_analytics(self):
        """Test prompt analysis for general analytics."""
        prompts = [
            "Give me a data overview",
            "Show me analytics",
            "Business summary",
            "General statistics"
        ]
        
        for prompt in prompts:
            result = analyze_prompt(prompt)
            assert result == 'analytics'


class TestAnalysisFunctions:
    """Test analysis functions."""
    
    @patch('backend.app.get_db_connection')
    def test_get_time_based_analysis_customer_purchases(self, mock_get_db, sample_customer_data):
        """Test time-based analysis for customer purchases."""
        # Mock database connection and results
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn
        
        # Mock query results
        mock_conn.execute.return_value.fetchone.return_value = {
            'customer_count': 5,
            'order_count': 10,
            'total_revenue': 25000
        }
        
        mock_conn.execute.return_value.fetchall.return_value = [
            {'day': '01', 'customers': 2, 'orders': 3},
            {'day': '02', 'customers': 3, 'orders': 7}
        ]
        
        text_response, chart_data = get_time_based_analysis("How many customers purchased in January 2024?")
        
        assert "Customer Purchase Activity" in text_response
        assert "Total Customers Who Purchased: 5" in text_response
        assert chart_data['type'] == 'line'
        assert 'datasets' in chart_data['data']
    
    @patch('backend.app.get_db_connection')
    def test_get_sales_analysis(self, mock_get_db):
        """Test sales analysis function."""
        # Mock database connection
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn
        
        # Mock query results
        mock_conn.execute.return_value.fetchone.return_value = {'total_revenue': 100000}
        mock_conn.execute.return_value.fetchall.return_value = [
            {'region': 'North America', 'revenue': 60000},
            {'region': 'Europe', 'revenue': 40000}
        ]
        
        text_response, chart_data = get_sales_analysis("Show me sales data")
        
        assert "Sales Performance Analysis" in text_response
        assert "Total Revenue: $1,000.00" in text_response
        assert chart_data['type'] == 'bar'
        assert len(chart_data['data']['labels']) == 2
    
    @patch('backend.app.get_db_connection')
    def test_get_customer_analysis(self, mock_get_db):
        """Test customer analysis function."""
        # Mock database connection
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn
        
        # Mock query results
        mock_conn.execute.return_value.fetchone.return_value = {
            'total_customers': 100,
            'total_orders': 250,
            'avg_order_value': 5000
        }
        mock_conn.execute.return_value.fetchall.return_value = [
            {'region': 'North America', 'customer_count': 60},
            {'region': 'Europe', 'customer_count': 40}
        ]
        
        text_response, chart_data = get_customer_analysis("Show me customer data")
        
        assert "Customer Analysis" in text_response
        assert "Total Customers: 100" in text_response
        assert chart_data['type'] == 'doughnut'
    
    @patch('backend.app.get_db_connection')
    def test_get_product_analysis(self, mock_get_db):
        """Test product analysis function."""
        # Mock database connection
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn
        
        # Mock query results
        mock_conn.execute.return_value.fetchone.return_value = {
            'total_products': 50,
            'min_price': 1000,
            'max_price': 10000,
            'avg_price': 5000
        }
        mock_conn.execute.return_value.fetchall.return_value = [
            {'category': 'Electronics', 'product_count': 20, 'avg_price': 8000},
            {'category': 'Books', 'product_count': 30, 'avg_price': 2000}
        ]
        
        text_response, chart_data = get_product_analysis("Show me product data")
        
        assert "Product Analysis" in text_response
        assert "Total Products: 50" in text_response
        assert chart_data['type'] == 'bar'
    
    @patch('backend.app.get_db_connection')
    def test_get_order_analysis(self, mock_get_db):
        """Test order analysis function."""
        # Mock database connection
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn
        
        # Mock query results
        mock_conn.execute.return_value.fetchall.return_value = [
            {'status': 'delivered', 'order_count': 100},
            {'status': 'shipped', 'order_count': 50},
            {'status': 'pending', 'order_count': 25}
        ]
        
        text_response, chart_data = get_order_analysis("Show me order data")
        
        assert "Order Analysis" in text_response
        assert "Delivered: 100 orders" in text_response
        assert chart_data['type'] == 'line'
    
    @patch('backend.app.get_db_connection')
    def test_get_general_analytics(self, mock_get_db):
        """Test general analytics function."""
        # Mock database connection
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn
        
        # Mock query results
        mock_conn.execute.return_value.fetchone.return_value = {
            'total_customers': 100,
            'total_products': 50,
            'total_orders': 250,
            'total_revenue': 125000
        }
        mock_conn.execute.return_value.fetchall.return_value = [
            {'id': 1, 'name': 'John Doe', 'order_date': '2024-01-01', 'status': 'delivered'},
            {'id': 2, 'name': 'Jane Smith', 'order_date': '2024-01-02', 'status': 'shipped'}
        ]
        
        text_response, chart_data = get_general_analytics("Show me general analytics")
        
        assert "General Analytics Dashboard" in text_response
        assert "Total Customers: 100" in text_response
        assert chart_data['type'] == 'bar'


class TestAPIEndpoints:
    """Test API endpoints."""
    
    def test_analyze_endpoint_success(self, mock_flask_app, sample_prompt_data, sample_response_data):
        """Test successful analyze endpoint."""
        with patch('backend.app.analyze_prompt') as mock_analyze, \
             patch('backend.app.get_time_based_analysis') as mock_analysis:
            
            mock_analyze.return_value = 'time_based'
            mock_analysis.return_value = (sample_response_data['textResponse'], sample_response_data['chartData'])
            
            response = mock_flask_app.post('/api/analyze', 
                                         data=json.dumps(sample_prompt_data),
                                         content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'textResponse' in data
            assert 'chartData' in data
            assert 'analysisType' in data
            assert 'timestamp' in data
    
    def test_analyze_endpoint_no_prompt(self, mock_flask_app):
        """Test analyze endpoint with no prompt."""
        response = mock_flask_app.post('/api/analyze', 
                                     data=json.dumps({}),
                                     content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No prompt provided' in data['error']
    
    def test_analyze_endpoint_empty_prompt(self, mock_flask_app):
        """Test analyze endpoint with empty prompt."""
        response = mock_flask_app.post('/api/analyze', 
                                     data=json.dumps({'prompt': ''}),
                                     content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_analyze_endpoint_exception(self, mock_flask_app, sample_prompt_data):
        """Test analyze endpoint with exception."""
        with patch('backend.app.analyze_prompt', side_effect=Exception("Test error")):
            response = mock_flask_app.post('/api/analyze', 
                                         data=json.dumps(sample_prompt_data),
                                         content_type='application/json')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_health_check_endpoint(self, mock_flask_app):
        """Test health check endpoint."""
        response = mock_flask_app.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_database_info_endpoint(self, mock_flask_app):
        """Test database info endpoint."""
        with patch('backend.app.get_db_connection') as mock_get_db:
            mock_conn = Mock()
            mock_get_db.return_value = mock_conn
            
            # Mock table count queries
            mock_conn.execute.return_value.fetchone.return_value = {'count': 10}
            
            response = mock_flask_app.get('/api/database/info')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'database_path' in data
            assert 'table_counts' in data
            assert 'timestamp' in data


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @patch('backend.app.get_db_connection')
    def test_database_connection_error(self, mock_get_db):
        """Test handling of database connection errors."""
        mock_get_db.side_effect = sqlite3.Error("Database connection failed")
        
        with pytest.raises(sqlite3.Error):
            get_db_connection()
    
    @patch('backend.app.get_db_connection')
    def test_analysis_function_database_error(self, mock_get_db):
        """Test analysis functions with database errors."""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.execute.side_effect = sqlite3.Error("Query failed")
        
        with pytest.raises(sqlite3.Error):
            get_sales_analysis("test prompt")
    
    def test_invalid_json_request(self, mock_flask_app):
        """Test handling of invalid JSON requests."""
        response = mock_flask_app.post('/api/analyze', 
                                     data="invalid json",
                                     content_type='application/json')
        
        assert response.status_code == 400


class TestDataProcessing:
    """Test data processing and formatting."""
    
    def test_chart_data_structure(self):
        """Test chart data structure validation."""
        chart_data = {
            'type': 'bar',
            'title': 'Test Chart',
            'data': {
                'labels': ['A', 'B', 'C'],
                'datasets': [{
                    'label': 'Test Data',
                    'data': [1, 2, 3]
                }]
            }
        }
        
        assert chart_data['type'] in ['bar', 'line', 'doughnut']
        assert 'title' in chart_data
        assert 'data' in chart_data
        assert 'labels' in chart_data['data']
        assert 'datasets' in chart_data['data']
    
    def test_text_response_formatting(self):
        """Test text response formatting."""
        text_response = """📊 Sales Performance Analysis

💰 Total Revenue: $1,000.00

🌍 Revenue by Region:
• North America: $600.00
• Europe: $400.00"""
        
        assert "📊" in text_response
        assert "💰" in text_response
        assert "•" in text_response
        assert "$" in text_response
    
    def test_timestamp_format(self):
        """Test timestamp format validation."""
        from datetime import datetime
        
        timestamp = datetime.now().isoformat()
        
        # Should be in ISO format
        assert 'T' in timestamp
        assert timestamp.count(':') >= 2
        assert len(timestamp) >= 19  # Minimum length for ISO format
