#!/usr/bin/env python3
"""
Test script to verify frontend-backend communication
"""

import requests
import json

# Base URLs
BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_endpoints():
    """Test backend API endpoints"""
    print("🔍 Testing Backend Endpoints...")
    
    endpoints = [
        ("/", "GET", "Root endpoint"),
        ("/posts/", "GET", "Posts list"),
        ("/categories/", "GET", "Categories list"),
        ("/login/", "POST", "Login endpoint"),
        ("/signup/", "POST", "Signup endpoint"),
    ]
    
    for endpoint, method, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BACKEND_URL}{endpoint}")
            else:
                response = requests.post(f"{BACKEND_URL}{endpoint}", json={})
            
            status = "✅" if response.status_code in [200, 201, 404] else "❌"
            print(f"{status} {description}: {response.status_code}")
            
        except requests.exceptions.ConnectionError:
            print(f"❌ {description}: Connection failed (Backend not running)")
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)}")

def test_cors():
    """Test CORS configuration"""
    print("\n🔍 Testing CORS Configuration...")
    
    try:
        # Test preflight request
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'content-type',
        }
        
        response = requests.options(f"{BACKEND_URL}/posts/", headers=headers)
        
        if response.status_code == 200:
            print("✅ CORS preflight request successful")
        else:
            print(f"❌ CORS preflight failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ CORS test failed: {str(e)}")

def test_frontend_connection():
    """Test if frontend is accessible"""
    print("\n🔍 Testing Frontend Connection...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not accessible (React dev server not running)")
    except Exception as e:
        print(f"❌ Frontend test failed: {str(e)}")

def main():
    print("🚀 Frontend-Backend Integration Test")
    print("=" * 50)
    
    test_backend_endpoints()
    test_cors()
    test_frontend_connection()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print("1. Backend should be running on http://127.0.0.1:8000")
    print("2. Frontend should be running on http://localhost:3000")
    print("3. CORS should be configured to allow frontend-backend communication")
    print("4. API endpoints should be accessible from the frontend")
    
    print("\n🎯 To test the full integration:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Try logging in/signing up")
    print("3. Check if posts and categories load")
    print("4. Test the like/comment functionality")

if __name__ == "__main__":
    main() 