import requests
import json

url = 'http://localhost/v1/chat-messages'
headers = {
'Authorization': 'Bearer app-1pkTwJrxNZVJ0AJB8jNeeJ9S',  # 注意密钥要放到配置文件或者环境变量中，不要明文保存
'Content-Type': 'application/json',
}
data = {
"inputs": {"manager_id": "M001"},
"query": "请帮我推荐理财类的客户。",
"response_mode": "blocking",
"conversation_id": "",
"user": "abc-123"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.text)
