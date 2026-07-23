import asyncio

from langchain_community.chat_models import ChatTongyi
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

async def main():
    #1.创建客户端
    cline = MultiServerMCPClient(
        {
            "weather":{
                "transport":"stdio",
                "command":"E:\\agent2.0\\.venv\\Scripts\\python.exe",
                "args":["E:\\agent2.0\\agent\\MCP_Server\\weather.py"]
            }
        }
    )

    #2.获取工具列表
    tools = await cline.get_tools()

    #print(tools)

    #3.创建客户端
    agent = create_agent(
        model=ChatTongyi(model="qwen3-max"),
        tools=tools,
        system_prompt="你是一个助手，可以调用工具帮用户解决问题"
    )

    #4.使用agent
    weather_response = await agent.ainvoke({"messages":[("user","北京的天气怎么样？")]})
    print(weather_response)
    """
    {'messages': [HumanMessage(content='北京的天气怎么样？', additional_kwargs={}, response_metadata={}, id='960eeeac-278f-4066-8e84-ccebe98204c3'), 
    AIMessage(content='', additional_kwargs={'tool_calls': [{'function': {'arguments': '{"city": "北京"}', 'name': 'get_current_weather'}, 'id': 'call_b30f66acf89541969d14d6c9', 'index': 0, 'type': 'function'}]}, response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'tool_calls', 'request_id': '472f546a-3a90-983e-922b-03fcfb27e423', 'token_usage': {'input_tokens': 430, 'output_tokens': 22, 'prompt_tokens_details': {'cached_tokens': 0}, 'total_tokens': 452}}, id='lc_run--019f7898-3eae-75b0-947e-36fb811915f3-0', tool_calls=[{'name': 'get_current_weather', 'args': {'city': '北京'}, 'id': 'call_b30f66acf89541969d14d6c9', 'type': 'tool_call'}], invalid_tool_calls=[]),
    ToolMessage(content=[{'type': 'text', 'text': '北京当前天气：100°C，风速 0km/h，天气状况：☀️ 超级热', 'id': 'lc_7e73fb9b-241c-47b8-904a-d7dd960c3ed7'}], name='get_current_weather', id='ff35ace9-2044-4f7b-85df-6f434a78bc2f', tool_call_id='call_b30f66acf89541969d14d6c9', artifact={'structured_content': {'result': '北京当前天气：100°C，风速 0km/h，天气状况：☀️ 超级热'}}),
    AIMessage(content='北京当前的天气是100°C，风速为0 km/h，天气状况为☀️超级热。建议尽量避免外出，注意防暑降温，保持水分补充！', additional_kwargs={}, response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'stop', 'request_id': '04960456-93d0-98b4-916e-5ea6bbba2648', 'token_usage': {'input_tokens': 493, 'output_tokens': 39, 'prompt_tokens_details': {'cached_tokens': 0}, 'total_tokens': 532}}, id='lc_run--019f7898-4bbf-70f3-8c85-99f72ebedad3-0', tool_calls=[], invalid_tool_calls=[])]}
    """

if __name__ == '__main__':
    asyncio.run(main())