MODEL_PRICING = {
    "gpt-4o": {
        "input": 5.0,
        "output": 15.0,
    }
}


def calculate_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> float:
    pricing = MODEL_PRICING.get(model)

    if pricing is None:
        return 0.0

    input_cost = (
        prompt_tokens / 1_000_000
    ) * pricing["input"]

    output_cost = (
        completion_tokens / 1_000_000
    ) * pricing["output"]

    return round(input_cost + output_cost, 6)