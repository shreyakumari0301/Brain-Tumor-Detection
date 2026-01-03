#!/usr/bin/env python3
"""Quick script to test if backend is running"""
import requests
import sys

BACKEND_URL = "http://localhost:8000"

def test_backend():
    print(f"Testing backend at {BACKEND_URL}...")
    
    try:
        # Test root endpoint
        print("\n1. Testing root endpoint...")
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test health endpoint
        print("\n2. Testing health endpoint...")
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        print("\n✅ Backend is running and accessible!")
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to {BACKEND_URL}")
        print("\nPossible issues:")
        print("  1. Backend is not running")
        print("  2. Backend is running on a different port")
        print("  3. Firewall is blocking the connection")
        print("  4. If using WSL, networking might need special configuration")
        print("\nTo start the backend:")
        print("  cd backend")
        print("  python main.py")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_backend()
    sys.exit(0 if success else 1)

