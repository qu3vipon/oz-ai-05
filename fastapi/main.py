from fastapi import FastAPI, Path, Query, Body, HTTPException, Depends
from sqlalchemy import select

from schema import UserSignUpRequest, UserUpdateRequest, UserResponse

from connection import SessionFactory, get_session
from models import User


app = FastAPI()

@app.get(
    "/users",
    summary="전체 사용자 조회 API",
    response_model=list[UserResponse],
    status_code=200
)
def get_users_handler(
    session = Depends(get_session)
):
    stmt = select(User)
    result = session.execute(stmt)
    users: list[User] = result.scalars().all()
    return users

@app.get(
    "/users/search",
    summary="회원 검색 API",
    response_model=list[UserResponse],
    status_code=200  # 응답이 성공한 경우, 사용할 상태코드 값 지정
)
def search_user_handler(
    name: str | None = Query(None),
    session = Depends(get_session),
):
    if name is None:
        return []

    # 검색어(name)를 name 컬럼에 포함하는 사용자 조회
    stmt = select(User).where(User.name.contains(name))
    result = session.execute(stmt)
    users: list[User] = result.scalars().all()
    return users

@app.get(
    "/users/{user_id}",
    summary="회원 조회 API",
    response_model=UserResponse,
    status_code=200
)
def get_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_session),
):
    # Python 구현한 SQL 쿼리문
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user: User | None = result.scalar()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="존재하지 않는 사용자 ID입니다."
        )
    return user
    
@app.post(
    "/users",
    summary="회원 가입 API",
    response_model=UserResponse,
    status_code=201
)
def user_sign_up_handler(
    # 클라이언트가 보낸 데이터를 검사하고, 유효성 검사가 끝난 데이터
    body: UserSignUpRequest,
    session = Depends(get_session),
):
    new_user = User(name=body.name, password=body.password)
    session.add(new_user)    
    session.commit()
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
    session = Depends(get_session),
):
    stmt = select(User).where(User.id == user_id)
    
    result = session.execute(stmt)
    user = result.scalar()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="존재하지 않는 사용자 ID입니다."
        )

    if body.name:
        user.name = body.name
    if body.password:
        user.password = body.password
    
    session.commit()
    return user

@app.delete(
    "/users/{user_id}",
    summary="회원 삭제 API",
    response_model=None,
    status_code=204  # NO CONTENT
)
def delete_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_session),
):
    stmt = select(User).where(User.id == user_id)
    
    result = session.execute(stmt)
    user = result.scalar()   
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="존재하지 않는 사용자 ID입니다."
        )
    
    session.delete(user)  # 삭제 마킹
    session.commit()
