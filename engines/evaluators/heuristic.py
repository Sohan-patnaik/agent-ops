from .base import BaseEvaluator
from typing import Dict, List

import re

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "of", "to", "in",
    "for", "on", "with", "at", "by", "from", "it", "this", "that", "these", "those",
    "i", "you", "he", "she", "they", "we", "us", "them", "my", "your", "his", "her"
}


def extract_words(text: str) -> List[str]:
    """Helper to extract normalized, lowercase alphanumeric words from text."""
    if not text:
        return []
    return re.findall(r'\b\w+\b', text.lower())


class HeuristicEvaluator(BaseEvaluator):

    def evaluate(self, prompt: str, response: str, context: List[str]) -> Dict[str, float]:
        answer_words = extract_words(response)
        combined_context = " ".join(context)
        context_words = set(extract_words(combined_context))

        # Faithfulness
        if not answer_words:
            faithfulness_score = 0.0
        else:
            matching_in_context = sum(
                1 for w in answer_words if w in context_words
            )
            faithfulness_score = matching_in_context / len(answer_words)

        # Relevance (MVP)
        relevance_score = faithfulness_score

        return {
            "faithfulness": round(faithfulness_score, 2),
            "relevance": round(relevance_score, 2),
            "overall_score": round(
                (faithfulness_score + relevance_score) / 2,
                2,
            ),
            "evaluator": "heuristic",
        }
