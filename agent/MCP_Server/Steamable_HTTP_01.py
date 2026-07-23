from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "database",
    host="127.0.0.1",
    port=8000,

    # Streamable HTTP 的访问路径
    streamable_http_path="/mcp",

    # 无状态模式：每个请求独立处理，适合生产部署
    stateless_http=True,

    # True：普通 JSON 响应
    # False：允许通过 SSE 流式返回响应
    json_response=True,
)


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    mcp.run(transport="streamable-http")