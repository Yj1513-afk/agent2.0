from typing import List, Dict, Any
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import BaseMessage
from openai import vector_stores

from config.setting import QaConfig
from indexing.vector_storage import VectorStoreManager
from .query_rewrite import QueryRewriter
from .rerank import RerankPipeline
from .answer import AnswerGenerator
from .vector_retrieve import recall_with_scores

class RagPipeline:
    """RAG在线流水线，只负责查询，不负责索引构建"""

    def __init__(self,config:QaConfig):
        self._config = config
        self._llm = None
        self._embeddings = None
        self._vector_store = {} #缓存向量库

    def _init_llm(self,api_key:str) -> ChatTongyi:
        if self._llm is None:
            self._llm = ChatTongyi(
                model="qwen3.7-max",
                streaming=True,
                temperature=0.3,  # 降低温度值，缩短首字延迟，使输出更稳定
                # 关键：通过 model_kwargs 传递百炼专属参数
                model_kwargs={
                    "enable_thinking": False  # 强制关闭深度思考模式
                },
                api_key=api_key
            )
        return self._llm

    def _init_embeddings(self,api_key:str) -> DashScopeEmbeddings:
        if self._embeddings is None:
            self._embeddings = DashScopeEmbeddings(
                model=self._config.embedding_model,
                dashscope_api_key=api_key
            )
        return self._embeddings

    def _load_vectorstore(self,file_hash:str,api_key:str) -> Chroma:
        """加载向量数据库(带缓存）"""
        cache_key = file_hash
        if cache_key not in self._vector_store:
            embeddings = self._init_embeddings(api_key)
            manager = VectorStoreManager(self._config,embeddings)
            self._vector_store[cache_key] = manager.load_or_build(file_hash)
        return self._vector_store[cache_key]

    def query(self,
              dashscope_api_key:str,
              file_hash:str,
              question:str,
              chat_history:List[BaseMessage],
              *,
              recall_k: int = 10,
              top_k: int = 4
              ):
        """
                执行 RAG 查询（默认启用查询改写和重排序）

                Args:
                    dashscope_api_key: API密钥
                    file_hash: 文件哈希
                    question: 用户问题
                    chat_history: 聊天历史
                    top_k: 最终返回文档数
                    recall_k: 初始召回数量
                """
        try:
            llm = self._init_llm(dashscope_api_key)
            vector_store = self._load_vectorstore(file_hash,dashscope_api_key)

            #1.查询改写
            rewrite = QueryRewriter(llm)
            search_query = rewrite.rewrite(question,chat_history)

            #2.向量召回
            recalled_docs, vec_scores = recall_with_scores(search_query,vector_store,k=recall_k)

            #3.重排序
            rerank_pipline = RerankPipeline(self._config,llm)
            evidence_list, context = rerank_pipline.rerank(
                query=search_query,
                recalled_docs=recalled_docs,
                vec_scores=vec_scores,
                final_top_n=top_k)

            #4.生成答案
            answer_gen = AnswerGenerator(llm)
            answer = answer_gen.generate(search_query,chat_history,context)
            
            return {
                "answer": answer,
                "context": context,
                "evidence": evidence_list,
                "search_query": search_query,
                "rewritten": search_query != question,
                "doc_count": len(evidence_list),
            }

        except  Exception as e:
            return {
                "error": f"查询失败：{str(e)}",
                "answer": "抱歉，处理你的请求时出现错误。",
                "context": "",
                "evidence":[],
                "search)_query": question,
                "rewritten": False,
                "doc_count": 0,
            }
