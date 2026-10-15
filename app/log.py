"""Structured logging setup with secret scrubbing.

All log output is JSON so downstream log systems can index it. The scrub
processor masks sensitive keys before rendering.
"""

import logging
from typing import Any

import structlog
from structlog.typing import EventDict

# Keys whose values must never appear in logs.
REDACTED_KEYS = frozenset({"password", "token", "secret", "authorization", "api_key"})


def scrub_sensitive(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Replace values of sensitive keys with a fixed placeholder."""
    for key in event_dict:
        if key.lower() in REDACTED_KEYS:
            event_dict[key] = "[REDACTED]"
    return event_dict


def configure_logging() -> None:
    """Configure structlog for JSON output with scrubbing and timestamps."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            scrub_sensitive,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(level=logging.INFO)


def get_logger(name: str) -> Any:
    return structlog.get_logger(name)
