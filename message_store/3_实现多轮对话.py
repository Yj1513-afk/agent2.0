from typing import Dict

from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage,AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#会话储存管理类
_session_messages: Dict[str, BaseChatMessageHistory] = {}
#Memory类
class Memory:
    def __init__(self, session_id: str):
        self.session_id = session_id
        if self.session_id not in _session_messages:
            chat_history = InMemoryChatMessageHistory()
            _session_messages[self.session_id] = chat_history

#get_session_history
    def get_session_history(self):
        return _session_messages[self.session_id].messages

#add_human_message
    def add_human_message(self,message: str | HumanMessage):
        chat_history = _session_messages[self.session_id]
        if isinstance(message, str):
            chat_history.add_message(HumanMessage(content=message))
        else:
            chat_history.add_message(message)

#add_ai_message
    def add_ai_message(self,message: str | AIMessage):
        chat_history = _session_messages[self.session_id]
        if isinstance(message, str):
            chat_history.add_message(AIMessage(content=message))
        else:
            chat_history.add_message(message)

#获取所有消息列表
    def messages(self) -> list[BaseMessage]:
        return self.get_session_history()

#对话类
class Chat:
#init
    def __init__(self, session_id: str, system_prompt: str = "你是一个友好的AI助手。"):
        self.memory = Memory(session_id)
        self.model = ChatTongyi(
            model="qwen3.7-max",
            streaming=True,
            temperature=0.3,            # 降低温度值，缩短首字延迟，使输出更稳定
            # 关键：通过 model_kwargs 传递百炼专属参数
            model_kwargs={
                "enable_thinking": False  # 强制关闭深度思考模式
        })
        self.chat_history = self.memory.messages()
        self.ChatPromptTemplate = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.parser = StrOutputParser()
        self.chain = self.ChatPromptTemplate | self.model | self.parser

#send
    def send(self,user_message: str):
        res = self.chain.stream({
            "history":self.chat_history,
            "input":user_message
        })
        full_reply = ""
        for chunk in res:
            if chunk:
                full_reply += chunk
                yield chunk
        self.memory.add_human_message(user_message)
        self.memory.add_ai_message(full_reply)

if __name__ == "__main__":
    session = Chat("user_001")

    print("用户: 你好，我叫阿苑")
    print("AI: ", end='', flush=True)
    for chunk in session.send("你好，我叫阿苑"):
        print(chunk, end='', flush=True)
    print()

    print("用户: 我叫什么名字？")
    print("AI: ", end='', flush=True)
    for chunk in session.send("我叫什么名字？"):
        print(chunk, end='', flush=True)
    print()