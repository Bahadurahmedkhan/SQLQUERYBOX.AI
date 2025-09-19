#!/usr/bin/env python3
"""
Advanced Analytics SQL Agent CLI Interface

Interactive command-line interface for the advanced analytics SQL agent.
This agent provides sophisticated business intelligence capabilities with complex queries.

Usage:
    python 04_complex_queries_cli.py
"""

# Load environment variables first (including GOOGLE_API_KEY)
from dotenv import load_dotenv; load_dotenv()

# Import Gemini configuration
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_config import *  # Load Gemini API key

# Core LangChain imports for agent functionality
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini language model integration
from langchain.agents import initialize_agent, AgentType  # Agent creation and configuration
from langchain.schema import SystemMessage  # System message formatting for agents
from langchain_community.utilities import SQLDatabase  # Database schema inspection utilities

# Data validation and tool creation imports
from pydantic import BaseModel, Field  # Data validation and serialization
from langchain.tools import BaseTool  # Base class for creating custom tools
from typing import Type  # Type hinting for better code documentation

# Database and utility imports
import sqlalchemy  # Database engine and connection management
import re  # Regular expressions for SQL pattern matching and validation

# Database Configuration
DB_URL = "sqlite:///sql_agent_class.db"

# Create Database Engine
engine = sqlalchemy.create_engine(DB_URL)

class QueryInput(BaseModel):
    """
    Pydantic model for analytics query input validation.
    """
    sql: str = Field(description="A single read-only SELECT statement, bounded with LIMIT when returning many rows.")

class SafeSQLTool(BaseTool):
    """
    Advanced Analytics SQL Tool - Secure Complex Query Execution
    """
    name: str = "execute_sql"
    description: str = "Execute one read-only SELECT."
    args_schema: Type[BaseModel] = QueryInput

    def _run(self, sql: str) -> str | dict:
        """
        Execute complex analytics SQL with comprehensive security validation.
        """
        # Step 1: Input Normalization
        s = sql.strip().rstrip(";")

        # Step 2: Security Validation Layer
        if re.search(r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|REPLACE)\b", s, re.I):
            return "ERROR: write operations are not allowed."

        if ";" in s:
            return "ERROR: multiple statements are not allowed."

        if not re.match(r"(?is)^\s*select\b", s):
            return "ERROR: only SELECT statements are allowed."

        # Step 3: Performance Optimization
        if not re.search(r"\blimit\s+\d+\b", s, re.I) and not re.search(r"\bcount\(|\bgroup\s+by\b|\bsum\(|\bavg\(|\bmax\(|\bmin\(", s, re.I):
            s += " LIMIT 200"  # Conservative limit for analytics queries

        # Step 4: Secure Query Execution
        try:
            with engine.connect() as conn:
                result = conn.exec_driver_sql(s)
                rows = result.fetchall()
                cols = list(result.keys()) if result.keys() else []
                return {"columns": cols, "rows": [list(r) for r in rows]}

        except Exception as e:
            return f"ERROR: {e}"

    def _arun(self, *args, **kwargs):
        """Async version - not implemented."""
        raise NotImplementedError

