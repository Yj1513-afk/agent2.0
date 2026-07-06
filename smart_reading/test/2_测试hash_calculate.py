from indexing.hash_calculate import HashCalculate

hash_calculate = HashCalculate()
path = "../data/files/sample_document.pdf"
print(hash_calculate.compute_hash_from_file(path))