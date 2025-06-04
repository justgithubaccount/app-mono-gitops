import logging
import sys

import structlog


logging.basicConfig(stream=sys.stdout, format="%(message)s", level=logging.INFO)

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        structlog.processors.TimeStamper(fmt="iso", key="timestamp"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)


def with_context(**kwargs):
    """Return a logger pre-bound with contextual information."""
    return structlog.get_logger("chat").bind(**kwargs)
