from .base import BaseEvaluator
from typing import Dict, List
import os

try:
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False


class RagasEvaluator(BaseEvaluator):
    def evaluate(self, prompt: str, response: str, context: List[str]) -> Dict[str, float]:
        # If ragas is not available or no OpenAI API key is set, default to HeuristicEvaluato

        # Convert context to list for Ragas format
        data_samples = {
            'question': [prompt],
            'response': [response],
            'contexts': [context]
        }
        dataset = Dataset.from_dict(data_samples)

        # Execute Ragas evaluation
        result = evaluate(
            dataset,
            metrics=[faithfulness, answer_relevancy]
        )

        f_score = result.get("faithfulness", 0.0)
        r_score = result.get("answer_relevancy", 0.0)

        # Handle possible NaN/None values from LLM evaluation failures
        if f_score is None or str(f_score) == "nan":
            f_score = 0.0
        if r_score is None or str(r_score) == "nan":
            r_score = 0.0

        return {
            "faithfulness": round(float(f_score), 2),
            "relevance": round(float(r_score), 2),
            "overall_score": round(
                (f_score + r_score) / 2,
                2,
            ),
            "evaluator": "ragas"
        }
