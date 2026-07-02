import numpy as np
from typing import List, Tuple
from rank_bm25 import BM25Okapi
from langchain_community.embeddings import DashScopeEmbeddings


# ========== 余弦相似度函数 ==========
def cosine_similarity(vec1, vec2):
    """余弦相似度（值越大越相似）"""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# ========== 1. 准备数据 ==========
user_query = "GPT-4 参数量"

documents = [
    "GPT-4 是OpenAI发布的大语言模型，拥有约1.76万亿个参数",
    "GPT-3 的参数规模为1750亿，参数量比较大，是当时最大的语言模型之一",
    "GPT-3.5 的参数规模为1750亿，相比GPT-3有显著提升",
    "GPT-2 的参数规模为15亿，在当时已经是非常大的模型",
    "大语言模型的参数量直接影响推理能力",
]

# ========== 2. 初始化嵌入模型 ==========
embeddings = DashScopeEmbeddings(model="text-embedding-v1")


# ========== 3. 向量相似度搜索 ==========
def vector_search(query: str, docs: List[str]) -> List[Tuple[int, float]]:
    """向量检索：返回 (文档索引, 相似度分数)"""
    # 计算查询向量和文档向量
    query_embedding = embeddings.embed_query(query)
    doc_embeddings = embeddings.embed_documents(docs)

    # 计算余弦相似度
    similarities = [cosine_similarity(query_embedding, doc_vec) for doc_vec in doc_embeddings]

    # 返回按相似度降序排列的结果
    ranked = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
    return ranked


# ========== 4. BM25 关键词搜索 ==========
import jieba


def chinese_tokenizer(text: str) -> List[str]:
    """使用 jieba 进行中文分词"""
    return list(jieba.cut(text.strip()))


def bm25_search(query: str, docs: List[str]) -> List[Tuple[int, float]]:
    """BM25检索：返回 (文档索引, BM25分数)"""
    # 使用 jieba 分词
    tokenized_docs = [chinese_tokenizer(doc) for doc in docs]
    bm25 = BM25Okapi(tokenized_docs)

    tokenized_query = chinese_tokenizer(query)
    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return ranked


# ========== 5. 结果融合（Reciprocal Rank Fusion） ==========
def reciprocal_rank_fusion(
        rank_lists: List[List[Tuple[int, float]]],
        k: int = 60
) -> List[Tuple[int, float]]:
    """
    RRF融合多个排序列表

    Args:
        rank_lists: 多个排序列表，每个为 [(doc_id, score), ...]
        k: 平滑参数，默认60

    Returns:
        融合后的排序列表 [(doc_id, rrf_score), ...]
    """
    fusion_scores = {}

    for rank_list in rank_lists:
        for rank, (doc_id, score) in enumerate(rank_list, start=1):
            rrf_score = 1.0 / (k + rank)
            if doc_id not in fusion_scores:
                fusion_scores[doc_id] = 0.0
            fusion_scores[doc_id] += rrf_score

    fused = sorted(fusion_scores.items(), key=lambda x: x[1], reverse=True)
    return fused


# ========== 6. 执行搜索 ==========
print("=" * 60)
print(f"用户查询: {user_query}\n")

# 6.1 向量检索
print("【向量检索结果】")
vector_results = vector_search(user_query, documents)
for idx, score in vector_results:
    print(f"  文档 {idx} (相似度: {score:.4f}): {documents[idx]}")

print("\n" + "-" * 60)

# 6.2 BM25检索
print("【BM25检索结果】")
bm25_results = bm25_search(user_query, documents)
for idx, score in bm25_results:
    print(f"  文档 {idx} (BM25: {score:.4f}): {documents[idx]}")

print("\n" + "-" * 60)

# 6.3 融合结果
print("【RRF融合结果】")
fused_results = reciprocal_rank_fusion([vector_results, bm25_results])
for idx, rrf_score in fused_results:
    print(f"  文档 {idx} (RRF: {rrf_score:.4f}): {documents[idx]}")