# 调用大模型 API 参考指南

## 基本请求示例

```python
response = requests.post(endpoint, headers=self.headers, json=payload, timeout=30)
```

## API 端点

```
https://api.deepseek.com/chat/completions
```

## 请求参数 (Payload)

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 使用的模型名称 |
| `messages` | list | 对话消息列表，包含 `role` 和 `content` 字段 |
| `temperature` | float | 创造性参数，范围 0-2，越高越有创造性 |
| `max_tokens` | int | 最大输出长度（token 数） |
| `top_p` | float | 核采样，保持输出多样性，范围 0-1 |
| `frequency_penalty` | float | 重复词出现频率惩罚，范围 -2 到 2 |
| `presence_penalty` | float | 讨论新话题的倾向性，范围 -2 到 2 |
| `……` | |
## 响应处理

### 状态码
- `response.status_code` - HTTP 响应状态码

### 响应数据结构

```
服务器返回原始数据（字节流）
         ↓
response.content  (字节格式，最原始)
         ↓ 解码（根据 response.encoding）
response.text     (字符串格式)
         ↓ JSON 解析
response.json()   (Python 字典/列表)
```

## 完整代码示例

```python
import requests

# 配置
endpoint = "https://api.deepseek.com/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "你好！"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

# 发送请求
response = requests.post(endpoint, headers=headers, json=payload, timeout=30)

# 处理响应
if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"请求失败: {response.status_code}")
    print(response.text)
```

## 参考文档

https://api-docs.deepseek.com/zh-cn/api/create-chat-completion