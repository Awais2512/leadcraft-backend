from pydantic import BaseModel
from typing import Optional, Dict, Any

class ProposalCreate(BaseModel):
    job_id: str
    tone: Optional[str] = "friendly"

class ProposalResponse(BaseModel):
    id: str
    job_id: str
    user_id: str
    content: str
    tone: Optional[str] = None
    includes_estimates: Optional[bool] = None
    price_quote: Optional[Dict[str, Any]] = None
    timeline_est: Optional[Dict[str, Any]] = None
    status: Optional[str] = "draft"

class ProposalListResponse(BaseModel):
    proposals: list[ProposalResponse]
