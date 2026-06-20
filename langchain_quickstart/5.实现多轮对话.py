from langchain_community.chat_models import ChatTongyi


class MultiTurnChat:
    def __init__(self, model: str, system_prompt: str = None):
        self.llm = ChatTongyi(model=model, streaming=True)
        self.chat_history = []
        if system_prompt:
            self.chat_history.append(("system", system_prompt))

    def send(self,user_message: str):
        #将对话添加倒历史
        self.chat_history.append(("human", user_message))
        #调用模型
        res = self.llm.stream(input=self.chat_history)
        full_reply = ""
        for chunk in res:
            if chunk.content:
                full_reply += chunk.content
                yield chunk.content
        #添加模型回复到历史
        self.chat_history.append(("ai", full_reply))


if __name__ == "__main__":
    MTC = MultiTurnChat(
        model="qwen3.7-max"
    )
    print("欢迎，输入“exit”或“quit”退出")
    while True:
        user_message = input("用户：")
        if (user_message == "exit") | (user_message == "quit"):
            break
        if not user_message.strip():
            print("请勿输入空白字符")
            continue
        for chunk in MTC.send(user_message):
            print(chunk, end="", flush=True)
        print()
