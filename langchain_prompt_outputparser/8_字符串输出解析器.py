from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("解释一下{concept}是什么")
model = ChatTongyi(model="qwen3.7-max",streaming= True)
parser = StrOutputParser()

chain = prompt | model | parser
res = chain.stream(input={"concept":"机器学习"})

for chunk in res:
    print(chunk, end='', flush=True)