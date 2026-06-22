from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

#示例数据准备
examples = [
    {"input": "高兴", "output": "愉悦"},
    {"input": "快速", "output": "迅猛"},
    {"input": "美丽", "output": "绚丽"}
]

example_prompt = PromptTemplate.from_template(template="输入：{input}\n输出：{output}")

fewShot = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请根据以上示例，将输入词语转换为同义词",
    suffix="基于示例回答，输入：{input}\n输出：",
    input_variables=["input"],
    #example_separator="\n",
)
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

chain = fewShot | llm
res = chain.invoke(input= {"input": "悲伤"})
prompt_text = fewShot.format(input="悲伤")
print(prompt_text)