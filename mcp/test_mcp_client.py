import asyncio
from fastmcp import Client


async def test_health(client):

    result = await client.call_tool(
        "health",
        {}
    )

    print(result)

async def test_round1(client):

    result = await client.call_tool(
        "wealth_marketing_agent",
        {
            "user_id": "manager001",
            "manager_id": "10001",
            "query": "请帮我推荐理财客户。"
        }
    )

    print(result)

async def test_round2(client):

    result = await client.call_tool(
        "wealth_marketing_agent",
        {
            "user_id": "manager001",
            "manager_id": "10001",
            "query": "基金呢"
        }
    )

    print(result)    


async def test_round3(client):

    result = await client.call_tool(
        "wealth_marketing_agent",
        {
            "user_id": "manager001",
            "manager_id": "10001",
            "query": "贵金属呢"
        }
    )

    print(result)    

async def test_clear(client):

    result = await client.call_tool(
        "clear_session",
        {
            "user_id": "manager001"
        }
    )

    print(result)

async def main():

    client = Client(
        "http://localhost:8000/mcp"
    )

    async with client:

        print("\n====== health ======")
        await test_health(client)

        print("\n====== 第一轮 ======")
        await test_round1(client)

        print("\n====== 第二轮 ======")
        await test_round2(client)

        print("\n====== 第三轮 ======")
        await test_round3(client)

        print("\n====== clear ======")
        await test_clear(client)


if __name__ == "__main__":
    asyncio.run(main())    