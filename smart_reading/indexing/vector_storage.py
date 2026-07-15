# indexing/vectorstore.py
"""
向量库管理模块
"""
import logging
import shutil
from pathlib import Path
from typing import List, Optional

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document

from config.setting import QaConfig
logger = logging.getLogger(__name__)

class  VectorStoreManager:
    """向量库管理"""
    def __init__(self,config:QaConfig,embeddings:DashScopeEmbeddings) -> None:
        self._config = config
        self._embeddings = embeddings

    def load_or_build(self,
                      file_hash:str,
                      chunks:Optional[List[Document]] = None) -> Chroma:
        """
        加载已存在向量数据库，不存在创建
        :param file_hash: PDF哈希md5值
        :param chunks: 切分后的documents列表（新建时必须提供）
        :return Chroma 向量数据库
        """
        if not file_hash:
            raise ValueError("file_hash不能为空")

        persist_dir = self._get_persist_dir(file_hash)
        collection_name = self._get_collection_name(file_hash)

        #创建向量数据库
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self._embeddings,
            persist_directory = str(persist_dir),
            collection_metadata={"hnsw:space": "cosine"}
        )
        if self._has_data(vector_store):
            logger.info(f"加载已存在向量数据库：{persist_dir}")
            return vector_store

        #新建向量库
        logger.info(f"新建向量数据库：{persist_dir}")
        return self._build_vector_store(vector_store,chunks)


    def _get_persist_dir(self,file_hash:str) -> Path:
        """获取向量持久化目录"""
        # ./chroma_db/pdf_{file_hash}
        persist_dir = Path(self._config.chroma_root_dir) / f"pdf_{file_hash}"
        #parents递归创建
        #exist_ok，没有目录不报错
        persist_dir.mkdir(parents=True, exist_ok=True)
        return persist_dir

    def _get_collection_name(self,file_hash:str) ->  str:
        """获取向量数据库集合名称"""
        return f"{self._config.collection_prefix}_{file_hash}"

    def _has_data(self,vector_store:Chroma) -> bool:
        """判断向量数据库是否为空"""
        try:
            return vector_store._collection.count() > 0
        except Exception as e:
            logger.warning(f"检查数据库失败：{e}")
            return False


    def _build_vector_store(self,vector_store:Chroma,chunks:List[Document]) ->  Chroma:
        """
        新建向量数据库
        :param vector_store: Chroma向量数据库
        :param chunks: 切分后的documents列表
        :return: Chroma向量数据库
        """
        if  not chunks:
            raise ValueError("chunks不能为空")

        try:
            vector_store.add_documents(
                documents=chunks,
                ids=[f"doc-{idx}" for idx in range(1,len(chunks)+1)]
            )
            logger.info(f"成功添加{len(chunks)}个文本块到向量数据库")
            return vector_store
        except Exception as e:
            logger.error(f"新建向量数据库失败：{e}")
            raise RuntimeError(f"新建向量数据库失败：{e}")







