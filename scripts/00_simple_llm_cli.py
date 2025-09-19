#!/usr/bin/env python3
"""
Simple LLM CLI Interface

Interactive command-line interface for the simple LLM agent demo.
Users can enter prompts and get responses from the Gemini-powered agent.

Usage:
    python 00_simple_llm_cli.py
"""

# Load environment variables first (including GOOGLE_API_KEY)
from dotenv import load_dotenv; load_dotenv()

# Import Gemini configuration
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_config import *  # Load Gemini API key

# Import LangChain components for agent creation
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini language model integration
from langchain.agents import initialize_agent, AgentType  # Agent framework
from langchain.schema import SystemMessage  # System message configuration
from langchain.tools import BaseTool  # Base class for creating dummy tools
from pydantic import BaseModel, Field  # Data validation for tool inputs
from typing import Type  # Type hinting

class DummyInput(BaseModel):
    """
    Pydantic model for dummy tool input - not actually used.
    """
    query: str = Field(description="Any input - this tool does nothing")

class DummyTool(BaseTool):
    """
    Dummy Tool - Does Nothing But Allows Agent Creation
    """
    name: str = "dummy_tool"
    description: str = "A dummy tool that does nothing - used only for agent framework demo"
    args_schema: Type[BaseModel] = DummyInput

    def _run(self, query: str) -> str:
        return "This is a dummy tool that does nothing. I can only provide information through conversation."

    def _arun(self, *args, **kwargs):
        raise NotImplementedError

class SimpleLLMCLI:
    """
    Interactive CLI for Simple LLM Agent
    """
    
    def __init__(self):
        """Initialize the CLI and agent"""
        self.agent = None
        self.llm = None
        self.setup_agent()
    
    def setup_agent(self):
        """Set up the Gemini-powered agent"""
        try:
            print("🤖 Initializing Gemini language model...")
            
            # Initialize the Language Model
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0,
                convert_system_message_to_human=True
            )
            
            # Define System Message for Agent
            system_message = SystemMessage(
                content="""You are a helpful AI assistant specializing in explaining technology concepts.
                You provide clear, concise explanations and are always friendly and professional.
                You have access to one dummy tool, but you should prefer to answer questions directly through conversation."""
            )
            
            # Create Dummy Tool Instance
            dummy_tool = DummyTool()
            
            # Create Agent with Dummy Tool
            print("🎯 Creating agent with dummy tool...")
            self.agent = initialize_agent(
                tools=[dummy_tool],
                llm=self.llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=False,  # Set to False for cleaner CLI output
                agent_kwargs={
                    "system_message": system_message
                }
            )
            
            print("✅ Agent initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing agent: {e}")
            raise
    
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("\n" + "="*60)
        print("🤖 Simple LLM Agent CLI")
        print("="*60)
        print("This is a conversational AI agent powered by Google Gemini.")
        print("You can ask questions about technology, programming, or any topic!")
        print("\nCommands:")
        print("  - Type your question and press Enter")
        print("  - Type 'help' for more information")
        print("  - Type 'quit', 'exit', or 'q' to exit")
        print("  - Type 'clear' to clear the screen")
        print("="*60)
    
    def display_help(self):
        """Display help information"""
        print("\n📖 Help Information:")
        print("-" * 40)
        print("This agent can help you with:")
        print("• Technology concepts and explanations")
        print("• Programming questions and examples")
        print("• General knowledge and discussions")
        print("• Problem-solving and analysis")
        print("\nExample questions:")
        print("• 'What is machine learning?'")
        print("• 'Explain how databases work'")
        print("• 'What are the benefits of using AI agents?'")
        print("• 'How does natural language processing work?'")
        print("-" * 40)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_user_input(self):
        """Get user input with prompt"""
        try:
            return input("\n💬 You: ").strip()
        except KeyboardInterrupt:
            return "quit"
        except EOFError:
            return "quit"
    
    def process_query(self, query):
        """Process user query and return agent response"""
        try:
            print("\n🤖 Agent: ", end="", flush=True)
            
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
                    print("\n👋 Goodbye! Thanks for using the Simple LLM Agent CLI!")
                    break
                
                elif user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.clear_screen()
                    self.display_welcome()
                    continue
                
                elif not user_input:
                    print("Please enter a question or command.")
                    continue
                
                # Process the query
                self.process_query(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Simple LLM Agent CLI!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Please try again.")

def main():
    """Main function to run the CLI"""
    try:
        cli = SimpleLLMCLI()
        cli.run()
    except Exception as e:
        print(f"❌ Failed to start CLI: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure your .env file contains GOOGLE_API_KEY")
        print("2. Verify your virtual environment is activated")
        print("3. Check that you've installed requirements: pip install -r requirements.txt")
        print("4. Ensure you have internet connection for API calls")

if __name__ == "__main__":
    main()
