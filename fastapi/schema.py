from pydantic import BaseModel, Field


# 회원가입 요청에 사용되는 데이터 형식
class UserSignUpRequest(BaseModel):
    name: str = Field(..., min_length=2)
    password: str = Field(..., min_length=4, max_length=10)

# 회원 정보 수정 요청에 사용되는 데이터 형식
class UserUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=2)
    password: str | None = Field(None, min_length=4, max_length=10)

# 사용자 데이터를 응답할 때 사용하는 형식
class UserResponse(BaseModel):
    id: int
    name: str

# 사용자가 LLM에게 요청하는 데이터 형식
class UserInputRequest(BaseModel):
    user_input: str
