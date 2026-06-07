from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uvicorn


# =========================
# 配置
# =========================

from config import (
    DIFY_URL,
    DIFY_API_KEY,
    REQUEST_TIMEOUT
)


# =========================
# App
# =========================

app = FastAPI(
    title="Wealth Marketing API",
    version="1.0.0"
)


# =========================
# 会话缓存
# PoC阶段使用内存
# 生产建议Redis
# =========================

conversation_cache = {}


# =========================
# 请求对象
# =========================

class MarketingRequest(BaseModel):

    user_id: str

    manager_id: str

    query: str


# =========================
# 响应对象
# =========================

class MarketingResponse(BaseModel):

    success: bool

    answer: str

    conversation_id: str | None = None


# =========================
# Dify调用
# =========================

def call_dify(
    user_id: str,
    manager_id: str,
    query: str
):

    conversation_id = conversation_cache.get(
        user_id
    )

    payload = {
        "inputs": {
            "manager_id": manager_id
        },
        "query": query,
        "response_mode": "blocking",
        "user": user_id
    }

    if conversation_id:
        payload["conversation_id"] = conversation_id

    response = requests.post(
        DIFY_URL,
        headers={
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    result = response.json()

    new_conversation_id = result.get(
        "conversation_id"
    )

    if new_conversation_id:
        conversation_cache[user_id] = (
            new_conversation_id
        )

    return result


# =========================
# 健康检查
# =========================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =========================
# 清理会话
# =========================

@app.delete("/session/{user_id}")
def clear_session(user_id: str):

    conversation_cache.pop(
        user_id,
        None
    )

    return {
        "success": True
    }


# =========================
# 营销助手
# =========================

@app.post(
    "/marketing",
    response_model=MarketingResponse
)
def marketing(
    request: MarketingRequest
):

    try:

        result = call_dify(
            user_id=request.user_id,
            manager_id=request.manager_id,
            query=request.query
        )

        return MarketingResponse(
            success=True,
            answer=result.get(
                "answer",
                ""
            ),
            conversation_id=result.get(
                "conversation_id"
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# 启动
# =========================

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000
    )