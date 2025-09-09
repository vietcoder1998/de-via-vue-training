from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi import Body
from pydantic import BaseModel
from typing import Any, Dict
from app.services.analysis import AnalysisService

main_router = APIRouter()
service = AnalysisService()

class AnalyzeRequest(BaseModel):
    task: str
    model_type: str = "RandomForest"
    data: Dict[str, Any]

class AnalyzeResponse(BaseModel):
    result: Dict[str, Any]

@main_router.get("/", summary="Health check")
async def index():
    """Health check endpoint."""
    return JSONResponse({"message": "Hello FastAPI!"})

@main_router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Run analysis",
    description="Run analysis for a given task and model type."
)
async def analyze(request: AnalyzeRequest = Body(...)):
    """
    Analyze data using the specified task and model type.
    """
    result = await service.handle_request(request.dict())
    return {"result": result}
