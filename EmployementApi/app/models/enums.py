"""This file contains enums for the entire application"""
from enum import Enum


class UserRoleText(Enum):
    """Enum for user roles with string values."""
    ADMIN = "Admin"
    EMPLOYER = "Employer"
    EMPLOYEE = "Employee"


class UserRoleNumber(Enum):
    """Enum for user roles with numeric values."""
    ADMIN = 1
    EMPLOYER = 2
    EMPLOYEE = 3


class TokenType(Enum):
    """Enum for token types."""
    JWT = "jwt"
    REFRESH = "refresh_token"


class SameSite(Enum):
    """Enum for SameSite cookie attribute."""
    LAX = "lax"
    STRICT = "strict"
    NONE = "none"


def get_user_role_number(rol: str) -> str:
    """Convert user role string to corresponding integer string."""
    role_number = UserRoleNumber.EMPLOYEE.value  # Default to "3" for Employee
    if rol == UserRoleText.ADMIN.value:
        role_number = UserRoleNumber.ADMIN.value
    elif rol == UserRoleText.EMPLOYER.value:
        role_number = UserRoleNumber.EMPLOYER.value
    return role_number


def get_user_role_text(rol: int) -> str:
    """Convert user role string to corresponding integer string."""
    user_role_text = UserRoleText.EMPLOYEE.value  # Default to "Employee"
    if rol == UserRoleNumber.ADMIN.value:
        user_role_text = UserRoleText.ADMIN.value
    elif rol == UserRoleNumber.EMPLOYER.value:
        user_role_text = UserRoleText.EMPLOYER.value
    return user_role_text
