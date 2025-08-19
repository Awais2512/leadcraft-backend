from fastapi import APIRouter, Depends
from app.core.security import verify_jwt
from app.schemas.auth import AuthMeResponse, UserPayload

router = APIRouter()

@router.get("/me", response_model=AuthMeResponse)
def get_me(user=Depends(verify_jwt)):
    # Wrap JWT payload in Pydantic model
    return {"user": UserPayload(**user)}
