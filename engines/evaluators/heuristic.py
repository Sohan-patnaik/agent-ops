from base import BaseEvaluator
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
    def evaluate(self, prompt: str, answer: str, context: List[str]) -> Dict[str, float]:
        answer_words = extract_words(answer)
        combined_context = " ".join(context)
        context_words = set(extract_words(combined_context))
        question_words = extract_words(prompt)

        # 1. Faithfulness Heuristic: answer words appearing in context
        if not answer_words:
            faithfulness_score = 0.0
        else:
            matching_in_context = sum(
                1 for w in answer_words if w in context_words)
            faithfulness_score = matching_in_context / len(answer_words)

        # 2. Relevance Heuristic: answer words matching question keywords
        # Filter question keywords (exclude stopwords)
        question_keywords = [w for w in question_words if w not in STOPWORDS]
        if not question_keywords:
            # Fallback to all question words if everything is filtered out
            question_keywords = question_words

        if not question_keywords:
            relevance_score = 0.0
        else:
            answer_word_set = set(answer_words)
            matching_keywords = sum(
                1 for w in question_keywords if w in answer_word_set)
            relevance_score = matching_keywords / len(question_keywords)

        return {
            "faithfulness": round(faithfulness_score, 2),
            "relevance": round(relevance_score, 2),
            "overall_score": round(
                (faithfulness_score + relevance_score) / 2,
                2,
            ),
            "evaluator": "heuristic"
        }
