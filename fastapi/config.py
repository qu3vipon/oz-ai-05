# 프로젝트 설정 값을 관리하는 파일
from pydantic_settings import BaseSettings, SettingsConfigDict


# 설정 값의 형식 정의
class Settings(BaseSettings):
    openai_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()
