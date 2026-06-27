from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from engines.monitoring_engine import (
    get_all_monitoring_records,
    save_monitoring_record,
)

router = APIRouter()

class Metrics(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency: float
    cost: float


class MonitorRequest(BaseModel):
    prompt: str
    response: str
    model: str
    metrics: Metrics


class MonitorResponse(BaseModel):
    prompt: str
    response: str
    model: str
    metrics: Metrics

@router.post("/monitor", response_model=MonitorResponse)
def post_monitor(data: MonitorRequest):

    try:

        save_monitoring_record(
            prompt=data.prompt,
            response=data.response,
            model=data.model,
            metrics=data.metrics.model_dump(),
        )

        return MonitorResponse(
            prompt=data.prompt,
            response=data.response,
            model=data.model,
            metrics=data.metrics,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@router.get(
    "/monitor",
    response_model=List[Dict[str, Any]],
)
def get_monitor():

    return get_all_monitoring_records()