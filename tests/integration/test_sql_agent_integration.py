"""
Integration tests for SQL Agent components.

This module tests the integration between different SQL Agent components
including configuration, database operations, LLM integration, and CLI interfaces.
"""

import pytest
import os
import tempfile
import sqlite3
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestSQLAgentConfigurationIntegration:
    """Test SQL Agent configuration integration."""
    
    def test_config_with_database_integration(self, temp_db):
        """Test configuration integration with database."""
        with patch.dict(os.environ, {
            'GOOGLE_API_KEY': 'test-key',
            'DATABASE_URL': f'sqlite:///{temp_db}',
            'LLM_MODEL': 'gemini-1.5-flash',
            'LLM_TEMPERATURE': '0',
            'LOG_LEVEL': 'INFO'
        }):
            # Create test database
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE test (id INTEGER, name TEXT)')
            cursor.execute('INSERT INTO test VALUES (1, "test")')
            conn.commit()
            conn.close()
            
            # Test configuration with database
            from lectures.week_10.SQLAgent.config import Config
            config = Config()
            
            assert config.database.url == f'sqlite:///{temp_db}'
            assert config.get_database_path().name == os.path.basename(temp_db)
    
    def test_config_with_llm_integration(self):
        """Test configuration integration with LLM."""
        with patch.dict(os.environ, {
            'GOOGLE_API_KEY': 'test-key',
            'DATABASE_URL': 'sqlite:///test.db',
            'LLM_MODEL': 'gemini-1.5-pro',
            'LLM_TEMPERATURE': '0.5',
            'LLM_MAX_TOKENS': '1000',
            'LLM_TIMEOUT': '120'
        }):
            from lectures.week_10.SQLAgent.config import Config
            config = Config()
            
            assert config.llm.model == 'gemini-1.5-pro'
            assert config.llm.temperature == 0.5
            assert config.llm.max_tokens == '1000'
            assert config.llm.timeout == 120
            
            # Test API key retrieval
            api_key = config.get_api_key('google')
            assert api_key == 'test-key'
    
    def test_config_with_security_integration(self):
        """Test configuration integration with security settings."""
        with patch.dict(os.environ, {
            'GOOGLE_API_KEY': 'test-key',
            'DATABASE_URL': 'sqlite:///test.db',
            'MAX_QUERY_LIMIT': '500',
            'ENABLE_QUERY_LOGGING': 'false'
        }):
            from lectures.week_10.SQLAgent.config import Config
            config = Config()
            
            assert config.security.max_query_limit == 500
            assert config.security.enable_query_logging is False
            assert 'SELECT' in config.security.allowed_operations
            assert 'INSERT' in config.security.blocked_operations


class TestDatabaseManagerIntegration:
    """Test DatabaseManager integration."""
    
    def test_database_manager_with_real_database(self, temp_db):
        """Test DatabaseManager with real database."""
        # Create test database with schema
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
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
        
        # Insert test data
        cursor.execute('INSERT INTO customers VALUES (1, "John Doe", "john@example.com", "North America")')
        cursor.execute('INSERT INTO products VALUES (1, "Laptop", "Electronics", 100000)')
        
        conn.commit()
        conn.close()
        
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.database.max_connections = 10
            mock_config.database.connection_timeout = 30
            mock_config.database.include_tables = ['customers', 'products']
            
            from lectures.week_10.SQLAgent.shared_components import DatabaseManager
            
            db_manager = DatabaseManager()
            
            # Test connection
            assert db_manager.test_connection() is True
            
            # Test schema info
            schema_info = db_manager.get_schema_info()
            assert 'customers' in schema_info
            assert 'products' in schema_info
            
            # Test database instance
            db = db_manager.db
            assert db is not None
            
            # Cleanup
            db_manager.close()
    
    def test_database_manager_error_handling(self):
        """Test DatabaseManager error handling."""
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = 'sqlite:///nonexistent.db'
            mock_config.database.max_connections = 10
            mock_config.database.connection_timeout = 30
            mock_config.database.include_tables = ['customers']
            
            from lectures.week_10.SQLAgent.shared_components import DatabaseManager
            
            db_manager = DatabaseManager()
            
            # Test connection failure
            assert db_manager.test_connection() is False
            
            # Test schema info with error
            schema_info = db_manager.get_schema_info()
            assert "Error retrieving schema information" in schema_info


