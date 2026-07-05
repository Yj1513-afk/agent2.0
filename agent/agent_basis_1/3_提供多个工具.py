from langchain_community.chat_models import ChatTongyi
from langchain.tools import tool
from langchain.messages import ToolMessage

# 1. 创建模型客户端
llm = ChatTongyi(model="qwen3-max")


# 2. 给 LLM 添加工具
@tool
def get_weather(location: str) -> str:
    """
    获取某个位置的天气信息
    :param location: 地理位置
    :return: 天气情况
    """
    return f"{location}的天气是100摄氏度，请你准备防晒。"

@tool
def get_recommendations(city: str) -> str:
    """
    获取某个城市的旅游景点推荐
    :param city: 城市名称
    :return: 推荐景点列表
    """
    recommendations = {
        "北京": "故宫、天安门、长城、颐和园、天坛、鸟巢",
        "上海": "外滩、东方明珠、迪士尼乐园、豫园",
        "杭州": "西湖、灵隐寺、宋城、雷峰塔",
        "成都": "锦里、宽窄巷子、大熊猫基地、都江堰",
        "西安": "兵马俑、大雁塔、古城墙、华清池"
    }
    return recommendations.get(city, f"抱歉，暂无{city}的景点推荐信息。")


# 3. 绑定工具到 LLM
tools = [get_weather, get_recommendations]
model_with_tools = llm.bind_tools(tools=tools)

# 4. 调用模型
user_input_1 = "北京明天天气怎么样？并且北京有什么好玩的地方？"
# user_input = "北京明天天气怎么样？"
messages = [
    ("system", "你是一个友好的旅游和天气查询助手，可以同时查询天气和景点推荐。"),
    ("human", f"{user_input_1}")
]

result = model_with_tools.invoke(messages)
print(result)
"""
tool_calls=[
{'name': 'get_weather', 'args': {'location': '北京'}, 'id': 'call_4aecc8125f9f414c9f23eae1', 'type': 'tool_call'}, 
{'name': 'get_recommendations', 'args': {'city': '北京'}, 'id': 'call_fefb07f3dcfe4a02a5388c44', 'type': 'tool_call'}
]

"""