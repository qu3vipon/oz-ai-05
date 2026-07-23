import json
import uuid

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from redis import asyncio as aredis


redis_client = aredis.from_url(
    "redis://redis:6379", decode_responses=True
)

app = FastAPI()

class UserInputRequest(BaseModel):
    user_input: str

@app.post(
    "/chats",
    summary="응답 생성 API"
)
async def create_chat_handler(
    body: UserInputRequest
):
    # 요청마다 채널 ID 발급(중복 없는 고유한 값)
    channel_id = str(uuid.uuid4())

    # 채널 구독 -> 메시지 수신
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel_id)

    # 요청할 작업(job)을 정의
    job = {
        "user_input": body.user_input,
        "channel_id": channel_id
    }

    # 추론 요청 enqueue
    await redis_client.lpush("inference_queue", json.dumps(job))

    # 토큰을 N번 반환하는 함수
    async def token_generator():
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            token = message["data"]
            if token == "[DONE]":  # 더 이상 토큰이 오지 않음
                break
            yield token

    # 클라이언트 응답 
    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
    )
