import time
from typing import Any, Dict

import requests
from opentelemetry import trace

from .normalizer import normalize_response
from .pricing import calculate_cost

tracer = trace.get_tracer(__name__)


def monitor_call(
    api_url: str,
    prompt: str,
    response: Any,
) -> Dict[str, Any]:

    start = time.perf_counter()

    with tracer.start_as_current_span("llm.call") as span:

        llm = normalize_response(response)

        latency = time.perf_counter() - start

        cost = calculate_cost(
            model=llm["model"],
            prompt_tokens=llm["prompt_tokens"],
            completion_tokens=llm["completion_tokens"],
        )

        span.set_attribute("llm.prompt", prompt)
        span.set_attribute("llm.response", llm["content"])
        span.set_attribute("llm.model", llm["model"])
        span.set_attribute(
            "llm.prompt_tokens",
            llm["prompt_tokens"],
        )
        span.set_attribute(
            "llm.completion_tokens",
            llm["completion_tokens"],
        )
        span.set_attribute(
            "llm.total_tokens",
            llm["total_tokens"],
        )
        span.set_attribute(
            "llm.latency_ms",
            latency * 1000,
        )
        span.set_attribute(
            "llm.cost_usd",
            cost,
        )

        payload = {
            "prompt": prompt,
            "response": llm["content"],
            "model": llm["model"],
            "metrics": {
                "prompt_tokens": llm["prompt_tokens"],
                "completion_tokens": llm["completion_tokens"],
                "total_tokens": llm["total_tokens"],
                "latency": latency,
                "cost": cost,
            },
        }

    resp = requests.post(
        f"{api_url}/monitor",
        json=payload,
    )

    resp.raise_for_status()

    return resp.json()