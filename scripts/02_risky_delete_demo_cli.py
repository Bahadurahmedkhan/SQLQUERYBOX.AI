#!/usr/bin/env python3
"""
⚠️ DANGEROUS SQL Agent CLI Interface ⚠️

Interactive command-line interface for the DANGEROUS SQL agent demo.
This agent can execute ANY SQL including DELETE, DROP, etc.

⚠️ WARNING: This is for educational purposes only! ⚠️
NEVER use this pattern in production environments!

Usage:
    python 02_risky_delete_demo_cli.py
"""

# ⚠️ DEMO ONLY — allows arbitrary SQL including DELETE
import sqlalchemy  # SQL database engine and connection management
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini language model integration
from langchain.agents import initialize_agent, AgentType  # Agent creation and types
from langchain.tools import BaseTool  # Base class for creating custom tools
from pydantic import BaseModel, Field  # Data validation and serialization
from typing import Type  # Type hinting for better code documentation
from langchain.schema import SystemMessage  # System message formatting for agents
from dotenv import load_dotenv  # Environment variable loading

# Import Gemini configuration
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_config import *  # Load Gemini API key

# Load environment variables from .env file (including GOOGLE_API_KEY)
load_dotenv()

# Database Configuration
DB_URL = "sqlite:///sql_agent_class.db"

# Create Database Engine
engine = sqlalchemy.create_engine(DB_URL)

class SQLInput(BaseModel):
    """
    Pydantic model for SQL tool input validation.
    """
    sql: str = Field(description="Any SQL statement.")

class ExecuteAnySQLTool(BaseTool):
    """
    DANGEROUS Custom Tool - Executes ANY SQL Without Restrictions
    """
    name: str = "execute_any_sql"
    description: str = "Executes ANY SQL, including DML/DDL. DEMO ONLY."
    args_schema: Type[BaseModel] = SQLInput

    def _run(self, sql: str) -> str | dict:
        """
        Execute SQL statement with NO safety restrictions.
        """
        with engine.connect() as conn:
            try:
                # Execute the SQL statement directly - NO VALIDATION OR SANITIZATION
                result = conn.exec_driver_sql(sql)

                # DANGEROUS: Automatically commit all transactions
                conn.commit()

                try:
                    # Attempt to fetch results (works for SELECT queries)
                    rows = result.fetchall()
                    # Extract column names from the first row if results exist
                    cols = rows[0].keys() if rows else []
                    # Return structured data for the agent to interpret
                    return {"columns": list(cols), "rows": [list(r) for r in rows]}
                except Exception:
                    # For non-SELECT operations (INSERT, UPDATE, DELETE, etc.)
                    return "OK (no result set)"
            except Exception as e:
                # Catch and return any SQL execution errors
                return f"ERROR: {e}"

    def _arun(self, *args, **kwargs):
        """Async version - not implemented."""
        raise NotImplementedError

