from langchain_community.chat_models import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
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

# 2.调用模型
# 2.1. 准备提示词模板
prompt_template = PromptTemplate.from_template(
    "假设你是一个{expert}专家，请你解释一下{content}是什么。"
)
# 2.2. 替换占位符
prompt = prompt_template.format(expert="AI", content="Langgraph")
print(type(prompt))  # <class 'str'>
print(prompt)
# 2.3 调用模型
result = llm.stream(input=prompt)

# 3.处理输出
for chunk in result:
    print(chunk.content, end='', flush=True)