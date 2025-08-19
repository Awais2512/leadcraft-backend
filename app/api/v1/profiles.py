from fastapi import APIRouter, Depends
from app.core.security import verify_jwt
from app.services.supabase_client import supabase
from app.schemas.profiles import ProfileUpdate, ProfileResponse, ProfileListResponse

router = APIRouter()

@router.get("/me", response_model=ProfileListResponse)
def get_profile(user=Depends(verify_jwt)):
    user_id = user["sub"]
    profile = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    return {"profile": [ProfileResponse(**p) for p in profile.data]}

@router.post("/update", response_model=ProfileListResponse)
def update_profile(data: ProfileUpdate, user=Depends(verify_jwt)):
    user_id = user["sub"]
    updated = supabase.table("profiles").update(data.dict(exclude_unset=True)).eq("user_id", user_id).execute()
    return {"profile": [ProfileResponse(**p) for p in updated.data]}