class TestSafeSQLToolIntegration:
    """Test SafeSQLTool integration."""
    
    def test_safe_sql_tool_with_real_database(self, temp_db):
        """Test SafeSQLTool with real database."""
        # Create test database
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                region TEXT NOT NULL
            )
        ''')
        
        cursor.execute('INSERT INTO customers VALUES (1, "John Doe", "john@example.com", "North America")')
        cursor.execute('INSERT INTO customers VALUES (2, "Jane Smith", "jane@example.com", "Europe")')
        
        conn.commit()
        conn.close()
        
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.security.max_query_limit = 200
            mock_config.security.blocked_operations = ['INSERT', 'UPDATE', 'DELETE']
            mock_config.security.allowed_operations = ['SELECT']
            mock_config.security.enable_query_logging = True
            
            from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
            
            tool = SafeSQLTool()
            
            # Test valid SELECT query
            result = tool._run("SELECT * FROM customers")
            assert 'columns' in result
            assert 'rows' in result
            assert 'row_count' in result
            assert result['row_count'] == 2
            
            # Test query with LIMIT
            result = tool._run("SELECT * FROM customers LIMIT 1")
            assert result['row_count'] == 1
            
            # Test aggregation query
            result = tool._run("SELECT COUNT(*) as count FROM customers")
            assert result['row_count'] == 1
            assert result['rows'][0][0] == 2
    
    def test_safe_sql_tool_security_integration(self, temp_db):
        """Test SafeSQLTool security integration."""
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.security.max_query_limit = 200
            mock_config.security.blocked_operations = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE']
            mock_config.security.allowed_operations = ['SELECT']
            mock_config.security.enable_query_logging = True
            
            from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
            
            tool = SafeSQLTool()
            
            # Test blocked operations
            malicious_queries = [
                "INSERT INTO customers VALUES (999, 'hacker', 'hack@evil.com', 'Evil')",
                "UPDATE customers SET name = 'hacker' WHERE id = 1",
                "DELETE FROM customers WHERE id = 1",
                "DROP TABLE customers",
                "CREATE TABLE evil (id INT)"
            ]
            
            for query in malicious_queries:
                result = tool._run(query)
                assert 'ERROR:' in result
                assert 'not allowed' in result or 'forbidden' in result
    
    def test_safe_sql_tool_performance_integration(self, temp_db):
        """Test SafeSQLTool performance integration."""
        # Create test database with more data
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                region TEXT NOT NULL
            )
        ''')
        
        # Insert many records
        for i in range(1000):
            cursor.execute(f'INSERT INTO customers VALUES ({i}, "Customer {i}", "customer{i}@example.com", "Region {i % 5}")')
        
        conn.commit()
        conn.close()
        
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.security.max_query_limit = 100
            mock_config.security.blocked_operations = ['INSERT', 'UPDATE', 'DELETE']
            mock_config.security.allowed_operations = ['SELECT']
            mock_config.security.enable_query_logging = True
            
            from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
            
            tool = SafeSQLTool()
            
            # Test LIMIT enforcement
            result = tool._run("SELECT * FROM customers")
            assert result['row_count'] <= 100  # Should be limited to 100
            
            # Test aggregation without LIMIT
            result = tool._run("SELECT COUNT(*) as count FROM customers")
            assert result['row_count'] == 1
            assert result['rows'][0][0] == 1000


