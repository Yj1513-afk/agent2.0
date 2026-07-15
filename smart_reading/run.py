# run.py - PDF 问答系统（支持逐条消息，自动维护对话历史）
import os
from typing import Dict, Any, Optional

from chromadb.execution.expression import Select
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.indexing import index

from config.setting import QaConfig
from indexing.indexing_pipeline import IndexingPipeline
from querying.query_pipeline import RagPipeline


class PDFQA:
    """PDF问答系统封装类，支持逐条消息交互，自动维护对话历史"""

    def __init__(self,pdf_source:str,api_key:str):
        """

        :param pdf_source:
        :param api_key: 通义千问api
        """
        self.pdf_source = pdf_source
        self.api_key = api_key

        self.cfg = QaConfig()
        self.file_hash: Optional[str] = None
        self.chat_history: Optional[InMemoryChatMessageHistory] = None
        self.rag: Optional[RagPipeline] = None

    def _build_index(self) -> None:
        """构建向量索引，内部懒加载"""
        if self.file_hash is not None:
            return
        print(f"正在构建索引（首次构建会调用Embedding API，请稍候）...")
        print(f"PDF文件路径：{self.pdf_source}")
        indexer = IndexingPipeline(self.cfg,self.api_key)
        self.file_hash = indexer.build_from_source(self.pdf_source)
        self.chat_history = InMemoryChatMessageHistory()
        self.rag = RagPipeline(self.cfg)
        print(f"索引构建完成，file_hash：{self.file_hash}")


    def ask(self,question:str) -> Dict[str,Any]:
        """
        发送一条消息，返回答案，
        :param question: 用户问题
        :return: 包含answer，context，evidence，search_query,rewritten的字典
        """
        if not self.file_hash:
            #构建索引(内部懒加载
            self._build_index()

        res = self.rag.query(
            dashscope_api_key=self.api_key,
            file_hash=self.file_hash,
            question=question,
            chat_history=self.chat_history.messages,
            recall_k=10,
            top_k=4,
        )

        #更新聊天历史
        self.chat_history.add_user_message(question)
        self.chat_history.add_ai_message(res["answer"])

        return res




