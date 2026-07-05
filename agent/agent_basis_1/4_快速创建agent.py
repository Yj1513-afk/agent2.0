from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

llm = ChatTongyi(
    model="qwen3.7-max",
    streaming=True,
    temperature=0.3,            # 降低温度值，缩短首字延迟，使输出更稳定
    # 关键：通过 model_kwargs 传递百炼专属参数
    model_kwargs={
        "enable_thinking": False  # 强制关闭深度思考模式
    }
)

# 1.创建 tool
@tool
def get_goods_info_by_id(goods_id: int) -> str | None:
    """
    根据商品goods_id去查询商品信息
    :param goods_id: 商品id
    :return: 查询到的商品信息，没查询到就返回空
    """
    goods_info = {
        1: "爱疯手机",
        2: "华为电脑"
    }
    if goods_id not in goods_info:
        print(f"id为{goods_id}的商品不存在")
        return None
    goods = goods_info[goods_id]
    print(f"id为{goods_id}的商品为：{goods}")
    return goods

#2.创建agent
tools = [get_goods_info_by_id]
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个商品信息查询助手，如果用户传入商品id，请查询该商品信息。"
)

#3.使用agent
user_query = "商品id为1，是什么商品？"
res = agent.invoke(
    {"messages":[{"role": "user", "content": user_query}]}
)

print(type( res))
print( res)