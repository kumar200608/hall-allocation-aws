"""
Pydantic schemas for authentication.
"""

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    username: str | None = None
    role: str = "student"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str | None = None


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str | None
    username: str | None
    role: str

    class Config:
        from_attributes = True
