from pydoc import pager

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from pymupdf.extra import page_count

chroma = Chroma(
    persist_directory="./chroma_db",
    collection_name="test_collection",
    embedding_function=DashScopeEmbeddings(),
)

# 数据
date = [
    Document(page_content = "猫坐在垫子上"),
    Document(page_content = "一只猫坐在垫子上"),
    Document(page_content = "今天天气很好"),
]

chroma.add_documents(
    documents=date,
    ids=[f"id-{i}" for i in range(1,len(date)+1)]
)

#相似度查询
user_query = '猫在哪？'
res = chroma.similarity_search(user_query, k=1)
print( res)
chroma.delete(["id-2"])
res = chroma.similarity_search(user_query, k=1)
print( res)