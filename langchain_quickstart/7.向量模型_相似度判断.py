import numpy as np
from langchain_community.embeddings import DashScopeEmbeddings


def enclidean_distance(a, b):
    """计算欧式距离"""
    return np.linalg.norm(np.array( a) - np.array(b))

if __name__ == '__main__':
    texts = ["你好，我叫小明","你叫什么名字"]

    embedding = DashScopeEmbeddings()
    vectors = embedding.embed_documents(texts)

    print(enclidean_distance(vectors[0], vectors[1]))

