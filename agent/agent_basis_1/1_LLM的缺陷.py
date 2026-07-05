from langchain_community.chat_models import ChatTongyi

# 1.创建模型客户端
llm = ChatTongyi(model="qwen3-max")

# 2.调用模型
user_input = "明天北京的天气怎么样？"
messages = [
    ("system", "你是一个友好的天气查询助手"),
    ("human", f"{user_input}")
]
result = llm.invoke(messages)
print(type(result)) # <class 'langchain_core.messages.ai.AIMessage'>
print(result.content) # 你好！要获取明天北京的天气情况，我建议你查看权威天气预报平台