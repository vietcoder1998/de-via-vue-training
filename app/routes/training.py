from fastapi import APIRouter, Body, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.services.layer_3.ml import MLModels
import os
import shutil

training_router = APIRouter()
ml_service = MLModels()

class TrainingRequest(BaseModel):
    model_type: str = Field(..., example="RandomForest")
    csv_filename: str = Field(..., example="your_data.csv")
    target_column: str = Field(..., example="target")

class TrainingResponse(BaseModel):
    message: str = Field(..., example="RandomForest trained successfully.")

@training_router.post(
    "/train",
    response_model=TrainingResponse,
    summary="Train ML model",
    description="""
    Train a machine learning model with a CSV file from the data directory.
    - model_type: RandomForest, NeuralNetwork, XGBoost
    - csv_filename: Tên file CSV trong thư mục data/
    - target_column: Tên cột mục tiêu
    """
)
async def train_model(request: TrainingRequest = Body(...)):
    result = ml_service.train(request.model_type, request.csv_filename, request.target_column)
    if "error" in result:
        return JSONResponse(result, status_code=400)
    return {"message": result.get("message", "Training completed.")}

@training_router.post(
    "/train-with-file",
    response_model=TrainingResponse,
    summary="Train ML model with uploaded file",
    description="""
    Train a machine learning model by uploading a CSV file directly.
    - model_type: RandomForest, NeuralNetwork, XGBoost
    - target_column: Tên cột mục tiêu
    - file: CSV file upload
    """
)
async def train_with_file(
    model_type: str = Body(..., embed=True, example="RandomForest"),
    target_column: str = Body(..., embed=True, example="target"),
    file: UploadFile = File(...)
):
    save_path = os.path.join("data", file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = ml_service.train(model_type, file.filename, target_column)
    if "error" in result:
        return JSONResponse(result, status_code=400)
    return {"message": result.get("message", "Training completed.")}