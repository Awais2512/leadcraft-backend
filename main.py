from fastapi import FastAPI
from app.api.v1 import auth, profiles, jobs, proposals, simple_job_refiner

app = FastAPI(title="LeadCraft Backend")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["profiles"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(proposals.router, prefix="/api/v1/proposals", tags=["proposals"])
app.include_router(simple_job_refiner.router, prefix="/api/v1", tags=["job-refiner"])


if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",port=8000,reload=True)