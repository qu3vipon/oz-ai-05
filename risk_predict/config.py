from pydantic_settings import BaseSettings, SettingsConfigDict


# 프로젝트 내의 환경변수를 관리하는 클래스
class Settings(BaseSettings):
    jwt_secret_key: str
    openai_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()
