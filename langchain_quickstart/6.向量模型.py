from langchain_community.embeddings import DashScopeEmbeddings

#创建
embeddings = DashScopeEmbeddings(model="text-embedding-v1")

#文本向量化
res = embeddings.embed_query("你好，我叫小明")

#输出
print(res)