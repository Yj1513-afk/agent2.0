import hashlib

class HashCalculate:
    """根据文件内容计算文件hash"""
    def compute_hash(self,pdf_bytes:bytes) -> str:
        """从字节数据计算MD5值"""
        return hashlib.md5(pdf_bytes).hexdigest()

    def compute_hash_from_file(self,file_path:str) -> str:
        """从文件计算MD5值"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):#iter(functools.partial(f.read, 4096), b"")等价
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

