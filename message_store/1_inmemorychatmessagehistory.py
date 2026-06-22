from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

memory = InMemoryChatMessageHistory()

memory.add_message(HumanMessage(content="你是谁"))
memory.add_message(AIMessage(content="我是一个AI"))

print(memory.messages)