"""This file contains the security utilities for the Employment API, including password hashing."""
from passlib.context import CryptContext


def get_password_context() -> CryptContext:
    """Hash a password using bcrypt."""
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return get_password_context().hash(password)
