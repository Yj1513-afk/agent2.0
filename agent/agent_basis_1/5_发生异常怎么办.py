from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import ToolMessage
from langchain.tools import tool


# ========== 1. 定义工具 ==========

@tool
def search(query: str) -> str:
    """搜索信息。"""
    return f"结果：{query}"


@tool
def get_weather(location: str) -> str:
    """获取位置的天气信息。"""
    if location == "北京":
        raise ValueError("出错啦！")
    return f"{location} 的天气：晴朗，72°F"


# ========== 2. 定义错误处理中间件 ==========

@wrap_tool_call
def handle_tool_errors(request, handler):
    """使用自定义消息处理工具执行错误。"""
    try:
        return handler(request)
    except Exception as e:
        # 向模型返回自定义错误消息
        return ToolMessage(
            content=f"工具错误：请检查您的输入并重试。（{str(e)}）",
            tool_call_id=request.tool_call["id"]
        )


# ========== 3. 创建 Agent ==========

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[search, get_weather],
    middleware=[handle_tool_errors]
)


# ========== 4. 调用 Agent ==========
result = agent.invoke({
    "messages": [{"role": "user", "content": "明天北京天气如何？"}]
})

# 输出最终回复
print(result["messages"][-1].content)