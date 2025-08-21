from app.agents.job_refiner_crew import JobRefinerCrew

# Initialize crew_runner as None - will be instantiated when needed
crew_runner = None

def get_job_refiner_crew():
    """Get or create JobRefinerCrew instance"""
    global crew_runner
    if crew_runner is None:
        crew_runner = JobRefinerCrew()
    return crew_runner 