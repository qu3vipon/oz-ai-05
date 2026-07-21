from openai import OpenAI
from config import settings

from pydantic import BaseModel, Field


client = OpenAI(api_key=settings.openai_api_key)

user_input = input("질문을 입력하세요: ")

# ChatGPT가 응답하길 원하는 데이터 형식
class ResponseFormat(BaseModel):
    result: str = Field(description="최종 답변")
    confidence: float = Field(description="0~1 사이의 답변 신뢰도")

response = client.responses.parse(
    model="gpt-4o-mini",
    input=user_input,
    # 응답값을 프로그래밍적으로 손쉽게 사용하고 싶을 때
    text_format=ResponseFormat
)
