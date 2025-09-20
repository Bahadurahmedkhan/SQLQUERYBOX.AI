"""
Base CLI Class

This module provides a base CLI class that implements common CLI functionality
and ensures consistent behavior across all CLI interfaces.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from langchain.agents import AgentExecutor

from config import config
from shared_components import db_manager, llm_manager, error_handler

logger = logging.getLogger(__name__)


class BaseCLI(ABC):
    """
    Base CLI class providing common functionality for all CLI interfaces.
    
    This abstract base class implements common CLI patterns and provides
    a consistent interface for all CLI implementations.
    """
    
    def __init__(self, agent_name: str, description: str):
        """
        Initialize the base CLI.
        
        Args:
            agent_name: Name of the agent for display purposes
            description: Description of the agent's capabilities
        """
        self.agent_name = agent_name
        self.description = description
        self.agent: Optional[AgentExecutor] = None
        self.is_initialized = False
        
        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.{agent_name}")
        
    @abstractmethod
    def setup_agent(self) -> None:
        """
        Setup the specific agent implementation.
        
        This method must be implemented by subclasses to create
        their specific agent configuration.
        """
        pass
    
    @abstractmethod
    def get_help_examples(self) -> List[str]:
        """
        Get help examples specific to the agent.
        
        Returns:
            List of example questions for the agent
        """
        pass
    
    def initialize(self) -> bool:
        """
        Initialize the CLI and agent.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info(f"Initializing {self.agent_name}...")
            self.setup_agent()
            self.is_initialized = True
            self.logger.info(f"{self.agent_name} initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.agent_name}: {e}")
            return False
    
    def display_welcome(self) -> None:
        """Display welcome message and instructions."""
        print("\n" + "="*60)
        print(f"🤖 {self.agent_name}")
        print("="*60)
        print(self.description)
        print("\nCommands:")
        print("  - Type your question and press Enter")
        print("  - Type 'help' for example questions")
        print("  - Type 'schema' to see database structure")
        print("  - Type 'quit', 'exit', or 'q' to exit")
        print("  - Type 'clear' to clear the screen")
        print("="*60)
    
    def display_help(self) -> None:
        """Display help information with example questions."""
        print("\n📖 Help Information:")
        print("-" * 50)
        print("Example questions you can ask:")
        
        examples = self.get_help_examples()
        for example in examples:
            print(f"• '{example}'")
        
        print("-" * 50)
    
    def display_schema(self) -> None:
        """Display database schema information."""
        try:
            print("\n🏗️  Database Schema:")
            print("-" * 50)
            
            schema_info = db_manager.get_schema_info()
            print("Available tables and their structure:")
            print(schema_info)
            
            print("\n📋 Quick Table Overview:")
            for table in config.database.include_tables:
                print(f"• {table} - {self._get_table_description(table)}")
            
            print("-" * 50)
            
        except Exception as e:
            error_msg = error_handler.handle_database_error(e)
            print(f"❌ Error displaying schema: {error_msg}")
    
    def _get_table_description(self, table: str) -> str:
        """
        Get description for a table.
        
        Args:
            table: Table name
            
        Returns:
            Table description
        """
        descriptions = {
            "customers": "Customer information (id, name, email, region, etc.)",
            "products": "Product catalog (id, name, category, price, etc.)",
            "orders": "Order records (id, customer_id, order_date, status, etc.)",
            "order_items": "Order line items (id, order_id, product_id, quantity, etc.)",
            "payments": "Payment information (id, order_id, amount, method, etc.)",
            "refunds": "Refund records (id, order_id, amount, reason, etc.)",
            "categories": "Product categories (id, name, description, etc.)",
            "inventory_movements": "Stock tracking (id, product_id, movement_type, etc.)",
            "customer_segments": "Customer segmentation (id, name, criteria, etc.)"
        }
        return descriptions.get(table, "Table description not available")
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_user_input(self) -> str:
        """
        Get user input with prompt.
        
        Returns:
            User input string
        """
        try:
            return input(f"\n💬 Ask about your database: ").strip()
        except KeyboardInterrupt:
            return "quit"
        except EOFError:
            return "quit"
    
    def process_query(self, query: str) -> None:
        """
        Process user query and return agent response.
        
        Args:
            query: User's question
        """
        if not self.is_initialized:
            print("❌ Agent not initialized. Please restart the application.")
            return
        
        try:
            print(f"\n🤖 {self.agent_name}: ", end="", flush=True)
            
            # Get agent response
            response = self.agent.invoke({"input": query})
            
            # Display response
            print(response['output'])
            
            # Log the interaction
            self.logger.info(f"Query processed successfully: {query[:50]}...")
            
        except Exception as e:
            error_msg = error_handler.handle_general_error(e)
            print(f"❌ Error processing query: {error_msg}")
            print("Please try again with a different question.")
            self.logger.error(f"Query processing failed: {e}")
    
    def handle_special_commands(self, user_input: str) -> bool:
        """
        Handle special CLI commands.
        
        Args:
            user_input: User input string
            
        Returns:
            True if command was handled, False if input should be processed as query
        """
        user_input_lower = user_input.lower()
        
        if user_input_lower in ['quit', 'exit', 'q']:
            print(f"\n👋 Goodbye! Thanks for using the {self.agent_name}!")
            return True
        
        elif user_input_lower == 'help':
            self.display_help()
            return True
        
        elif user_input_lower == 'schema':
            self.display_schema()
            return True
        
        elif user_input_lower == 'clear':
            self.clear_screen()
            self.display_welcome()
            return True
        
        elif not user_input:
            print("Please enter a question about your database.")
            return True
        
        return False
    
    def run(self) -> None:
        """Main CLI loop."""
        if not self.initialize():
            print(f"❌ Failed to initialize {self.agent_name}")
            return
        
        self.display_welcome()
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                # Handle special commands
                if self.handle_special_commands(user_input):
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break
                    continue
                
                # Process the query
                self.process_query(user_input)
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Goodbye! Thanks for using the {self.agent_name}!")
                break
            except Exception as e:
                error_msg = error_handler.handle_general_error(e)
                print(f"\n❌ Unexpected error: {error_msg}")
                print("Please try again.")
                self.logger.error(f"Unexpected error in CLI loop: {e}")
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        try:
            db_manager.close()
            self.logger.info("CLI cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
