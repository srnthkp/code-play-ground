"""This is the User model for the Employment API."""
# pylint: disable=too-few-public-methods
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.db.session import Base


class User(Base):
    """User model for the Employment API."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    date_of_birth = Column(DateTime)  # Nullable for non-employees
    phone_number = Column(String, nullable=True)  # Nullable for non-employees
    # Nullable for non-employees
    employee_id = Column(Integer, unique=True, index=True, nullable=False)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    user_role = Column(Integer)  # e.g., "1=admin", "2=employer", "3=employee
    # Timestamp for creation
    created_at = Column(DateTime, default=datetime.now)
    # Timestamp for last modification
    modified_at = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now)
