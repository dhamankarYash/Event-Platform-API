from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import List, Optional

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Event schemas
class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    location: str = Field(..., min_length=1, max_length=255)
    date_time: datetime
    capacity: int = Field(..., gt=0, le=10000)

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    date_time: Optional[datetime] = None
    capacity: Optional[int] = Field(None, gt=0, le=10000)

class EventResponse(EventBase):
    id: int
    registered_count: int
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaginatedEventsResponse(BaseModel):
    events: List[EventResponse]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool

# Event registration schemas
class EventRegistrationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    registered_at: datetime
    
    class Config:
        from_attributes = True

class EventWithRegistrationStatus(EventResponse):
    is_registered: bool = False
