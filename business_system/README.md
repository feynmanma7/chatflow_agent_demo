# 1.启动mcp服务

# 2.启动mcp_http_server服务

# 3. 测试在下游系统基于http调用mcp服务
```shell
curl -X POST \
"http://localhost:9000/marketing" \
-H "Content-Type: application/json" \
-d '{
  "user_id":"manager001",
  "manager_id":"10001",
  "query":"推荐理财客户"
}'
```

