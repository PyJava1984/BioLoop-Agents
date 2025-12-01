import json
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Callable

import requests
from jsonschema import validate, ValidationError


# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------

def get_logger(name: str = "bioloop"):
    """
    Standardized structured logging for all agents.
    Emits JSON logs compatible with GCP Logging and OpenTelemetry.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '{"timestamp":"%(asctime)s","severity":"%(levelname)s","message":"%(message)s"}'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


logger = get_logger()


# ---------------------------------------------------------------------------
# Time Utilities
# ---------------------------------------------------------------------------

def now_utc_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def parse_timestamp(ts: str) -> datetime:
    """Parse an ISO-8601 timestamp."""
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# Pub/Sub Helpers
# ---------------------------------------------------------------------------

def encode_pubsub_message(payload: Dict[str, Any]) -> bytes:
    """Convert dict → JSON bytes for Pub/Sub."""
    try:
        return json.dumps(payload).encode("utf-8")
    except Exception as e:
        logger.error(f"Failed to encode Pub/Sub message: {e}")
        raise


def decode_pubsub_message(message: bytes) -> Dict[str, Any]:
    """Convert Pub/Sub bytes → dict."""
    try:
        return json.loads(message.decode("utf-8"))
    except Exception as e:
        logger.error(f"Failed to decode Pub/Sub message: {e}")
        raise


# ---------------------------------------------------------------------------
# Schema Validation
# ---------------------------------------------------------------------------

def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]):
    """
    Validate incoming payloads using JSON Schema.
    Ensures agent inputs are always clean and predictable.
    """
    try:
        validate(data, schema)
    except ValidationError as e:
        logger.error(f"Schema validation failed: {e.message}")
        raise


# ---------------------------------------------------------------------------
# HTTP Utilities
# ---------------------------------------------------------------------------

def http_post_json(
    url: str,
    payload: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10
) -> Dict[str, Any]:
    """
    Wrapper for POSTing JSON to other agents (A2A or external APIs).
    Includes error handling + safe defaults.
    """
    try:
        headers = headers or {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=timeout)

        if not response.ok:
            logger.error(
                f"HTTP POST failed: {response.status_code} {response.text} → URL: {url}"
            )
            response.raise_for_status()

        return response.json() if response.text else {}
    except Exception as e:
        logger.error(f"HTTP POST error for {url}: {str(e)}")
        raise


# ---------------------------------------------------------------------------
# Retry Helpers (Exponential Backoff)
# ---------------------------------------------------------------------------

def retry(
    func: Callable,
    retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 4.0,
    exceptions: tuple = (Exception,)
):
    """
    Generic retry decorator for network-dependent tasks
    (e.g., A2A calls, IoT fetches, climate API fetches).
    """

    def wrapper(*args, **kwargs):
        attempt = 0
        while attempt <= retries:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                if attempt == retries:
                    logger.error(f"Retry exhausted for {func.__name__}: {str(e)}")
                    raise

                delay = min(max_delay, base_delay * (2 ** attempt))
                logger.warning(
                    f"{func.__name__} failed (attempt {attempt+1}/{retries}). "
                    f"Retrying in {delay:.2f}s… Error: {str(e)}"
                )
                time.sleep(delay)
                attempt += 1

    return wrapper


# ---------------------------------------------------------------------------
# ID / UUID Helpers
# ---------------------------------------------------------------------------

def generate_event_id() -> str:
    """Unique ID for MCP or agent events."""
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Safe Execution Wrapper
# ---------------------------------------------------------------------------

def safe_run(label: str, fn: Callable, *args, **kwargs) -> Any:
    """
    Safely execute agent logic with structured error logging.
    Prevents a single failure from crashing the entire agent.
    """
    try:
        logger.info(f"Executing {label}…")
        return fn(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error during {label}: {str(e)}")
        return {
            "error": str(e),
            "label": label,
            "timestamp": now_utc_iso()
        }


# ---------------------------------------------------------------------------
# Pretty Printing / Debug Utility
# ---------------------------------------------------
