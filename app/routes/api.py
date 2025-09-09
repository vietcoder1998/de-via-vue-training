from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Dict
from app.services.layer_2.analysis import AnalysisService

main_router = APIRouter()
service = AnalysisService()

class AnalyzeRequest(BaseModel):
    task: str = Field(..., example="DCF")
    model_type: str = Field("RandomForest", example="RandomForest")
    data: Dict[str, Any] = Field(
        ...,
        example={
            "free_cash_flow": [100, 110, 121, 133.1, 146.41],
            "terminal_growth_rate": 0.02,
            "discount_rate": 0.1,
            "shares_outstanding": 10,
            "net_debt": 50
        },
        description="Kèm mẫu data: DCF, Comparable, WACC, ... Xem thêm ví dụ ở phần mô tả."
    )

class AnalyzeResponse(BaseModel):
    result: Dict[str, Any] = Field(
        ...,
        example={
            "enterprise_value": 1500.0,
            "equity_value": 1450.0,
            "equity_value_per_share": 145.0
        }
    )

@main_router.get("/", summary="Health check")
async def index():
    """Health check endpoint."""
    return JSONResponse({"message": "Hello FastAPI!"})

@main_router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Run analysis",
    description="""
        ### Ví dụ mẫu cho các tác vụ phân tích tài chính

        #### DCF (Discounted Cash Flow)
        **Input:**
        ```json
        {
            "free_cash_flow": [100, 110, 121, 133.1, 146.41],
            "terminal_growth_rate": 0.02,
            "discount_rate": 0.1,
            "shares_outstanding": 10,
            "net_debt": 50
        }
        ```
    """,
    response_description="Analysis result",
    response_model_exclude_none=True,
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "result": {
                            "enterprise_value": 1500.0,
                            "equity_value": 1450.0,
                            "equity_value_per_share": 145.0
                        }
                    }
                }
            },
        }
    },
)
async def analyze(request: AnalyzeRequest = Body(...)):
    result = await service.handle_request(request.model_dump())
    return {"result": result}