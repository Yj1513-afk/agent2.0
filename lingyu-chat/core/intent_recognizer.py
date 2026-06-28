import json
from typing import Any
import re

from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dataclasses import dataclass
from .prompt import INTENT_RECOGNIZE_PROMPT

@dataclass(frozen=True)
class IntentResult:
    """
    意图识别结果
    -intents:意图列表，每个元素为一个意图名称
    -slots：slot值字典，健为slot名称，值为slot值
    -confidence：置信度分数，0~1，越大越可信
    """
    intents: list[str]
    slots: dict[str, Any]
    confidence: float


class IntentRecognizer:
    """
    意图识别，通过大语言模型识别用户输入意图，返回IntentResult
    """

    def __init__(self, llm:ChatTongyi):
        #chain = prompt | llm | outputparser
        self.llm = llm
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system", INTENT_RECOGNIZE_PROMPT),
            ("ai", "上下文内容{chat_history}"),
            ("human", "{input}")
        ])
        self.__chain = self.__prompt | self.llm | StrOutputParser()

    def recognizer(self,user_input:str,chat_history:str=None) -> IntentResult:
        #1.调用llm识别意图，输出str格式json字符串
        chat_history = chat_history if chat_history else ""
        result = self.__chain.invoke({"input":user_input, "chat_history":chat_history})
        print( result)

        #2.解析输出
        #2.0str-》 json
        data = self.__parse_str_to_json(result)

        #2.1解析intents意图
        intents = data.get("intents")
        if not isinstance(intents,list):
            intent = data.get("intent")
            intents = [ intent] if isinstance(intent,str) else []
        #2.2解释 slots
        slots = data.get("slots") if isinstance(data.get("slots"),dict) else {}
        #2.3解析confidence
        try:
            confidence = float(data.get("confidence"))
        except:
            confidence = 0.0
        confidence = max(0.0,min(1.0,confidence))

        #3.返回结果
        return IntentResult(intents,slots,confidence)



    def __parse_str_to_json(self,text:str) -> dict[str,Any]:
        if not text or not text.strip():
            return {"intents":["general"],"slots":{},"confidence":0.0}

        #text-》json
        text = text.strip()
        try:
            return json.loads(text)
        except json.decoder.JSONDecodeError:
            pass

        find_text = re.search(r"{.*}",text,re.DOTALL)
        if find_text:
            try:
                return json.loads(find_text.group(0))
            except json.decoder.JSONDecodeError:
                pass

        #如果未找到json字符串，返回默认值
        return {"intents":["general"],"slots":{},"confidence":0.0}
