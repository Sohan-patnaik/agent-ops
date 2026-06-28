from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from engines.evaluation_engine import (
    evaluate,
    get_all_evaluation_records,
)

router = APIRouter()

class EvaluateRequest(BaseModel):
    prompt: str
    response: str
    context: List[str]

class EvaluateResponse(BaseModel):
    faithfulness: float
    relevance: float
    overall_score: float
    evaluator: str

@router.post("/evaluate", response_model=EvaluateResponse)
def post_evaluate(data: EvaluateRequest):

    try:

        result = evaluate(
            prompt=data.prompt,
            response=data.response,
            context=data.context,
        )

        return EvaluateResponse(
            faithfulness=result["faithfulness"],
            relevance=result["relevance"],
            overall_score=result["overall_score"],
            evaluator=result["evaluator"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@router.get(
    "/evaluate",
    response_model=List[Dict[str, Any]],
)
def get_evaluate():

    return get_all_evaluation_records()