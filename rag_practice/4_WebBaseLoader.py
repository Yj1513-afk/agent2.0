from langchain_community.document_loaders import WebBaseLoader

# 加载网页内容
loader = WebBaseLoader("https://python.langchain.com/docs/")
documents = loader.load()

print(f"加载了 {len(documents)} 个文档") # 加载了 1 个文档
print(f"元数据：{documents[0].metadata}") # 元数据：{'source': 'https://python.langchain.com/docs/', 'title': 'LangChain overview - Docs by LangChain',
print(f"标题: {documents[0].metadata.get('title', 'N/A')}") # 标题: LangChain overview - Docs by LangChain
print(f"URL: {documents[0].metadata['source']}") # URL: https://python.langchain.com/docs/
print(f"内容长度: {len(documents[0].page_content)} 字符") # 内容长度: 4311 字符