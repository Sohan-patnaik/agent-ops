import requests
from typing import Dict, Any, List, Union
from sdk.client import AgentOps
from core.config import AGENTOPS_API_URL

def run_orchestrated_pipeline(
    query: str,
    llm_response: Any,
    context: Union[str, List[str]],
    model: str = "gpt-4o",
    api_url: str = None
) -> Dict[str, Any]:
    """
    Orchestrates the lifecycle of an LLM query and response:
    1. Monitor: logs query/response statistics to the observability engine.
    2. Evaluate: evaluates response quality based on context.
    3. Report: returns the updated aggregated platform metrics.
    """
    url = api_url or AGENTOPS_API_URL
    client = AgentOps(api_url=url)
    
    # 1. Monitor
    monitor_result = client.monitor(
        prompt=query,
        response=llm_response
    )
    
    response_text = (
        llm_response.content
        if hasattr(llm_response, "content")
        else str(llm_response)
    )
    
    # 2. Evaluate
    eval_result = client.evaluate(
        question=query,
        answer=response_text,
        context=context
    )
    
    # 3. Report
    report_resp = requests.get(f"{url}/report")
    report_resp.raise_for_status()
    report_result = report_resp.json()
    
    return {
        "monitor": monitor_result,
        "evaluation": eval_result,
        "report": report_result
    }
