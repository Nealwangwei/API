import ollama

response = ollama.chat(
    model='deepseek-r1:8b',   # ← 必须是真实模型名
    messages=[
        {"role": "user", "content": "你好"}
    ]
)
print(response['message']['content'])
print(result.message.content)
