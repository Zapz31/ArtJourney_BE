from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str
    email: str
    created_at: datetime
    fullname: Optional[str] = None
    role: Optional[str] = "CUSTOMER"
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    birthday: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str