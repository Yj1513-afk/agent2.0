from typing import Dict, List

from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage,AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from core.prompt import SUMMARY_GENERATION_PROMPT

#会话摘要
_summary_store: Dict[str, str] = {}
#未摘要信息数量key是sessionid，value是未摘要信息数量
_unsummarized_cont: Dict[str, int] = {}
#默认配置
SUMMARY_BATCH_SIZE = 12

str_output_parser = StrOutputParser()

class SummaryManager:
    """负责摘要生成储存"""
    def __init__(self,chat_session_id:str) -> None:
        self.chat_session_id = chat_session_id
        #初始化摘要
        if chat_session_id not in _summary_store:
            _summary_store[chat_session_id] = ""
        if chat_session_id not in _unsummarized_cont:
            _unsummarized_cont[chat_session_id] = 0


    def get_summary(self) -> str:
        #return _summary_store[chat_session_id] if _summary_store[chat_session_id] else ""
        return  _summary_store.get(self.chat_session_id,"")

    def update_summary(self,new_summary:str) -> None:
        _summary_store[self.chat_session_id] = new_summary

    def get_unsummary_cont(self) -> int:
        return _unsummarized_cont.get(self.chat_session_id,0)

    def increment_unsummary_cont(self,delta:int = 1) -> None:
        current = _unsummarized_cont.get(self.chat_session_id,0)
        _unsummarized_cont[self.chat_session_id] = current + delta

    def reset_unsummarized_count(self,count:int=0):
        _unsummarized_cont[self.chat_session_id] = count

    def should_trigger_summary(self) -> bool:
        return self.get_unsummary_cont() >= SUMMARY_BATCH_SIZE

    def generate_incremental_summary(
            self,
            old_summary: str,
            new_messages: List[BaseMessage],
            llm: ChatTongyi | None = None
    ) -> str :
        if not new_messages:
            return old_summary

        #提取消息文本
        message_text = ""
        for msg in new_messages:
            if isinstance(msg,AIMessage):
                message_text += f"ai:{msg.content}\n"
            elif isinstance(msg,BaseMessage):
                message_text += f"human:{msg.content}\n"

        #如果没有大语言模型
        if not llm:
            return self._simple_summer(old_summary,message_text)

        try:
            summary_prompt = ChatPromptTemplate.from_messages([
                ("system", SUMMARY_GENERATION_PROMPT),
                ("human", f"旧摘要：{old_summary}\n新对话：{message_text}\n")
            ])
            chain = summary_prompt | llm | str_output_parser
            result = chain.invoke(input={})
            new_summary = result.strip()
            return new_summary
        except:
            return self._simple_summer(old_summary,message_text)

    def _simple_summer(self,old_summary:str,message_text:str) -> str:
        if old_summary and old_summary != "[摘要] 无":
            old_part = old_summary[:150] if len(old_summary) >= 150 else old_summary
            new_part = message_text[:150] if len(message_text) >= 150 else message_text
            return f"[摘要] {old_part}...{new_part}"
        else:
            new_part = message_text[:150] if len(message_text) >= 150 else message_text
            return f"[摘要] {new_part}"