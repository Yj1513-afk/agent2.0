from langchain_community.document_loaders import TextLoader

file_path = r'date\files\北京有什么好玩的.txt'

text_loader = TextLoader(file_path=file_path,encoding="utf-8")
docs = text_loader.load()
print(len(docs))
print(docs)
print(docs[0].page_content)
print(docs[0].metadata)