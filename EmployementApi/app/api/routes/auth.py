"""Authentication routes for the Employment API."""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api import deps
from app.api.deps import get_db, require_login
from app.schemas.user import RefreshRequest, UserCreate, UserOut, UserLogin
from app.crud import auth as crud_auth
from app.core.jwt_handle import decode_access_token, create_access_token
from app.models.enums import TokenType, SameSite, get_user_role_text

router = APIRouter()


class RegisterResponse(BaseModel):
    """Response model for user registration."""
    success: bool
    message: str
    user: UserOut


class LoginResponse(BaseModel):
    """Response model for user registration."""
    success: bool
    message: str
    jwt: str
    refresh_token: str


class TokenResponse(BaseModel):
    """Response model for token generation."""
    id: int
    jwt: str
    refresh_token: str


class RoleResponse(BaseModel):
    """Response model for Role."""
    success: bool
    message: str
    role: str


class EmployeeResponse(BaseModel):
    """Response model for Employee."""
    success: bool
    message: str
    employee: list[UserOut]


@router.post("/register", response_model=RegisterResponse)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        user = crud_auth.register_user(db=db, user_in=user_in)
        return RegisterResponse(
            success=True,
            message="User registered successfully.",
            user=user
        )
    except ValueError as e:
        # Custom error (e.g., user already exists)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        # General error
        raise HTTPException(
            status_code=500, detail="Internal server error") from e


@router.post("/login", response_model=LoginResponse)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db),
    # Set the X-Use-Token: true
    x_use_token: str = Header(default=None, alias="X-Use-Token")
):
    """Login user endpoint (to be implemented)."""
    try:
        logged_in_user = crud_auth.login_user(db=db, login_data=login_data)
        # If X-Use-Token header is present and true, return tokens in body (for mobile/API)
        if x_use_token and x_use_token.lower() == "true":
            return {
                "success": True,
                "message": "User logged in successfully.",
                "jwt": logged_in_user.jwt,
                "refresh_token": logged_in_user.refresh_token
            }
        # Otherwise, set tokens as cookies (for browsers)
        response = JSONResponse(
            content={
                "success": True,
                "message": "User logged in successfully."
            }
        )
        # Set JWT as HttpOnly cookie
        response.set_cookie(
            key=TokenType.JWT.value,
            value=logged_in_user.jwt,
            httponly=False,
            secure=False,  # Set to True in production (HTTPS)
            samesite=SameSite.LAX.value
        )
        # Set Refresh Token as HttpOnly cookie
        response.set_cookie(
            key=TokenType.REFRESH.value,
            value=logged_in_user.refresh_token,
            httponly=False,
            secure=False,  # Set to True in production (HTTPS)
            samesite=SameSite.LAX.value  # Use None for cross-site cookies
        )
        return response
    except ValueError as e:
        # Custom error (e.g., user already exists)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        # General error
        raise HTTPException(
            status_code=500, detail="Internal server error") from e


@router.post("/refresh")
def refresh_token(
    request: Request,
    x_use_token: str = Header(default=None, alias="X-Use-Token"),
    body: RefreshRequest = None
):
    """
    Refresh the access token using the refresh_token cookie (browser)
    or from the request body (mobile/API). Expecting a JSON body with "refresh_token" key
    """
    token = None

    # If X-Use-Token header is present and true, get token from body
    if x_use_token and x_use_token.lower() == "true":
        if body and body.refresh_token:
            token = body.refresh_token
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No refresh token provided in body"
            )
    else:
        # Otherwise, get token from cookie
        token = request.cookies.get(TokenType.REFRESH.value)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No refresh token cookie found"
            )

    payload = decode_access_token(token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    new_access_token = create_access_token({"sub": payload["sub"]})

    if x_use_token and x_use_token.lower() == "true":
        return {
            "success": True,
            "message": "Token refreshed",
            "access_token": new_access_token
        }

    response = JSONResponse(
        content={"success": True, "message": "Token refreshed"})
    response.set_cookie(
        key=TokenType.JWT.value,
        value=new_access_token,
        httponly=True,
        secure=False,  # Set to True in production
        samesite=SameSite.LAX.value
    )
    return response


@router.post("/logout")
def logout(x_use_token: str = Header(default=None, alias="X-Use-Token")):
    """
    Logout user by clearing cookies (browser) or just returning success (mobile/API).
    """
    response = JSONResponse(
        content={"success": True, "message": "Logged out successfully."}
    )
    # Only clear cookies for browser clients
    if not (x_use_token and x_use_token.lower() == "true"):
        response.set_cookie(
            key=TokenType.JWT.value,
            value="",
            httponly=True,
            secure=False,  # Set to True in production
            samesite=SameSite.LAX.value,
            max_age=0
        )
        response.set_cookie(
            key=TokenType.REFRESH.value,
            value="",
            httponly=True,
            secure=False,  # Set to True in production
            samesite=SameSite.LAX.value,
            max_age=0
        )
    return response


@router.get("/protected")
def protected_route(current_user=Depends(require_login)):
    # A sample protected route to demonstrate authentication
    """A protected route that requires authentication."""
    return {"msg": "You are authenticated!", "user": current_user}


@router.get("/get_user_role")
def get_user_role(db: Session = Depends(deps.get_db), current_user=Depends(deps.require_login)):
    """Retrieve the role of the currently logged-in user."""
    logged_in_user = deps.get_current_user_from_payload(
        db=db, payload=current_user)

    return RoleResponse(
        success=True,
        message="User role retrieved successfully.",
        role=get_user_role_text(
            logged_in_user.user_role) if logged_in_user.user_role else "Unknown"
    )


@router.get("/get_employees")
def get_employees(db: Session = Depends(deps.get_db), current_user=Depends(deps.require_login)):
    """Retrieve all the employees."""

    return EmployeeResponse(
        success=True,
        message="Employees retrieved successfully.",
        employee=crud_auth.get_all_employees(db=db)
    )
