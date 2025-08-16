from fastapi import APIRouter, Depends
from app.core.security import verify_jwt
from app.services.supabase_client import supabase

router = APIRouter()

@router.get("/me")
def get_profile(user=Depends(verify_jwt)):
    user_id = user["sub"]
    profile = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    return {"profile": profile.data}


@router.post("/update")
def create_or_update_profile(data: dict, user=Depends(verify_jwt)):
    user_id = user["sub"]
    existing_profile = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    
    if existing_profile.data:
        updated = supabase.table("profiles").update(data).eq("user_id", user_id).execute()
        return {"updated": updated.data}
    else:
        try:
            data["user_id"] = user_id
            data["user_id"] = user_id
            created = supabase.table("profiles").insert(data).execute()
            return {"created": created.data}
        except Exception as e:
            return {"error": str(e)}
