from fastapi import APIRouter, Body, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Dict, List
from app.services.layer_2.analysis import AnalysisService
import csv
import io

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

class MultiAnalyzeResponse(BaseModel):
    results: List[Dict[str, Any]]

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

@main_router.post(
    "/analyze-csv",
    response_model=MultiAnalyzeResponse,
    summary="Analyze multiple cases from CSV file",
    description="""
    Upload a CSV file and run analysis for each row.
    The CSV header must match the expected data fields (e.g. free_cash_flow, terminal_growth_rate, ...).
    """,
)
async def analyze_csv(
    task: str = Body(..., embed=True, example="DCF"),
    model_type: str = Body(..., embed=True, example="RandomForest"),
    file: UploadFile = File(...)
):
    # Read CSV file
    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    results = []
    for row in reader:
        # Convert numeric fields
        data = {}
        for k, v in row.items():
            # Try to parse lists (for free_cash_flow)
            if "[" in v and "]" in v:
                try:
                    data[k] = [float(x) for x in v.strip("[]").split(",")]
                except Exception:
                    data[k] = v
            else:
                try:
                    data[k] = float(v)
                except Exception:
                    data[k] = v
        req = {"task": task, "model_type": model_type, "data": data}
        result = await service.handle_request(req)
        results.append(result)
    return {"results": results}