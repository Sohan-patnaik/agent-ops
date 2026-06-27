from typing import Any, Dict


def normalize_response(response: Any) -> Dict[str, Any]:
    """
    Convert an LLM response into a common format.

    Currently supports:
    - LangChain AIMessage
    """

    content = (
        response.content
        if hasattr(response, "content")
        else str(response)
    )

    metadata = (
        response.response_metadata
        if hasattr(response, "response_metadata")
        else {}
    ) or {}

    usage = metadata.get("token_usage", {})

    return {
        "content": content,
        "model": (
            metadata.get("model_name")
            or metadata.get("model")
            or "unknown"
        ),
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get(
            "completion_tokens",
            0,
        ),
        "total_tokens": usage.get(
            "total_tokens",
            0,
        ),
    }