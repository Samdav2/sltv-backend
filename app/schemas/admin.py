from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.admin import AdminRole
import uuid
from datetime import datetime

class AdminBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[AdminRole] = AdminRole.TEAM
    is_active: Optional[bool] = True

class AdminCreate(AdminBase):
    name: str
    email: EmailStr
    password: str
    role: AdminRole

class AdminUpdate(AdminBase):
    password: Optional[str] = None

class AdminRead(AdminBase):
    id: uuid.UUID
    name: str
    email: EmailStr
    role: AdminRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
