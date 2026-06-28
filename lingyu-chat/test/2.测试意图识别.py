from langchain_community.chat_models import ChatTongyi

from core.intent_recognizer import IntentRecognizer

llm = ChatTongyi(
    model="qwen3.7-max",
    streaming=True,
    temperature=0.3,            # 降低温度值，缩短首字延迟，使输出更稳定
    # 关键：通过 model_kwargs 传递百炼专属参数
    model_kwargs={
        "enable_thinking": False  # 强制关闭深度思考模式
    }
)
recognizer = IntentRecognizer(llm)
res = recognizer.recognizer("我的订单号是2026565565565")
print( res)
res = recognizer.recognizer("我的订单号是2026565565565", "human:我要退货\nai:请提供你的订单号。")
print(res)