#!/usr/bin/env python3
"""
Test script for Simple Job Refiner Flow
Tests the streamlined two-step process
"""

def test_simple_crew():
    """Test the simple crew directly"""
    print("🧪 Testing Simple Refiner Crew")
    print("=" * 40)
    
    try:
        from app.agents.simple_refiner_crew import SimpleRefinerCrew
        
        crew = SimpleRefinerCrew()
        print("✅ Crew instantiated successfully")
        
        # Test initial processing
        print("\n1️⃣ Testing initial processing...")
        result = crew.process_initial("We need a simple website for our bakery")
        
        print(f"✅ Title: {result.get('title')}")
        print(f"✅ Project Type: {result.get('project_type')}")
        print(f"✅ Questions: {len(result.get('questions', []))} generated")
        print(f"✅ Description length: {len(result.get('refined_description', ''))}")
        
        # Test refining with answers
        print("\n2️⃣ Testing refining with answers...")
        sample_answers = [
            {
                "question_id": "q1",
                "question": "What's your budget?",
                "answer": "$5000",
                "skipped": False
            },
            {
                "question_id": "q2", 
                "question": "Do you need online ordering?",
                "answer": "Yes, for pastries and cakes",
                "skipped": False
            }
        ]
        
        refined_result = crew.refine_with_answers(
            previous_refined_description=result.get('refined_description'),
            title=result.get('title'),
            project_type=result.get('project_type'),
            answers=sample_answers
        )
        
        print(f"✅ Final description length: {len(refined_result.get('final_refined_description', ''))}")
        print("✅ Refining with answers successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_api_import():
    """Test API import"""
    print("\n🌐 Testing API Import")
    print("=" * 30)
    
    try:
        from app.api.v1.simple_job_refiner import router
        print("✅ Simple job refiner API imported successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Simple Job Refiner Flow - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Simple Crew Test", test_simple_crew),
        ("API Import Test", test_api_import)
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
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Simple flow is working correctly.")
        print("\n🚀 Ready to use!")
        print("\nNext steps:")
        print("1. Start server: uvicorn main:app --reload")
        print("2. Test with curl examples in SIMPLE_JOB_REFINER_CURL.md")
        return True
    else:
        print("⚠️  Some tests failed.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

