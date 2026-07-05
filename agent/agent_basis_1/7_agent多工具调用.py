from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langchain.agents import create_agent

# 2. 工具调用
# 2.1. 模拟商品数据库
product_db = {
    "iPhone": {"id": 101, "price": 5999},
    "MacBook": {"id": 102, "price": 12999},
    "小米手机": {"id": 103, "price": 3999},
}

# 2.2. 工具A：根据名称获取ID
@tool(description="根据商品名称获取对应的商品ID")
def get_product_id_by_name(name: str) -> int | None:
    """输入商品名称（如'iPhone'），返回商品ID"""
    name_lower = name.lower()
    for prod_name, info in product_db.items():
        if prod_name.lower() == name_lower:
            print(f"[工具A] 商品 '{name}' 的 ID 是 {info['id']}")
            return info['id']
    print(f"[工具A] 未找到商品 '{name}'")
    return None

# 2.3. 工具B：根据ID获取价格
@tool(description="根据商品ID查询商品价格")
def get_product_price_by_id(product_id: int) -> str | None:
    """输入商品ID，返回价格字符串"""
    for prod_name, info in product_db.items():
        if info['id'] == product_id:
            price = info['price']
            print(f"[工具B] ID {product_id} 的商品 '{prod_name}' 价格为 {price} 元")
            return f"{prod_name} 的价格是 {price} 元"
    print(f"[工具B] 未找到 ID {product_id} 对应的商品")
    return None

# 3. 创建 Agent
agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_product_id_by_name, get_product_price_by_id],
    system_prompt="你是一个商品查询助手。当用户询问某个商品的价格时，请先调用 get_product_id_by_name 获取商品ID，"
           "然后再调用 get_product_price_by_id 获取价格，最后把价格告知用户。"
)

# 4. 调用 Agent 执行任务
user_query = "我想知道小米手机的价格是多少？"
print(f"用户问题：{user_query}\n")

# 调用 agent 并打印结果
result = agent.invoke({
    "messages": [{"role": "user", "content": user_query}]
})

# 5. 提取最终回答
print(result['messages'])


"""
[
HumanMessage(content='我想知道小米手机的价格是多少？', additional_kwargs={}, response_metadata={}, id='82559f8c-d165-4da9-a9ce-b58b49b97cb1'), 

AIMessage(content='', additional_kwargs={'tool_calls': [{'function': {'arguments': '{"name": "小米手机"}', 'name': 'get_product_id_by_name'}, 
'id': 'call_4dab8d10e2d2421a9d1f2b7f', 'index': 0, 'type': 'function'}]}, 
tool_calls=[{'name': 'get_product_id_by_name', 'args': {'name': '小米手机'}, 'id': 'call_4dab8d10e2d2421a9d1f2b7f', 'type': 'tool_call'}], invalid_tool_calls=[]), 

ToolMessage(content='103', name='get_product_id_by_name', id='3248ad64-9808-48f9-abef-dc7d713d4067', tool_call_id='call_4dab8d10e2d2421a9d1f2b7f'), 

AIMessage(content='', additional_kwargs={'tool_calls': [{'function': {'arguments': '{"product_id": 103}', 'name': 'get_product_price_by_id'}, 'id': 'call_cd9d39451b7049e3af01379d', 'index': 0, 'type': 'function'}]}, response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'tool_calls', 'request_id': '7d806c36-4d02-9b4a-8082-7a0eae809fdd', 'token_usage': {'input_tokens': 410, 'output_tokens': 27, 'prompt_tokens_details': {'cached_tokens': 320}, 'total_tokens': 437}}, id='lc_run--019f0d3d-172d-7f50-b9fb-011dd5764903-0', tool_calls=[{'name': 'get_product_price_by_id', 'args': {'product_id': 103}, 'id': 'call_cd9d39451b7049e3af01379d', 'type': 'tool_call'}], invalid_tool_calls=[]), 

ToolMessage(content='小米手机 的价格是 3999 元', name='get_product_price_by_id', id='f3dba3b6-6fac-447c-8feb-6db22b34922b', tool_call_id='call_cd9d39451b7049e3af01379d'), 

AIMessage(content='小米手机的价格是 3999 元。', additional_kwargs={}, response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'stop', 'request_id': '4fcf7fa0-785d-92ba-b4c8-be3c4741cde6', 'token_usage': {'input_tokens': 464, 'output_tokens': 12, 'prompt_tokens_details': {'cached_tokens': 384}, 'total_tokens': 476}}, id='lc_run--019f0d3d-1e50-7f13-9ff8-d63cb547aefa-0', tool_calls=[], invalid_tool_calls=[])]


"""