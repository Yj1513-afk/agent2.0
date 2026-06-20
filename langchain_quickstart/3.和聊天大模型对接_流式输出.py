from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatTongyi(model="qwen3.7-max",streaming= True)

#准备上下文
chat_history = [
    SystemMessage(content="背景设定：你是一个话唠AI老师。"),
    HumanMessage(content="你是谁")
]

res = llm.stream(input=chat_history)

print(res)
for chunk in res:
    print(chunk.content,end="",flush=True)