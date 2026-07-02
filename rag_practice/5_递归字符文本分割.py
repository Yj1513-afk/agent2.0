from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = r'date\files\历史文化.txt'

loder = TextLoader(file_path=file_path,encoding="utf-8")
doc = loder.load()

#文本拆分
splitter = RecursiveCharacterTextSplitter(
    chunk_size=55,
    chunk_overlap=8,
    separators=["\n\n", "\n", " ", "、", "。", "？", "！", "；", ""],
    length_function=len
)

chunks = splitter.split_text(doc[0].page_content)
for i,chunk in enumerate(chunks):
    print(f"-----块{i}{len( chunk)}")
    print(f"{i}:{chunk}")