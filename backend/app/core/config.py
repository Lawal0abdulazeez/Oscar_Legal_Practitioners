from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, Field, PostgresDsn, validator
from typing import Optional, List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "Oscar Legal Practitioners"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database - enforced from environment
    POSTGRES_USER: str = Field(..., description="Database username")
    POSTGRES_PASSWORD: str = Field(..., description="Database password")
    POSTGRES_SERVER: str = Field(..., description="Database host")
    POSTGRES_PORT: str = Field("5432", description="Database port")
    POSTGRES_DB: str = Field(..., description="Database name")
    
    # Internal Database URL (constructed from above)
    SQLALCHEMY_DATABASE_URL: Optional[str] = None

    # Security - CRITICAL: Must be in .env
    SECRET_KEY: str = Field(..., description="Secret key for JWT")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - Load as valid JSON list or use default for dev
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("SQLALCHEMY_DATABASE_URL", pre=True, allow_reuse=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, any]) -> any:
        if isinstance(v, str):
            return v
        
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        ).unicode_string()

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
