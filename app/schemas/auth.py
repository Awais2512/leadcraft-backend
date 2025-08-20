from pydantic import BaseModel, EmailStr
from typing import Any, Dict

class UserPayload(BaseModel):
    sub: str
    email: EmailStr | None = None
    role: str | None = None
    exp: int | None = None
    iat: int | None = None
    other_claims: Dict[str, Any] | None = None

class AuthMeResponse(BaseModel):
    user: UserPayload
