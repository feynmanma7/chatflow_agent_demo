# 1. Shell测试dify api

```shell
curl -X POST 'http://localhost/v1/chat-messages' \
--header 'Authorization: Bearer app-1pkTwJrxNZVJ0AJB8jNeeJ9S' \
--header 'Content-Type: application/json' \
--data-raw '{
  "inputs": {"manager_id": "M001"},
  "query": "请帮我推荐理财类的客户。",
  "response_mode": "streaming",
  "conversation_id": "",
  "user": "abc-123",
  "files": [
      {
        "type": "image",
        "transfer_method": "remote_url",
        "url": "https://cloud.dify.ai/logo/logo-site.png"
      }
    ]
}'
```

# 2. Python测试dify api
```shell
python test_dify.py
```
