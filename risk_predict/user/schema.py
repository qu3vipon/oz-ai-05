from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# request
class UserSignUpRequest(BaseModel):
    email: EmailStr = Field(..., examples=["alex@fastapi.com"])
    password: str = Field(..., min_length=4, examples=["password123"])

class UserLogInRequest(BaseModel):
    email: EmailStr = Field(..., examples=["alex@fastapi.com"])
    password: str = Field(..., min_length=4, examples=["password123"])

# response
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
