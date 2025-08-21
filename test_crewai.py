#!/usr/bin/env python3
"""
Test script for CrewAI setup
Run this to verify your CrewAI implementation is working correctly
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from crewai import Agent, Task, Crew, Process, LLM
        print("✅ CrewAI core modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import CrewAI: {e}")
        return False
    
    try:
        from app.agents.crew import LeadCraftCrew
        print("✅ LeadCraftCrew imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import LeadCraftCrew: {e}")
        return False
    
    try:
        import yaml
        print("✅ PyYAML imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PyYAML: {e}")
        return False
    
    return True

def test_yaml_configs():
    """Test if YAML configuration files are valid"""
    print("\n🔍 Testing YAML configurations...")
    
    try:
        with open("app/agents/config/agents.yaml", "r") as f:
            agents_config = yaml.safe_load(f)
        print("✅ Agents YAML loaded successfully")
        
        with open("app/agents/config/tasks.yaml", "r") as f:
            tasks_config = yaml.safe_load(f)
        print("✅ Tasks YAML loaded successfully")
        
        # Check if required agents exist
        required_agents = ["job_refiner_agent", "question_generator_agent", "skill_extractor_agent"]
        for agent in required_agents:
            if agent in agents_config["agents"]:
                print(f"✅ Agent '{agent}' found")
            else:
                print(f"❌ Agent '{agent}' missing")
                return False
        
        # Check if required tasks exist
        required_tasks = ["refine_job_description", "generate_clarification_questions", "extract_skills_and_match"]
        for task in required_tasks:
            if task in tasks_config["tasks"]:
                print(f"✅ Task '{task}' found")
            else:
                print(f"❌ Task '{task}' missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ YAML configuration error: {e}")
        return False

def test_crew_creation():
    """Test if crew can be created successfully"""
    print("\n🔍 Testing crew creation...")
    
    try:
        from app.agents.crew import LeadCraftCrew
        
        # Create crew instance
        crew = LeadCraftCrew()
        print("✅ LeadCraftCrew instance created successfully")
        
        # Build agents
        agents = crew.build_agents()
        print(f"✅ Built {len(agents)} agents successfully")
        
        # Build tasks
        tasks = crew.build_tasks(agents)
        print(f"✅ Built {len(tasks)} tasks successfully")
        
        # Build crews
        crews = crew.build_crews()
        print(f"✅ Built {len(crews)} crews successfully")
        
        # Check if job_description crew exists
        if "job_description" in crews:
            print("✅ Job description crew found")
        else:
            print("❌ Job description crew missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Crew creation error: {e}")
        return False

def test_simple_execution():
    """Test a simple crew execution"""
    print("\n🔍 Testing simple execution...")
    
    try:
        from app.agents.crew import LeadCraftCrew
        
        crew = LeadCraftCrew()
        crews = crew.build_crews()
        
        # Get the job description crew
        job_crew = crews["job_description"]
        
        # Test with simple input
        test_input = {
            "raw_description": "We need a simple website with contact form",
            "user_profile_skills": "HTML, CSS, JavaScript"
        }
        
        print("🚀 Starting crew execution...")
        result = job_crew.kickoff(inputs=test_input)
        
        print(f"✅ Crew execution completed successfully!")
        print(f"📊 Result type: {type(result)}")
        print(f"📝 Result content: {str(result)[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Crew execution error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 CrewAI Setup Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("YAML Config Test", test_yaml_configs),
        ("Crew Creation Test", test_crew_creation),
        ("Simple Execution Test", test_simple_execution)
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
        print("🎉 All tests passed! Your CrewAI setup is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
