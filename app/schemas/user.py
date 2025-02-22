from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import date, datetime

class UserBase(BaseModel):
    fullname: str
    role: str = Field(..., description="User role in the system")
    gender: str = Field(..., max_length=1, description="M or F")
    phone_number: str
    email: EmailStr
    birthday: date

    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['M', 'F']:
            raise ValueError('Gender must be either M or F')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="User password")
    manager_id: Optional[str] = None

class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    role: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    birthday: Optional[date] = None
    manager_id: Optional[str] = None

    @validator('gender')
    def validate_gender(cls, v):
        if v is not None and v not in ['M', 'F']:
            raise ValueError('Gender must be either M or F')
        return v

class UserInDB(UserBase):
    id: str
    manager_id: Optional[str] = None
    banned_by: Optional[str] = None
    password: str
    created_at: datetime
    deleted_at: Optional[datetime] = None
    banned_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: str
    manager_id: Optional[str] = None
    banned_by: Optional[str] = None
    created_at: datetime
    deleted_at: Optional[datetime] = None
    banned_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserList(BaseModel):
    id: str
    fullname: str
    role: str
    email: EmailStr
    created_at: datetime
    banned_at: Optional[datetime] = None

    class Config:
        from_attributes = True