class AdvancedAnalyticsCLI:
    """
    Interactive CLI for Advanced Analytics SQL Agent
    """
    
    def __init__(self):
        """Initialize the CLI and advanced analytics agent"""
        self.agent = None
        self.llm = None
        self.db = None
        self.setup_agent()
    
    def setup_agent(self):
        """Set up the advanced analytics agent"""
        try:
            print("📊 Initializing Advanced Analytics SQL Agent...")
            print("📊 This agent provides sophisticated business intelligence capabilities.")
            
            # Advanced Database Schema Configuration
            self.db = SQLDatabase.from_uri(DB_URL, include_tables=["customers","orders","order_items","products","refunds","payments","categories","inventory_movements","customer_segments"])
            
            # Extract Comprehensive Schema Information
            schema_context = self.db.get_table_info()
            
            # Advanced System Message with Business Logic
            system = f"""You are a careful analytics engineer for SQLite.
            Use only listed tables. Revenue = sum(quantity*unit_price_cents) - refunds.amount_cents.
            \n\nSchema:\n{schema_context}"""
            
            # Initialize Advanced Language Model
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0,
                convert_system_message_to_human=True
            )
            
            # Create Analytics Tool Instance
            tool = SafeSQLTool()
            
            # Create Advanced Analytics Agent
            print("🎯 Creating advanced analytics agent...")
            self.agent = initialize_agent(
                tools=[tool],
                llm=self.llm,
                agent=AgentType.OPENAI_FUNCTIONS,
                verbose=False,  # Set to False for cleaner CLI output
                agent_kwargs={"system_message": SystemMessage(content=system)}
            )
            
            print("✅ Advanced Analytics Agent initialized!")
            
        except Exception as e:
            print(f"❌ Error initializing analytics agent: {e}")
            raise
    
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("\n" + "="*60)
        print("📊 Advanced Analytics SQL Agent CLI")
        print("="*60)
        print("This agent provides sophisticated business intelligence capabilities:")
        print("📈 Complex multi-table JOINs and aggregations")
        print("📊 Revenue analysis and customer lifetime value")
        print("📅 Time-series analysis and trend identification")
        print("👥 Customer segmentation and performance rankings")
        print("🔄 Multi-turn conversations for iterative analysis")
        print("\nCommands:")
        print("  - Type your analytics question and press Enter")
        print("  - Type 'help' for example analytics queries")
        print("  - Type 'schema' to see database structure")
        print("  - Type 'examples' for complex query examples")
        print("  - Type 'quit', 'exit', or 'q' to exit")
        print("  - Type 'clear' to clear the screen")
        print("="*60)
    
    def display_help(self):
        """Display help information with example analytics queries"""
        print("\n📖 Analytics Help Information:")
        print("-" * 50)
        print("Example analytics questions you can ask:")
        print("\n💰 Revenue Analytics:")
        print("• 'What's our total revenue by month?'")
        print("• 'Show me revenue trends for the last 6 months'")
        print("• 'Which products generate the most revenue?'")
        print("• 'What's our net revenue after refunds?'")
        
        print("\n👥 Customer Analytics:")
        print("• 'Who are our top customers by lifetime value?'")
        print("• 'Show me customer acquisition trends'")
        print("• 'What's the average customer lifetime value?'")
        print("• 'Which regions have the highest customer value?'")
        
        print("\n📦 Order Analytics:")
        print("• 'What's our average order value by customer segment?'")
        print("• 'Show me order frequency analysis'")
        print("• 'Which days of the week have the most orders?'")
        print("• 'What's our order completion rate?'")
        
        print("\n🛍️  Product Analytics:")
        print("• 'Which product categories perform best?'")
        print("• 'Show me product performance rankings'")
        print("• 'What's our inventory turnover rate?'")
        print("• 'Which products have the highest margins?'")
        
        print("\n📊 Business Intelligence:")
        print("• 'Show me a comprehensive business dashboard'")
        print("• 'What are our key performance indicators?'")
        print("• 'Identify trends and patterns in our data'")
        print("• 'Compare performance across different segments'")
        print("-" * 50)
    
    def display_schema(self):
        """Display database schema information"""
        try:
            print("\n🏗️  Database Schema:")
            print("-" * 50)
            
            # Get table information
            schema_info = self.db.get_table_info()
            print("Available tables and their structure:")
            print(schema_info)
            
            print("\n📋 Business Logic:")
            print("• Revenue = sum(quantity * unit_price_cents) - refunds.amount_cents")
            print("• Customer Lifetime Value = Total revenue per customer minus refunds")
            print("• Net Revenue = Gross revenue minus refunds")
            print("• Order Value = sum(order_items.total_price_cents)")
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Error displaying schema: {e}")
    
    def display_examples(self):
        """Display complex query examples"""
        print("\n📊 Complex Analytics Examples:")
        print("-" * 50)
        print("Here are some sophisticated analytics queries you can try:")
        
        print("\n💰 Revenue Analysis:")
        print("• 'Top 5 products by gross revenue (before refunds)'")
        print("• 'Weekly net revenue for the last 6 weeks'")
        print("• 'Revenue by product category with growth rates'")
        
        print("\n👥 Customer Lifecycle:")
        print("• 'Customer lifetime value ranking with segmentation'")
        print("• 'First-time vs repeat customer analysis'")
        print("• 'Customer acquisition cost by channel'")
        
        print("\n📈 Time Series Analysis:")
        print("• 'Monthly revenue trends with year-over-year comparison'")
        print("• 'Seasonal patterns in product sales'")
        print("• 'Customer retention rates by cohort'")
        
        print("\n🔄 Multi-Turn Analysis:")
        print("• Start with: 'What categories drive the most revenue?'")
        print("• Follow up: 'Break down the top category by product'")
        print("• Then ask: 'Show me the performance of the top product over time'")
        
        print("\n📊 Advanced Business Intelligence:")
        print("• 'Comprehensive business performance dashboard'")
        print("• 'Identify top-performing customer segments'")
        print("• 'Product-market fit analysis'")
        print("• 'Revenue optimization opportunities'")
        print("-" * 50)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_user_input(self):
        """Get user input with prompt"""
        try:
            return input("\n💬 Ask your analytics question: ").strip()
        except KeyboardInterrupt:
            return "quit"
        except EOFError:
            return "quit"
    
    def process_query(self, query):
        """Process user query and return agent response"""
        try:
            print("\n🤖 Analytics Agent: ", end="", flush=True)
            
            # Get agent response
            response = self.agent.invoke({"input": query})
            
            # Display response
            print(response['output'])
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            print("Please try again with a different question.")
    
    def run(self):
        """Main CLI loop"""
        self.display_welcome()
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Thanks for using the Advanced Analytics CLI!")
                    break
                
                elif user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                elif user_input.lower() == 'schema':
                    self.display_schema()
                    continue
                
                elif user_input.lower() == 'examples':
                    self.display_examples()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.clear_screen()
                    self.display_welcome()
                    continue
                
                elif not user_input:
                    print("Please enter an analytics question.")
                    continue
                
                # Process the query
                self.process_query(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Advanced Analytics CLI!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Please try again.")

def main():
    """Main function to run the CLI"""
    try:
        cli = AdvancedAnalyticsCLI()
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
