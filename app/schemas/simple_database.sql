-- Simple Job Refiner Database Schema
-- Job Sessions Table (simplified)
CREATE TABLE IF NOT EXISTS job_sessions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    raw_description TEXT NOT NULL,
    refined_description TEXT,
    final_refined_description TEXT,
    title VARCHAR(255),
    project_type VARCHAR(100),
    questions JSONB,
    answers JSONB,
    status VARCHAR(50) NOT NULL DEFAULT 'initial_processed',
    project_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- Simple Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    raw_description TEXT NOT NULL,
    project_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- Indexes
CREATE INDEX IF NOT EXISTS idx_job_sessions_user_id ON job_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_job_sessions_status ON job_sessions(status);
CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id);
-- RLS Policies
ALTER TABLE job_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
-- Job Sessions RLS
CREATE POLICY "Users can manage their own job sessions" ON job_sessions FOR ALL USING (auth.uid() = user_id);
-- Projects RLS  
CREATE POLICY "Users can manage their own projects" ON projects FOR ALL USING (auth.uid() = user_id);
