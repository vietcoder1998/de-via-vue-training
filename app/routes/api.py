from fastapi import APIRouter, Body, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Dict, List
from app.services.layer_1.analysis import AnalysisService
from app.services.layer_1.transformer import DataTransformer
import csv
import io

main_router = APIRouter()
service = AnalysisService()
transformer = DataTransformer()

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
    This endpoint is for **batch analysis** (not for model training).
    """,
)
async def analyze_csv(
    task: str = Body(..., embed=True, example="DCF"),
    model_type: str = Body(..., embed=True, example="RandomForest"),
    file: UploadFile = File(...)
):
    """
    Analyze multiple cases from a CSV file. Each row will be transformed and analyzed.
    This does NOT train the model, it only runs predictions/analysis.
    """
    content = await file.read()
    decoded = content.decode("utf-8")
    # Use transformer to parse CSV to JSON
    if task.lower() == "consistency":
        rows = transformer.csv_to_json_consistency(io.StringIO(decoded))
    elif task.lower() in ["abnormal finding", "dcf"]:
        rows = transformer.csv_to_json_abnormal(io.StringIO(decoded))
    elif task.lower() == "wacc":
        rows = transformer.csv_to_json_wacc(io.StringIO(decoded))
    else:
        rows = transformer.csv_to_json_abnormal(io.StringIO(decoded))
    results = []
    for data in rows:
        req = {"task": task, "model_type": model_type, "data": data}
        result = await service.handle_request(req)
        results.append(result)
    return {"results": results}