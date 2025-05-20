from typing import List, Optional
from ..schemas import Message
from ..core.config import get_settings
import httpx
import logging

logger = logging.getLogger("llm-client")

class LLMClient:
    """
    LLMClient отвечает за запросы к внешнему LLM-proxy (litellm/openai-proxy).
    Сюда можно делегировать логику авторизации, ретраев, логирования.
    """

    def __init__(self, settings=None):
        self.settings = settings or get_settings()

    async def generate_reply(self, messages: List[Message], user_api_key: Optional[str] = None) -> str:
        payload = {
            "model": self.settings.chat_model,
            "messages": [m.dict() for m in messages],
        }

        # Используем ключ клиента, если передан, иначе дефолтный из настроек
        api_key = user_api_key or self.settings.openai_api_key

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{self.settings.llm_api_url}/chat/completions",
                    json=payload,
                    headers={"Authorization": f"Bearer {api_key}"}
                )
                response.raise_for_status()
                data = response.json()
        except httpx.RequestError as e:
            logger.error(f"Request to LLM failed: {e}")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"LLM-proxy error: {e.response.status_code} {e.response.text}")
            raise

        if "choices" not in data or not data["choices"]:
            logger.error(f"Malformed LLM response: {data}")
            raise ValueError("Malformed LLM response")

        return data["choices"][0]["message"]["content"]
