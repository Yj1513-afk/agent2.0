from openai import OpenAI
from pyexpat.errors import messages

#1.创建客户端对象
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

chat_history = []

user_message_1 = "你好，我叫小明"
chat_history.append({"role": "user", "content": user_message_1})

#第一次请求
compltion = client.chat.completions.create(
    model="qwen3.7-max",
    messages=chat_history,
)
chat_history.append({"role": "assistant", "content": compltion.choices[0].message.content})

#输出第一次结果
print(compltion.choices[0].message.content)

#第二次
user_message_2 = "你好，我叫什么"
chat_history.append({"role": "user", "content": user_message_2})

compltion1 = client.chat.completions.create(
    model="qwen3.7-max",
    messages=chat_history,
)

#输出结果
print(compltion1.choices[0].message.content)