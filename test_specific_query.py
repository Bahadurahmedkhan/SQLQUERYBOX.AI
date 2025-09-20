#!/usr/bin/env python3
"""
Test the specific query that was failing
"""

import requests
import json

def test_specific_query():
    """Test the specific query about January 2024"""
    print("🧪 Testing Specific Query...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test the specific query that was failing
    test_prompt = "How many customers purchased something in January 2024?"
    
    print(f"Testing: '{test_prompt}'")
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
            print(f"   Text response:")
            print(f"   {data['textResponse']}")
            print(f"   Chart type: {data['chartData']['type']}")
            print(f"   Chart title: {data['chartData']['title']}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Specific query testing completed!")

if __name__ == "__main__":
    test_specific_query()