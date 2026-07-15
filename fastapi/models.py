# 클래스-테이블 매핑 관계 관리
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


# 매핑 관계를 관리하는 최상위 클래스
class Base(DeclarativeBase):
    pass

# User 클래스 <-> user 테이블
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(16))
    password: Mapped[str] = mapped_column(String(32))
