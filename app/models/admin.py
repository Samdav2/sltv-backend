import uuid
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field
from datetime import datetime

class AdminRole(str, Enum):
    SUPER = "super"
    MANAGER = "manager"
    TEAM = "team"

class AdminBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)
    role: AdminRole = Field(default=AdminRole.TEAM)
    is_active: bool = True
    is_verified: bool = False

class Admin(AdminBase, table=True):
    __tablename__ = "admin"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
