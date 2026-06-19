from openai import OpenAI


class MultiTurnChat:
    def __init__(self, base_url: str, model: str, system_prompt: str = None):
        self.client = OpenAI(base_url=base_url)
        self.model = model
        self.chat_history = []
        if system_prompt:
            self.chat_history.append({"role": "system", "content": system_prompt})

    def add_user_message(self,user_message: str):
        self.chat_history.append({"role": "user", "content": user_message})

    def send(self,user_message: str) -> str:
        #1.添加用户消息到历史
        self.add_user_message(user_message)
        #2.调用模型
        completion = self.client.chat.completions.create(model=self.model, messages=self.chat_history)
        #3.提取模型回复结果
        result = completion.choices[0].message.content
        #4.添加模型回复到历史
        self.chat_history.append({"role": "assistant", "content": result})
        return result


if __name__ == "__main__":
    MTC = MultiTurnChat(
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen3.7-max"
    )
    print("欢迎，输入“exit”或“quit”退出")
    while True:
        user_message = input("用户：")
        if (user_message == "exit") | (user_message == "quit"):#user_message in ["exit", "quit"]:
            break
        if not user_message.strip():
            print("请勿输入空白字符")
            continue
        print(MTC.send(user_message))