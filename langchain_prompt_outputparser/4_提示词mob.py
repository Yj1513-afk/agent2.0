from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate

# 1.创建模型的客户端
llm = ChatTongyi(
    model="qwen3.7-max",
    streaming=True,
    temperature=0.3,            # 降低温度值，缩短首字延迟，使输出更稳定
    # 关键：通过 model_kwargs 传递百炼专属参数
    model_kwargs={
        "enable_thinking": False  # 强制关闭深度思考模式
    }
)

#提示词模板
prompt_tmplate = PromptTemplate.from_template(
    "假设你是一个{expert}专家，喜欢用言简意赅的方式回答问题，请你解释一下{content}是什么。"
)

chain = prompt_tmplate | llm

res = chain.stream(input={"expert":"AI", "content":"Langgraph"})

for chunk in res:
    print(chunk.content, end='', flush=True)