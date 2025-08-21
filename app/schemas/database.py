from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

# Database table schemas for Job Refiner Crew

class JobRefinerSession(BaseModel):
    """Database schema for job refiner processing sessions"""
    id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User ID who owns the session")
    raw_description: str = Field(..., description="Original raw project description")
    status: str = Field(..., description="Current session status")
    initial_analysis: Optional[Dict[str, Any]] = Field(None, description="Initial project analysis")
    ambiguity_analysis: Optional[Dict[str, Any]] = Field(None, description="Ambiguity detection results")
    client_responses: Optional[Dict[str, Any]] = Field(None, description="Client feedback responses")
    refined_analysis: Optional[Dict[str, Any]] = Field(None, description="Refined analysis with feedback")
    project_id: Optional[str] = Field(None, description="Final project ID if completed")
    created_at: str = Field(..., description="Session creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    finalized_at: Optional[str] = Field(None, description="Finalization timestamp")

class Project(BaseModel):
    """Database schema for finalized projects"""
    id: str = Field(..., description="Unique project identifier")
    user_id: str = Field(..., description="User ID who owns the project")
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="Project description")
    raw_description: str = Field(..., description="Original raw description")
    project_type: str = Field(..., description="Type of project (job, project, service, etc.)")
    complexity_level: str = Field(..., description="Project complexity level")
    industry: str = Field(..., description="Primary industry")
    category: str = Field(..., description="Project category")
    subcategory: str = Field(..., description="Project subcategory")
    estimated_duration: str = Field(..., description="Estimated project duration")
    estimated_team_size: str = Field(..., description="Estimated team size needed")
    project_management_approach: str = Field(..., description="Recommended project management approach")
    status: str = Field(..., description="Project status")
    created_at: str = Field(..., description="Project creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

class ProjectRequirements(BaseModel):
    """Database schema for detailed project requirements"""
    id: str = Field(..., description="Unique requirements identifier")
    project_id: str = Field(..., description="Associated project ID")
    scope_of_work: str = Field(..., description="Detailed scope of work")
    technical_requirements: str = Field(..., description="Technical requirements")
    deliverables: str = Field(..., description="Project deliverables")
    timeline: str = Field(..., description="Project timeline")
    risk_assessment: str = Field(..., description="Risk assessment and mitigation")
    assumptions_constraints: str = Field(..., description="Assumptions and constraints")
    success_criteria: str = Field(..., description="Success criteria")
    next_steps: str = Field(..., description="Next steps and recommendations")
    created_at: str = Field(..., description="Creation timestamp")

class ProjectSkill(BaseModel):
    """Database schema for project skills"""
    id: str = Field(..., description="Unique skill identifier")
    project_id: str = Field(..., description="Associated project ID")
    skill_name: str = Field(..., description="Skill name")
    category: str = Field(..., description="Skill category")
    importance: str = Field(..., description="Skill importance level")
    proficiency_level: str = Field(..., description="Required proficiency level")
    is_explicit: bool = Field(..., description="Whether skill was explicitly mentioned")
    created_at: str = Field(..., description="Creation timestamp")

# SQL table creation scripts
SQL_CREATE_TABLES = """
-- Job Refiner Sessions Table
CREATE TABLE IF NOT EXISTS job_refiner_sessions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    raw_description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'initial_processed',
    initial_analysis JSONB,
    ambiguity_analysis JSONB,
    client_responses JSONB,
    refined_analysis JSONB,
    project_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finalized_at TIMESTAMP WITH TIME ZONE
);

-- Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    raw_description TEXT NOT NULL,
    project_type VARCHAR(100) NOT NULL,
    complexity_level VARCHAR(50) NOT NULL,
    industry VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100) NOT NULL,
    estimated_duration VARCHAR(100) NOT NULL,
    estimated_team_size VARCHAR(100) NOT NULL,
    project_management_approach VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Project Requirements Table
CREATE TABLE IF NOT EXISTS project_requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    scope_of_work TEXT NOT NULL,
    technical_requirements TEXT NOT NULL,
    deliverables TEXT NOT NULL,
    timeline TEXT NOT NULL,
    risk_assessment TEXT NOT NULL,
    assumptions_constraints TEXT NOT NULL,
    success_criteria TEXT NOT NULL,
    next_steps TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Project Skills Table
CREATE TABLE IF NOT EXISTS project_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    skill_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    importance VARCHAR(50) NOT NULL,
    proficiency_level VARCHAR(100) NOT NULL,
    is_explicit BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_job_refiner_sessions_user_id ON job_refiner_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_job_refiner_sessions_status ON job_refiner_sessions(status);
CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_project_requirements_project_id ON project_requirements(project_id);
CREATE INDEX IF NOT EXISTS idx_project_skills_project_id ON project_skills(project_id);
CREATE INDEX IF NOT EXISTS idx_project_skills_category ON project_skills(category);

-- Row Level Security (RLS) policies
ALTER TABLE job_refiner_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_requirements ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_skills ENABLE ROW LEVEL SECURITY;

-- RLS Policies for job_refiner_sessions
CREATE POLICY "Users can view their own sessions" ON job_refiner_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own sessions" ON job_refiner_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own sessions" ON job_refiner_sessions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own sessions" ON job_refiner_sessions
    FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for projects
CREATE POLICY "Users can view their own projects" ON projects
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own projects" ON projects
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own projects" ON projects
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own projects" ON projects
    FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for project_requirements
CREATE POLICY "Users can view requirements for their own projects" ON project_requirements
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM projects 
            WHERE projects.id = project_requirements.project_id 
            AND projects.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert requirements for their own projects" ON project_requirements
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM projects 
            WHERE projects.id = project_requirements.project_id 
            AND projects.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update requirements for their own projects" ON project_requirements
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM projects 
            WHERE projects.id = project_requirements.project_id 
            AND projects.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete requirements for their own projects" ON project_requirements
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM projects 
            WHERE projects.id = project_requirements.project_id 
            AND projects.user_id = auth.uid()
        )
    );

-- RLS Policies for project_skills
CREATE POLICY "Users can view skills for their own projects" ON project_skills
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM projects 
            WHERE projects.id = project_skills.project_id 
            AND projects.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert skills for their own projects" ON project_skills
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM projects 
            WHERE projects.id = project_skills.project_id 
            AND projects.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update skills for their own projects" ON project_skills
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM projects 
            WHERE projects.id = project_skills.project_id 
            AND projects.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete skills for their own projects" ON project_skills
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM projects 
            WHERE projects.id = project_skills.project_id 
            AND projects.user_id = auth.uid()
        )
    );
"""

# Database utility functions
class DatabaseUtils:
    @staticmethod
    def create_tables(supabase_client):
        """Create all required tables for the job refiner system"""
        try:
            # Execute the SQL script
            result = supabase_client.rpc('exec_sql', {'sql': SQL_CREATE_TABLES}).execute()
            return {"success": True, "message": "Tables created successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def check_table_exists(supabase_client, table_name: str):
        """Check if a table exists in the database"""
        try:
            result = supabase_client.table(table_name).select("id").limit(1).execute()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_table_info(supabase_client, table_name: str):
        """Get information about a table structure"""
        try:
            # This is a simplified approach - in production you might want to use
            # proper schema introspection
            result = supabase_client.table(table_name).select("*").limit(1).execute()
            if result.data:
                return {
                    "table_name": table_name,
                    "has_data": True,
                    "sample_record": result.data[0]
                }
            else:
                return {
                    "table_name": table_name,
                    "has_data": False,
                    "sample_record": None
                }
        except Exception as e:
            return {
                "table_name": table_name,
                "error": str(e)
            }
