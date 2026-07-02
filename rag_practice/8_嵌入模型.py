from langchain_community.embeddings import DashScopeEmbeddings

embedding_model = DashScopeEmbeddings()#(model=...)
user_input = "猫坐在垫子上"
res = embedding_model.embed_query(user_input)
print(len(res))