#有问题
from langchain_community.llms.tongyi import Tongyi

#创建
llm = Tongyi(model="qwen-max")

#调用
result = llm.invoke(input="你好，我是小明")

#输出
print(type( result))
print(result)
