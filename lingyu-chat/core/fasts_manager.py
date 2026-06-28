from typing import Dict

#全局存储，关键事实，key是chat_session_id，value是slots插槽
_facts_store: Dict[str,Dict[str,str]] = {}

class FactManager:
    def __init__(self,chat_session_id:str):
        self.chat_session_id = chat_session_id
        if chat_session_id not in _facts_store:
            _facts_store[self.chat_session_id] = {}

    def get_all_facts(self) -> Dict[str,str]:
        return _facts_store[self.chat_session_id]

    def get_fact(self,key:str) -> str:
        return _facts_store[self.chat_session_id].get(key,"")

    def update_facts(self,new_facts:Dict[str,str]) -> None:
        if self.chat_session_id not in _facts_store:
            _facts_store[self.chat_session_id] = {}
        #过滤空值
        _facts_store[self.chat_session_id].update({
            k: v for k, v in new_facts.items() if v
        })

    def set_fact(self,key:str,value:str) -> None:
        if self.chat_session_id not in _facts_store:
            _facts_store[self.chat_session_id] = {}
        if value:
            _facts_store[self.chat_session_id][ key] = value

    def clear_facts(self) -> None:
        """清空当前会话的slots插槽"""
        if self.chat_session_id in _facts_store:
            _facts_store[self.chat_session_id] = {}

    def delete_session(self) -> None:
        """删除当前会话"""
        if self.chat_session_id in _facts_store:
            del _facts_store[self.chat_session_id]