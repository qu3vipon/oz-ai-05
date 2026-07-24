from fastapi import FastAPI

from user import router as user_router


app = FastAPI(
    title="건강 위험도 예측 서비스"
)

# User 라우터를 FastAPI 서버에 추가
app.include_router(user_router.router)
