from fastapi import APIRouter, Depends, HTTPException
from app.core.security import verify_jwt
from app.services.supabase_client import supabase
from app.services.ai_stub import generate_proposal
from app.schemas.proposals import ProposalCreate, ProposalResponse, ProposalListResponse

router = APIRouter()

@router.post("/", response_model=ProposalResponse)
def create_proposal(data: ProposalCreate, user=Depends(verify_jwt)):
    user_id = user["sub"]

    job = supabase.table("jobs").select("*").eq("id", data.job_id).single().execute()
    if not job.data:
        raise HTTPException(status_code=404, detail="Job not found")

    profile = supabase.table("profiles").select("*").eq("user_id", user_id).single().execute()
    if not profile.data:
        raise HTTPException(status_code=404, detail="Profile not found")

    proposal_text = generate_proposal(job.data, profile.data, tone=data.tone)

    proposal = supabase.table("proposals").insert({
        "user_id": user_id,
        "job_id": data.job_id,
        "content": proposal_text,
        "tone": data.tone or profile.data.get("tone_default"),
        "status": "draft"
    }).execute()

    return ProposalResponse(**proposal.data[0])

@router.get("/", response_model=ProposalListResponse)
def list_proposals(user=Depends(verify_jwt)):
    user_id = user["sub"]
    proposals = supabase.table("proposals").select("*").eq("user_id", user_id).execute()
    return {"proposals": [ProposalResponse(**p) for p in proposals.data]}
