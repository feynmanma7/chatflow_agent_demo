from fastmcp import FastMCP
import requests

from config import (
    DIFY_URL,
    DIFY_API_KEY,
    REQUEST_TIMEOUT
)

mcp = FastMCP("WealthMarketingAgent")

# Demo阶段先放内存
conversation_cache = {}


def call_dify(
    user_id: str,
    manager_id: str,
    query: str
):

    conversation_id = conversation_cache.get(user_id)

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

    if result.get("conversation_id"):
        conversation_cache[user_id] = result["conversation_id"]

    return result


@mcp.tool()
def health():
    """
    健康检查
    """

    return {
        "status": "ok"
    }


@mcp.tool()
def clear_session(
    user_id: str
):
    """
    清除会话
    """

    conversation_cache.pop(
        user_id,
        None
    )

    return {
        "success": True
    }


@mcp.tool()
def wealth_marketing_agent(
    user_id: str,
    manager_id: str,
    query: str
):
    """
    理财经理营销助手

    示例：

    推荐理财客户

    推荐基金客户

    推荐安心盈客户

    推荐最近可能购买保险的客户
    """

    result = call_dify(
        user_id=user_id,
        manager_id=manager_id,
        query=query
    )

    return {
        "answer": result.get("answer"),
        "conversation_id": result.get("conversation_id")
    }


if __name__ == "__main__":

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )