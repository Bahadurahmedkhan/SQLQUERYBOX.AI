#!/usr/bin/env python3
"""
Test the complete integration between frontend and backend
"""

import requests
import json
import time

def test_integration():
    """Test the complete integration"""
    print("🧪 Testing Complete Integration...")
    print("=" * 60)
    
    # Test different types of prompts
    test_prompts = [
        "Show me sales performance and revenue data",
        "Analyze customer demographics and regions", 
        "What are the best selling products?",
        "Show me order trends and status distribution",
        "Give me a business overview and key metrics"
    ]
    
    base_url = "http://localhost:5000"
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{i}. Testing prompt: '{prompt}'")
        print("-" * 50)
        
        try:
            response = requests.post(
                f"{base_url}/api/analyze",
                json={"prompt": prompt},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success!")
                print(f"   Analysis type: {data['analysisType']}")
                print(f"   Text response: {data['textResponse'][:100]}...")
                print(f"   Chart type: {data['chartData']['type']}")
                print(f"   Chart title: {data['chartData']['title']}")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    print("\n" + "=" * 60)
    print("🎉 Integration testing completed!")
    print("\n💡 Now you can:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Try the same prompts in the web interface")
    print("3. You should see '✅ Real Data' instead of mock data")
    print("4. Charts should show actual database values")

if __name__ == "__main__":
    test_integration()
