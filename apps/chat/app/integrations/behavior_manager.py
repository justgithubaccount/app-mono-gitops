import yaml
from app.logger import enrich_context

class BehaviorManager:
    """Loads and stores agent behavior from Notion."""

    def __init__(self, notion_client, page_id: str):
        self.notion_client = notion_client
        self.page_id = page_id
        self.behavior = {}

    async def refresh(self) -> None:
        log = enrich_context(event="behavior_refresh", page_id=self.page_id)
        data = await self.notion_client.fetch_page(self.page_id)
        log.info("Behavior page retrieved")
        try:
            # Expect first child to be a code block with YAML
            for block in data.get("results", []):
                if block.get("type") == "code":
                    text = block["code"].get("rich_text", [])
                    content = "".join(t.get("plain_text", "") for t in text)
                    self.behavior = yaml.safe_load(content) or {}
                    log.bind(event="behavior_loaded").info("Behavior updated")
                    return
            log.bind(event="behavior_not_found").warning("No YAML code block found")
        except Exception as e:
            log.bind(event="behavior_parse_error", error=str(e)).error("Failed to parse behavior")
            raise
