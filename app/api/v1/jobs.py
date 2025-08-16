from fastapi import APIRouter, Depends
from app.core.security import verify_jwt
from app.services.supabase_client import supabase
from app.services.ai_stub import parse_job_post

router = APIRouter()

@router.post("/")
def create_job(data: dict, user=Depends(verify_jwt)):
    user_id = user["sub"]
    raw_post = data.get("raw_post", "")
    parsed = parse_job_post(raw_post)

    job = supabase.table("jobs").insert({
        "user_id": user_id,
        "platform": data.get("platform", "upwork"),
        "title": data.get("title"),
        "url": data.get("url"),
        "raw_post": raw_post,
        "parsed_needs": parsed,
    }).execute()

    return {"job": job.data}
