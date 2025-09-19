#!/usr/bin/env python3
"""
Simple SQL Agent CLI Interface

Interactive command-line interface for the simple SQL agent.
Users can ask natural language questions about the database and get SQL-generated responses.

Usage:
    python 01_simple_agent_cli.py
"""

import sys
import os
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our improved modules
from base_cli import BaseCLI
from shared_components import db_manager, llm_manager
from config import config

# Import necessary LangChain components for SQL agent functionality
from langchain.agents.agent_toolkits import SQLDatabaseToolkit, create_sql_agent

class SimpleSQLAgentCLI(BaseCLI):
    """
    Interactive CLI for Simple SQL Agent
    
    This agent provides basic SQL querying capabilities with unrestricted access.
    It's designed for educational purposes to understand agent concepts.
    """
    
    def __init__(self):
        """Initialize the Simple SQL Agent CLI"""
        super().__init__(
            agent_name="Simple SQL Agent CLI",
            description="This agent can answer questions about your database using natural language! Ask questions about customers, products, orders, and more."
        )
    
    def setup_agent(self) -> None:
        """Set up the Gemini-powered SQL agent"""
        try:
            print("🤖 Initializing Gemini language model...")
            
            # Get LLM instance from manager
            llm = llm_manager.llm
            
            print("🗄️  Connecting to database...")
            
            # Get database instance from manager
            db = db_manager.db
            
            print("🎯 Creating SQL agent...")
            
            # Create SQL Agent
            self.agent = create_sql_agent(
                llm=llm,
                toolkit=SQLDatabaseToolkit(db=db, llm=llm),
                agent_type="openai-tools",
                verbose=False  # Set to False for cleaner CLI output
            )
            
            print("✅ SQL Agent initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing SQL agent: {e}")
            raise
    
    def get_help_examples(self) -> List[str]:
        """Get help examples specific to the simple agent"""
        return [
            "How many customers do we have?",
            "Show me customers from North America",
            "Who are our top customers by revenue?",
            "What products do we sell?",
            "Which product category is most popular?",
            "Show me products under $50",
            "How many orders were placed this month?",
            "What's our total revenue?",
            "Show me recent orders",
            "What's our average order value?",
            "Which region has the most customers?",
            "Show me monthly sales trends"
        ]

def main():
    """Main function to run the CLI"""
    try:
        with SimpleSQLAgentCLI() as cli:
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
