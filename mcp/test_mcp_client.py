import asyncio
import time

from fastmcp import Client

# =========================
# 测试配置
# =========================

MCP_URL = "http://localhost:8000/mcp"
USER_ID = "manager001"
MANAGER_ID = "10001"


# =========================
# 通用调用封装
# =========================

async def safe_call_tool(client: Client, tool_name: str, arguments: dict):
    """安全调用 MCP tool，失败时打印错误但不中断测试流程"""
    try:
        start = time.monotonic()
        result = await client.call_tool(tool_name, arguments)
        elapsed = time.monotonic() - start
        print(f"[耗时 {elapsed:.2f}s] {result}")
    except Exception as e:
        print(f"[失败] {type(e).__name__}: {e}")


# =========================
# 测试用例
# =========================

async def test_health(client: Client):
    print("\n====== health =====")
    await safe_call_tool(client, "health", {})


async def test_round(client: Client, user_id: str, manager_id: str,
                     query: str, label: str = ""):
    """单轮对话测试"""
    title = f"第{label}轮" if label else "对话"
    print(f"\n====== {title} =====")
    print(f"提问: {query}")
    await safe_call_tool(client, "wealth_marketing_agent", {
        "user_id": user_id,
        "manager_id": manager_id,
        "query": query
    })


async def test_clear(client: Client, user_id: str):
    print("\n====== clear =====")
    await safe_call_tool(client, "clear_session", {
        "user_id": user_id
    })


# =========================
# 主流程
# =========================

async def main():
    client = Client(MCP_URL)

    rounds = [
        "请帮我推荐理财客户。",
        "基金呢",
        "贵金属呢"
    ]

    async with client:

        await test_health(client)

        for i, query in enumerate(rounds, 1):
            await test_round(client, USER_ID, MANAGER_ID, query, str(i))

        await test_clear(client, USER_ID)

    print("\n✅ 测试完成")


if __name__ == "__main__":
    asyncio.run(main())
