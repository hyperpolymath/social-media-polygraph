from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
import uuid

from app.models import User, UserCreate, Token, APIKeyCreate, APIKeyResponse, APIKey
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    generate_api_key,
    hash_api_key,
)
from app.core.config import settings
from app.db import arango_manager
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate) -> User:
    """
    Register a new user.

    Args:
        user_data: User registration data

    Returns:
        Created user

    Raises:
        HTTPException: If email or username already exists
    """
    users_collection = arango_manager.get_collection("users")

    # Check if email exists
    existing = users_collection.find({"email": user_data.email}, limit=1)
    if existing.count() > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check if username exists
    existing = users_collection.find({"username": user_data.username}, limit=1)
    if existing.count() > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Create user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user_data.password)

    user_doc = {
        "_key": user_id,
        "id": user_id,
        "email": user_data.email,
        "username": user_data.username,
        "full_name": user_data.full_name,
        "hashed_password": hashed_password,
        "is_active": True,
        "is_superuser": False,
        "created_at": datetime.utcnow().isoformat(),
    }

    users_collection.insert(user_doc)

    # Remove password from response
    user_doc.pop("hashed_password")
    return User(**user_doc)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Login with username/email and password.

    Args:
        form_data: OAuth2 password form

    Returns:
        Access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    users_collection = arango_manager.get_collection("users")

    # Find user by username or email
    user_cursor = users_collection.find(
        {
            "$or": [
                {"username": form_data.username},
                {"email": form_data.username},
            ]
        },
        limit=1,
    )

    if user_cursor.count() == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    user = user_cursor.next()

    # Verify password
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    # Update last login
    users_collection.update({
        "_key": user["_key"],
        "last_login": datetime.utcnow().isoformat(),
    })

    # Create tokens
    access_token = create_access_token(subject=user["id"])
    refresh_token = create_refresh_token(subject=user["id"])

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post("/api-keys", response_model=APIKeyResponse)
async def create_api_key(
    key_data: APIKeyCreate,
    user_id: str = Depends(get_current_user),
) -> APIKeyResponse:
    """
    Create a new API key for the authenticated user.

    Args:
        key_data: API key creation data
        user_id: Authenticated user ID

    Returns:
        Created API key with the actual key (only shown once)
    """
    api_keys_collection = arango_manager.get_collection("api_keys")

    # Generate API key
    api_key = generate_api_key()
    key_hash = hash_api_key(api_key)

    # Create API key document
    key_id = str(uuid.uuid4())
    key_doc = {
        "_key": key_id,
        "id": key_id,
        "user_id": user_id,
        "key_hash": key_hash,
        "name": key_data.name,
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
        "rate_limit": key_data.rate_limit,
    }

    api_keys_collection.insert(key_doc)

    return APIKeyResponse(
        api_key=APIKey(**key_doc),
        key=api_key,
    )


@router.get("/me", response_model=User)
async def get_current_user_info(
    user_id: str = Depends(get_current_user),
) -> User:
    """
    Get current user information.

    Args:
        user_id: Authenticated user ID

    Returns:
        User information
    """
    users_collection = arango_manager.get_collection("users")
    user = users_collection.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.pop("hashed_password", None)
    return User(**user)


from datetime import datetime
