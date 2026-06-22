from langchain_community.llms.tongyi import Tongyi
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# 创建解析器
parser = JsonOutputParser()

# 定义提示词模板，要求模型输出JSON格式
prompt = PromptTemplate.from_template(
    "请根据以下描述，提取书籍信息并以JSON格式输出。\n"
    "描述：{description}\n"
    "输出格式：{{\"title\": \"书名\", \"author\": \"作者\", \"year\": 出版年份}}"
)

model = ChatTongyi(model="qwen3-max", streaming=True)
chain = prompt | model | parser

result = chain.invoke({"description": "《三体》是刘慈欣创作的科幻小说，于2008年首次出版。"})
print(result) # {'title': '三体', 'author': '刘慈欣', 'year': 2008}
print(type(result)) # <class 'dict'>