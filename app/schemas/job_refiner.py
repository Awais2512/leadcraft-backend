from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from enum import Enum

# Enums for classification
class ProjectType(str, Enum):
    JOB = "job"
    PROJECT = "project"
    SERVICE = "service"
    CONSULTATION = "consultation"
    MAINTENANCE = "maintenance"
    TRAINING = "training"

class ComplexityLevel(str, Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"

class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class SkillCategory(str, Enum):
    PROGRAMMING = "programming"
    DESIGN = "design"
    DATABASE = "database"
    INFRASTRUCTURE = "infrastructure"
    MANAGEMENT = "management"
    COMMUNICATION = "communication"
    ANALYSIS = "analysis"
    TESTING = "testing"
    DEPLOYMENT = "deployment"

# Base models for individual components
class ProjectAnalysis(BaseModel):
    """Initial project analysis output"""
    project_type: ProjectType = Field(..., description="Classification of the request type")
    complexity_level: ComplexityLevel = Field(..., description="Assessed complexity level")
    primary_industry: str = Field(..., description="Primary industry or domain")
    scope_breakdown: List[str] = Field(..., description="High-level scope components")
    risk_assessment: List[str] = Field(..., description="Identified risks and concerns")
    recommended_next_steps: List[str] = Field(..., description="Recommended actions")
    estimated_duration: Optional[str] = Field(None, description="Estimated project duration")
    estimated_budget_range: Optional[str] = Field(None, description="Estimated budget range")

class AmbiguityItem(BaseModel):
    """Individual ambiguity item"""
    description: str = Field(..., description="Description of the ambiguity")
    category: str = Field(..., description="Category of the ambiguity")
    priority: PriorityLevel = Field(..., description="Priority level of the ambiguity")
    risk_level: str = Field(..., description="Risk level if not clarified")
    impact: str = Field(..., description="Impact on project success")

class ClarificationQuestion(BaseModel):
    """Individual clarification question"""
    question: str = Field(..., description="The clarification question")
    category: str = Field(..., description="Category of the question")
    priority: PriorityLevel = Field(..., description="Priority of the question")
    context: str = Field(..., description="Context for why this question is important")
    expected_answer_type: str = Field(..., description="Type of answer expected")

class AmbiguityAnalysis(BaseModel):
    """Comprehensive ambiguity analysis"""
    ambiguities: List[AmbiguityItem] = Field(..., description="List of identified ambiguities")
    questions_by_category: Dict[str, List[ClarificationQuestion]] = Field(..., description="Questions organized by category")
    questions_by_priority: Dict[PriorityLevel, List[ClarificationQuestion]] = Field(..., description="Questions organized by priority")
    risk_summary: str = Field(..., description="Summary of overall risk assessment")
    recommendations: List[str] = Field(..., description="Recommendations for addressing ambiguities")

class ClientResponse(BaseModel):
    """Individual client response to a question"""
    question_id: Optional[str] = Field(None, description="Identifier for the question")
    question: str = Field(..., description="The question that was asked")
    answer: Optional[str] = Field(None, description="Client's answer to the question")
    skipped: bool = Field(False, description="Whether the client skipped this question")
    skip_reason: Optional[str] = Field(None, description="Reason for skipping if applicable")
    additional_context: Optional[str] = Field(None, description="Any additional context provided")

class ClientInteractionSummary(BaseModel):
    """Summary of client interaction process"""
    questions_presented: List[ClarificationQuestion] = Field(..., description="Questions presented to client")
    client_responses: List[ClientResponse] = Field(..., description="All client responses received")
    skipped_questions: List[ClientResponse] = Field(..., description="Questions that were skipped")
    feedback_integration: str = Field(..., description="Summary of integrated client feedback")
    information_completeness: str = Field(..., description="Assessment of information completeness")
    recommendations: List[str] = Field(..., description="Recommendations for proceeding")
    communication_quality: str = Field(..., description="Quality of client communication")

class SkillRequirement(BaseModel):
    """Individual skill requirement"""
    skill_name: str = Field(..., description="Name of the skill")
    category: SkillCategory = Field(..., description="Category of the skill")
    importance: PriorityLevel = Field(..., description="Importance level of the skill")
    proficiency_level: str = Field(..., description="Required proficiency level")
    is_explicit: bool = Field(..., description="Whether the skill was explicitly mentioned")
    description: str = Field(..., description="Description of the skill requirement")
    alternatives: Optional[List[str]] = Field(None, description="Alternative skills that could work")

class SkillsAnalysis(BaseModel):
    """Comprehensive skills analysis"""
    explicit_skills: List[SkillRequirement] = Field(..., description="Skills explicitly mentioned")
    implicit_skills: List[SkillRequirement] = Field(..., description="Skills logically required")
    skills_by_category: Dict[SkillCategory, List[SkillRequirement]] = Field(..., description="Skills organized by category")
    skills_by_importance: Dict[PriorityLevel, List[SkillRequirement]] = Field(..., description="Skills organized by importance")
    critical_skill_gaps: List[str] = Field(..., description="Critical skills that might be missing")
    recommendations: List[str] = Field(..., description="Recommendations for skill requirements")
    technology_stack: List[str] = Field(..., description="Recommended technology stack")

class ProjectClassification(BaseModel):
    """Final project classification"""
    project_type: ProjectType = Field(..., description="Final project type classification")
    primary_category: str = Field(..., description="Primary project category")
    subcategory: str = Field(..., description="Project subcategory")
    industry_classification: str = Field(..., description="Industry-specific classification")
    complexity_level: ComplexityLevel = Field(..., description="Confirmed complexity assessment")
    project_management_approach: str = Field(..., description="Recommended project management methodology")
    estimated_team_size: str = Field(..., description="Estimated team size needed")
    estimated_duration: str = Field(..., description="Estimated project duration")
    resource_requirements: List[str] = Field(..., description="Resource requirements")
    project_characteristics: List[str] = Field(..., description="Key project characteristics")

class ProjectSection(BaseModel):
    """Individual section of the project document"""
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")
    subsections: Optional[List['ProjectSection']] = Field(None, description="Subsections if any")

class RefinedProjectDescription(BaseModel):
    """Final refined project description document"""
    executive_summary: str = Field(..., description="Executive summary of the project")
    project_overview: ProjectSection = Field(..., description="Project overview and objectives")
    scope_of_work: ProjectSection = Field(..., description="Detailed scope of work")
    technical_requirements: ProjectSection = Field(..., description="Technical requirements and skills")
    deliverables: ProjectSection = Field(..., description="Deliverables and acceptance criteria")
    timeline: ProjectSection = Field(..., description="Timeline and milestones")
    risk_assessment: ProjectSection = Field(..., description="Risk assessment and mitigation")
    assumptions_constraints: ProjectSection = Field(..., description="Assumptions and constraints")
    success_criteria: ProjectSection = Field(..., description="Success criteria")
    next_steps: ProjectSection = Field(..., description="Next steps and recommendations")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata about the document")

# Main output schema
class JobRefinerCrewOutput(BaseModel):
    """Complete output from the Job Description Refiner Crew"""
    project_analysis: ProjectAnalysis = Field(..., description="Initial project analysis")
    ambiguity_analysis: AmbiguityAnalysis = Field(..., description="Ambiguity detection and questions")
    client_interaction: ClientInteractionSummary = Field(..., description="Client interaction summary")
    skills_analysis: SkillsAnalysis = Field(..., description="Technical skills analysis")
    project_classification: ProjectClassification = Field(..., description="Final project classification")
    refined_description: RefinedProjectDescription = Field(..., description="Final refined project description")
    
    # Metadata
    processing_timestamp: str = Field(..., description="When the processing was completed")
    total_processing_time: Optional[float] = Field(None, description="Total processing time in seconds")
    crew_version: str = Field(..., description="Version of the crew that processed this")
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_analysis": {
                    "project_type": "project",
                    "complexity_level": "moderate",
                    "primary_industry": "Technology",
                    "scope_breakdown": ["Frontend development", "Backend API", "Database design"],
                    "risk_assessment": ["Timeline constraints", "Technical complexity"],
                    "recommended_next_steps": ["Clarify timeline", "Define technical requirements"]
                },
                "processing_timestamp": "2024-01-15T10:30:00Z",
                "crew_version": "1.0.0"
            }
        }

# Utility schemas for API responses
class JobRefinerRequest(BaseModel):
    """Input request for job refiner crew"""
    raw_description: str = Field(..., description="Raw project description from user")
    client_responses: Optional[List[ClientResponse]] = Field(None, description="Client responses to clarification questions")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences for processing")

class JobRefinerResponse(BaseModel):
    """API response from job refiner crew"""
    success: bool = Field(..., description="Whether the processing was successful")
    data: Optional[JobRefinerCrewOutput] = Field(None, description="Processed output data")
    error: Optional[str] = Field(None, description="Error message if processing failed")
    message: str = Field(..., description="Response message")
    processing_id: str = Field(..., description="Unique processing identifier")

# Update the forward reference
ProjectSection.model_rebuild()
