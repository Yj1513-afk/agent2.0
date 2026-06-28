import logging
import os
import time

from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config import *
from core.intent_recognizer_with_structured_output import IntentRecognizer
from core.memory import Memory
from core.protocol import ChatResponse,ChatRequest

CONFIDENCE_THRESHOLD = 0.3
RECENT_MESSAGES = 2*3

log = logging.getLogger(__name__)

def _handle_low_confidence(
        intent_result,
        user_input: str
) -> str | None:
    return "抱歉，我没太理解您的需求。请问您是想：\n" \
           "1️⃣ 查询物流进度\n" \
           "2️⃣ 修改收货地址\n" \
           "3️⃣ 申请退货退款\n" \
           "4️⃣ 投诉建议\n" \
           "请回复数字或具体需求。"

def _system_prompt_by_intent(intent: str) -> str:
    mapping = {
        "track_shipping": "你是电商物流查询客服。先要订单号/运单号；如果缺失就追问。",
        "change_address": "你是电商改地址客服。先确认是否已发货；需要订单号+新地址。",
        "refund": "你是电商退货退款客服。先给3步结论，再给注意事项，最后引导用户提供订单号。",
        "complaint": "你是电商投诉处理客服。先安抚，再收集订单号与问题细节，给出处理时效。",
        "general": "你是一个友好、简洁的聊天助手。",
    }
    return mapping.get(intent.strip(), mapping["general"])

class ChatService:
    def __init__(self,api_key:str| None = None):

        #初始化日志记录
        if not logging.root.handlers:
            logging.basicConfig(level=logging.INFO)

        #初始化llm
        if api_key:
            os.environ['DASHSCOPE_API_KEY'] = api_key
        elif not os.environ.get('DASHSCOPE_API_KEY'):
            raise RuntimeError("api_key not set")

        self.__llm = ChatTongyi(
            model= TONGYI_MODEL,
            temperature=TEMPERATURE,            # 降低温度值，缩短首字延迟，使输出更稳定
            # 关键：通过 model_kwargs 传递百炼专属参数
            model_kwargs={
                "enable_thinking": ENABLE_THINKING  # 强制关闭深度思考模式
            }
        )
        self.__intent_recognizer = IntentRecognizer(ChatTongyi(model=INTENT_RECOGNIZE_MODEL))
        self.__memory_cache: dict[str, Memory] = {}

    def get_memory(self,chat_session_id: str) -> Memory:
        if chat_session_id not in self.__memory_cache:
            self.__memory_cache[chat_session_id] = Memory(chat_session_id)
        return self.__memory_cache[chat_session_id]

    def handle(self,request: ChatRequest) -> ChatResponse:
        start_time = time.time()

        try:
            #1.意图识别
            memory = self.get_memory(request.chat_session_id)
            intent_result  = self.__intent_recognizer.recognizer(
                request.user_input,
                memory.get_messages_text(RECENT_MESSAGES)
            )

            #2.低置信度处理
            if intent_result.confidence <= CONFIDENCE_THRESHOLD:
                return ChatResponse(
                    user_id=request.user_id,
                    chat_session_id=request.chat_session_id,
                    trace_id=request.trace_id,
                    response=_handle_low_confidence(intent_result,request.user_input)
                )
            #todo 是否需要将回答添加到历史记录？

            #3.确认主要意图，路由到对应链接
            intents = intent_result.intents
            intent_context = intents[0] if intents else "general"
            #intent_context = _system_prompt_by_intent(intent_result.intents[0] if intent_result.intents else "general")

            #4.根据不同意图，构建提示词
            prompt = ChatPromptTemplate.from_messages([
                ("system", _system_prompt_by_intent(intent_context)),
                #("system", "你是一个电商助手"),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{user_input}")
            ])

            #5.记忆管理，上下文准备,事实+摘要+最近消息
            memory_messages = memory.prepare_memory_for_llm()

            #6.大模型调用
            parser = StrOutputParser()
            chain = prompt | self.__llm | parser
            response = chain.invoke(input={"chat_history":memory_messages, "user_input":request.user_input})
            #7.写回历史消息
            memory.add_user_message(request.user_input,llm=self.__llm)
            memory.add_ai_message(response,llm=self.__llm)

            #8关键事实管理
            memory.update_key_facts(intent_result.slots)
            #9.日志记录
            self.__log(
                req=request,
                intents=intent_result.intents,
                confidence=intent_result.confidence,
                action="normal",
                latency_ms=int((time.time() - start_time) * 1000),
            )
            return ChatResponse(
                user_id=request.user_id,
                chat_session_id=request.chat_session_id,
                trace_id=request.trace_id,
                response=response
            )
        except Exception as e:
            # 异常处理，记录错误日志
            self.__log(
                req=request,
                intents=["error"],
                confidence=0.0,
                action="error",
                latency_ms=int((time.time() - start_time) * 1000),
                error=str(e),
            )
            raise e


    def __log(self,
            *,
            req: ChatRequest,
            intents: list[str],
            confidence: float,
            action: str,
            latency_ms: int,
            error: str | None = None):
        payload = {
            "trace_id": req.trace_id,
            "user_id": req.user_id,
            "session_id": req.chat_session_id,
            "intents": intents,
            "confidence": confidence,
            "action": action,
            "latency_ms": latency_ms
        }

        if error:
            payload["error"] = error
            logging.error(payload)
        else:
            logging.info(payload)



















