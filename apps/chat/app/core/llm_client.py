from typing import List
from ..schemas import Message
from ..core.config import get_settings
import httpx
import logging
import json

logger = logging.getLogger("llm-client")

class LLMClient:
    """
    LLMClient отвечает за запросы к внешнему LLM-proxy (litellm/openai-proxy).
    """

    def __init__(self, settings=None):
        self.settings = settings or get_settings()
        logger.info("LLMClient initialized with:")
        logger.info("  → chat_model: %s", self.settings.chat_model)
        logger.info("  → llm_api_url: %s", self.settings.llm_api_url)

    async def generate_reply(self, messages: List[Message]) -> str:
        payload = {
            "model": self.settings.chat_model,
            "messages": [m.dict() for m in messages],
        }

        logger.info("🔹 Sending request to LLM")
        logger.debug("📦 Payload: %s", json.dumps(payload, ensure_ascii=False, indent=2))
        logger.debug("🔗 URL: %s", f"{self.settings.llm_api_url}/chat/completions")

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{self.settings.llm_api_url}/chat/completions",
                    json=payload,
                )
                logger.info("📥 Response received with status %s", response.status_code)
                logger.debug("📭 Response headers: %s", response.headers)
                logger.debug("📄 Response body: %s", response.text)

                response.raise_for_status()
                data = response.json()
        except httpx.RequestError as e:
            logger.error("❌ Request to LLM failed: %s", str(e))
            raise
        except httpx.HTTPStatusError as e:
            logger.error("❌ LLM-proxy error: %s %s", e.response.status_code, e.response.text)
            raise

        if "choices" not in data or not data["choices"]:
            logger.error("⚠️ Malformed LLM response: %s", data)
            raise ValueError("Malformed LLM response")

        return data["choices"][0]["message"]["content"]
