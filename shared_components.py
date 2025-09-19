"""
Shared Components Module

This module contains shared components and utilities used across the SQL Agent project.
It eliminates code duplication and provides consistent functionality.
"""

import re
import logging
import sqlalchemy
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain.schema import SystemMessage

from config import config

logger = logging.getLogger(__name__)


class QueryInput(BaseModel):
    """
    Pydantic model for SQL query input validation.
    
    This model ensures that all SQL queries are properly validated
    before execution.
    """
    sql: str = Field(
        description="A single read-only SELECT statement, bounded with LIMIT when returning many rows.",
        min_length=1,
        max_length=10000
    )


class SafeSQLTool(BaseTool):
    """
    Secure SQL Tool - Only Allows Read-Only SELECT Operations
    
    This tool provides secure SQL execution with comprehensive validation
    and safety guardrails. It's designed to prevent SQL injection attacks
    and unauthorized data modifications.
    """
    
    name: str = "execute_sql"
    description: str = "Execute exactly one SELECT statement; DML/DDL is forbidden."
    args_schema: type[BaseModel] = QueryInput

    def __init__(self, **kwargs):
        """Initialize the SafeSQLTool with configuration."""
        super().__init__(**kwargs)
        self.engine = sqlalchemy.create_engine(config.database.url)
        self.max_limit = config.security.max_query_limit
        self.blocked_operations = config.security.blocked_operations
        self.allowed_operations = config.security.allowed_operations

    def _run(self, sql: str) -> Union[str, Dict[str, Any]]:
        """
        Execute SQL with comprehensive security validation.
        
        Args:
            sql: SQL query to execute
            
        Returns:
            Query results or error message
        """
        try:
            # Log the query if logging is enabled
            if config.security.enable_query_logging:
                logger.info(f"Executing SQL query: {sql[:100]}...")
            
            # Step 1: Clean and Normalize Input
            cleaned_sql = self._clean_sql_input(sql)
            
            # Step 2: Security Validation
            validation_result = self._validate_sql_security(cleaned_sql)
            if validation_result != "VALID":
                logger.warning(f"SQL validation failed: {validation_result}")
                return f"ERROR: {validation_result}"
            
            # Step 3: Performance Optimization
            optimized_sql = self._optimize_sql_performance(cleaned_sql)
            
            # Step 4: Safe SQL Execution
            return self._execute_sql_safely(optimized_sql)
            
        except Exception as e:
            error_msg = f"SQL execution error: {str(e)}"
            logger.error(error_msg)
            return f"ERROR: {error_msg}"

    def _clean_sql_input(self, sql: str) -> str:
        """
        Clean and normalize SQL input.
        
        Args:
            sql: Raw SQL input
            
        Returns:
            Cleaned SQL string
        """
        return sql.strip().rstrip(";")

    def _validate_sql_security(self, sql: str) -> str:
        """
        Validate SQL for security compliance.
        
        Args:
            sql: SQL query to validate
            
        Returns:
            "VALID" if query is safe, error message otherwise
        """
        # Check for blocked operations
        for operation in self.blocked_operations:
            if re.search(rf"\b{operation}\b", sql, re.IGNORECASE):
                return f"write operations are not allowed (blocked: {operation})"
        
        # Check for multiple statements
        if ";" in sql:
            return "multiple statements are not allowed"
        
        # Check for allowed operations (whitelist approach)
        if not re.match(r"(?is)^\s*select\b", sql):
            return "only SELECT statements are allowed"
        
        # Check for potentially dangerous patterns
        dangerous_patterns = [
            r"\bunion\b.*\bselect\b",  # UNION-based attacks
            r"\bexec\b",               # EXEC statements
            r"\bsp_\w+",              # Stored procedures
            r"\bxp_\w+",              # Extended procedures
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, sql, re.IGNORECASE):
                return f"potentially dangerous pattern detected: {pattern}"
        
        return "VALID"

    def _optimize_sql_performance(self, sql: str) -> str:
        """
        Optimize SQL for performance by adding LIMIT if needed.
        
        Args:
            sql: SQL query to optimize
            
        Returns:
            Optimized SQL query
        """
        # Check if LIMIT is already present
        if re.search(r"\blimit\s+\d+\b", sql, re.IGNORECASE):
            return sql
        
        # Check if it's an aggregation query (doesn't need LIMIT)
        aggregation_patterns = [
            r"\bcount\(",
            r"\bgroup\s+by\b",
            r"\bsum\(",
            r"\bavg\(",
            r"\bmax\(",
            r"\bmin\(",
            r"\bdistinct\b"
        ]
        
        for pattern in aggregation_patterns:
            if re.search(pattern, sql, re.IGNORECASE):
                return sql
        
        # Add LIMIT for performance
        return f"{sql} LIMIT {self.max_limit}"

    def _execute_sql_safely(self, sql: str) -> Dict[str, Any]:
        """
        Execute SQL query safely with proper error handling.
        
        Args:
            sql: SQL query to execute
            
        Returns:
            Query results as dictionary
        """
        try:
            with self.engine.connect() as conn:
                result = conn.exec_driver_sql(sql)
                rows = result.fetchall()
                columns = list(result.keys()) if result.keys() else []
                
                return {
                    "columns": columns,
                    "rows": [list(row) for row in rows],
                    "row_count": len(rows)
                }
        except Exception as e:
            raise Exception(f"Database execution error: {str(e)}")

    def _arun(self, *args, **kwargs):
        """Async version - not implemented."""
        raise NotImplementedError("Async execution not implemented")


