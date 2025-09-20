#!/usr/bin/env python3
"""
Test script to verify backend API is working
"""

import requests
import json

def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Backend API...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test database info endpoint
    try:
        print("\n2. Testing database info endpoint...")
        response = requests.get(f"{base_url}/api/database/info", timeout=5)
        if response.status_code == 200:
            print("✅ Database info endpoint working")
            data = response.json()
            print(f"   Database path: {data['database_path']}")
            print("   Table counts:")
            for table, count in data['table_counts'].items():
                print(f"     {table}: {count} records")
        else:
            print(f"❌ Database info endpoint failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Database info endpoint error: {e}")
    
    # Test analyze endpoint
    try:
        print("\n3. Testing analyze endpoint...")
        test_prompt = "Show me sales data"
        response = requests.post(
            f"{base_url}/api/analyze",
            json={"prompt": test_prompt},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Analyze endpoint working")
            data = response.json()
            print(f"   Analysis type: {data['analysisType']}")
            print(f"   Text response length: {len(data['textResponse'])} characters")
            print(f"   Chart data type: {data['chartData']['type']}")
        else:
            print(f"❌ Analyze endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Analyze endpoint error: {e}")
    
    print("\n🎉 Backend testing completed!")
    return True

if __name__ == "__main__":
    test_backend()
