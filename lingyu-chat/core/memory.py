from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage

from core.chat_history_manager import ChatHistoryManager
from core.fasts_manager import FactManager
from core.intent_recognizer_with_structured_output import IntentRecognizer
from core.summary_manager import SummaryManager

SESSION_KEY = "session_id"


class Memory:
    def __init__(self, chat_session_id: str,):
        self.chat_session_id = chat_session_id
        self.session_key = f"{SESSION_KEY}:{self.chat_session_id}"


        #初始化三管理器
        self.chat_history_manager = ChatHistoryManager(chat_session_id)
        self.summary_manager = SummaryManager(chat_session_id)
        self.facts_manager = FactManager(chat_session_id)

        #self.session_history = self.chat_history_manager.get_history_object()
        #self.messages = self.chat_history_manager.get_messages()
        #self.recent_messages = self.chat_history_manager.get_recent_messages(RECENTLY_MESSAGE_COUNT)
        #self.recent_messages_text = self.chat_history_manager.get_recent_messages_text(RECENTLY_MESSAGE_COUNT)

    """对话历史相关"""
    def get_session_history_object(self) -> BaseChatMessageHistory:
        return self.chat_history_manager.get_history_object()

    def get_messages(self) -> list[BaseMessage]:
        return self.chat_history_manager.get_messages()

    def get_recent_messages(self,count:int) -> list[BaseMessage]:
        return self.chat_history_manager.get_recent_messages(count)

    def get_messages_text(self,count:int) -> str:
        return self.chat_history_manager.get_recent_messages_text(count)

    """添加消息"""
    def add_user_message(self,content:str,llm:ChatTongyi):
        self.chat_history_manager.add_user_message(content)
        self.summary_manager.increment_unsummary_cont()
        bool = self.summary_manager.should_trigger_summary()
        if bool:
            self._trim_and_summarized(llm)

    def add_ai_message(self,content:str,llm:ChatTongyi):
        self.chat_history_manager.add_ai_message(content)
        self.summary_manager.increment_unsummary_cont()
        self._trim_and_summarized(llm)

    def get_key_facts(self) -> dict:
        return self.facts_manager.get_all_facts()

    def update_key_facts(self,new_facts:dict):
        self.facts_manager.update_facts(new_facts)

    def clear_key_facts(self):
        self.facts_manager.clear_facts()

    """摘要相关"""
    def _trim_and_summarized(self,llm:ChatTongyi):
        bool = self.summary_manager.should_trigger_summary()
        if not bool:
            return

        unsummary_cont = self.summary_manager.get_unsummary_cont()
        unsummary_messages = self.get_recent_messages(unsummary_cont)
        # 获取未摘要的消息阿苑版
        # new_messages = messages[summarized_count:]
        # if new_messages:
        #     old_summary = self.summary.get_summary()
        #     new_summary = self.summary.generate_incremental_summary(
        #         old_summary,
        #         new_messages,
        #         llm
        #     )
        #     self.summary.update_summary(new_summary)
        #     self.summary.reset_unsummarized_count()
        #     print("摘要生成")

        #本人版
        if unsummary_messages:
            old_summary = self.summary_manager.get_summary()
            new_summary = self.summary_manager.generate_incremental_summary(old_summary,unsummary_messages,llm)
            self.summary_manager.update_summary(new_summary)
            print("摘要生成")
            self.summary_manager.reset_unsummarized_count()



    """准备上下文"""
    def prepare_memory_for_llm(self) -> list[BaseMessage]:
        """事实+摘要+最近消息"""
        res = []
        facts = self.get_key_facts()
        if facts:
            fasts_text = " | ".join(f"{k}:{v}" for k,v in facts.items())
            res.append(AIMessage(content=f"[关键事实]{fasts_text}"))
        summary = self.summary_manager.get_summary()
        if summary:
            res.append(AIMessage(content=f"[摘要]{summary}"))

        unsummary_history = self.chat_history_manager.get_recent_messages(self.summary_manager.get_unsummary_cont())
        if unsummary_history:
            res.extend(unsummary_history)

        return res