class DatabaseManager:
    """
    Database connection and management utility.
    
    This class provides centralized database management with proper
    connection pooling and resource cleanup.
    """
    
    def __init__(self):
        """Initialize database manager."""
        self.engine = sqlalchemy.create_engine(
            config.database.url,
            pool_size=config.database.max_connections,
            pool_timeout=config.database.connection_timeout,
            pool_recycle=3600  # Recycle connections every hour
        )
        self._db_instance = None

    @property
    def db(self) -> SQLDatabase:
        """
        Get SQLDatabase instance with lazy initialization.
        
        Returns:
            SQLDatabase instance
        """
        if self._db_instance is None:
            self._db_instance = SQLDatabase.from_uri(
                config.database.url,
                include_tables=config.database.include_tables
            )
        return self._db_instance

    def get_schema_info(self) -> str:
        """
        Get database schema information.
        
        Returns:
            Formatted schema information
        """
        try:
            return self.db.get_table_info()
        except Exception as e:
            logger.error(f"Error getting schema info: {e}")
            return "Error retrieving schema information"

    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

    def close(self):
        """Close database connections."""
        if self.engine:
            self.engine.dispose()
        logger.info("Database connections closed")


class LLMManager:
    """
    Language Model management utility.
    
    This class provides centralized LLM management with proper
    configuration and error handling.
    """
    
    def __init__(self):
        """Initialize LLM manager."""
        self._llm_instance = None

    @property
    def llm(self) -> ChatGoogleGenerativeAI:
        """
        Get LLM instance with lazy initialization.
        
        Returns:
            ChatGoogleGenerativeAI instance
        """
        if self._llm_instance is None:
            try:
                self._llm_instance = ChatGoogleGenerativeAI(
                    model=config.llm.model,
                    temperature=config.llm.temperature,
                    convert_system_message_to_human=True
                )
                logger.info(f"LLM initialized with model: {config.llm.model}")
            except Exception as e:
                logger.error(f"Failed to initialize LLM: {e}")
                raise
        return self._llm_instance

    def create_system_message(self, content: str) -> SystemMessage:
        """
        Create system message for the agent.
        
        Args:
            content: System message content
            
        Returns:
            SystemMessage instance
        """
        return SystemMessage(content=content)


class ErrorHandler:
    """
    Centralized error handling utility.
    
    This class provides consistent error handling patterns
    across the application.
    """
    
    @staticmethod
    def handle_database_error(error: Exception) -> str:
        """
        Handle database-related errors.
        
        Args:
            error: Database error
            
        Returns:
            User-friendly error message
        """
        error_msg = str(error).lower()
        
        if "no such table" in error_msg:
            return "The requested table does not exist in the database."
        elif "no such column" in error_msg:
            return "The requested column does not exist in the table."
        elif "syntax error" in error_msg:
            return "There is a syntax error in the SQL query."
        elif "database is locked" in error_msg:
            return "The database is currently locked. Please try again later."
        else:
            return f"Database error: {str(error)}"

    @staticmethod
    def handle_llm_error(error: Exception) -> str:
        """
        Handle LLM-related errors.
        
        Args:
            error: LLM error
            
        Returns:
            User-friendly error message
        """
        error_msg = str(error).lower()
        
        if "api key" in error_msg:
            return "API key is invalid or missing. Please check your configuration."
        elif "rate limit" in error_msg:
            return "API rate limit exceeded. Please try again later."
        elif "timeout" in error_msg:
            return "Request timed out. Please try again."
        else:
            return f"LLM error: {str(error)}"

    @staticmethod
    def handle_general_error(error: Exception) -> str:
        """
        Handle general errors.
        
        Args:
            error: General error
            
        Returns:
            User-friendly error message
        """
        return f"An unexpected error occurred: {str(error)}"


# Global instances
db_manager = DatabaseManager()
llm_manager = LLMManager()
error_handler = ErrorHandler()
