import jwt
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer

from config import settings


# JWT를 생성하는 함수
def create_access_token(user_id: int):
    # subject: 토큰의 주체
    # expiration time: 만료 시간
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    return jwt.encode(
        payload=payload, key=settings.jwt_secret_key, algorithm="HS256"
    )

# JWT를 검증하는 함수
def verify_access_token(access_token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt=access_token, key=settings.jwt_secret_key, algorithms=["HS256"]
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 토큰 형식입니다."
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="만료된 토큰입니다."
        )
    return payload


# HTTP Authorization 헤더에서 Bearer 값을 자동으로 읽어오는 객체
http_bearer = HTTPBearer()

def verify_user(
    auth_header = Depends(http_bearer)
) -> int:
    access_token = auth_header.credentials
    payload = verify_access_token(access_token=access_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="sub 값이 없습니다."
        )
    return int(user_id)
