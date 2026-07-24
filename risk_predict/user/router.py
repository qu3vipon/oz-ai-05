from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from auth.jwt import create_access_token, verify_user
from auth.password import hash_password, verify_password
from database.connection import get_session
from user.schema import UserSignUpRequest, UserLogInRequest, UserResponse
from user.model import User


# User 관련된 API 함수를 관리하는 객체
router = APIRouter(prefix="/users", tags=["User"])

@router.post(
    "",
    summary="회원가입 API",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,  # 응답 데이터의 형식이 UserResponse에 맞는지 검사
)
async def signup_user_handler(
    body: UserSignUpRequest,
    session = Depends(get_session),
):
    # 이메일 중복 검사
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()  # 데이터가 0개 또는 1개
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 가입된 이메일 주소입니다."
        )

    # 비밀번호 해싱
    hashed_password = hash_password(plain_password=body.password)

    # 회원 정보 저장 
    new_user = User(email=body.email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()  # INSERT INTO 쿼리 발생
    await session.refresh(new_user)  # created_at 새로고침 -> SELECT

    return new_user

@router.post(
    "/login",
    summary="로그인 API",
    status_code=status.HTTP_200_OK,
)
async def login_user_handler(
    body: UserLogInRequest,
    session = Depends(get_session),
):
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일과 비밀번호가 일치하지 않습니다."
        )

    # 클라이언트가 보낸 비밀번호와 DB에 저장된 해시 값을 비교
    is_verified = verify_password(
        plain_password=body.password,  
        hashed_password=user.hashed_password
    )
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일과 비밀번호가 일치하지 않습니다."
        )

    # JWT 발급
    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token}

@router.get(
    "/me",
    summary="내 정보 API",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_me_handler(
    # 헤더에서 JWT 토큰을 확인하고, 토큰을 검증하는 의존성 함수를 자동 실행
    user_id: int = Depends(verify_user),
    session = Depends(get_session)
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt) 
    user = result.scalar()
    return user
