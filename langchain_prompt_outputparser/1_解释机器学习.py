from langchain_community.chat_models import ChatTongyi
from langchain_community.llms.tongyi import Tongyi

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
user_query_1 = "请简单介绍机器学习"
user_query_2 = """
请从以下几个方面介绍机器学习：
1. 定义（一句话概括）
2. 三大分类（监督学习、无监督学习、强化学习）
3. 一个生活化的例子
4. 与深度学习的区别（用表格呈现）

要求：语言通俗，适合零基础初学者
"""

result = llm.stream(input=user_query_2)

# 3.处理输出
for chunk in result:
    print(chunk.content, end='', flush=True)