import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # API
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "RscoutX API"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./rscoutx.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    # LLM
    LLM_PROVIDER: str = "openai"  # openai or ollama
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2"
    
    # Scraper
    SCRAPER_CACHE_MINUTES: int = 30
    SCRAPER_TIMEOUT_SECONDS: int = 30
    SCRAPER_MAX_RETRIES: int = 3
    SCRAPER_CACHE_TTL_MINUTES: int = 30
    ROBOTEVENTS_API_KEY: Optional[str] = None  # Add your RobotEvents API key here
    
    # Path Rendering
    # Use absolute path to avoid issues with working directory
    MAP_IMAGE_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "pushback_map.png")
    DEFAULT_MAP_WIDTH: int = 3600
    DEFAULT_MAP_HEIGHT: int = 3600
    FIELD_WIDTH_MM: int = 3600
    FIELD_HEIGHT_MM: int = 3600
    
    # SSL
    SSL_CERTFILE: Optional[str] = None
    SSL_KEYFILE: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
