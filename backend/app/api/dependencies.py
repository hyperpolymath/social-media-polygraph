from typing import Optional
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from jose import JWTError

from app.core.security import decode_token
from app.core.config import settings
from app.db import arango_manager

# Security schemes
bearer_scheme = HTTPBearer()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> str:
    """
    Get current user from JWT token.

    Args:
        credentials: Bearer token credentials

    Returns:
        User ID

    Raises:
        HTTPException: If token is invalid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = decode_token(token)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return user_id

    except JWTError:
        raise credentials_exception


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(
        HTTPBearer(auto_error=False)
    ),
) -> Optional[str]:
    """
    Get current user from JWT token, but don't require authentication.

    Args:
        credentials: Optional bearer token credentials

    Returns:
        User ID or None
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        return user_id
    except JWTError:
        return None


async def verify_api_key(
    api_key: Optional[str] = Security(api_key_header),
) -> Optional[str]:
    """
    Verify API key and return associated user ID.

    Args:
        api_key: API key from header

    Returns:
        User ID or None

    Raises:
        HTTPException: If API key is invalid
    """
    if not api_key:
        return None

    # Get API key from database
    api_keys_collection = arango_manager.get_collection("api_keys")

    # Find by key hash (in production, hash the incoming key first)
    cursor = api_keys_collection.find({"key_hash": api_key, "is_active": True}, limit=1)

    if cursor.count() == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    api_key_doc = cursor.next()

    # Update last_used timestamp
    api_keys_collection.update({
        "_key": api_key_doc["_key"],
        "last_used": datetime.utcnow().isoformat(),
    })

    return api_key_doc["user_id"]


async def get_current_active_user(
    user_id: str = Depends(get_current_user),
) -> dict:
    """
    Get current active user details.

    Args:
        user_id: User ID from token

    Returns:
        User document

    Raises:
        HTTPException: If user not found or inactive
    """
    users_collection = arango_manager.get_collection("users")
    user = users_collection.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


async def get_current_superuser(
    user: dict = Depends(get_current_active_user),
) -> dict:
    """
    Verify current user is a superuser.

    Args:
        user: Current user

    Returns:
        User document

    Raises:
        HTTPException: If user is not a superuser
    """
    if not user.get("is_superuser", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    return user


from datetime import datetime
