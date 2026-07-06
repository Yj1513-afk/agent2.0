import logging
from pathlib import Path
from typing import List
import logging
from urllib.parse import urlparse

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.setting import QaConfig

logger = logging.getLogger(__name__)

class PdfIngestor:
    """PDF文档切分"""

    #中文文本分隔符
    SEPARATORS = [
        "(?<=\n)", "(?<=。)", "(?<=！)", "(?<=？)", "(?<=；)", "(?<=，)", " ", ""
    ]

    def __init__(self,config:QaConfig) -> None:
        """
        初始化PDF加载器
        :param config: 配置信息
        """
        self._config = config

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._config.chunk_size,
            chunk_overlap=self._config.chunk_overlap,
            is_separator_regex=True,
            separators=self.SEPARATORS
        )

    def _split_document(self,documents:List[Document]) -> List[Document]:
        """
        切分文档为文本块
        :param documents: 原始document列表
        :return: 切分后的document列表
        """
        if not documents:
            logger.info("PDF为空，无法切分")
            return []

        try:
            chunks = self._splitter.split_documents(documents)
            logger.debug(f"切分PDF文档成功，{len(documents)}页共切分为{len(chunks)}个文本块")
            return chunks
        except  Exception as e:
            #logger.error(f"切分PDF文档时发生错误：{e}")
            raise RuntimeError(f"文本切分失败：{e}")

    def ingest(self,pdf_source:str) -> List[Document]:
        """
        加载PDF文档并切分
        :param pdf_source: PDF文件路径
        :return: 切分后的document列表
        """
        if not  pdf_source:
            raise ValueError("pdf_source不能为空")

        #网络文件，本地文件区分
        if self._is_url(pdf_source):
            logger.info(f"检测到URL，加载网络PDF文档：{pdf_source}")
            return self._ingest_from_url(pdf_source)
        else:
            logger.info(f"检测到本地文件，加载本地PDF文档：{pdf_source}")
            return self._ingest_from_file(pdf_source)


    def _is_url(self,source:str) -> bool:
        try:
            result = urlparse(source)
            return all([result.scheme in ['http','https'], result.netloc])
        except Exception:
            return False

    def _ingest_from_url(self,url:str) -> List[Document]:
        #判断文件是否存在requests()是否有返回
        try:
            documents = PyMuPDFLoader(url).load()
            return self._split_document(documents)
        except Exception as e:
            raise RuntimeError(f"加载PDF文档失败{url}：{e}")

    def _ingest_from_file(self,file_path:str) -> List[Document]:
        """
        本地文件加载
        :param file_path:
        :return: 切分后的document
        """
        path = Path(file_path)
        #检验文件存在
        if not path.exists():
            raise FileNotFoundError(f"文件不存在：{file_path}")
        if not path.is_file():
            raise ValueError(f"不是文件：{file_path}")

        try:
            documents = PyMuPDFLoader(file_path).load()
            return self._split_document(documents)
        except Exception as e:
            raise RuntimeError(f"加载PDF文档失败{file_path}：{e}")

if __name__ == '__main__':
    path = "../data/files/sample_document.pdf"

    ingestor = PdfIngestor(QaConfig())
    data = ingestor.ingest(path)
    print(len(data))
    print(data)