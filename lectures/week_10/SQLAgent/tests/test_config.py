"""
Test Configuration Module

This module contains tests for the configuration management system.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from config import Config, config


class TestConfig:
    """Test cases for the Config class."""
    
    def test_config_initialization(self):
        """Test that config initializes with default values."""
        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'}):
            test_config = Config()
            
            assert test_config.database.url == "sqlite:///sql_agent_class.db"
            assert test_config.llm.model == "gemini-1.5-flash"
            assert test_config.security.max_query_limit == 200
            assert test_config.logging.level == "INFO"
    
    def test_missing_required_env_var(self):
        """Test that missing required environment variables raise ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Required environment variable 'GOOGLE_API_KEY' is not set"):
                Config()
    
    def test_get_api_key(self):
        """Test API key retrieval."""
        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_google_key'}):
            test_config = Config()
            
            assert test_config.get_api_key('google') == 'test_google_key'
            
            with pytest.raises(ValueError, match="Unknown service: invalid"):
                test_config.get_api_key('invalid')
    
    def test_get_database_path(self):
        """Test database path extraction."""
        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'}):
            test_config = Config()
            
            db_path = test_config.get_database_path()
            assert str(db_path) == "sql_agent_class.db"
    
    def test_to_dict(self):
        """Test configuration to dictionary conversion."""
        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'}):
            test_config = Config()
            config_dict = test_config.to_dict()
            
            assert 'database' in config_dict
            assert 'llm' in config_dict
            assert 'security' in config_dict
            assert 'logging' in config_dict
            
            assert config_dict['database']['url'] == "sqlite:///sql_agent_class.db"
            assert config_dict['llm']['model'] == "gemini-1.5-flash"


class TestGlobalConfig:
    """Test cases for the global config instance."""
    
    def test_global_config_exists(self):
        """Test that global config instance exists."""
        assert config is not None
        assert isinstance(config, Config)
