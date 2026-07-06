import hashlib

text = "hello world"
hash_value = hashlib.md5(text.encode('utf-8'))
print(hash_value.hexdigest())
print(hash_value)