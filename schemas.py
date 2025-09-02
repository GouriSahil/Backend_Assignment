from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Schema for user registration"""
    username: str
    email: EmailStr
    password: str
    role: str  # "instructor" or "client"
    
    class Config:
        from_attributes = True


class ClassCreate(BaseModel):
    """Schema for creating a fitness class"""
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int
    
    class Config:
        from_attributes = True


class BookingRequest(BaseModel):
    """Schema for booking a slot in a fitness class"""
    class_id: int
    client_name: str
    client_email: EmailStr
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    username: str
    email: str
    role: str
    
    class Config:
        from_attributes = True


class ClassResponse(BaseModel):
    """Schema for class response"""
    id: int
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int
    
    class Config:
        from_attributes = True


class BookingResponse(BaseModel):
    """Schema for booking response"""
    id: int
    class_id: int
    client_name: str
    client_email: str
    
    class Config:
        from_attributes = True
