from openai import OpenAI

#1.创建客户端对象
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

#第一次请求
completion = client.chat.completions.create(
    model="qwen3.7-max",
    messages=[
#        {"role":"system","content":"你是一个话唠助手"},
        {"role":"user","content":"你好，我叫小明，你可以干嘛"},
    ],
    stream=True
)

#输出结果
for chunk in completion:
    if chunk.choices and len(chunk.choices) > 0:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="", flush=True)#刷新缓冲区
    elif hasattr(chunk, "usage") and chunk.usage:
        print(chunk.usage)