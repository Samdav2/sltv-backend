import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    full_name: Optional[str] = None

class User(UserBase, table=True):
    __tablename__ = "user"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    transactions: List["Transaction"] = Relationship(back_populates="user")
    tickets: List["Ticket"] = Relationship(back_populates="user")
    profile: Optional["UserProfile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False, "lazy": "selectin"}
    )
