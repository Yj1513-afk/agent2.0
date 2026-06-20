from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatTongyi(model="qwen3.7-max")

#准备上下文
chat_history = [
    ('system', "背景设定：你是一个AI老师，喜欢用简短的语言回答问题。"),
    ('human', "你是谁")
    #SystemMessage(content="背景设定：你是一个AI老师，喜欢用简短的语言回答问题。"),
    #HumanMessage(content="你是谁")
]

res = llm.invoke(input=chat_history)

print(type(res))
print(res)