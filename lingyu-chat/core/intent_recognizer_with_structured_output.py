from typing import Any

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from core.prompt import INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT


class IntentResult(BaseModel):
    """
    意图识别结果
    -intents :意图列表，每个元素为一个意图名称
    -slots：slot值字典，健为slot名称，值为slot值
    -confidence：置信度分数，
    0~1，越大越可信
    """
    intents: list[str] = Field(...,description="意图列表，每个元素为一个意图名称")
    slots: dict[str, Any] = Field(...,description="slot值字典，健为slot名称，值为slot值")
    confidence: float = Field(...,description="置信度分数，0~1，越大越可信")

class IntentRecognizer:
    """
    意图识别，通过大语言模型识别用户输入意图，返回IntentResult
    """

    def __init__(self, llm:ChatTongyi):
        #chain = prompt | llm | outputparser
        self.llm = llm
        self.__llm = llm.with_structured_output(IntentResult)
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system", INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT),
            ("ai", "上下文内容{chat_history}"),
            ("human", "{input}")
        ])
        self.__chain = self.__prompt | self.__llm

    def recognizer(self,user_input:str,chat_history:str | None = None) -> IntentResult:
        #1.调用llm识别意图，输出str格式json字符串
        chat_history = chat_history if chat_history else ""
        result = self.__chain.invoke(input={"chat_history":chat_history, "input":user_input})
        print( result)
        if result is None:
            return IntentResult(intents=["general"],slots={},confidence=0.0)
        return result

