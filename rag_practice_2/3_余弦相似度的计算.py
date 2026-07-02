import numpy as np
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document

# ======================
# 1. 准备数据
# ======================
data = [
    Document(page_content="猫坐在垫子上"),
    Document(page_content="一只猫在垫子上休息"),
    Document(page_content="今天天气很好")
]
user_query = "猫在哪？"
# ======================
# 2. 初始化 embedding
# ======================
embeddings = DashScopeEmbeddings()
texts = [doc.page_content for doc in data]
all_embeddings = embeddings.embed_documents(texts) # List[str]
# query embedding
query_embedding = embeddings.embed_query(user_query)
# ======================
# 3. 定义距离计算函数
# ======================
def cosine_similarity(vec1, vec2):
    """余弦相似度（值越大越相似）"""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
# ======================
# 4. 计算每个文档的三种度量
# ======================
print("=" * 60)
print("余弦相似度对比（Query: 猫在哪？）")
print("=" * 60)

for i, doc in enumerate(data):
    print(f"\n文档{i+1}: {doc.page_content}")
    print(f"余弦相似度: {cosine_similarity(query_embedding, all_embeddings[i]):.6f}")