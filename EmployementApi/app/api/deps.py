"""This file contains the dependency for database session management in the Employment API."""
from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.jwt_handle import decode_access_token
from app.crud import auth as crud_auth
from app.db.session import SessionLocal

# Uncomment if you want to use OAuth2PasswordBearer for token-based authentication
# from fastapi.security import OAuth2PasswordBearer
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# def require_login(token: str = Depends(oauth2_scheme)):
#     """Dependency to require a valid JWT token for protected routes."""
#     payload = decode_access_token(token)
#     if payload is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#         )
#     return payload


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_login(request: Request):
    """Dependency to require a valid JWT token from either cookies or Authorization header."""
    # 1. Try to get JWT from cookie (for browser-based clients like web apps)
    jwt_token = request.cookies.get("jwt")
    if not jwt_token:
        # 2. If not in cookie, try Authorization header manually (for mobile/API clients)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            jwt_token = auth_header.split(" ", 1)[1]
    if not jwt_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (no JWT found in cookie or header)",
        )
    payload = decode_access_token(jwt_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return payload


def get_current_user_from_payload(db: Session, payload: dict):
    """Extract the user ID from the decoded JWT payload."""
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: 'sub' not found",
        )
    return crud_auth.get_user_by_email(db=db, email=email)
