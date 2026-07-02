from langchain_text_splitters import RecursiveCharacterTextSplitter

# 测试文本：一个没有空格和标点的超长字符串
text = "这是一个超长超长超长超长超长超长超长超长超长超长超长超长超长超长超长的单词"

# 创建分割器
splitter = RecursiveCharacterTextSplitter(
    chunk_size=20,  # 每个块最大20个字符
    chunk_overlap=5,  # 块之间重叠5个字符
    separators=[" ", ""],  # 先尝试按空格切，最后按字符切
    length_function=len
)
# 执行分割
chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"\n--- 块 {i + 1} (长度: {len(chunk)}) ---")
    print(f"内容: {chunk}")
    print("-" * 40)