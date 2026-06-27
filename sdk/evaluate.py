import requests
from typing import Any, Dict, List, Union


def evaluate_call(
    api_url: str,
    prompt: str,
    response: Any,
    context: Union[str, List[str]],
) -> Dict[str, Any]:
    """
    Sends evaluation inputs to the AgentOps API.
    """

    # Extract answer text
    answer = (
        response.content
        if hasattr(response, "content")
        else str(response)
    )

    # Normalize context
    if isinstance(context, str):
        context = [context]

    payload = {
        "prompt": prompt,
        "answer": answer,
        "context": context,
    }

    resp = requests.post(
        f"{api_url}/evaluate",
        json=payload,
    )

    resp.raise_for_status()

    return resp.json()