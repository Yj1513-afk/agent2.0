from langchain_core.prompts import ChatPromptTemplate

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "假设你是一个{expert}专家"),
        ("human", "请解释一下{content}是什么")
    ]
)
prompt = chat_prompt_template.format(expert="AI", content="Langgraph")
print(type(prompt))
print(prompt)

prompt1 = chat_prompt_template.invoke(input={"expert":"AI", "content":"Langgraph"})
print(type(prompt1))
print(prompt1)
print(prompt1.to_string())