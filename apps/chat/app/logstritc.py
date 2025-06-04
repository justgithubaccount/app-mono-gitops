import logging
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().isoformat()

logger = logging.getLogger("chat")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(CustomJsonFormatter())
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

class LogWrapper(logging.LoggerAdapter):
    def bind(self, **kwargs):
        extra = self.extra.copy()
        extra.update(kwargs)
        return LogWrapper(self.logger, extra)

def with_context(**kwargs):
    return LogWrapper(logger, kwargs)
