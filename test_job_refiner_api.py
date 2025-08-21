#!/usr/bin/env python3
"""
Test script for Job Description Refiner Crew API endpoints
Run this to verify your API implementation is working correctly
"""

import sys
import os
import requests
import json
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

def test_api_endpoints():
    """Test the Job Refiner API endpoints"""
    print("🧪 Testing Job Refiner Crew API Endpoints")
    print("=" * 60)
    
    # Configuration
    base_url = "http://localhost:8000/api/v1/job-refiner"
    test_token = "your-test-jwt-token-here"  # Replace with actual test token
    
    headers = {
        "Authorization": f"Bearer {test_token}",
        "Content-Type": "application/json"
    }
    
    # Test data
    test_description = "We need a React website with user authentication and admin dashboard"
    test_preferences = {
        "industry": "Technology",
        "budget": "Medium",
        "timeline": "3-6 months"
    }
    
    print("🔍 Testing API endpoints...")
    
    try:
        # Test 1: Process Initial Description
        print("\n1️⃣ Testing: Process Initial Description")
        print(f"   URL: POST {base_url}/process-initial")
        
        initial_data = {
            "raw_description": test_description,
            "client_responses": [],
            "user_preferences": test_preferences
        }
        
        response = requests.post(
            f"{base_url}/process-initial",
            headers=headers,
            json=initial_data
        )
        
        if response.status_code == 200:
            result = response.json()
            processing_id = result.get("processing_id")
            print(f"   ✅ Success! Processing ID: {processing_id}")
            
            # Test 2: Get Session Status
            print("\n2️⃣ Testing: Get Session Status")
            print(f"   URL: GET {base_url}/session/{processing_id}")
            
            status_response = requests.get(
                f"{base_url}/session/{processing_id}",
                headers=headers
            )
            
            if status_response.status_code == 200:
                print("   ✅ Success! Session status retrieved")
            else:
                print(f"   ❌ Failed! Status: {status_response.status_code}")
            
            # Test 3: Submit Client Feedback
            print("\n3️⃣ Testing: Submit Client Feedback")
            print(f"   URL: POST {base_url}/submit-client-feedback/{processing_id}")
            
            feedback_data = [
                {
                    "question": "What user roles do you need?",
                    "answer": "Admin and regular users",
                    "skipped": False,
                    "skip_reason": None,
                    "additional_context": "Admin should have full access"
                },
                {
                    "question": "What is your budget range?",
                    "answer": None,
                    "skipped": True,
                    "skip_reason": "Budget not finalized",
                    "additional_context": None
                }
            ]
            
            feedback_response = requests.post(
                f"{base_url}/submit-client-feedback/{processing_id}",
                headers=headers,
                json=feedback_data
            )
            
            if feedback_response.status_code == 200:
                print("   ✅ Success! Client feedback processed")
            else:
                print(f"   ❌ Failed! Status: {feedback_response.status_code}")
            
            # Test 4: Finalize Description
            print("\n4️⃣ Testing: Finalize Description")
            print(f"   URL: POST {base_url}/finalize-description/{processing_id}")
            
            finalize_data = {
                "title": "React Website with Authentication",
                "description": "Modern React website with user authentication and admin dashboard",
                "additional_notes": "Focus on security and user experience"
            }
            
            finalize_response = requests.post(
                f"{base_url}/finalize-description/{processing_id}",
                headers=headers,
                json=finalize_data
            )
            
            if finalize_response.status_code == 200:
                result = finalize_response.json()
                project_id = result.get("project_id")
                print(f"   ✅ Success! Project ID: {project_id}")
            else:
                print(f"   ❌ Failed! Status: {finalize_response.status_code}")
            
            # Test 5: Get User Sessions
            print("\n5️⃣ Testing: Get User Sessions")
            print(f"   URL: GET {base_url}/user-sessions")
            
            sessions_response = requests.get(
                f"{base_url}/user-sessions",
                headers=headers
            )
            
            if sessions_response.status_code == 200:
                print("   ✅ Success! User sessions retrieved")
            else:
                print(f"   ❌ Failed! Status: {sessions_response.status_code}")
            
            # Test 6: Get Crew Info
            print("\n6️⃣ Testing: Get Crew Information")
            print(f"   URL: GET {base_url}/crew-info")
            
            crew_response = requests.get(
                f"{base_url}/crew-info",
                headers=headers
            )
            
            if crew_response.status_code == 200:
                print("   ✅ Success! Crew information retrieved")
            else:
                print(f"   ❌ Failed! Status: {crew_response.status_code}")
            
            # Test 7: Delete Session
            print("\n7️⃣ Testing: Delete Session")
            print(f"   URL: DELETE {base_url}/session/{processing_id}")
            
            delete_response = requests.delete(
                f"{base_url}/session/{processing_id}",
                headers=headers
            )
            
            if delete_response.status_code == 200:
                print("   ✅ Success! Session deleted")
            else:
                print(f"   ❌ Failed! Status: {delete_response.status_code}")
            
        else:
            print(f"   ❌ Failed! Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure your FastAPI server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 API testing completed!")

def test_database_schema():
    """Test database schema creation"""
    print("\n🗄️ Testing Database Schema")
    print("=" * 40)
    
    try:
        from app.schemas.database import DatabaseUtils, SQL_CREATE_TABLES
        
        print("✅ Database schema definitions loaded successfully")
        print(f"✅ SQL script length: {len(SQL_CREATE_TABLES)} characters")
        
        # Check if we can import the database utilities
        utils = DatabaseUtils()
        print("✅ Database utilities imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Database schema error: {e}")
        return False

def test_schemas():
    """Test Pydantic schemas"""
    print("\n📋 Testing Pydantic Schemas")
    print("=" * 40)
    
    try:
        from app.schemas.job_refiner import (
            JobRefinerRequest, JobRefinerResponse, JobRefinerCrewOutput,
            ClientResponse, ProjectAnalysis, AmbiguityAnalysis
        )
        
        # Test request schema
        test_request = JobRefinerRequest(
            raw_description="Test description",
            client_responses=[],
            user_preferences={}
        )
        print("✅ JobRefinerRequest schema validation successful")
        
        # Test response schema
        test_response = JobRefinerResponse(
            success=True,
            data=None,
            error=None,
            message="Test message",
            processing_id="test-id"
        )
        print("✅ JobRefinerResponse schema validation successful")
        
        # Test client response schema
        test_client_response = ClientResponse(
            question="Test question?",
            answer="Test answer",
            skipped=False
        )
        print("✅ ClientResponse schema validation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Job Description Refiner Crew - Complete Test Suite")
    print("=" * 70)
    
    tests = [
        ("Database Schema Test", test_database_schema),
        ("Pydantic Schemas Test", test_schemas),
        ("API Endpoints Test", test_api_endpoints)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Job Refiner Crew API is ready!")
        print("\n🚀 Next steps:")
        print("   1. Start your FastAPI server: uvicorn main:app --reload")
        print("   2. Set up your database tables")
        print("   3. Test with real JWT tokens")
        print("   4. Integrate with your frontend")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
