#!/usr/bin/env python3
"""
Safe SQL Agent CLI Interface

Interactive command-line interface for the secure SQL agent with comprehensive safety guardrails.
This agent only allows read-only SELECT operations with multiple security layers.

Usage:
    python 03_guardrailed_agent_cli.py
"""

import sys
import os
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our improved modules
from base_cli import BaseCLI
from shared_components import SafeSQLTool, db_manager, llm_manager
from config import config

# Import necessary LangChain components
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage

class SafeSQLAgentCLI(BaseCLI):
    """
    Interactive CLI for Secure SQL Agent
    
    This agent provides secure SQL querying capabilities with comprehensive
    safety guardrails and read-only access.
    """
    
    def __init__(self):
        """Initialize the Secure SQL Agent CLI"""
        super().__init__(
            agent_name="Safe SQL Agent CLI",
            description="This agent has comprehensive security guardrails: ✅ Only SELECT statements allowed ✅ Automatic LIMIT injection ✅ SQL injection protection ✅ Multiple statement prevention ✅ Read-only operations only"
        )
    
    def setup_agent(self) -> None:
        """Set up the secure SQL agent"""
        try:
            print("🛡️  Initializing Secure SQL Agent...")
            print("🛡️  This agent has comprehensive safety guardrails.")
            
            # Get database and LLM instances from managers
            db = db_manager.db
            llm = llm_manager.llm
            
            # Extract Database Schema Information
            schema_context = db.get_table_info()
            
            # System Message Configuration
            system = f"You are a careful analytics engineer for SQLite. Use only these tables.\n\n{schema_context}"
            
            # Create Safe Tool Instance
            safe_tool = SafeSQLTool()
            
            # Create Secure Agent
            print("🎯 Creating secure agent with safety guardrails...")
            self.agent = initialize_agent(
                tools=[safe_tool],
                llm=llm,
                agent=AgentType.OPENAI_FUNCTIONS,
                verbose=False,  # Set to False for cleaner CLI output
                agent_kwargs={"system_message": SystemMessage(content=system)}
            )
            
            print("✅ Secure SQL Agent initialized!")
            
        except Exception as e:
            print(f"❌ Error initializing secure agent: {e}")
            raise
    
    def get_help_examples(self) -> List[str]:
        """Get help examples specific to the secure agent"""
        return [
            "How many customers do we have?",
            "Show me customers by region",
            "Who are our top 10 customers by revenue?",
            "What's the average customer lifetime value?",
            "What products do we sell?",
            "Which product category generates the most revenue?",
            "Show me products with low stock",
            "What's our best-selling product?",
            "How many orders were placed this month?",
            "What's our total revenue?",
            "Show me order trends by month",
            "What's the average order value?",
            "Show me revenue by region",
            "What's our monthly growth rate?",
            "Which customers have the highest order frequency?",
            "Show me product performance rankings"
        ]
    
    def handle_special_commands(self, user_input: str) -> bool:
        """
        Handle special CLI commands including security features.
        
        Args:
            user_input: User input string
            
        Returns:
            True if command was handled, False if input should be processed as query
        """
        user_input_lower = user_input.lower()
        
        if user_input_lower == 'security':
            self.display_security_features()
            return True
        
        # Call parent class method for other commands
        return super().handle_special_commands(user_input)
    
    def display_security_features(self):
        """Display security features information"""
        print("\n🛡️  Security Features:")
        print("-" * 50)
        print("This agent implements multiple layers of security:")
        print("\n✅ Input Validation:")
        print("• Regex pattern matching for dangerous operations")
        print("• Whitelist approach (only SELECT allowed)")
        print("• Multiple statement prevention")
        
        print("\n✅ Performance Protection:")
        print(f"• Automatic LIMIT injection (max {config.security.max_query_limit} rows)")
        print("• Result set size control")
        print("• Resource exhaustion prevention")
        
        print("\n✅ SQL Injection Protection:")
        print("• Pattern-based validation")
        print("• Statement chaining prevention")
        print("• Comprehensive error handling")
        
        print("\n✅ Access Control:")
        print("• Read-only operations only")
        print("• No data modification possible")
        print("• Schema-based restrictions")
        
        print("\n🚫 Blocked Operations:")
        for operation in config.security.blocked_operations:
            print(f"• {operation}")
        print("• Multiple statements (;)")
        print("-" * 50)

def main():
    """Main function to run the CLI"""
    try:
        with SafeSQLAgentCLI() as cli:
            cli.run()
    except Exception as e:
        print(f"❌ Failed to start CLI: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure your .env file contains GOOGLE_API_KEY")
        print("2. Verify your virtual environment is activated")
        print("3. Check that you've installed requirements: pip install -r requirements.txt")
        print("4. Ensure the database file 'sql_agent_class.db' exists")
        print("5. Ensure you have internet connection for API calls")

if __name__ == "__main__":
    main()
