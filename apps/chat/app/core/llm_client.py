from typing import List, Optional
from ..schemas import Message
from ..core.config import get_settings
from app.logger import with_context
import httpx
import time

class LLMClient:
    def __init__(self, settings=None):
        self.settings = settings or get_settings()
        with_context(
            event="llm_client_init",
            model=self.settings.chat_model,
            llm_api_url=self.settings.llm_api_url,
        ).info("LLM client initialized")

    async def generate_reply(
        self,
        messages: List[Message],
        user_api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> str:
        user_message = messages[-1].content if messages else ""

        log = with_context(
            project_id=project_id,
            user_message=user_message,
            model=self.settings.chat_model,
            trace_id=trace_id,
        )

        log.bind(event="llm_request_sent").info("Sending request to LLM")

        try:
            start = time.time()
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{self.settings.llm_api_url}/chat/completions",
                    json={
                        "model": self.settings.chat_model,
                        "messages": [m.dict() for m in messages],
                    },
                )
                response.raise_for_status()
                data = response.json()
            duration = time.time() - start

        except httpx.RequestError as e:
            log.bind(
                event="llm_network_error",
                error=str(e)
            ).error("Network error during LLM call")
            raise

        except httpx.HTTPStatusError as e:
            log.bind(
                event="llm_http_error",
                status_code=e.response.status_code,
                response=e.response.text
            ).error("HTTP error during LLM call")
            raise

        if "choices" not in data or not data["choices"]:
            log.bind(
                event="llm_malformed_response",
                data=data
            ).error("Malformed response from LLM")
            raise ValueError("Malformed LLM response")

        reply = data["choices"][0]["message"]["content"]

        log.bind(
            event="llm_response_received",
            ai_reply=reply,
            latency=duration,
        ).info("LLM replied successfully")

        return reply
