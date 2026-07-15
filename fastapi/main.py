from fastapi import FastAPI, Path, Query, Body, HTTPException

from schema import UserSignUpRequest, UserUpdateRequest, UserResponse

from connection import SessionFactory
from models import User


app = FastAPI()

# 임시 데이터베이스 
users: list[dict[str, int | str]] = [
    {"id": 1, "name": "alex", "password": "1234"},
    {"id": 2, "name": "bob", "password": "1234"},
    {"id": 3, "name": "chris", "password": "1234"},
]

@app.get(
    "/users",
    summary="전체 사용자 조회 API",
    response_model=list[UserResponse],
    status_code=200
)
def get_users_handler():
    return users

@app.get(
    "/users/search",
    summary="회원 검색 API",
    response_model=list[UserResponse],
    status_code=200  # 응답이 성공한 경우, 사용할 상태코드 값 지정
)
def search_user_handler(
    # GET /users/search?name=alex
    name: str | None = Query(None)
):
    result = []
    if name is None:
        return result

    for user in users:
        if name in user["name"]:
            result.append(user)
    return result

@app.get(
    "/users/{user_id}",
    summary="회원 조회 API",
    response_model=UserResponse,
    status_code=200
)
def get_user_handler(
    user_id: int = Path(..., ge=1)
):
    for user in users:
        if user_id == user["id"]:
            return user
    
    # user_id에 해당하는 user가 없는 경우
    raise HTTPException(
        status_code=404,
        detail="존재하지 않는 사용자 ID입니다."
    )

@app.post(
    "/users",
    summary="회원 가입 API",
    response_model=UserResponse,
    status_code=201
)
def user_sign_up_handler(
    # 클라이언트가 보낸 데이터를 검사하고, 유효성 검사가 끝난 데이터
    body: UserSignUpRequest  
):
    new_user = User(name=body.name, password=body.password)

    session = SessionFactory()
    session.add(new_user)
    session.commit()

    session.close()
    return new_user

@app.patch(
    "/users/{user_id}",
    summary="회원 정보 수정 API",
    response_model=UserResponse,
    status_code=200
)
def update_user_handler(
    user_id: int = Path(..., ge=1),
    body: UserUpdateRequest = Body(...),
):
    for user in users:
        if user_id == user["id"]:
            if body.name is not None:
                user["name"] = body.name
            if body.password is not None:
                user["password"] = body.password
            return user
    
    raise HTTPException(
        status_code=404,
        detail="존재하지 않는 사용자 ID입니다."
    )

@app.delete(
    "/users/{user_id}",
    summary="회원 삭제 API",
    response_model=None,
    status_code=204  # NO CONTENT
)
def delete_user_handler(
    user_id: int = Path(..., ge=1)
):
    for user in users:
        if user_id == user["id"]:
            users.remove(user)
            return
    
    raise HTTPException(
        status_code=404,
        detail="존재하지 않는 사용자 ID입니다."
    )
