from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt_templater = ChatPromptTemplate.from_messages([
    ("system", "假设你是一个AI专家"),
    MessagesPlaceholder("history"),
    ("human", "我刚才问了什么内容")
])

chat_history = [
    ("human", "请解释一下机器学习是什么"),
    ("ai", "机器学习是一种基于计算机算法的机器智能训练方法。")
]

prompt = chat_prompt_templater.format(history=chat_history)
print(type(prompt))
print( prompt)