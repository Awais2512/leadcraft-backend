from fastapi import APIRouter, Depends
from app.core.security import verify_jwt

router = APIRouter()

@router.get("/me")
def get_me(user=Depends(verify_jwt)):
    return {"user": user}
