from typing import Optional
from pydantic import BaseModel

class UserProfileCreate(BaseModel):
    phone_number: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    lga: Optional[str] = None
    nin: Optional[str] = None
    bvn: Optional[str] = None

class UserProfileUpdate(BaseModel):
    phone_number: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    lga: Optional[str] = None
    nin: Optional[str] = None
    bvn: Optional[str] = None

class UserProfileRead(BaseModel):
    phone_number: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    lga: Optional[str] = None
    nin: Optional[str] = None
    bvn: Optional[str] = None
