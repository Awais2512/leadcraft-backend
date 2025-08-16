def parse_job_post(text: str):
    # TODO: Replace with real AI call
    return {
        "skills": ["Python", "FastAPI"],
        "deliverables": ["Backend API", "Supabase integration"],
        "budget_hint": "$500-1000"
    }

def generate_proposal(job: dict, profile: dict, tone="friendly"):
    # TODO: Replace with real AI call
    return f"""
Hi {job.get('title', 'there')},

I understand you're looking for {job['parsed_needs'].get('deliverables', [])}.
With my {profile.get('experienced_years', 0)} years of experience in {', '.join(profile.get('skills', []))}, 
I can deliver efficiently and on time.

Looking forward to collaborating!
"""
