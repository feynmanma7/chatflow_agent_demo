# 1. 启动mcp服务
```shell
python mcp_server.py
```

# 2. 测试mcp服务
```shell
python test_mcp_client.py
```

```shell
curl -X POST \
http://localhost:8000/mcp/WealthMarketingAgent \
-H "Content-Type: application/json" \
-d '{
    "manager_id":"M001",
    "product_id":"P12345"
}'
```

# 3. 测试基于http调用mcp 
```shell
python mcp_http_server.py
```
