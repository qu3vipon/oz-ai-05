from database.connection import async_engine
from sqlalchemy.orm import DeclarativeBase


# SQLAlchemy ORM 클래스 관리하는 최상위 클래스
class Base(DeclarativeBase):
    pass

# 비동기 방식으로 Base에 등록된 테이블을 생성하는 함수
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
