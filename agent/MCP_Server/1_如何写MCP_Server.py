#1.导入FastMCP
from mcp.server.fastmcp import FastMCP

#2.创建MCP_Server对象
mcp = FastMCP("weather")

#3.注册工具

@mcp.tool()
def get_current_weather(city: str) -> str:
    """
    获取指定城市当前天气
    :param city:城市地址
    :return:天气信息
    """
    return f"{city}:100摄氏度，风速0km/h，天气状况：超级热"

#4.启动mcp server
if __name__ == '__main__':
    mcp.run(transport="stdio")