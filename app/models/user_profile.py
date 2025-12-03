import uuid
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class UserProfileBase(SQLModel):
    phone_number: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    lga: Optional[str] = None
    nin: Optional[str] = None  # National Identity Number
    bvn: Optional[str] = None  # Bank Verification Number

class UserProfile(UserProfileBase, table=True):
    __tablename__ = "user_profile"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True)
    user: "User" = Relationship(back_populates="profile")
