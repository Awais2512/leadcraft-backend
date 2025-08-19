from fastapi import APIRouter, Depends
from app.core.security import verify_jwt
from app.services.supabase_client import supabase
from app.services.ai_stub import parse_job_post
from app.schemas.jobs import JobCreate, JobResponse, JobListResponse

router = APIRouter()

@router.post("/", response_model=JobResponse)
def create_job(data: JobCreate, user=Depends(verify_jwt)):
    user_id = user["sub"]
    parsed = parse_job_post(data.raw_post)

    job = supabase.table("jobs").insert({
        "user_id": user_id,
        "platform": data.platform,
        "title": data.title,
        "url": str(data.url) if data.url else None,
        "raw_post": data.raw_post,
        "parsed_needs": parsed,
    }).execute()

    return JobResponse(**job.data[0])

@router.get("/", response_model=JobListResponse)
def list_jobs(user=Depends(verify_jwt)):
    user_id = user["sub"]
    jobs = supabase.table("jobs").select("*").eq("user_id", user_id).execute()
    return {"jobs": [JobResponse(**j) for j in jobs.data]}
