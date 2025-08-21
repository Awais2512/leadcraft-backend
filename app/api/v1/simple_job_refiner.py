from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import uuid

from app.core.security import verify_jwt
from app.services.supabase_client import supabase

router = APIRouter(prefix="/job-refiner", tags=["Job Refiner"])

# Simple request/response models
class InitialProcessRequest(BaseModel):
    raw_description: str

class Question(BaseModel):
    id: str
    question: str
    category: str
    priority: str

class InitialProcessResponse(BaseModel):
    success: bool
    session_id: str
    refined_description: str
    title: str
    project_type: str
    questions: List[Question]
    message: str

class QuestionAnswer(BaseModel):
    question_id: str
    question: str
    answer: Optional[str] = None
    skipped: bool = False

class RefineRequest(BaseModel):
    session_id: str
    previous_refined_description: str
    title: str
    project_type: str
    answers: List[QuestionAnswer]

class RefineResponse(BaseModel):
    success: bool
    session_id: str
    final_refined_description: str
    title: str
    project_type: str
    message: str

# In-memory storage for sessions (simple approach)
sessions = {}

@router.post("/process-initial", response_model=InitialProcessResponse)
async def process_initial(
    request: InitialProcessRequest,
    user=Depends(verify_jwt)
):
    """
    Process raw description and generate initial refined description with questions.
    """
    try:
        user_id = user["sub"]
        session_id = str(uuid.uuid4())
        
        # Import crew here to avoid initialization issues
        from app.agents.simple_refiner_crew import SimpleRefinerCrew
        
        crew = SimpleRefinerCrew()
        result = crew.process_initial(request.raw_description)
        
        # Store session data
        sessions[session_id] = {
            "user_id": user_id,
            "raw_description": request.raw_description,
            "refined_description": result["refined_description"],
            "title": result["title"],
            "project_type": result["project_type"],
            "questions": result["questions"],
            "status": "initial_processed",
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Save to database
        supabase.table("job_sessions").insert({
            "id": session_id,
            "user_id": user_id,
            "raw_description": request.raw_description,
            "refined_description": result["refined_description"],
            "title": result["title"],
            "project_type": result["project_type"],
            "questions": result["questions"],
            "status": "initial_processed",
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        
        return InitialProcessResponse(
            success=True,
            session_id=session_id,
            refined_description=result["refined_description"],
            title=result["title"],
            project_type=result["project_type"],
            questions=[Question(**q) for q in result["questions"]],
            message="Initial processing completed successfully"
        )
        
    except Exception as e:
        print(f"❌ Error in initial processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refine-with-answers", response_model=RefineResponse)
async def refine_with_answers(
    request: RefineRequest,
    user=Depends(verify_jwt)
):
    """
    Re-refine description with client answers to questions.
    """
    try:
        user_id = user["sub"]
        
        # Verify session belongs to user
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[request.session_id]
        if session["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Import crew here
        from app.agents.simple_refiner_crew import SimpleRefinerCrew
        
        crew = SimpleRefinerCrew()
        result = crew.refine_with_answers(
            previous_refined_description=request.previous_refined_description,
            title=request.title,
            project_type=request.project_type,
            answers=request.answers
        )
        
        # Update session
        session.update({
            "final_refined_description": result["final_refined_description"],
            "answers": [ans.dict() for ans in request.answers],
            "status": "refined_completed",
            "updated_at": datetime.utcnow().isoformat()
        })
        
        # Update database
        supabase.table("job_sessions").update({
            "final_refined_description": result["final_refined_description"],
            "answers": [ans.dict() for ans in request.answers],
            "status": "refined_completed",
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", request.session_id).execute()
        
        return RefineResponse(
            success=True,
            session_id=request.session_id,
            final_refined_description=result["final_refined_description"],
            title=request.title,
            project_type=request.project_type,
            message="Description refined successfully with client answers"
        )
        
    except Exception as e:
        print(f"❌ Error in refining: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    user=Depends(verify_jwt)
):
    """Get session data."""
    try:
        user_id = user["sub"]
        
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[session_id]
        if session["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return session
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/finalize/{session_id}")
async def finalize_project(
    session_id: str,
    final_data: Dict[str, Any],
    user=Depends(verify_jwt)
):
    """
    Finalize the project and save to projects table.
    """
    try:
        user_id = user["sub"]
        
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[session_id]
        if session["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Create project record
        project_data = {
            "user_id": user_id,
            "title": final_data.get("title", session.get("title")),
            "description": session.get("final_refined_description", session.get("refined_description")),
            "raw_description": session.get("raw_description"),
            "project_type": session.get("project_type"),
            "status": "active",
            "created_at": datetime.utcnow().isoformat()
        }
        
        project = supabase.table("projects").insert(project_data).execute()
        project_id = project.data[0]["id"]
        
        # Update session
        session["project_id"] = project_id
        session["status"] = "completed"
        
        supabase.table("job_sessions").update({
            "project_id": project_id,
            "status": "completed"
        }).eq("id", session_id).execute()
        
        return {
            "success": True,
            "project_id": project_id,
            "message": "Project finalized successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

