import logging
import sys

import structlog
from opentelemetry.trace import get_current_span


logging.basicConfig(stream=sys.stdout, format="%(message)s", level=logging.INFO)

def add_trace_context(_, __, event_dict):
    span = get_current_span()
    if span and span.get_span_context().trace_id != 0:
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        structlog.processors.TimeStamper(fmt="iso", key="timestamp"),
        add_trace_context,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)


def with_context(**kwargs):
    """Return a logger pre-bound with contextual information."""
    return structlog.get_logger("chat").bind(**kwargs)


def enrich_context(event: str, **kwargs):
    """Return logger enriched with an event name and extra fields."""
    return structlog.get_logger("chat").bind(event=event, **kwargs)
