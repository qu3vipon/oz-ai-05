# 데이터베이스에 요청을 하기 위한 연결 정보를 관리
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# sqlite를 사용하는데, 그 위치가 현재 프로젝트의 example.db
DATABASE_URL = "sqlite:///./example.db"

# 데이터베이스 통신을 위한 중간 매개체
engine = create_engine(DATABASE_URL, echo=True)

# 실제 요청을 보내는 단위
SessionFactory = sessionmaker(
    bind=engine,
    autocommit=False,  # 메모리 상의 데이터를 다루는 방식
    autoflush=False,
    expire_on_commit=False
)
