from openai import OpenAI
from pyexpat.errors import messages

#1.创建客户端对象
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

#第一次请求
compltion = client.chat.completions.create(
    model="qwen3.7-max",
    messages=[
#        {"role":"system","content":"你是一个助手"},
        {"role":"user","content":"你好，我叫小明"},
    ]
)
#第二次
compltion1 = client.chat.completions.create(
    model="qwen3.7-max",
    messages=[
#        {"role":"system","content":"你是一个助手"},
        {"role":"user","content":"你好，我叫什么"},
    ]
)

#输出结果
#print(compltion.model_dump_json())
print(compltion.choices[0].message.content)
print(compltion1.choices[0].message.content)