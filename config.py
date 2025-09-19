"""
Centralized Configuration Management

This module provides centralized configuration management for the SQL Agent project.
It handles environment variables, API keys, database settings, and other configuration
parameters in a secure and maintainable way.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    url: str
    include_tables: list[str]
    max_connections: int = 10
    connection_timeout: int = 30


@dataclass
class LLMConfig:
    """Language Model configuration settings."""
    model: str
    temperature: float
    max_tokens: Optional[int] = None
    timeout: int = 60


@dataclass
class SecurityConfig:
    """Security configuration settings."""
    max_query_limit: int = 200
    allowed_operations: list[str]
    blocked_operations: list[str]
    enable_query_logging: bool = True


@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    level: str
    format: str
    file_path: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


class Config:
    """
    Centralized configuration management class.
    
    This class provides a single source of truth for all configuration
    parameters used throughout the SQL Agent application.
    """
    
    def __init__(self):
        """Initialize configuration with default values and environment overrides."""
        self._setup_logging()
        self._validate_required_env_vars()
        
        # Database configuration
        self.database = DatabaseConfig(
            url=self._get_env_var("DATABASE_URL", "sqlite:///sql_agent_class.db"),
            include_tables=[
                "customers", "orders", "order_items", "products", 
                "refunds", "payments", "categories", "inventory_movements", 
                "customer_segments"
            ],
            max_connections=int(self._get_env_var("DB_MAX_CONNECTIONS", "10")),
            connection_timeout=int(self._get_env_var("DB_CONNECTION_TIMEOUT", "30"))
        )
        
        # LLM configuration
        self.llm = LLMConfig(
            model=self._get_env_var("LLM_MODEL", "gemini-1.5-flash"),
            temperature=float(self._get_env_var("LLM_TEMPERATURE", "0")),
            max_tokens=self._get_env_var("LLM_MAX_TOKENS", None),
            timeout=int(self._get_env_var("LLM_TIMEOUT", "60"))
        )
        
        # Security configuration
        self.security = SecurityConfig(
            max_query_limit=int(self._get_env_var("MAX_QUERY_LIMIT", "200")),
            allowed_operations=["SELECT"],
            blocked_operations=["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE", "REPLACE"],
            enable_query_logging=self._get_env_var("ENABLE_QUERY_LOGGING", "true").lower() == "true"
        )
        
        # Logging configuration
        self.logging = LoggingConfig(
            level=self._get_env_var("LOG_LEVEL", "INFO"),
            format=self._get_env_var("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            file_path=self._get_env_var("LOG_FILE", None),
            max_file_size=int(self._get_env_var("LOG_MAX_FILE_SIZE", str(10 * 1024 * 1024))),
            backup_count=int(self._get_env_var("LOG_BACKUP_COUNT", "5"))
        )
    
    def _get_env_var(self, key: str, default: Optional[str] = None) -> str:
        """
        Get environment variable with fallback to default value.
        
        Args:
            key: Environment variable name
            default: Default value if environment variable is not set
            
        Returns:
            Environment variable value or default
            
        Raises:
            ValueError: If required environment variable is missing
        """
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value
    
    def _validate_required_env_vars(self) -> None:
        """Validate that all required environment variables are set."""
        required_vars = ["GOOGLE_API_KEY"]
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        log_format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format=log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("sql_agent.log") if os.getenv("LOG_FILE") else logging.NullHandler()
            ]
        )
    
    def get_api_key(self, service: str) -> str:
        """
        Get API key for specified service.
        
        Args:
            service: Service name (e.g., 'google', 'openai')
            
        Returns:
            API key for the service
            
        Raises:
            ValueError: If API key is not found
        """
        key_mapping = {
            "google": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY"
        }
        
        env_var = key_mapping.get(service.lower())
        if not env_var:
            raise ValueError(f"Unknown service: {service}")
        
        api_key = os.getenv(env_var)
        if not api_key:
            raise ValueError(f"API key for {service} not found in environment variables")
        
        return api_key
    
    def get_database_path(self) -> Path:
        """
        Get the database file path.
        
        Returns:
            Path object for the database file
        """
        db_url = self.database.url
        if db_url.startswith("sqlite:///"):
            db_path = db_url.replace("sqlite:///", "")
            return Path(db_path)
        else:
            raise ValueError(f"Unsupported database URL format: {db_url}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of configuration
        """
        return {
            "database": {
                "url": self.database.url,
                "include_tables": self.database.include_tables,
                "max_connections": self.database.max_connections,
                "connection_timeout": self.database.connection_timeout
            },
            "llm": {
                "model": self.llm.model,
                "temperature": self.llm.temperature,
                "max_tokens": self.llm.max_tokens,
                "timeout": self.llm.timeout
            },
            "security": {
                "max_query_limit": self.security.max_query_limit,
                "allowed_operations": self.security.allowed_operations,
                "blocked_operations": self.security.blocked_operations,
                "enable_query_logging": self.security.enable_query_logging
            },
            "logging": {
                "level": self.logging.level,
                "format": self.logging.format,
                "file_path": self.logging.file_path,
                "max_file_size": self.logging.max_file_size,
                "backup_count": self.logging.backup_count
            }
        }


# Global configuration instance
config = Config()
