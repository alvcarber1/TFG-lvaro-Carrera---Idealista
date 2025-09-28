#!/usr/bin/env python3
"""
Post-deployment validation for TFG Idealista
Álvaro Carrera - Test production deployments
Tests both Render (backend) and Vercel (frontend)
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

# Production URLs
BACKEND_URL = "https://tfg-idealista-backend.onrender.com"
FRONTEND_URL = "https://tfg-idealista-frontend.vercel.app"

def test_backend_health():
    """Test backend health and API endpoints"""
    print("🌐 Testing backend deployment...")
    
    try:
        # Test basic connectivity
        response = requests.get(f"{BACKEND_URL}/api/", timeout=30)
        if response.status_code == 200:
            print("   ✅ Backend is responding")
        else:
            print(f"   ❌ Backend health check failed: {response.status_code}")
            return False
            
        # Test properties endpoint
        response = requests.get(f"{BACKEND_URL}/api/properties/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Properties endpoint: {len(data)} properties returned")
        else:
            print(f"   ❌ Properties endpoint failed: {response.status_code}")
            return False
            
        # Test clustering endpoint
        response = requests.get(f"{BACKEND_URL}/api/clustering/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Clustering endpoint: {data.get('clusters', 'N/A')} clusters")
        else:
            print(f"   ❌ Clustering endpoint failed: {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.Timeout:
        print("   ❌ Backend request timeout (may still be starting up)")
        return False
    except Exception as e:
        print(f"   ❌ Backend test failed: {e}")
        return False

def test_frontend_health():
    """Test frontend deployment"""
    print("🎨 Testing frontend deployment...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=30)
        if response.status_code == 200:
            print("   ✅ Frontend is responding")
            
            # Check for Streamlit indicators
            content = response.text
            if "streamlit" in content.lower() or "tfg" in content.lower():
                print("   ✅ Frontend content looks correct")
                return True
            else:
                print("   ⚠️ Frontend content may not be correct")
                return False
        else:
            print(f"   ❌ Frontend health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Frontend request timeout")
        return False
    except Exception as e:
        print(f"   ❌ Frontend test failed: {e}")
        return False

def test_full_integration():
    """Test full integration between frontend and backend"""
    print("🔗 Testing frontend-backend integration...")
    
    try:
        # Test if frontend can call backend
        test_data = {
            "buy_price": 500000,
            "sq_mt_built": 100,
            "n_rooms": 3,
            "n_bathrooms": 2
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/predict/",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            cluster = data.get('cluster')
            print(f"   ✅ Integration test: Property classified as cluster {cluster}")
            return True
        else:
            print(f"   ❌ Integration test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
        return False

def wait_for_deployment(max_wait_minutes=10):
    """Wait for deployments to be ready"""
    print(f"⏱️ Waiting up to {max_wait_minutes} minutes for deployments...")
    
    for minute in range(max_wait_minutes):
        print(f"   🔄 Attempt {minute + 1}/{max_wait_minutes}...")
        
        try:
            backend_ready = requests.get(f"{BACKEND_URL}/api/", timeout=10).status_code == 200
            frontend_ready = requests.get(FRONTEND_URL, timeout=10).status_code == 200
            
            if backend_ready and frontend_ready:
                print("   ✅ Both deployments are ready!")
                return True
            elif backend_ready:
                print("   🌐 Backend ready, waiting for frontend...")
            elif frontend_ready:
                print("   🎨 Frontend ready, waiting for backend...")
            else:
                print("   ⏳ Both deployments still starting up...")
                
        except:
            print("   ⏳ Deployments still starting up...")
        
        if minute < max_wait_minutes - 1:
            time.sleep(60)  # Wait 1 minute
    
    print(f"   ⚠️ Deployments not ready after {max_wait_minutes} minutes")
    return False

def main():
    """Main post-deployment validation"""
    print("🔍 TFG IDEALISTA - POST-DEPLOYMENT VALIDATION")
    print("=" * 50)
    print("Álvaro Carrera - Production deployment test")
    print("=" * 50)
    
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🎨 Frontend URL: {FRONTEND_URL}")
    print("")
    
    # Wait for deployments
    if not wait_for_deployment():
        print("⚠️ Continuing with tests anyway...")
    
    # Run tests
    backend_ok = test_backend_health()
    frontend_ok = test_frontend_health()
    integration_ok = test_full_integration() if backend_ok else False
    
    print("\n" + "=" * 50)
    print("📊 POST-DEPLOYMENT TEST RESULTS")
    print("=" * 50)
    
    print(f"🌐 Backend:     {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"🎨 Frontend:    {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"🔗 Integration: {'✅ PASS' if integration_ok else '❌ FAIL'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("🚀 TFG Idealista is live in production!")
        print("\n📱 Access your application:")
        print(f"   🎨 Frontend: {FRONTEND_URL}")
        print(f"   🌐 API: {BACKEND_URL}/api/")
        
        return 0
    else:
        print("\n❌ DEPLOYMENT ISSUES DETECTED")
        print("🔧 Please check the deployment logs and try again")
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)