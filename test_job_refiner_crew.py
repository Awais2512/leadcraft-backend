#!/usr/bin/env python3
"""
Test script for Job Description Refiner Crew
Run this to verify your new crew implementation is working correctly
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
        from app.agents.job_refiner_crew import JobRefinerCrew
        print("✅ JobRefinerCrew imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import JobRefinerCrew: {e}")
        return False
    
    try:
        from app.schemas.job_refiner import JobRefinerRequest, JobRefinerCrewOutput
        print("✅ Job refiner schemas imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import job refiner schemas: {e}")
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
        with open("app/agents/config/job_refiner_agents.yaml", "r") as f:
            agents_config = yaml.safe_load(f)
        print("✅ Job refiner agents YAML loaded successfully")
        
        with open("app/agents/config/job_refiner_tasks.yaml", "r") as f:
            tasks_config = yaml.safe_load(f)
        print("✅ Job refiner tasks YAML loaded successfully")
        
        # Check if required agents exist
        required_agents = [
            "project_analyzer_agent", 
            "ambiguity_detector_agent", 
            "client_interaction_agent",
            "skill_extractor_agent", 
            "project_classifier_agent", 
            "description_refiner_agent"
        ]
        
        for agent in required_agents:
            if agent in agents_config["agents"]:
                print(f"✅ Agent '{agent}' found")
            else:
                print(f"❌ Agent '{agent}' missing")
                return False
        
        # Check if required tasks exist
        required_tasks = [
            "initial_project_analysis",
            "detect_ambiguities_and_generate_questions", 
            "manage_client_interaction",
            "extract_technical_skills",
            "classify_project_type",
            "create_final_refined_description"
        ]
        
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
        from app.agents.job_refiner_crew import JobRefinerCrew
        
        # Create crew instance
        crew = JobRefinerCrew()
        print("✅ JobRefinerCrew instance created successfully")
        
        # Build agents
        agents = crew.build_agents()
        print(f"✅ Built {len(agents)} agents successfully")
        
        # Build tasks
        tasks = crew.build_tasks(agents)
        print(f"✅ Built {len(tasks)} tasks successfully")
        
        # Build crew
        crew_instance = crew.build_crew()
        print("✅ Crew built successfully")
        
        # Get crew info
        crew_info = crew.get_crew_info()
        print(f"✅ Crew info retrieved: {crew_info['crew_name']} v{crew_info['version']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Crew creation error: {e}")
        return False

def test_schema_validation():
    """Test if Pydantic schemas work correctly"""
    print("\n🔍 Testing schema validation...")
    
    try:
        from app.schemas.job_refiner import JobRefinerRequest, JobRefinerCrewOutput
        
        # Test request schema
        test_request = JobRefinerRequest(
            raw_description="We need a React app with authentication",
            client_responses=[],
            user_preferences={}
        )
        print("✅ JobRefinerRequest schema validation successful")
        
        # Test output schema (with minimal data)
        from app.schemas.job_refiner import (
            ProjectAnalysis, AmbiguityAnalysis, ClientInteractionSummary,
            SkillsAnalysis, ProjectClassification, RefinedProjectDescription,
            ProjectType, ComplexityLevel
        )
        
        test_output = JobRefinerCrewOutput(
            project_analysis=ProjectAnalysis(
                project_type=ProjectType.PROJECT,
                complexity_level=ComplexityLevel.MODERATE,
                primary_industry="Technology",
                scope_breakdown=["Frontend", "Backend"],
                risk_assessment=["Timeline"],
                recommended_next_steps=["Clarify requirements"]
            ),
            ambiguity_analysis=AmbiguityAnalysis(
                ambiguities=[],
                questions_by_category={},
                questions_by_priority={},
                risk_summary="Low risk",
                recommendations=[]
            ),
            client_interaction=ClientInteractionSummary(
                questions_presented=[],
                client_responses=[],
                skipped_questions=[],
                feedback_integration="No feedback",
                information_completeness="Complete",
                recommendations=[],
                communication_quality="Good"
            ),
            skills_analysis=SkillsAnalysis(
                explicit_skills=[],
                implicit_skills=[],
                skills_by_category={},
                skills_by_importance={},
                critical_skill_gaps=[],
                recommendations=[],
                technology_stack=[]
            ),
            project_classification=ProjectClassification(
                project_type=ProjectType.PROJECT,
                primary_category="Web Development",
                subcategory="Frontend",
                industry_classification="Technology",
                complexity_level=ComplexityLevel.MODERATE,
                project_management_approach="Agile",
                estimated_team_size="2-3 developers",
                estimated_duration="4-6 weeks",
                resource_requirements=["Frontend Developer", "Backend Developer"],
                project_characteristics=["Modern UI", "Authentication"]
            ),
            refined_description=RefinedProjectDescription(
                executive_summary="React app with authentication",
                project_overview=None,
                scope_of_work=None,
                technical_requirements=None,
                deliverables=None,
                timeline=None,
                risk_assessment=None,
                assumptions_constraints=None,
                success_criteria=None,
                next_steps=None,
                metadata={}
            ),
            processing_timestamp="2024-01-15T10:30:00Z",
            total_processing_time=1.5,
            crew_version="1.0.0"
        )
        print("✅ JobRefinerCrewOutput schema validation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation error: {e}")
        return False

def test_simple_execution():
    """Test a simple crew execution"""
    print("\n🔍 Testing simple execution...")
    
    try:
        from app.agents.job_refiner_crew import JobRefinerCrew
        from app.schemas.job_refiner import JobRefinerRequest
        
        crew = JobRefinerCrew()
        
        # Create test request
        test_request = JobRefinerRequest(
            raw_description="We need a simple website with contact form and blog",
            client_responses=[],
            user_preferences={"industry": "Technology", "budget": "Medium"}
        )
        
        print("🚀 Starting Job Refiner Crew execution...")
        print(f"📝 Input: {test_request.raw_description}")
        
        # Process the request
        result = crew.process_project_description(test_request)
        
        print(f"✅ Crew execution completed successfully!")
        print(f"📊 Result type: {type(result)}")
        print(f"🏗️ Project Type: {result.project_analysis.project_type}")
        print(f"📈 Complexity: {result.project_analysis.complexity_level}")
        print(f"⏱️ Processing time: {result.total_processing_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Crew execution error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Job Description Refiner Crew Test Suite")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("YAML Config Test", test_yaml_configs),
        ("Crew Creation Test", test_crew_creation),
        ("Schema Validation Test", test_schema_validation),
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
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Job Refiner Crew is working correctly.")
        print("\n🚀 Ready to process project descriptions!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
