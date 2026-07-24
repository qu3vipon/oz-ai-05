from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database.orm import Base


class User(Base):
    __tablename__ = "user"

    # 기본키 id 컬럼 
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    # email 컬럼(중복 불가)
    email: Mapped[str] = mapped_column(
        String(256), unique=True
    )
    # 비밀번호 해시(암호화된 값)
    hashed_password: Mapped[str] = mapped_column(String(256))
    # 회원이 가입한 시각(DB에 저장된 시각을 자동 저장)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now() 
    )
