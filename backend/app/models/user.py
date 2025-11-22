from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """Base user model."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    full_name: Optional[str] = Field(None, description="Full name")


class UserCreate(UserBase):
    """Model for user registration."""

    password: str = Field(..., min_length=8, description="Password")


class UserUpdate(BaseModel):
    """Model for updating user information."""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)


class User(UserBase):
    """Full user model."""

    id: str = Field(..., description="Unique user identifier")
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInDB(User):
    """User model with hashed password."""

    hashed_password: str


class Token(BaseModel):
    """JWT token model."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str  # user_id
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None


class APIKey(BaseModel):
    """API key model."""

    id: str
    user_id: str
    key_hash: str
    name: str = Field(..., description="Friendly name for this API key")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    rate_limit: int = Field(default=100, description="Requests per minute")


class APIKeyCreate(BaseModel):
    """Model for creating an API key."""

    name: str = Field(..., description="Friendly name for this API key")
    rate_limit: int = Field(default=100, ge=1, le=10000)


class APIKeyResponse(BaseModel):
    """Response when creating an API key."""

    api_key: APIKey
    key: str = Field(..., description="The actual API key (only shown once)")
