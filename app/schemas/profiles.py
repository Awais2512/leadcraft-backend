from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    services: Optional[str] = None
    skills: Optional[List[str]] = None
    hourly_rate: Optional[float] = None
    availability: Optional[str] = None
    tone_default: Optional[str] = None
    experienced_years: Optional[int] = Field(default=0, ge=0, le=80)

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: str
    user_id: str

class ProfileListResponse(BaseModel):
    profile: list[ProfileResponse]
