from langchain_community.document_loaders import PyMuPDFLoader

file_path = r'date\files\sample_document.pdf'

pdf_loader = PyMuPDFLoader(file_path=file_path)
#loader()一次加载
docs = pdf_loader.load()
#print(type(docs))  class 'list'
#print(type(docs[0])) Document page_context Metadata
for doc in docs:
    print(f"内容:{doc.page_content[:100]}")
    print(f"元数据:{doc.metadata}")
    print()
