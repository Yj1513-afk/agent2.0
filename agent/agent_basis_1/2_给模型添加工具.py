from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool

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

#2.添加工具
@tool
def get_weather(location:str):
    """
    获取某位置天气信息
    :param location:位置信息
    :return：天气情况
    """
    return f"{ location}今天是晴天,35摄氏度，请注意防晒"

#3.将工具绑定到模型中
tools = [get_weather]
#for tool,i in enumerate(tools):
model_with_tools = llm.bind_tools(tools)

#调用模型
user_input = "今天在杭州的天气如何"
messages = [
    ("system", "你是一个友好的天气查询助手"),
    ("human", f"{user_input}")
]

res = model_with_tools.invoke(input=messages)
#print(res.content)

#4.根据tool调用工具
tool_map = {tool.name: tool for tool in tools}
print(type(tool_map))
print(tools[0])

if res.tool_calls:
    #将ai响应添加到历史
    messages.append(res)

    #解析tool_calls
    for tool_call in res.tool_calls:
        tool_mane = tool_call['name']
        tool_args = tool_call['args']
        tool_id = tool_call['id']

        tool_func = tool_map[tool_mane]
        if tool_func:
            try:
                tool_res = tool_func.invoke(tool_args)
                print(f"工具调用{tool_mane}成功，结果为：{tool_res}")
                #创建ToolMessage ，添加到历史中
                tool_message = ToolMessage(
                    tool_call_id=tool_id,
                    content=tool_res
                )
                messages.append(tool_message)
            except Exception as e:
                tool_message = ToolMessage(
                    tool_call_id=tool_id,
                    content=f"工具调用失败：{str( e)}"
                )
                messages.append(tool_message)

        else:
            tool_message = ToolMessage(
                tool_call_id=tool_id,
                content=f"没有找到工具：{tool_mane}"
            )
            messages.append(tool_message)

else:
    print("没有工具调用")
    print(res.content)

#5.再次调用
for mes in messages:
    print(f"{type(mes).__name__}: {mes}")

res = model_with_tools.invoke(input=messages)
print(res.content)