import yaml
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from crewai import Agent, Task, Crew, Process, LLM
from app.schemas.job_refiner import (
    JobRefinerCrewOutput, JobRefinerRequest, 
    ProjectAnalysis, AmbiguityAnalysis, ClientInteractionSummary,
    SkillsAnalysis, ProjectClassification, RefinedProjectDescription
)


class JobRefinerCrew:
    """
    Sophisticated Job Description Refiner Crew
    
    This crew processes raw project descriptions through multiple specialized agents
    to create comprehensive, professional project requirements documents.
    
    Execution Flow:
    1. Initial Analysis (Parallel with Ambiguity Detection)
    2. Client Interaction Management
    3. Skills Extraction
    4. Project Classification
    5. Final Document Creation
    """
    
    def __init__(self, model: str = "gemini/gemini-2.0-flash", temperature: float = 0.7):
        """
        Initialize JobRefinerCrew with LLM and configuration.
        
        Args:
            model: LLM model to use for agents
            temperature: Creativity level for LLM responses
        """
        self.llm = LLM(model=model, temperature=temperature)
        self.base_dir = Path(__file__).resolve().parent
        self.config_dir = self.base_dir / "config"
        self.crew_version = "1.0.0"
        self._crew = None  # Lazy initialization
        
    def _load_yaml(self, path: Path) -> dict:
        """Load and parse YAML configuration file."""
        with open(path, "r") as f:
            return yaml.safe_load(f)
    
    def build_agents(self) -> Dict[str, Agent]:
        """Build all agents for the job refiner crew."""
        config = self._load_yaml(self.config_dir / "job_refiner_agents.yaml")
        agents = {}
        
        for name, cfg in config["agents"].items():
            agents[name] = Agent(
                role=cfg["role"],
                goal=cfg["goal"],
                backstory=cfg["backstory"],
                llm=self.llm,
                memory=cfg.get("memory", False),
                verbose=cfg.get("verbose", True),
                allow_delegation=cfg.get("allow_delegation", False),
            )
        
        return agents
    
    def build_tasks(self, agents: Dict[str, Agent]) -> Dict[str, Task]:
        """Build all tasks for the job refiner crew."""
        config = self._load_yaml(self.config_dir / "job_refiner_tasks.yaml")
        tasks = {}
        
        # First pass: create task objects
        for name, cfg in config["tasks"].items():
            tasks[name] = Task(
                description=cfg["description"],
                expected_output=cfg.get("expected_output"),
                agent=agents[cfg["agent"]],
                async_execution=cfg.get("async_execution", False),
                markdown=cfg.get("markdown", True),
            )
        
        # Second pass: attach contexts
        for name, cfg in config["tasks"].items():
            if "context" in cfg:
                tasks[name].context = [tasks[c] for c in cfg["context"]]
        
        return tasks
    
    def build_crew(self) -> Crew:
        """Build the job refiner crew with optimized execution strategy."""
        agents = self.build_agents()
        tasks = self.build_tasks(agents)
        
        # Create the crew with sequential process and delegation for complex orchestration
        crew = Crew(
            agents=[
                agents["project_analyzer_agent"],
                agents["ambiguity_detector_agent"],
                agents["client_interaction_agent"],
                agents["skill_extractor_agent"],
                agents["project_classifier_agent"],
                agents["description_refiner_agent"],
            ],
            tasks=[
                tasks["initial_project_analysis"],
                tasks["detect_ambiguities_and_generate_questions"],
                tasks["manage_client_interaction"],
                tasks["extract_technical_skills"],
                tasks["classify_project_type"],
                tasks["create_final_refined_description"],
            ],
            process=Process.sequential,  # Sequential execution with dependencies
            verbose=True,
            memory=True,  # Enable memory for complex multi-step processes
            manager_llm=self.llm,  # Manager LLM for coordination
        )
        
        return crew
    
    def get_crew(self) -> Crew:
        """Get the crew instance, building it if necessary."""
        if self._crew is None:
            self._crew = self.build_crew()
        return self._crew
    
    def process_project_description(
        self, 
        request: JobRefinerRequest
    ) -> JobRefinerCrewOutput:
        """
        Process a raw project description through the complete crew workflow.
        Args:
            request: JobRefinerRequest containing raw description and optional client response  
        Returns:
            JobRefinerCrewOutput with complete processed results
        """
        start_time = time.time()
        
        # Get the crew (build if necessary)
        crew = self.get_crew()
        
        # Prepare inputs for the crew
        inputs = {
            "raw_description": request.raw_description,
            "client_responses": request.client_responses or [],
            "user_preferences": request.user_preferences or {},
        }
        
        # Execute the crew workflow
        print("🚀 Starting Job Description Refiner Crew execution...")
        result = crew.kickoff(inputs=inputs)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Parse and structure the results
        structured_output = self._parse_crew_results(result, processing_time)
        
        return structured_output
    
    def _parse_crew_results(self, crew_result: Any, processing_time: float) -> JobRefinerCrewOutput:
        """
        Parse the crew execution results into structured Pydantic models.
        
        Args:
            crew_result: Raw result from crew execution
            processing_time: Total processing time in seconds
            
        Returns:
            Structured JobRefinerCrewOutput
        """
        # Extract individual task results
        task_results = {}
        if hasattr(crew_result, 'tasks'):
            for task in crew_result.tasks:
                task_name = task.name if hasattr(task, 'name') else str(task)
                task_results[task_name] = task.output if hasattr(task, 'output') else str(task)
        
        # Parse each component (this is a simplified parser - in production you'd want more robust parsing)
        try:
            # For now, we'll create a basic structure
            # In a real implementation, you'd parse the actual text outputs into structured data
            
            structured_output = JobRefinerCrewOutput(
                project_analysis=ProjectAnalysis(
                    project_type="project",  # Default values - would be parsed from actual output
                    complexity_level="moderate",
                    primary_industry="Technology",
                    scope_breakdown=["To be determined from crew output"],
                    risk_assessment=["To be determined from crew output"],
                    recommended_next_steps=["To be determined from crew output"]
                ),
                ambiguity_analysis=AmbiguityAnalysis(
                    ambiguities=[],
                    questions_by_category={},
                    questions_by_priority={},
                    risk_summary="To be determined from crew output",
                    recommendations=[]
                ),
                client_interaction=ClientInteractionSummary(
                    questions_presented=[],
                    client_responses=[],
                    skipped_questions=[],
                    feedback_integration="To be determined from crew output",
                    information_completeness="To be determined from crew output",
                    recommendations=[],
                    communication_quality="To be determined from crew output"
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
                    project_type="project",
                    primary_category="To be determined",
                    subcategory="To be determined",
                    industry_classification="To be determined",
                    complexity_level="moderate",
                    project_management_approach="To be determined",
                    estimated_team_size="To be determined",
                    estimated_duration="To be determined",
                    resource_requirements=[],
                    project_characteristics=[]
                ),
                refined_description=RefinedProjectDescription(
                    executive_summary="To be determined from crew output",
                    project_overview=None,  # Would be parsed from actual output
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
                processing_timestamp=datetime.utcnow().isoformat() + "Z",
                total_processing_time=processing_time,
                crew_version=self.crew_version
            )
            
            return structured_output
            
        except Exception as e:
            print(f"Error parsing crew results: {e}")
            # Return a basic output with error information
            return JobRefinerCrewOutput(
                project_analysis=ProjectAnalysis(
                    project_type="project",
                    complexity_level="moderate",
                    primary_industry="Unknown",
                    scope_breakdown=["Error parsing results"],
                    risk_assessment=["Error parsing results"],
                    recommended_next_steps=["Review crew output manually"]
                ),
                ambiguity_analysis=AmbiguityAnalysis(
                    ambiguities=[],
                    questions_by_category={},
                    questions_by_priority={},
                    risk_summary="Error parsing results",
                    recommendations=["Review crew output manually"]
                ),
                client_interaction=ClientInteractionSummary(
                    questions_presented=[],
                    client_responses=[],
                    skipped_questions=[],
                    feedback_integration="Error parsing results",
                    information_completeness="Error parsing results",
                    recommendations=["Review crew output manually"],
                    communication_quality="Unknown"
                ),
                skills_analysis=SkillsAnalysis(
                    explicit_skills=[],
                    implicit_skills=[],
                    skills_by_category={},
                    skills_by_importance={},
                    critical_skill_gaps=[],
                    recommendations=["Review crew output manually"],
                    technology_stack=[]
                ),
                project_classification=ProjectClassification(
                    project_type="project",
                    primary_category="Unknown",
                    subcategory="Unknown",
                    industry_classification="Unknown",
                    complexity_level="moderate",
                    project_management_approach="Unknown",
                    estimated_team_size="Unknown",
                    estimated_duration="Unknown",
                    resource_requirements=[],
                    project_characteristics=[]
                ),
                refined_description=RefinedProjectDescription(
                    executive_summary="Error parsing crew results",
                    project_overview=None,
                    scope_of_work=None,
                    technical_requirements=None,
                    deliverables=None,
                    timeline=None,
                    risk_assessment=None,
                    assumptions_constraints=None,
                    success_criteria=None,
                    next_steps=None,
                    metadata={"error": str(e)}
                ),
                processing_timestamp=datetime.utcnow().isoformat() + "Z",
                total_processing_time=processing_time,
                crew_version=self.crew_version
            )
    
    def get_crew_info(self) -> Dict[str, Any]:
        """Get information about the crew configuration."""
        return {
            "crew_name": "Job Description Refiner Crew",
            "version": self.crew_version,
            "agents": [
                "Project Analyzer Agent",
                "Ambiguity Detector Agent", 
                "Client Interaction Agent",
                "Skill Extractor Agent",
                "Project Classifier Agent",
                "Description Refiner Agent"
            ],
            "execution_strategy": "Hierarchical with delegation",
            "memory_enabled": True,
            "llm_model": str(self.llm.model),
            "temperature": self.llm.temperature
        }
