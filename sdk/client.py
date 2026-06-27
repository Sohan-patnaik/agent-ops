from typing import List, Union, Dict, Any
from core.config import AGENTOPS_API_URL
from sdk.monitor import monitor_call
from sdk.evaluate import evaluate_call

class AgentOps:
    """
    Main entry point for the AgentOps SDK.
    Handles communication with the AgentOps platform.
    """
    def __init__(self, api_url: str = None):
        self.api_url = api_url or AGENTOPS_API_URL

    def monitor(
        self,
        prompt: str,
        response: Any
    ) -> Dict[str, Any]:
        """
        Logs a query and response to the dashboard.
        """
        return monitor_call(
            api_url=self.api_url,
            prompt=prompt,
            response=response,
        )

    def evaluate(
        self,
        question: str,
        answer: str,
        context: Union[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Evaluates the answer based on faithfulness and relevance metrics.
        """
        return evaluate_call(
            api_url=self.api_url,
            question=question,
            answer=answer,
            context=context
        )
