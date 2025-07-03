"""This is the CRUD operations for employee registration in the Employment API."""
from sqlalchemy.orm import Session
from app.core.security import get_password_context, get_password_hash
from app.core.jwt_handle import create_access_token, create_refresh_token
from app.models.enums import UserRoleNumber, get_user_role_number
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserLogin, TokenResponse


def register_user(db: Session, user_in: UserCreate) -> UserOut:
    """Register a new user in the database."""
    try:
        # Check if the user already exists
        existing_user = db.query(User).filter_by(email=user_in.email).first()
        if existing_user:
            raise ValueError("User with this email already exists.")

        db_user = User(
            email=user_in.email,
            username=user_in.username,
            password_hash=get_password_hash(user_in.password),
            date_of_birth=user_in.date_of_birth,
            full_name=user_in.employee_name,
            phone_number=user_in.phone_number,
            user_role=get_user_role_number(user_in.role),
            employee_id=get_employee_id(db)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        output_user = UserOut(
            employee_id=db_user.employee_id,
            email=db_user.email,
            full_name=db_user.full_name,
            user_role=db_user.user_role
        )
        return output_user
    except Exception as e:
        db.rollback()
        raise ValueError(
            f"An error occurred while registering the user: {str(e)}") from e


def login_user(db: Session, login_data: UserLogin) -> TokenResponse:
    """Login user endpoint (to be implemented)."""
    try:
        existing_user = db.query(User).filter_by(
            username=login_data.username).first()
        if not existing_user:
            raise ValueError("User does not exists.")
        if not get_password_context().verify(login_data.password, existing_user.password_hash):
            raise ValueError("Incorrect password.")
        return TokenResponse(
            id=existing_user.id,
            jwt=create_access_token({"sub": existing_user.email}),
            refresh_token=create_refresh_token({"sub": existing_user.email})
        )
    except Exception as e:
        raise ValueError(f"Login failed: {str(e)}") from e


def get_employee_id(db: Session) -> int:
    """Generate a unique employee ID."""
    last_user = db.query(User).order_by(User.id.desc()).first()
    if last_user:
        return last_user.employee_id + 1
    return 10000  # Starting employee ID from 10000


def get_user_by_email(db: Session, email: str) -> UserOut:
    """Retrieve a user by their email."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("User not found.")
    return UserOut(
        id=user.id,
        employee_id=user.employee_id,
        email=user.email,
        full_name=user.full_name,
        user_role=user.user_role
    )


def get_all_employees(db: Session) -> list[UserOut]:
    """Retrieve all employees."""
    users = db.query(User).filter_by(
        user_role=UserRoleNumber.EMPLOYEE.value).all()
    if not users:
        raise ValueError("No employees found.")
    return [UserOut(
        id=user.id,
        employee_id=user.employee_id,
        email=user.email,
        full_name=user.full_name,
        user_role=user.user_role
    ) for user in users]
