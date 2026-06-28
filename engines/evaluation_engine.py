from datetime import datetime
from typing import Any, Dict, List

from .evaluators.base import BaseEvaluator
from .evaluators.ragas import RagasEvaluator
from .evaluators.heuristic import HeuristicEvaluator
# In-memory storage (MVP)
_evaluation_records: List[Dict[str, Any]] = []


def get_evaluator() -> BaseEvaluator:
    return HeuristicEvaluator()


def evaluate(
    prompt: str,
    response: str,
    context: List[str],
) -> Dict[str, Any]:
    """
    Run evaluation and save the result.
    """

    evaluator = get_evaluator()

    scores = evaluator.evaluate(
        prompt,
        response,
        context,
    )

    record = save_evaluation_record(
        prompt=prompt,
        response=response,
        context=context,
        scores=scores,
    )

    return record


def save_evaluation_record(
    prompt: str,
    response: str,
    context: List[str],
    scores: Dict[str, float],
) -> Dict[str, Any]:

    record = {
        "prompt": prompt,
        "response": response,
        "context": context,
        "faithfulness": scores["faithfulness"],
        "relevance": scores["relevance"],
        "overall_score": round(
            (
                scores["faithfulness"] +
                scores["relevance"]
            ) / 2,
            2,
        ),
        "evaluator": scores["evaluator"],
        "timestamp": datetime.utcnow().isoformat(),
    }

    _evaluation_records.append(record)

    return record


def get_all_evaluation_records() -> List[Dict[str, Any]]:
    return _evaluation_records
