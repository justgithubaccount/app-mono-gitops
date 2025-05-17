from typing import List
from ..schemas import Message
from ..core.llm_client import LLMClient

class ChatService:
    """
    ChatService инкапсулирует бизнес-логику чата.
    Можно расширять, мокать, делегировать мидлам/джунам для добавления фичей.
    """
    def __init__(self, llm_client: LLMClient = None):
        # Можно подменять клиента на тестах, например, на фейковый.
        self.llm_client = llm_client or LLMClient()

    async def get_ai_reply(self, messages: List[Message]) -> str:
        # Можно добавить обработку pre/post-processing, логику ветвления, etc.
        reply = await self.llm_client.generate_reply(messages)
        return reply
