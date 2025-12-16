from typing import List
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "VTU Backend"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "RS256"

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://ezyvtu.com.ng",
        "https://www.ezyvtu.com.ng",
        "https://sltv-frontend.vercel.app"
    ]
    ALLOWED_HOSTS: List[str] = ["*"]

    @property
    def JWT_PRIVATE_KEY(self) -> str:
        key = os.getenv("JWT_PRIVATE_KEY")
        if key:
            return key.replace("\\n", "\n")
        try:
            with open("certs/private.pem", "r") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    @property
    def JWT_PUBLIC_KEY(self) -> str:
        key = os.getenv("JWT_PUBLIC_KEY")
        if key:
            return key.replace("\\n", "\n")
        try:
            with open("certs/public.pem", "r") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # MobileNig Settings
    MOBILENIG_PUBLIC_KEY: str = os.getenv("MOBILENIG_PUBLIC_KEY", "")
    MOBILENIG_SECRET_KEY: str = os.getenv("MOBILENIG_SECRET_KEY", "")
    MOBILENIG_BASE_URL: str = "https://enterprise.mobilenig.com/api/v2"

    # Paystack Settings
    PAYSTACK_PUBLIC_KEY: str = os.getenv("PAYSTACK_PUBLIC_KEY", "")
    PAYSTACK_SECRET_KEY: str = os.getenv("PAYSTACK_SECRET_KEY", "")
    PAYSTACK_BASE_URL: str = "https://api.paystack.co"

    # SMTP Email Settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 465))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_SSL: bool = True
    MAIL_FROM: str = os.getenv("MAIL_FROM", "")
    MAIL_FROM_NAME: str = "EZY VTU"

    # SLTV Settings
    SLTV_USERNAME: str = os.getenv("SLTV_USERNAME", "")
    SLTV_PASSWORD: str = os.getenv("SLTV_PASSWORD", "")

    # VTpass Settings
    VTPASS_API_KEY: str = os.getenv("VTPASS_API_KEY", "")
    VTPASS_PUBLIC_KEY: str = os.getenv("VTPASS_PUBLIC_KEY", "")
    VTPASS_SECRET_KEY: str = os.getenv("VTPASS_SECRET_KEY", "")
    VTPASS_BASE_URL: str = "https://sandbox.vtpass.com/api"

    # eBills Africa Settings
    EBILLS_USERNAME: str = os.getenv("EBILLS_USERNAME", "")
    EBILLS_PASSWORD: str = os.getenv("EBILLS_PASSWORD", "")
    EBILLS_BASE_URL: str = "https://ebills.africa/wp-json"


    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 465))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_SSL: bool = True
    MAIL_FROM: str = os.getenv("MAIL_FROM", "")
    MAIL_FROM_NAME: str = "EZY VTU"

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
