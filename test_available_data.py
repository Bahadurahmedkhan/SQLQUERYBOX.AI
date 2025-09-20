#!/usr/bin/env python3
"""
Test queries with available data
"""

import requests
import json

def test_available_data():
    """Test queries with available data"""
    print("🧪 Testing Queries with Available Data...")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test queries that should have data
    test_queries = [
        "How many customers purchased something in July 2024?",
        "What was the revenue in August 2024?",
        "Show me customer data for June 2024"
    ]
    
    for i, test_prompt in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: '{test_prompt}'")
        print("-" * 50)
        
        try:
            response = requests.post(
                f"{base_url}/api/analyze",
                json={"prompt": test_prompt},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Success!")
                print(f"   Analysis type: {data['analysisType']}")
                print(f"   Text response preview:")
                print(f"   {data['textResponse'][:200]}...")
                print(f"   Chart type: {data['chartData']['type']}")
                print(f"   Chart title: {data['chartData']['title']}")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Available data testing completed!")

if __name__ == "__main__":
    test_available_data()
