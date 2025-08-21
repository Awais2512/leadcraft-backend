from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from app.core.security import verify_jwt
from app.services.supabase_client import supabase
from app.agents.job_refiner_crew import JobRefinerCrew
from app.schemas.job_refiner import (
    JobRefinerRequest, JobRefinerResponse, JobRefinerCrewOutput,
    ClientResponse, ProjectAnalysis, AmbiguityAnalysis
)

router = APIRouter(prefix="/job-refiner", tags=["Job Description Refiner"])

# Initialize the crew lazily
def get_crew():
    """Get JobRefinerCrew instance"""
    return JobRefinerCrew()

# In-memory storage for processing sessions (in production, use Redis or database)
processing_sessions = {}

@router.post("/process-initial", response_model=JobRefinerResponse)
async def process_initial_description(
    request: JobRefinerRequest,
    user=Depends(verify_jwt),
    background_tasks: BackgroundTasks = None
):
    """
    Process initial raw project description and generate clarification questions.
    
    This endpoint:
    1. Analyzes the raw description
    2. Identifies ambiguities
    3. Generates clarification questions
    4. Returns initial analysis and questions for client
    """
    try:
        user_id = user["sub"]
        
        # Generate unique processing ID
        processing_id = str(uuid.uuid4())
        
        # Process the initial description
        print(f"🚀 Processing initial description for user {user_id}")
        crew = get_crew()
        result = crew.process_project_description(request)
        
        # Store the result in processing sessions
        processing_sessions[processing_id] = {
            "user_id": user_id,
            "initial_request": request.dict(),
            "initial_result": result.dict(),
            "status": "initial_processed",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Save to database for tracking
        session_record = supabase.table("job_refiner_sessions").insert({
            "id": processing_id,
            "user_id": user_id,
            "raw_description": request.raw_description,
            "status": "initial_processed",
            "initial_analysis": result.project_analysis.dict(),
            "ambiguity_analysis": result.ambiguity_analysis.dict(),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }).execute()
        
        # Return initial analysis and questions
        return JobRefinerResponse(
            success=True,
            data=result,
            message="Initial description processed successfully. Clarification questions generated.",
            processing_id=processing_id
        )
        
    except Exception as e:
        print(f"❌ Error processing initial description: {e}")
        return JobRefinerResponse(
            success=False,
            data=None,
            error=str(e),
            message="Failed to process initial description",
            processing_id=""
        )

@router.post("/submit-client-feedback/{processing_id}", response_model=JobRefinerResponse)
async def submit_client_feedback(
    processing_id: str,
    client_responses: List[ClientResponse],
    user=Depends(verify_jwt)
):
    """
    Submit client responses to clarification questions and re-process the description.
    
    This endpoint:
    1. Receives client feedback on clarification questions
    2. Integrates feedback into the project context
    3. Re-processes the description with enhanced information
    4. Returns refined project description
    """
    try:
        user_id = user["sub"]
        
        # Verify processing session exists and belongs to user
        if processing_id not in processing_sessions:
            raise HTTPException(status_code=404, detail="Processing session not found")
        
        session = processing_sessions[processing_id]
        if session["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Access denied to this session")
        
        # Update session with client responses
        session["client_responses"] = [resp.dict() for resp in client_responses]
        session["status"] = "feedback_received"
        session["updated_at"] = datetime.utcnow().isoformat()
        
        # Create new request with client feedback
        updated_request = JobRefinerRequest(
            raw_description=session["initial_request"]["raw_description"],
            client_responses=client_responses,
            user_preferences=session["initial_request"].get("user_preferences", {})
        )
        
        # Re-process with client feedback
        print(f"🔄 Re-processing description with client feedback for session {processing_id}")
        crew = get_crew()
        refined_result = crew.process_project_description(updated_request)
        
        # Update session with refined result
        session["refined_result"] = refined_result.dict()
        session["status"] = "refined_completed"
        session["updated_at"] = datetime.utcnow().isoformat()
        
        # Update database
        supabase.table("job_refiner_sessions").update({
            "status": "refined_completed",
            "client_responses": [resp.dict() for resp in client_responses],
            "refined_analysis": refined_result.dict(),
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", processing_id).execute()
        
        return JobRefinerResponse(
            success=True,
            data=refined_result,
            message="Description refined successfully with client feedback",
            processing_id=processing_id
        )
        
    except Exception as e:
        print(f"❌ Error processing client feedback: {e}")
        return JobRefinerResponse(
            success=False,
            data=None,
            error=str(e),
            message="Failed to process client feedback",
            processing_id=processing_id
        )

@router.post("/finalize-description/{processing_id}")
async def finalize_description(
    processing_id: str,
    final_data: Dict[str, Any],
    user=Depends(verify_jwt)
):
    """
    Finalize the refined project description and save to database.
    
    This endpoint:
    1. Receives final approval from frontend
    2. Saves the complete project description to database
    3. Creates project/job records
    4. Marks session as completed
    """
    try:
        user_id = user["sub"]
        
        # Verify processing session exists and belongs to user
        if processing_id not in processing_sessions:
            raise HTTPException(status_code=404, detail="Processing session not found")
        
        session = processing_sessions[processing_id]
        if session["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Access denied to this session")
        
        # Verify session has refined result
        if "refined_result" not in session:
            raise HTTPException(status_code=400, detail="Description must be refined before finalization")
        
        # Extract project information
        refined_result = session["refined_result"]
        project_analysis = refined_result["project_analysis"]
        project_classification = refined_result["project_classification"]
        refined_description = refined_result["refined_description"]
        
        # Save to projects table
        project_data = {
            "user_id": user_id,
            "title": final_data.get("title", "Untitled Project"),
            "description": refined_description["executive_summary"],
            "raw_description": session["initial_request"]["raw_description"],
            "project_type": project_analysis["project_type"],
            "complexity_level": project_analysis["complexity_level"],
            "industry": project_analysis["primary_industry"],
            "category": project_classification["primary_category"],
            "subcategory": project_classification["subcategory"],
            "estimated_duration": project_classification["estimated_duration"],
            "estimated_team_size": project_classification["estimated_team_size"],
            "project_management_approach": project_classification["project_management_approach"],
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        project_record = supabase.table("projects").insert(project_data).execute()
        project_id = project_record.data[0]["id"] if project_record.data else None
        
        # Save detailed requirements
        if project_id:
            requirements_data = {
                "project_id": project_id,
                "scope_of_work": refined_description.get("scope_of_work", {}).get("content", ""),
                "technical_requirements": refined_description.get("technical_requirements", {}).get("content", ""),
                "deliverables": refined_description.get("deliverables", {}).get("content", ""),
                "timeline": refined_description.get("timeline", {}).get("content", ""),
                "risk_assessment": refined_description.get("risk_assessment", {}).get("content", ""),
                "assumptions_constraints": refined_description.get("assumptions_constraints", {}).get("content", ""),
                "success_criteria": refined_description.get("success_criteria", {}).get("content", ""),
                "next_steps": refined_description.get("next_steps", {}).get("content", ""),
                "created_at": datetime.utcnow().isoformat()
            }
            
            supabase.table("project_requirements").insert(requirements_data).execute()
        
        # Save skills analysis
        if project_id:
            skills_analysis = refined_result["skills_analysis"]
            for skill_category, skills in skills_analysis["skills_by_category"].items():
                for skill in skills:
                    skill_data = {
                        "project_id": project_id,
                        "skill_name": skill["skill_name"],
                        "category": skill["category"],
                        "importance": skill["importance"],
                        "proficiency_level": skill["proficiency_level"],
                        "is_explicit": skill["is_explicit"],
                        "created_at": datetime.utcnow().isoformat()
                    }
                    supabase.table("project_skills").insert(skill_data).execute()
        
        # Update session status
        session["status"] = "completed"
        session["project_id"] = project_id
        session["updated_at"] = datetime.utcnow().isoformat()
        
        # Update database session
        supabase.table("job_refiner_sessions").update({
            "status": "completed",
            "project_id": project_id,
            "finalized_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", processing_id).execute()
        
        return {
            "success": True,
            "message": "Project description finalized and saved successfully",
            "project_id": project_id,
            "processing_id": processing_id
        }
        
    except Exception as e:
        print(f"❌ Error finalizing description: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to finalize project description"
        }

@router.get("/session/{processing_id}")
async def get_session_status(
    processing_id: str,
    user=Depends(verify_jwt)
):
    """
    Get the current status and data of a processing session.
    """
    try:
        user_id = user["sub"]
        
        # Check in-memory sessions first
        if processing_id in processing_sessions:
            session = processing_sessions[processing_id]
            if session["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="Access denied to this session")
            return session
        
        # Check database
        db_session = supabase.table("job_refiner_sessions").select("*").eq("id", processing_id).eq("user_id", user_id).single().execute()
        
        if not db_session.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return db_session.data
        
    except Exception as e:
        print(f"❌ Error retrieving session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-sessions")
async def get_user_sessions(
    user=Depends(verify_jwt),
    limit: int = 10,
    offset: int = 0
):
    """
    Get all processing sessions for the current user.
    """
    try:
        user_id = user["sub"]
        
        sessions = supabase.table("job_refiner_sessions").select("*").eq("user_id", user_id).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
        
        return {
            "sessions": sessions.data,
            "total": len(sessions.data),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        print(f"❌ Error retrieving user sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{processing_id}")
async def delete_session(
    processing_id: str,
    user=Depends(verify_jwt)
):
    """
    Delete a processing session.
    """
    try:
        user_id = user["sub"]
        
        # Check if session exists and belongs to user
        db_session = supabase.table("job_refiner_sessions").select("*").eq("id", processing_id).eq("user_id", user_id).single().execute()
        
        if not db_session.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Delete from database
        supabase.table("job_refiner_sessions").delete().eq("id", processing_id).execute()
        
        # Remove from in-memory storage
        if processing_id in processing_sessions:
            del processing_sessions[processing_id]
        
        return {"success": True, "message": "Session deleted successfully"}
        
    except Exception as e:
        print(f"❌ Error deleting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/crew-info")
async def get_crew_information():
    """
    Get information about the Job Refiner Crew configuration.
    """
    try:
        crew = get_crew()
        crew_info = crew.get_crew_info()
        return {
            "success": True,
            "crew_info": crew_info
        }
    except Exception as e:
        print(f"❌ Error retrieving crew info: {e}")
        return {
            "success": False,
            "error": str(e)
        }
