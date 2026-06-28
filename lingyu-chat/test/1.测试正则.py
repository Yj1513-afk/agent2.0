import json
import re


def extract_json(text: str):
    find_text = re.search(r"{.*}", text, re.DOTALL)
    if find_text:
        try:
            return json.loads(find_text.group(0))
        except json.decoder.JSONDecodeError:
            print(f"'''{text}'''不是一个json字符串")

    return  {}

s1 = 'asdfghgfds{"a":"1"}'
print(extract_json(s1))