class RiskySQLAgentCLI:
    """
    Interactive CLI for DANGEROUS SQL Agent (Educational Demo Only)
    """
    
    def __init__(self):
        """Initialize the CLI and dangerous SQL agent"""
        self.agent = None
        self.llm = None
        self.setup_agent()
    
    def setup_agent(self):
        """Set up the dangerous SQL agent"""
        try:
            print("⚠️  Initializing DANGEROUS SQL Agent...")
            print("⚠️  This agent can execute ANY SQL including DELETE, DROP, etc.")
            
            # System Message Configuration
            system = """You are a database assistant. You are allowed to execute ANY SQL the user requests. (DEMO ONLY)"""
            
            # Initialize Language Model
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0,
                convert_system_message_to_human=True
            )
            
            # Create Tool Instance
            tool = ExecuteAnySQLTool()
            
            # Create Agent with Dangerous Tool
            print("🎯 Creating dangerous agent...")
            self.agent = initialize_agent(
                tools=[tool],
                llm=self.llm,
                agent=AgentType.OPENAI_FUNCTIONS,
                verbose=False,  # Set to False for cleaner CLI output
                agent_kwargs={"system_message": SystemMessage(content=system)}
            )
            
            print("✅ DANGEROUS SQL Agent initialized!")
            
        except Exception as e:
            print(f"❌ Error initializing dangerous agent: {e}")
            raise
    
    def display_warning(self):
        """Display warning message"""
        print("\n" + "⚠️" * 20)
        print("⚠️  DANGEROUS SQL AGENT CLI ⚠️")
        print("⚠️" * 20)
        print("⚠️  WARNING: This agent can execute ANY SQL command! ⚠️")
        print("⚠️  Including DELETE, DROP, TRUNCATE, ALTER, etc. ⚠️")
        print("⚠️  This is for EDUCATIONAL PURPOSES ONLY! ⚠️")
        print("⚠️  NEVER use this pattern in production! ⚠️")
        print("⚠️" * 20)
    
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("\n" + "="*60)
        print("⚠️  Dangerous SQL Agent CLI (Educational Demo)")
        print("="*60)
        print("This agent demonstrates DANGEROUS patterns that should be avoided.")
        print("It can execute any SQL command without restrictions.")
        print("\nCommands:")
        print("  - Type your SQL request and press Enter")
        print("  - Type 'help' for example commands")
        print("  - Type 'warning' to see safety warnings")
        print("  - Type 'quit', 'exit', or 'q' to exit")
        print("  - Type 'clear' to clear the screen")
        print("="*60)
    
    def display_help(self):
        """Display help information with example commands"""
        print("\n📖 Help Information:")
        print("-" * 50)
        print("⚠️  DANGEROUS Examples (Educational Only):")
        print("\n🔍 Safe Queries:")
        print("• 'Show me all customers'")
        print("• 'What products do we have?'")
        print("• 'How many orders are there?'")
        
        print("\n⚠️  DANGEROUS Queries (Will Actually Execute!):")
        print("• 'Delete all customers'")
        print("• 'Drop the products table'")
        print("• 'Update all orders to status cancelled'")
        print("• 'Insert a test customer'")
        
        print("\n⚠️  WARNING: These commands will actually modify your database!")
        print("Make sure you have a backup before experimenting!")
        print("-" * 50)
    
    def display_warning_details(self):
        """Display detailed warning information"""
        print("\n⚠️  SECURITY WARNINGS:")
        print("-" * 50)
        print("This agent demonstrates what NOT to do in production:")
        print("• No input validation or sanitization")
        print("• Allows DELETE, DROP, TRUNCATE, ALTER operations")
        print("• No user permissions or access controls")
        print("• Direct SQL execution without safety checks")
        print("• Automatic transaction commits")
        print("\n✅ Proper security measures include:")
        print("• Input validation using regex patterns")
        print("• Whitelist approach (only SELECT statements)")
        print("• Automatic LIMIT injection")
        print("• SQL injection protection")
        print("• Multiple statement prevention")
        print("• Read-only database users")
        print("-" * 50)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_user_input(self):
        """Get user input with prompt"""
        try:
            return input("\n⚠️  Enter SQL command: ").strip()
        except KeyboardInterrupt:
            return "quit"
        except EOFError:
            return "quit"
    
    def process_query(self, query):
        """Process user query and return agent response"""
        try:
            print("\n🤖 Dangerous Agent: ", end="", flush=True)
            
            # Get agent response
            response = self.agent.invoke({"input": query})
            
            # Display response
            print(response['output'])
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            print("Please try again with a different command.")
    
    def run(self):
        """Main CLI loop"""
        self.display_warning()
        self.display_welcome()
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Remember: This was for educational purposes only!")
                    break
                
                elif user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                elif user_input.lower() == 'warning':
                    self.display_warning_details()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.clear_screen()
                    self.display_warning()
                    self.display_welcome()
                    continue
                
                elif not user_input:
                    print("Please enter a SQL command.")
                    continue
                
                # Process the query
                self.process_query(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Remember: This was for educational purposes only!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Please try again.")

def main():
    """Main function to run the CLI"""
    try:
        cli = RiskySQLAgentCLI()
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
