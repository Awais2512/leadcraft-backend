from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any

class JobCreate(BaseModel):
    platform: str
    title: str
    raw_post: str
    url: Optional[HttpUrl] = None

class JobParsed(BaseModel):
    skills: list[str]
    deliverables: list[str]
    budget_hint: Optional[str] = None

class JobResponse(BaseModel):
    id: str
    user_id: str
    platform: str
    title: str
    url: Optional[str]
    raw_post: str
    parsed_needs: Dict[str, Any] | None = None
    job_type: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    status: Optional[str] = "draft"

class JobListResponse(BaseModel):
    jobs: list[JobResponse]
