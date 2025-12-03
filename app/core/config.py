from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "VTU Backend"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./vtu.db"
    SECRET_KEY: str = "changethis"
    ALGORITHM: str = "RS256"

    @property
    def JWT_PRIVATE_KEY(self) -> str:
        with open("certs/private.pem", "r") as f:
            return f.read()

    @property
    def JWT_PUBLIC_KEY(self) -> str:
        with open("certs/public.pem", "r") as f:
            return f.read()
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # MobileNig Settings
    # MobileNig Settings
    MOBILENIG_PUBLIC_KEY: str
    MOBILENIG_SECRET_KEY: str
    MOBILENIG_BASE_URL: str = "https://enterprise.mobilenig.com/api/v2"

    # Paystack Settings
    PAYSTACK_PUBLIC_KEY: str
    PAYSTACK_SECRET_KEY: str
    PAYSTACK_BASE_URL: str = "https://api.paystack.co"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
