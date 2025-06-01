from loguru import logger
import sys
import json

def flat_json_formatter(record):
    flat = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "logger": record["name"],
        "module": record["module"],
        "function": record["function"],
        "line": record["line"],
        "event": record["extra"].get("event"),
        "project_id": record["extra"].get("project_id"),
        "trace_id": record["extra"].get("trace_id"),
        "model": record["extra"].get("model"),
        "job": record["extra"].get("job"),
        "user_message": record["extra"].get("user_message"),
        "ai_reply": record["extra"].get("ai_reply"),
    }
    return json.dumps({k: v for k, v in flat.items() if v is not None}) + "\n"

# Очищаем стандартные хендлеры
logger.remove()

# ✅ Передаём через sink
logger.add(
    sink=lambda msg: sys.stdout.write(flat_json_formatter(msg.record)),
    enqueue=True,
    level="INFO",
)

def with_context(**kwargs):
    return logger.bind(**kwargs)
