from typing import List, Dict, Any
from datetime import datetime

# In-memory database (MVP)
_monitoring_records: List[Dict[str, Any]] = []


def save_monitoring_record(
    prompt: str,
    response: str,
    model: str,
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Save a normalized monitoring record.

    metrics = {
        "prompt_tokens": int,
        "completion_tokens": int,
        "total_tokens": int,
        "latency": float,
        "cost": float
    }
    """

    record = {
        "prompt": prompt,
        "response": response,
        "model": model,
        "metrics": {
            "prompt_tokens": metrics.get("prompt_tokens", 0),
            "completion_tokens": metrics.get("completion_tokens", 0),
            "total_tokens": metrics.get("total_tokens", 0),
            "latency": metrics.get("latency", 0.0),
            "cost": metrics.get("cost", 0.0),
        },
        "timestamp": datetime.utcnow().isoformat(),
    }

    _monitoring_records.append(record)

    return record


def get_all_monitoring_records() -> List[Dict[str, Any]]:
    """
    Return all monitoring records.
    """
    return _monitoring_records