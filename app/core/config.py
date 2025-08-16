from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL:str
    SUPABASE_KEY:str
    SUPABASE_JWT_SECRET:str


    API_PREFIX:str = "/api"
    DEBUG:bool = True
    PORT:str = "8000"

    ALLOWED_ORIGINS:list = ["*"]


    SUPABASE_ANON_KEY : str

    SUPABASE_AUDIENCE:str = "authenticated"
    SUPABASE_SERVICE_ROLE_KEY :str
    JWT_SECRET :str
    SUPABASE_JWT_ISSUER:str 
    SUPABASE_PROJECT_ID:str

    DATABASE_URL:str
    class Config:
        env_file = ".env"

settings = Settings()
