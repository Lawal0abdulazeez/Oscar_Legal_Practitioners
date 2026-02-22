from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, Field, field_validator
from typing import Optional, List, Union, Any

class Settings(BaseSettings):
    PROJECT_NAME: str = "Oscar Legal Practitioners"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database - enforced from environment
    POSTGRES_USER: str = Field("postgres", description="Database username")
    POSTGRES_PASSWORD: str = Field("postgres", description="Database password")
    POSTGRES_SERVER: str = Field("localhost", description="Database host")
    POSTGRES_PORT: str = Field("5432", description="Database port")
    POSTGRES_DB: str = Field("oscar_legal", description="Database name")
    
    # Internal Database URL (constructed from above)
    SQLALCHEMY_DATABASE_URL: Optional[str] = None

    # Security - CRITICAL: Must be in .env
    SECRET_KEY: str = Field("changeme", description="Secret key for JWT")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - Allow list of strings or Any Http Url
    BACKEND_CORS_ORIGINS: List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @field_validator("SQLALCHEMY_DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        if isinstance(v, str) and v:
            return v
        
        # Access values from info.data
        data = info.data
        user = data.get("POSTGRES_USER")
        password = data.get("POSTGRES_PASSWORD")
        host = data.get("POSTGRES_SERVER")
        port = data.get("POSTGRES_PORT")
        db = data.get("POSTGRES_DB")
        
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
