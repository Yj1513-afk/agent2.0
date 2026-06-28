from typing import Dict, List
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage
from pyexpat.errors import messages

# 全局存储：对话历史 (key是chat_session_id，value是BaseChatMessageHistory的实现类)
_session_store: Dict[str, BaseChatMessageHistory] = {}


class ChatHistoryManager:
    """负责对话历史的存储与读取"""

    def __init__(self, chat_session_id: str) -> None:
        self.chat_session_id = chat_session_id

    def get_history_object(self) -> BaseChatMessageHistory:
        """获取当前会话的历史记录对象"""
        if self.chat_session_id not in _session_store:
            _session_store[self.chat_session_id] = InMemoryChatMessageHistory()
        return _session_store[self.chat_session_id]

    def get_messages(self) -> List[BaseMessage]:
        """获取当前会话的所有消息列表"""
        return self.get_history_object().messages

    def add_user_message(self, content: str) -> None:
        """添加用户消息"""
        self.get_history_object().add_user_message(content)

    def add_ai_message(self, content: str) -> None:
        """添加AI消息"""
        self.get_history_object().add_ai_message(content)

    def get_recent_messages(self, count: int) -> List[BaseMessage]:
        """获取最近 N 条消息"""
        messages = self.get_messages()
        return messages[-count:] if messages else []

    def get_recent_messages_text(self, count: int) -> str:
        """获取最近 N 条消息文本"""
        messages = self.get_recent_messages(count)
        res = ""
        for msg in messages:
            res += f"{msg.type}:{msg.content}\n"
        return  res

    def clear(self) -> None:
        """清空当前会话的历史记录"""
        if self.chat_session_id in _session_store:
            _session_store[self.chat_session_id] = InMemoryChatMessageHistory()