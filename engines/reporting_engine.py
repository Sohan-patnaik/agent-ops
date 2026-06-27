from typing import Dict, Any
from engines.monitoring_engine import get_all_monitoring_records
from engines.evaluation_engine import get_all_evaluation_records

def generate_report() -> Dict[str, Any]:

    monitoring = get_all_monitoring_records()
    evaluation = get_all_evaluation_records()

    total_requests = len(monitoring)
    total_evaluations = len(evaluation)

    if monitoring:

        avg_latency = sum(
            r["metrics"]["latency"]
            for r in monitoring
        ) / total_requests

        avg_tokens = sum(
            r["metrics"]["total_tokens"]
            for r in monitoring
        ) / total_requests

        avg_cost = sum(
            r["metrics"]["cost"]
            for r in monitoring
        ) / total_requests

        total_cost = sum(
            r["metrics"]["cost"]
            for r in monitoring
        )

    else:

        avg_latency = 0.0
        avg_tokens = 0.0
        avg_cost = 0.0
        total_cost = 0.0

    if evaluation:

        avg_faithfulness = sum(
            r["faithfulness"]
            for r in evaluation
        ) / total_evaluations

        avg_relevance = sum(
            r["relevance"]
            for r in evaluation
        ) / total_evaluations

        avg_score = sum(
            r["overall_score"]
            for r in evaluation
        ) / total_evaluations

    else:

        avg_faithfulness = 0.0
        avg_relevance = 0.0
        avg_score = 0.0

    latest_request = monitoring[-1] if monitoring else None

    return {

        "total_requests": total_requests,
        "total_evaluations": total_evaluations,

        "monitoring": {

            "avg_latency": round(avg_latency, 2),
            "avg_tokens": round(avg_tokens, 2),
            "avg_cost": round(avg_cost, 6),
            "total_cost": round(total_cost, 6),
        },

        "evaluation": {

            "avg_faithfulness": round(avg_faithfulness, 2),
            "avg_relevance": round(avg_relevance, 2),
            "avg_score": round(avg_score, 2),
        },

        "latest_request": latest_request,
    }