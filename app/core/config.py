from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL:str
    SUPABASE_KEY:str
    SUPABASE_JWT_SECRET:str

    GEMINI_API_KEY:str
    OPENAI_API_KEY:str

    API_PREFIX:str = "/api"
    DEBUG:bool = True
    PORT:str = "8000"
    ALLOWED_ORIGINS:list = ["*"]


    SUPABASE_AUDIENCE:str = "authenticated"
    SUPABASE_PROJECT_ID:str
    SUPABASE_ANON_KEY : str
    SUPABASE_SERVICE_ROLE_KEY :str

    DATABASE_URL:str
    
    class Config:
        env_file = ".env"

settings = Settings()
