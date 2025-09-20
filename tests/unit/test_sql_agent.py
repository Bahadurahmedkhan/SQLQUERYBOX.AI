"""
Unit tests for SQL Agent components.

This module tests all the SQL Agent functionality including:
- Configuration management
- Database operations
- LLM integration
- Security features
- CLI interfaces
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestConfiguration:
    """Test configuration management."""
    
    def test_config_initialization(self, mock_env_vars):
        """Test configuration initialization."""
        with patch('lectures.week_10.SQLAgent.config.os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda key, default=None: {
                'GOOGLE_API_KEY': 'test-key',
                'DATABASE_URL': 'sqlite:///test.db',
                'LLM_MODEL': 'gemini-1.5-flash',
                'LLM_TEMPERATURE': '0',
                'LOG_LEVEL': 'INFO'
            }.get(key, default)
            
            from lectures.week_10.SQLAgent.config import Config
            
            config = Config()
            
            assert config.database.url == 'sqlite:///test.db'
            assert config.llm.model == 'gemini-1.5-flash'
            assert config.llm.temperature == 0.0
            assert config.security.max_query_limit == 200
    
    def test_database_config(self, mock_env_vars):
        """Test database configuration."""
        with patch('lectures.week_10.SQLAgent.config.os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda key, default=None: {
                'DATABASE_URL': 'sqlite:///test.db',
                'DB_MAX_CONNECTIONS': '20',
                'DB_CONNECTION_TIMEOUT': '60'
            }.get(key, default)
            
            from lectures.week_10.SQLAgent.config import Config
            
            config = Config()
            
            assert config.database.max_connections == 20
            assert config.database.connection_timeout == 60
            assert 'customers' in config.database.include_tables
            assert 'products' in config.database.include_tables
    
    def test_security_config(self, mock_env_vars):
        """Test security configuration."""
        with patch('lectures.week_10.SQLAgent.config.os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda key, default=None: {
                'GOOGLE_API_KEY': 'test-key',
                'MAX_QUERY_LIMIT': '500',
                'ENABLE_QUERY_LOGGING': 'false'
            }.get(key, default)
            
            from lectures.week_10.SQLAgent.config import Config
            
            config = Config()
            
            assert config.security.max_query_limit == 500
            assert config.security.enable_query_logging is False
            assert 'SELECT' in config.security.allowed_operations
            assert 'INSERT' in config.security.blocked_operations
    
    def test_llm_config(self, mock_env_vars):
        """Test LLM configuration."""
        with patch('lectures.week_10.SQLAgent.config.os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda key, default=None: {
                'GOOGLE_API_KEY': 'test-key',
                'LLM_MODEL': 'gemini-1.5-pro',
                'LLM_TEMPERATURE': '0.5',
                'LLM_MAX_TOKENS': '1000',
                'LLM_TIMEOUT': '120'
            }.get(key, default)
            
            from lectures.week_10.SQLAgent.config import Config
            
            config = Config()
            
            assert config.llm.model == 'gemini-1.5-pro'
            assert config.llm.temperature == 0.5
            assert config.llm.max_tokens == '1000'
            assert config.llm.timeout == 120
    
    def test_missing_required_env_vars(self):
        """Test handling of missing required environment variables."""
        with patch('lectures.week_10.SQLAgent.config.os.getenv', return_value=None):
            from lectures.week_10.SQLAgent.config import Config
            
            with pytest.raises(ValueError, match="Missing required environment variables"):
                Config()
    
    def test_get_api_key(self, mock_env_vars):
        """Test API key retrieval."""
        with patch('lectures.week_10.SQLAgent.config.os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda key, default=None: {
                'GOOGLE_API_KEY': 'test-google-key',
                'OPENAI_API_KEY': 'test-openai-key'
            }.get(key, default)
            
            from lectures.week_10.SQLAgent.config import Config
            
            config = Config()
            
            assert config.get_api_key('google') == 'test-google-key'
            assert config.get_api_key('openai') == 'test-openai-key'
            
            with pytest.raises(ValueError, match="Unknown service"):
                config.get_api_key('unknown')
    
    def test_database_path_extraction(self, mock_env_vars):
        """Test database path extraction."""
        with patch('lectures.week_10.SQLAgent.config.os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda key, default=None: {
                'GOOGLE_API_KEY': 'test-key',
                'DATABASE_URL': 'sqlite:///test.db'
            }.get(key, default)
            
            from lectures.week_10.SQLAgent.config import Config
            
            config = Config()
            db_path = config.get_database_path()
            
            assert db_path.name == 'test.db'
            assert str(db_path).endswith('test.db')


class TestSharedComponents:
    """Test shared components functionality."""
    
    def test_query_input_validation(self):
        """Test QueryInput model validation."""
        from lectures.week_10.SQLAgent.shared_components import QueryInput
        
        # Test valid input
        valid_input = QueryInput(sql="SELECT * FROM customers LIMIT 10")
        assert valid_input.sql == "SELECT * FROM customers LIMIT 10"
        
        # Test empty input
        with pytest.raises(ValueError):
            QueryInput(sql="")
        
        # Test too long input
        long_sql = "SELECT * FROM customers " + "WHERE id > 0 " * 1000
        with pytest.raises(ValueError):
            QueryInput(sql=long_sql)
    
    def test_safe_sql_tool_initialization(self, mock_env_vars, temp_db):
        """Test SafeSQLTool initialization."""
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.security.max_query_limit = 200
            mock_config.security.blocked_operations = ['INSERT', 'UPDATE', 'DELETE']
            mock_config.security.allowed_operations = ['SELECT']
            mock_config.security.enable_query_logging = True
            
            from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
            
            tool = SafeSQLTool()
            
            assert tool.name == "execute_sql"
            assert tool.max_limit == 200
            assert 'INSERT' in tool.blocked_operations
            assert 'SELECT' in tool.allowed_operations
    
    def test_sql_security_validation(self, mock_env_vars, temp_db):
        """Test SQL security validation."""
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.security.max_query_limit = 200
            mock_config.security.blocked_operations = ['INSERT', 'UPDATE', 'DELETE']
            mock_config.security.allowed_operations = ['SELECT']
            mock_config.security.enable_query_logging = True
            
            from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
            
            tool = SafeSQLTool()
            
            # Test valid SELECT query
            result = tool._validate_sql_security("SELECT * FROM customers")
            assert result == "VALID"
            
            # Test blocked operations
            result = tool._validate_sql_security("INSERT INTO customers VALUES (1, 'test')")
            assert "write operations are not allowed" in result
            
            result = tool._validate_sql_security("UPDATE customers SET name = 'test'")
            assert "write operations are not allowed" in result
            
            result = tool._validate_sql_security("DELETE FROM customers")
            assert "write operations are not allowed" in result
            
            # Test multiple statements
            result = tool._validate_sql_security("SELECT * FROM customers; SELECT * FROM products")
            assert "multiple statements are not allowed" in result
            
            # Test non-SELECT statements
            result = tool._validate_sql_security("CREATE TABLE test (id INT)")
            assert "only SELECT statements are allowed" in result
    
    def test_sql_optimization(self, mock_env_vars, temp_db):
        """Test SQL query optimization."""
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.security.max_query_limit = 200
            mock_config.security.blocked_operations = ['INSERT', 'UPDATE', 'DELETE']
            mock_config.security.allowed_operations = ['SELECT']
            mock_config.security.enable_query_logging = True
            
            from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
            
            tool = SafeSQLTool()
            
            # Test adding LIMIT to simple query
            optimized = tool._optimize_sql_performance("SELECT * FROM customers")
            assert "LIMIT 200" in optimized
            
            # Test not adding LIMIT to aggregation query
            optimized = tool._optimize_sql_performance("SELECT COUNT(*) FROM customers")
            assert "LIMIT" not in optimized
            
            # Test not adding LIMIT when already present
            optimized = tool._optimize_sql_performance("SELECT * FROM customers LIMIT 10")
            assert optimized == "SELECT * FROM customers LIMIT 10"
    
    def test_database_manager(self, mock_env_vars, temp_db):
        """Test DatabaseManager functionality."""
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
            assert isinstance(schema_info, str)
    
    def test_llm_manager(self, mock_env_vars):
        """Test LLMManager functionality."""
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.llm.model = 'gemini-1.5-flash'
            mock_config.llm.temperature = 0
            
            with patch('lectures.week_10.SQLAgent.shared_components.ChatGoogleGenerativeAI') as mock_llm_class:
                mock_llm_instance = Mock()
                mock_llm_class.return_value = mock_llm_instance
                
                from lectures.week_10.SQLAgent.shared_components import LLMManager
                
                llm_manager = LLMManager()
                llm = llm_manager.llm
                
                assert llm == mock_llm_instance
                mock_llm_class.assert_called_once()
    
    def test_error_handler(self):
        """Test ErrorHandler functionality."""
        from lectures.week_10.SQLAgent.shared_components import ErrorHandler
        
        # Test database error handling
        db_error = Exception("no such table: customers")
        error_msg = ErrorHandler.handle_database_error(db_error)
        assert "table does not exist" in error_msg
        
        db_error = Exception("no such column: name")
        error_msg = ErrorHandler.handle_database_error(db_error)
        assert "column does not exist" in error_msg
        
        # Test LLM error handling
        llm_error = Exception("API key is invalid")
        error_msg = ErrorHandler.handle_llm_error(llm_error)
        assert "API key is invalid" in error_msg
        
        llm_error = Exception("rate limit exceeded")
        error_msg = ErrorHandler.handle_llm_error(llm_error)
        assert "rate limit exceeded" in error_msg
        
        # Test general error handling
        general_error = Exception("Something went wrong")
        error_msg = ErrorHandler.handle_general_error(general_error)
        assert "unexpected error occurred" in error_msg


class TestBaseCLI:
    """Test BaseCLI functionality."""
    
    def test_base_cli_initialization(self):
        """Test BaseCLI initialization."""
        from lectures.week_10.SQLAgent.base_cli import BaseCLI
        
        # Create a concrete implementation for testing
        class TestCLI(BaseCLI):
            def setup_agent(self):
                pass
            
            def get_help_examples(self):
                return ["Test question 1", "Test question 2"]
        
        cli = TestCLI("Test Agent", "Test description")
        
        assert cli.agent_name == "Test Agent"
        assert cli.description == "Test description"
        assert cli.is_initialized is False
    
    def test_cli_initialization(self):
        """Test CLI initialization process."""
        from lectures.week_10.SQLAgent.base_cli import BaseCLI
        
        class TestCLI(BaseCLI):
            def setup_agent(self):
                self.agent = Mock()
            
            def get_help_examples(self):
                return ["Test question"]
        
        cli = TestCLI("Test Agent", "Test description")
        
        # Test initialization
        result = cli.initialize()
        assert result is True
        assert cli.is_initialized is True
        assert cli.agent is not None
    
    def test_cli_initialization_failure(self):
        """Test CLI initialization failure handling."""
        from lectures.week_10.SQLAgent.base_cli import BaseCLI
        
        class TestCLI(BaseCLI):
            def setup_agent(self):
                raise Exception("Initialization failed")
            
            def get_help_examples(self):
                return []
        
        cli = TestCLI("Test Agent", "Test description")
        
        # Test initialization failure
        result = cli.initialize()
        assert result is False
        assert cli.is_initialized is False
    
    def test_special_commands_handling(self):
        """Test special commands handling."""
        from lectures.week_10.SQLAgent.base_cli import BaseCLI
        
        class TestCLI(BaseCLI):
            def setup_agent(self):
                pass
            
            def get_help_examples(self):
                return []
        
        cli = TestCLI("Test Agent", "Test description")
        
        # Test quit commands
        assert cli.handle_special_commands("quit") is True
        assert cli.handle_special_commands("exit") is True
        assert cli.handle_special_commands("q") is True
        
        # Test help command
        assert cli.handle_special_commands("help") is True
        
        # Test schema command
        assert cli.handle_special_commands("schema") is True
        
        # Test clear command
        assert cli.handle_special_commands("clear") is True
        
        # Test empty input
        assert cli.handle_special_commands("") is True
        
        # Test regular input
        assert cli.handle_special_commands("Show me customers") is False
    
    def test_table_descriptions(self):
        """Test table description functionality."""
        from lectures.week_10.SQLAgent.base_cli import BaseCLI
        
        class TestCLI(BaseCLI):
            def setup_agent(self):
                pass
            
            def get_help_examples(self):
                return []
        
        cli = TestCLI("Test Agent", "Test description")
        
        # Test known table descriptions
        assert "Customer information" in cli._get_table_description("customers")
        assert "Product catalog" in cli._get_table_description("products")
        assert "Order records" in cli._get_table_description("orders")
        
        # Test unknown table
        assert "not available" in cli._get_table_description("unknown_table")


class TestCLIScripts:
    """Test CLI script functionality."""
    
    def test_simple_llm_cli_initialization(self):
        """Test SimpleLLMCLI initialization."""
        with patch('lectures.week_10.SQLAgent.scripts.00_simple_llm_cli.ChatGoogleGenerativeAI') as mock_llm, \
             patch('lectures.week_10.SQLAgent.scripts.00_simple_llm_cli.initialize_agent') as mock_agent:
            
            mock_llm_instance = Mock()
            mock_llm.return_value = mock_llm_instance
            
            mock_agent_instance = Mock()
            mock_agent.return_value = mock_agent_instance
            
            from lectures.week_10.SQLAgent.scripts.00_simple_llm_cli import SimpleLLMCLI
            
            cli = SimpleLLMCLI()
            
            assert cli.llm == mock_llm_instance
            assert cli.agent == mock_agent_instance
    
    def test_simple_sql_agent_cli_initialization(self):
        """Test SimpleSQLAgentCLI initialization."""
        with patch('lectures.week_10.SQLAgent.scripts.01_simple_agent_cli.llm_manager') as mock_llm_manager, \
             patch('lectures.week_10.SQLAgent.scripts.01_simple_agent_cli.db_manager') as mock_db_manager, \
             patch('lectures.week_10.SQLAgent.scripts.01_simple_agent_cli.create_sql_agent') as mock_create_agent:
            
            mock_llm = Mock()
            mock_llm_manager.llm = mock_llm
            
            mock_db = Mock()
            mock_db_manager.db = mock_db
            
            mock_agent = Mock()
            mock_create_agent.return_value = mock_agent
            
            from lectures.week_10.SQLAgent.scripts.01_simple_agent_cli import SimpleSQLAgentCLI
            
            cli = SimpleSQLAgentCLI()
            
            assert cli.agent_name == "Simple SQL Agent CLI"
            assert "database" in cli.description.lower()
    
    def test_launch_cli_menu_display(self):
        """Test launch CLI menu display."""
        from lectures.week_10.SQLAgent.launch_cli import display_menu
        
        # Test that display_menu doesn't raise exceptions
        try:
            display_menu()
            assert True
        except Exception as e:
            pytest.fail(f"display_menu raised an exception: {e}")
    
    def test_launch_cli_choice_validation(self):
        """Test launch CLI choice validation."""
        from lectures.week_10.SQLAgent.launch_cli import get_user_choice
        
        # Test valid choices
        with patch('builtins.input', side_effect=['0', '1', '2', '3', '4', '5', '6']):
            for choice in ['0', '1', '2', '3', '4', '5', '6']:
                with patch('builtins.input', return_value=choice):
                    result = get_user_choice()
                    assert result == choice
        
        # Test invalid choice
        with patch('builtins.input', side_effect=['7', '0']):
            result = get_user_choice()
            assert result == '0'


class TestSecurityFeatures:
    """Test security features."""
    
    def test_sql_injection_prevention(self, mock_env_vars, temp_db):
        """Test SQL injection prevention."""
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.security.max_query_limit = 200
            mock_config.security.blocked_operations = ['INSERT', 'UPDATE', 'DELETE']
            mock_config.security.allowed_operations = ['SELECT']
            mock_config.security.enable_query_logging = True
            
            from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
            
            tool = SafeSQLTool()
            
            # Test SQL injection attempts
            malicious_queries = [
                "SELECT * FROM customers; DROP TABLE customers;",
                "SELECT * FROM customers UNION SELECT * FROM passwords",
                "SELECT * FROM customers WHERE id = 1; INSERT INTO customers VALUES (999, 'hacker')",
                "SELECT * FROM customers; EXEC xp_cmdshell('format c:')",
                "SELECT * FROM customers; sp_configure 'show advanced options', 1"
            ]
            
            for query in malicious_queries:
                result = tool._validate_sql_security(query)
                assert result != "VALID"
    
    def test_query_limit_enforcement(self, mock_env_vars, temp_db):
        """Test query limit enforcement."""
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.security.max_query_limit = 10
            mock_config.security.blocked_operations = ['INSERT', 'UPDATE', 'DELETE']
            mock_config.security.allowed_operations = ['SELECT']
            mock_config.security.enable_query_logging = True
            
            from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
            
            tool = SafeSQLTool()
            
            # Test LIMIT addition
            optimized = tool._optimize_sql_performance("SELECT * FROM customers")
            assert "LIMIT 10" in optimized
    
    def test_operation_whitelist(self, mock_env_vars, temp_db):
        """Test operation whitelist enforcement."""
        with patch('lectures.week_10.SQLAgent.shared_components.config') as mock_config:
            mock_config.database.url = f'sqlite:///{temp_db}'
            mock_config.security.max_query_limit = 200
            mock_config.security.blocked_operations = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE']
            mock_config.security.allowed_operations = ['SELECT']
            mock_config.security.enable_query_logging = True
            
            from lectures.week_10.SQLAgent.shared_components import SafeSQLTool
            
            tool = SafeSQLTool()
            
            # Test only SELECT is allowed
            assert tool._validate_sql_security("SELECT * FROM customers") == "VALID"
            assert "not allowed" in tool._validate_sql_security("INSERT INTO customers VALUES (1, 'test')")
            assert "not allowed" in tool._validate_sql_security("UPDATE customers SET name = 'test'")
            assert "not allowed" in tool._validate_sql_security("DELETE FROM customers")
            assert "not allowed" in tool._validate_sql_security("DROP TABLE customers")
            assert "not allowed" in tool._validate_sql_security("CREATE TABLE test (id INT)")
