from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    
class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: Optional[EmailStr]=None
    password: Optional[str]=None
    
class UserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str = "bearer"
    

    