class TestLLMManagerIntegration:
    """Test LLMManager integration."""
    
    def test_llm_manager_with_config(self):
        """Test LLMManager with configuration."""
        with patch.dict(os.environ, {
            'GOOGLE_API_KEY': 'test-key',
            'DATABASE_URL': 'sqlite:///test.db',
            'LLM_MODEL': 'gemini-1.5-flash',
            'LLM_TEMPERATURE': '0'
        }):
            with patch('lectures.week_10.SQLAgent.shared_components.ChatGoogleGenerativeAI') as mock_llm_class:
                mock_llm_instance = Mock()
                mock_llm_class.return_value = mock_llm_instance
                
                from lectures.week_10.SQLAgent.shared_components import LLMManager
                
                llm_manager = LLMManager()
                llm = llm_manager.llm
                
                assert llm == mock_llm_instance
                mock_llm_class.assert_called_once_with(
                    model='gemini-1.5-flash',
                    temperature=0,
                    convert_system_message_to_human=True
                )
    
    def test_llm_manager_system_message_creation(self):
        """Test LLMManager system message creation."""
        with patch.dict(os.environ, {
            'GOOGLE_API_KEY': 'test-key',
            'DATABASE_URL': 'sqlite:///test.db'
        }):
            from lectures.week_10.SQLAgent.shared_components import LLMManager
            
            llm_manager = LLMManager()
            
            # Test system message creation
            system_message = llm_manager.create_system_message("Test system message")
            assert system_message.content == "Test system message"
            assert hasattr(system_message, 'content')


class TestErrorHandlerIntegration:
    """Test ErrorHandler integration."""
    
    def test_error_handler_with_real_errors(self):
        """Test ErrorHandler with real error scenarios."""
        from lectures.week_10.SQLAgent.shared_components import ErrorHandler
        
        # Test database errors
        db_errors = [
            (sqlite3.OperationalError("no such table: customers"), "table does not exist"),
            (sqlite3.OperationalError("no such column: name"), "column does not exist"),
            (sqlite3.OperationalError("syntax error"), "syntax error"),
            (sqlite3.OperationalError("database is locked"), "locked"),
            (Exception("Unknown database error"), "Database error")
        ]
        
        for error, expected_text in db_errors:
            error_msg = ErrorHandler.handle_database_error(error)
            assert expected_text in error_msg.lower()
        
        # Test LLM errors
        llm_errors = [
            (Exception("API key is invalid"), "API key"),
            (Exception("rate limit exceeded"), "rate limit"),
            (Exception("request timeout"), "timeout"),
            (Exception("Unknown LLM error"), "LLM error")
        ]
        
        for error, expected_text in llm_errors:
            error_msg = ErrorHandler.handle_llm_error(error)
            assert expected_text in error_msg.lower()
        
        # Test general errors
        general_error = Exception("Something went wrong")
        error_msg = ErrorHandler.handle_general_error(general_error)
        assert "unexpected error occurred" in error_msg


class TestCLIIntegration:
    """Test CLI integration."""
    
    def test_base_cli_integration(self):
        """Test BaseCLI integration."""
        from lectures.week_10.SQLAgent.base_cli import BaseCLI
        
        class TestCLI(BaseCLI):
            def setup_agent(self):
                self.agent = Mock()
                self.agent.invoke = Mock(return_value={'output': 'Test response'})
            
            def get_help_examples(self):
                return ["Test question 1", "Test question 2"]
        
        cli = TestCLI("Test Agent", "Test description")
        
        # Test initialization
        assert cli.initialize() is True
        assert cli.is_initialized is True
        
        # Test special commands
        assert cli.handle_special_commands("quit") is True
        assert cli.handle_special_commands("help") is True
        assert cli.handle_special_commands("schema") is True
        assert cli.handle_special_commands("clear") is True
        assert cli.handle_special_commands("Show me data") is False
        
        # Test table descriptions
        assert "Customer information" in cli._get_table_description("customers")
        assert "Product catalog" in cli._get_table_description("products")
    
    def test_cli_with_mock_components(self):
        """Test CLI with mocked components."""
        with patch('lectures.week_10.SQLAgent.base_cli.db_manager') as mock_db_manager, \
             patch('lectures.week_10.SQLAgent.base_cli.error_handler') as mock_error_handler:
            
            mock_db_manager.get_schema_info.return_value = "Mock schema info"
            mock_error_handler.handle_database_error.return_value = "Mock error message"
            
            from lectures.week_10.SQLAgent.base_cli import BaseCLI
            
            class TestCLI(BaseCLI):
                def setup_agent(self):
                    pass
                
                def get_help_examples(self):
                    return []
            
            cli = TestCLI("Test Agent", "Test description")
            
            # Test schema display
            cli.display_schema()
            mock_db_manager.get_schema_info.assert_called_once()


