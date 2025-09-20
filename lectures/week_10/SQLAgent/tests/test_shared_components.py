"""
Test Shared Components Module

This module contains tests for the shared components and utilities.
"""

import pytest
from unittest.mock import patch, MagicMock, Mock
from shared_components import SafeSQLTool, DatabaseManager, LLMManager, ErrorHandler


class TestSafeSQLTool:
    """Test cases for the SafeSQLTool class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        with patch('shared_components.sqlalchemy.create_engine'):
            self.tool = SafeSQLTool()
    
    def test_valid_select_query(self):
        """Test that valid SELECT queries are executed."""
        with patch.object(self.tool, '_execute_sql_safely') as mock_execute:
            mock_execute.return_value = {"columns": ["id", "name"], "rows": [[1, "test"]], "row_count": 1}
            
            result = self.tool._run("SELECT * FROM customers LIMIT 10")
            
            assert isinstance(result, dict)
            assert "columns" in result
            assert "rows" in result
            assert "row_count" in result
    
    def test_blocked_operations(self):
        """Test that blocked operations are rejected."""
        blocked_queries = [
            "INSERT INTO customers VALUES (1, 'test')",
            "UPDATE customers SET name = 'test'",
            "DELETE FROM customers WHERE id = 1",
            "DROP TABLE customers",
            "TRUNCATE TABLE customers",
            "ALTER TABLE customers ADD COLUMN test VARCHAR(50)",
            "CREATE TABLE test (id INT)",
            "REPLACE INTO customers VALUES (1, 'test')"
        ]
        
        for query in blocked_queries:
            result = self.tool._run(query)
            assert "ERROR" in result
            assert "not allowed" in result
    
    def test_multiple_statements(self):
        """Test that multiple statements are rejected."""
        result = self.tool._run("SELECT * FROM customers; SELECT * FROM products;")
        assert "ERROR" in result
        assert "multiple statements" in result
    
    def test_non_select_statements(self):
        """Test that non-SELECT statements are rejected."""
        result = self.tool._run("SHOW TABLES")
        assert "ERROR" in result
        assert "only SELECT statements" in result
    
    def test_limit_injection(self):
        """Test that LIMIT is automatically added when needed."""
        with patch.object(self.tool, '_execute_sql_safely') as mock_execute:
            mock_execute.return_value = {"columns": ["id"], "rows": [[1]], "row_count": 1}
            
            # Mock the _optimize_sql_performance method to test limit injection
            with patch.object(self.tool, '_optimize_sql_performance') as mock_optimize:
                mock_optimize.return_value = "SELECT * FROM customers LIMIT 200"
                
                self.tool._run("SELECT * FROM customers")
                mock_optimize.assert_called_once()
    
    def test_clean_sql_input(self):
        """Test SQL input cleaning."""
        result = self.tool._clean_sql_input("  SELECT * FROM customers;  ")
        assert result == "SELECT * FROM customers"
    
    def test_validate_sql_security(self):
        """Test SQL security validation."""
        # Valid query
        assert self.tool._validate_sql_security("SELECT * FROM customers") == "VALID"
        
        # Invalid queries
        assert "not allowed" in self.tool._validate_sql_security("INSERT INTO customers VALUES (1)")
        assert "multiple statements" in self.tool._validate_sql_security("SELECT 1; SELECT 2")
        assert "only SELECT statements" in self.tool._validate_sql_security("SHOW TABLES")


class TestDatabaseManager:
    """Test cases for the DatabaseManager class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        with patch('shared_components.sqlalchemy.create_engine'):
            self.db_manager = DatabaseManager()
    
    def test_database_property(self):
        """Test database property lazy initialization."""
        with patch('shared_components.SQLDatabase.from_uri') as mock_from_uri:
            mock_db = MagicMock()
            mock_from_uri.return_value = mock_db
            
            db = self.db_manager.db
            
            assert db == mock_db
            mock_from_uri.assert_called_once()
    
    def test_get_schema_info(self):
        """Test schema information retrieval."""
        with patch.object(self.db_manager, 'db') as mock_db:
            mock_db.get_table_info.return_value = "schema info"
            
            result = self.db_manager.get_schema_info()
            
            assert result == "schema info"
            mock_db.get_table_info.assert_called_once()
    
    def test_test_connection_success(self):
        """Test successful database connection."""
        with patch.object(self.db_manager, 'engine') as mock_engine:
            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__.return_value = mock_conn
            
            result = self.db_manager.test_connection()
            
            assert result is True
            mock_conn.execute.assert_called_once()
    
    def test_test_connection_failure(self):
        """Test failed database connection."""
        with patch.object(self.db_manager, 'engine') as mock_engine:
            mock_engine.connect.side_effect = Exception("Connection failed")
            
            result = self.db_manager.test_connection()
            
            assert result is False


class TestLLMManager:
    """Test cases for the LLMManager class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.llm_manager = LLMManager()
    
    def test_llm_property(self):
        """Test LLM property lazy initialization."""
        with patch('shared_components.ChatGoogleGenerativeAI') as mock_llm_class:
            mock_llm = MagicMock()
            mock_llm_class.return_value = mock_llm
            
            llm = self.llm_manager.llm
            
            assert llm == mock_llm
            mock_llm_class.assert_called_once()
    
    def test_create_system_message(self):
        """Test system message creation."""
        from langchain.schema import SystemMessage
        
        content = "Test system message"
        message = self.llm_manager.create_system_message(content)
        
        assert isinstance(message, SystemMessage)
        assert message.content == content


class TestErrorHandler:
    """Test cases for the ErrorHandler class."""
    
    def test_handle_database_error(self):
        """Test database error handling."""
        # Test specific error types
        assert "does not exist" in ErrorHandler.handle_database_error(Exception("no such table"))
        assert "does not exist" in ErrorHandler.handle_database_error(Exception("no such column"))
        assert "syntax error" in ErrorHandler.handle_database_error(Exception("syntax error"))
        assert "locked" in ErrorHandler.handle_database_error(Exception("database is locked"))
        
        # Test generic error
        assert "Database error" in ErrorHandler.handle_database_error(Exception("generic error"))
    
    def test_handle_llm_error(self):
        """Test LLM error handling."""
        # Test specific error types
        assert "API key" in ErrorHandler.handle_llm_error(Exception("api key invalid"))
        assert "rate limit" in ErrorHandler.handle_llm_error(Exception("rate limit exceeded"))
        assert "timed out" in ErrorHandler.handle_llm_error(Exception("request timeout"))
        
        # Test generic error
        assert "LLM error" in ErrorHandler.handle_llm_error(Exception("generic error"))
    
    def test_handle_general_error(self):
        """Test general error handling."""
        result = ErrorHandler.handle_general_error(Exception("test error"))
        assert "unexpected error" in result
        assert "test error" in result
