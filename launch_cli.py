#!/usr/bin/env python3
"""
SQL Agent CLI Launcher

Interactive launcher to choose and run any of the SQL agent CLI interfaces.
This launcher provides a unified entry point for all SQL agent implementations.

Usage:
    python launch_cli.py
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def display_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("🚀 SQL Agent CLI Launcher")
    print("="*60)
    print("Choose which SQL agent CLI to run:")
    print()
    print("1. 🤖 Simple LLM Agent CLI")
    print("   - Conversational AI without database access")
    print("   - General technology and programming questions")
    print()
    print("2. 🗄️  Simple SQL Agent CLI")
    print("   - Basic SQL agent with unrestricted database access")
    print("   - Natural language to SQL conversion")
    print()
    print("3. ⚠️  Dangerous SQL Agent CLI (Educational)")
    print("   - Shows dangerous patterns (what NOT to do)")
    print("   - Can execute ANY SQL including DELETE, DROP, etc.")
    print()
    print("4. 🛡️  Safe SQL Agent CLI (Recommended)")
    print("   - Production-ready secure SQL agent")
    print("   - Only SELECT statements, comprehensive security")
    print()
    print("5. 📊 Advanced Analytics CLI (Recommended)")
    print("   - Sophisticated business intelligence")
    print("   - Complex queries and multi-turn conversations")
    print()
    print("6. 🧪 Test Database (No API Required)")
    print("   - Test database structure and sample queries")
    print("   - No rate limits or API calls")
    print()
    print("0. ❌ Exit")
    print("="*60)

def get_user_choice():
    """Get user's menu choice"""
    while True:
        try:
            choice = input("\nEnter your choice (0-6): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("❌ Invalid choice. Please enter a number between 0-6.")
        except KeyboardInterrupt:
            return '0'
        except EOFError:
            return '0'

def run_cli(script_name: str, description: str) -> None:
    """
    Run the specified CLI script with improved error handling.
    
    Args:
        script_name: Name of the script to run
        description: Description of the script for user display
    """
    try:
        print(f"\n🚀 Launching {description}...")
        print("="*50)
        
        # Change to scripts directory
        script_path = Path("scripts") / script_name
        
        # Verify script exists
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            return
        
        # Run the script
        result = subprocess.run([sys.executable, str(script_path)], check=True)
        logger.info(f"Successfully completed {script_name}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")
        logger.error(f"Script {script_name} failed with exit code {e.returncode}")
    except FileNotFoundError:
        print(f"❌ Script not found: {script_name}")
        logger.error(f"Script file not found: {script_path}")
    except KeyboardInterrupt:
        print(f"\n👋 Exiting {description}...")
        logger.info(f"User interrupted {script_name}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logger.error(f"Unexpected error running {script_name}: {e}")

def run_database_test() -> None:
    """
    Run the database test script with improved error handling.
    """
    try:
        print(f"\n🧪 Running Database Test...")
        print("="*50)
        
        # Verify test script exists
        test_script = Path("test_database.py")
        if not test_script.exists():
            print(f"❌ Database test script not found: {test_script}")
            return
        
        # Run the test script
        result = subprocess.run([sys.executable, str(test_script)], check=True)
        logger.info("Database test completed successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running database test: {e}")
        logger.error(f"Database test failed with exit code {e.returncode}")
    except FileNotFoundError:
        print(f"❌ Database test script not found")
        logger.error("Database test script file not found")
    except KeyboardInterrupt:
        print(f"\n👋 Exiting database test...")
        logger.info("User interrupted database test")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logger.error(f"Unexpected error running database test: {e}")

def main():
    """Main launcher function"""
    while True:
        try:
            display_menu()
            choice = get_user_choice()
            
            if choice == '0':
                print("\n👋 Goodbye! Thanks for using the SQL Agent CLI Launcher!")
                break
            
            elif choice == '1':
                run_cli("00_simple_llm_cli.py", "Simple LLM Agent CLI")
            
            elif choice == '2':
                run_cli("01_simple_agent_cli.py", "Simple SQL Agent CLI")
            
            elif choice == '3':
                print("\n⚠️  WARNING: This agent can execute dangerous SQL commands!")
                confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    run_cli("02_risky_delete_demo_cli.py", "Dangerous SQL Agent CLI")
                else:
                    print("❌ Cancelled.")
            
            elif choice == '4':
                run_cli("03_guardrailed_agent_cli.py", "Safe SQL Agent CLI")
            
            elif choice == '5':
                run_cli("04_complex_queries_cli.py", "Advanced Analytics CLI")
            
            elif choice == '6':
                run_database_test()
            
            # Ask if user wants to continue
            print("\n" + "="*50)
            continue_choice = input("Would you like to run another CLI? (yes/no): ").strip().lower()
            if continue_choice not in ['yes', 'y']:
                print("\n👋 Goodbye! Thanks for using the SQL Agent CLI Launcher!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using the SQL Agent CLI Launcher!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
