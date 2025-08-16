from fastapi import APIRouter, Depends
from app.core.security import verify_jwt
from app.services.supabase_client import supabase
from app.services.ai_stub import generate_proposal

router = APIRouter()

@router.post("/")
def create_proposal(data: dict, user=Depends(verify_jwt)):
    user_id = user["sub"]
    job_id = data["job_id"]

    job = supabase.table("jobs").select("*").eq("id", job_id).single().execute()
    profile = supabase.table("profiles").select("*").eq("user_id", user_id).single().execute()

    proposal_text = generate_proposal(job.data, profile.data, tone=data.get("tone"))

    proposal = supabase.table("proposals").insert({
        "user_id": user_id,
        "job_id": job_id,
        "content": proposal_text,
        "tone": data.get("tone", profile.data.get("tone_default")),
        "status": "draft"
    }).execute()

    return {"proposal": proposal.data}
