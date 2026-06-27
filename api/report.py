from fastapi import APIRouter
from engines.reporting_engine import generate_report

router = APIRouter()

@router.get("/report")
def get_report():
    """
    GET /report
    Returns the aggregated metrics report containing counts, average latencies, average cost, 
    and average evaluations scores.
    """
    return generate_report()