class TestEndToEndIntegration:
    """Test end-to-end integration scenarios."""
    
    def test_complete_sql_agent_workflow(self, temp_db):
        """Test complete SQL agent workflow."""
        # Create test database
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                region TEXT NOT NULL
            )
        ''')
        
        cursor.execute('INSERT INTO customers VALUES (1, "John Doe", "john@example.com", "North America")')
        cursor.execute('INSERT INTO customers VALUES (2, "Jane Smith", "jane@example.com", "Europe")')
        
        conn.commit()
        conn.close()
        
        with patch.dict(os.environ, {
            'GOOGLE_API_KEY': 'test-key',
            'DATABASE_URL': f'sqlite:///{temp_db}',
            'LLM_MODEL': 'gemini-1.5-flash',
            'LLM_TEMPERATURE': '0'
        }):
            with patch('lectures.week_10.SQLAgent.shared_components.ChatGoogleGenerativeAI') as mock_llm_class, \
                 patch('lectures.week_10.SQLAgent.scripts.01_simple_agent_cli.create_sql_agent') as mock_create_agent:
                
                mock_llm_instance = Mock()
                mock_llm_class.return_value = mock_llm_instance
                
                mock_agent = Mock()
                mock_agent.invoke = Mock(return_value={'output': 'Found 2 customers'})
                mock_create_agent.return_value = mock_agent
                
                from lectures.week_10.SQLAgent.scripts.01_simple_agent_cli import SimpleSQLAgentCLI
                
                cli = SimpleSQLAgentCLI()
                
                # Test initialization
                assert cli.initialize() is True
                assert cli.is_initialized is True
                
                # Test agent setup
                assert cli.agent is not None
                
                # Test help examples
                examples = cli.get_help_examples()
                assert len(examples) > 0
                assert any("customer" in example.lower() for example in examples)
    
    def test_security_workflow_integration(self, temp_db):
        """Test security workflow integration."""
        with patch.dict(os.environ, {
            'GOOGLE_API_KEY': 'test-key',
            'DATABASE_URL': f'sqlite:///{temp_db}',
            'MAX_QUERY_LIMIT': '100',
            'ENABLE_QUERY_LOGGING': 'true'
        }):
            with patch('lectures.week_10.SQLAgent.shared_components.ChatGoogleGenerativeAI') as mock_llm_class:
                mock_llm_instance = Mock()
                mock_llm_class.return_value = mock_llm_instance
                
                from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
                
                tool = SafeSQLTool()
                
                # Test security validation workflow
                malicious_queries = [
                    "SELECT * FROM customers; DROP TABLE customers;",
                    "'; INSERT INTO customers VALUES (999, 'hacker', 'hack@evil.com', 'Evil'); --",
                    "SELECT * FROM customers UNION SELECT * FROM sqlite_master"
                ]
                
                for query in malicious_queries:
                    result = tool._run(query)
                    assert 'ERROR:' in result
                    assert any(keyword in result for keyword in ['not allowed', 'forbidden', 'dangerous'])
                
                # Test valid query workflow
                valid_result = tool._run("SELECT 1 as test")
                assert 'ERROR:' not in valid_result
                assert 'columns' in valid_result
                assert 'rows' in valid_result
