"""This will contain the schemas for user registration and output."""
# pylint: disable=too-few-public-methods

from typing import Optional
from pydantic import BaseModel, EmailStr

from app.models.enums import UserRoleText


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    username: str
    password: str
    date_of_birth: str
    employee_name: str
    phone_number: str
    # e.g., "admin", "employer", "employee"
    role: Optional[str] = UserRoleText.EMPLOYEE


class UserOut(BaseModel):
    """Schema for outputting user data."""
    employee_id: int
    email: str
    full_name: str
    user_role: int  # e.g., "1=admin", "2=employer", "3=employee"
    id: Optional[int] = None  # Optional ID for the user, useful for responses

    class Config:
        """Enable ORM mode for SQLAlchemy compatibility."""
        from_attributes = True  # Tells FastAPI how to read SQLAlchemy objects


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str

    class Config:
        """Enable ORM mode for SQLAlchemy compatibility."""
        from_attributes = True  # Tells FastAPI how to read SQLAlchemy objects


class TokenResponse(BaseModel):
    """Schema for token response."""
    id: int
    jwt: str
    refresh_token: str

    class Config:
        """Enable ORM mode for SQLAlchemy compatibility."""
        from_attributes = True  # Tells FastAPI how to read SQLAlchemy objects


class RefreshRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str
