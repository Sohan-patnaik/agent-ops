from abc import ABC, abstractmethod
from typing import Dict

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, question: str, answer: str, context: str) -> Dict[str, float]:
        """Runs evaluation and returns metric scores."""
        pass