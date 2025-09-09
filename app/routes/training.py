from fastapi import APIRouter, Body, UploadFile, File, Query, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.services.layer_3.training import ModelTrainer
import os
import shutil
from datetime import datetime
import io
import base64

training_router = APIRouter()
trainer = ModelTrainer(data_dir="data", models_dir="models")


# Request and response models
class TrainingRequest(BaseModel):
    model_type: str = Field(..., example="RandomForest")
    csv_filename: str = Field(..., example="your_data.csv")
    target_column: str = Field(..., example="target")


class HyperparameterTuningRequest(BaseModel):
    model_type: str = Field(..., example="rf")
    csv_filename: str = Field(..., example="your_data.csv")
    target_column: str = Field(..., example="target")


class AnomalyDetectionRequest(BaseModel):
    csv_filename: str = Field(..., example="your_data.csv")
    contamination: float = Field(0.1, example=0.1)


class TrainingResponse(BaseModel):
    message: str = Field(..., example="RandomForest trained successfully.")
    model_name: str = Field(..., example="rf_target_20251009_120000")
    metrics: Dict[str, Any] = Field(..., example={"r2_score": 0.95, "mse": 0.05})


class ModelListResponse(BaseModel):
    models: List[str] = Field(..., example=["rf_model_20251009", "nn_model_20251009"])


class CSVListResponse(BaseModel):
    files: List[str] = Field(..., example=["data1.csv", "data2.csv"])


class FeatureImportanceResponse(BaseModel):
    model_name: str
    feature_importance: Dict[str, float]
    image_base64: Optional[str] = None


# Routes
@training_router.get(
    "/models",
    response_model=ModelListResponse,
    summary="List available models",
    description="Get a list of all available trained models.",
)
async def list_models():
    models = trainer.list_available_models()
    return {"models": models}


@training_router.get(
    "/data",
    response_model=CSVListResponse,
    summary="List available CSV files",
    description="Get a list of all available CSV files in the data directory.",
)
async def list_csv_files():
    files = trainer.list_csv_files()
    return {"files": files}


@training_router.post(
    "/train",
    response_model=TrainingResponse,
    summary="Train ML model",
    description="""
    Train a machine learning model with a CSV file from the data directory.
    - model_type: RandomForest, NeuralNetwork
    - csv_filename: Tên file CSV trong thư mục data/
    - target_column: Tên cột mục tiêu
    """,
)
async def train_model(request: TrainingRequest = Body(...)):
    try:
        if request.model_type.lower() in ["randomforest", "rf"]:
            model, metadata = trainer.train_random_forest(
                request.csv_filename, request.target_column
            )
            model_name = list(trainer.training_history.keys())[-1]
        elif request.model_type.lower() in ["neuralnetwork", "nn", "mlp"]:
            model, metadata = trainer.train_neural_network(
                request.csv_filename, request.target_column
            )
            model_name = list(trainer.training_history.keys())[-1]
        else:
            return JSONResponse(
                {"error": f"Unsupported model type: {request.model_type}"},
                status_code=400,
            )

        return {
            "message": f"{request.model_type} trained successfully on {request.csv_filename}.",
            "model_name": model_name,
            "metrics": metadata["metrics"],
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@training_router.post(
    "/train-with-file",
    response_model=TrainingResponse,
    summary="Train ML model with uploaded file",
    description="""
    Train a machine learning model by uploading a CSV file directly.
    - model_type: RandomForest, NeuralNetwork
    - target_column: Tên cột mục tiêu
    - file: CSV file upload
    """,
)
async def train_with_file(
    model_type: str = Body(..., embed=True, example="RandomForest"),
    target_column: str = Body(..., embed=True, example="target"),
    file: UploadFile = File(...),
):
    try:
        # Create a unique filename to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        save_path = os.path.join("data", filename)

        # Save uploaded file
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Train model
        if model_type.lower() in ["randomforest", "rf"]:
            model, metadata = trainer.train_random_forest(filename, target_column)
            model_name = list(trainer.training_history.keys())[-1]
        elif model_type.lower() in ["neuralnetwork", "nn", "mlp"]:
            model, metadata = trainer.train_neural_network(filename, target_column)
            model_name = list(trainer.training_history.keys())[-1]
        else:
            return JSONResponse(
                {"error": f"Unsupported model type: {model_type}"}, status_code=400
            )

        return {
            "message": f"{model_type} trained successfully with uploaded file.",
            "model_name": model_name,
            "metrics": metadata["metrics"],
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@training_router.post(
    "/anomaly-detection",
    summary="Anomaly detection",
    description="""
    Train an anomaly detection model using Isolation Forest.
    Returns anomaly detection results and saves the model.
    """,
)
async def train_anomaly_detection(request: AnomalyDetectionRequest = Body(...)):
    try:
        model, metadata, outliers = trainer.train_anomaly_detection(
            request.csv_filename, request.contamination
        )
        model_name = list(trainer.training_history.keys())[-1]

        return {
            "message": "Anomaly detection model trained successfully.",
            "model_name": model_name,
            "metrics": metadata["metrics"],
            "num_outliers": len(outliers),
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@training_router.post(
    "/hyperparameter-tuning",
    summary="Hyperparameter tuning",
    description="""
    Perform hyperparameter tuning for the selected model type.
    - model_type: 'rf' (RandomForest), 'nn' (Neural Network), 'ridge', or 'lasso'
    """,
)
async def tune_hyperparameters(request: HyperparameterTuningRequest = Body(...)):
    try:
        best_model, metadata = trainer.hyperparameter_tuning(
            request.csv_filename, request.target_column, request.model_type
        )
        model_name = list(trainer.training_history.keys())[-1]

        return {
            "message": f"Hyperparameter tuning completed for {request.model_type}.",
            "model_name": model_name,
            "best_params": metadata["best_hyperparameters"],
            "metrics": metadata["metrics"],
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@training_router.get(
    "/feature-importance/{model_name}",
    response_model=FeatureImportanceResponse,
    summary="Get feature importance",
    description="Get feature importance for a trained model and optional visualization.",
)
async def get_feature_importance(
    model_name: str,
    top_n: int = Query(10, description="Number of top features to show"),
    include_plot: bool = Query(False, description="Include plot as base64 image"),
):
    try:
        # Load model
        loaded_data = trainer.load_model(model_name)

        # Extract feature importance
        if isinstance(loaded_data, dict) and "metadata" in loaded_data:
            feature_importance = loaded_data["metadata"].get("feature_importance", {})
        else:
            return JSONResponse(
                {"error": "No feature importance data available"}, status_code=404
            )

        # Sort and limit to top N
        sorted_features = dict(
            sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:top_n]
        )

        result = {"model_name": model_name, "feature_importance": sorted_features}

        # Generate plot if requested
        if include_plot:
            try:
                fig = trainer.plot_feature_importance(model_name, top_n)
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                img_base64 = base64.b64encode(buf.read()).decode("ascii")
                result["image_base64"] = img_base64
            except Exception as plot_error:
                # Just log the error but continue without the plot
                print(f"Error generating plot: {str(plot_error)}")

        return result
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@training_router.get(
    "/history",
    summary="Get training history",
    description="Export training history to a CSV file and return the path.",
)
async def export_history():
    try:
        history_path = trainer.export_training_history()
        if history_path and os.path.exists(history_path):
            return FileResponse(
                history_path, filename="training_history.csv", media_type="text/csv"
            )
        else:
            return JSONResponse(
                {"error": "No training history available"}, status_code=404
            )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@training_router.get(
    "/model-details/{model_name}",
    summary="Get model details",
    description="Get detailed information about a trained model.",
)
async def get_model_details(model_name: str):
    try:
        # Load model
        loaded_data = trainer.load_model(model_name)

        # Extract metadata
        if isinstance(loaded_data, dict) and "metadata" in loaded_data:
            metadata = loaded_data["metadata"]
            timestamp = loaded_data.get("timestamp", "Unknown")

            return {
                "model_name": model_name,
                "algorithm": metadata.get("algorithm", "Unknown"),
                "timestamp": timestamp,
                "metrics": metadata.get("metrics", {}),
                "hyperparameters": metadata.get(
                    "hyperparameters", metadata.get("best_hyperparameters", {})
                ),
                "feature_columns": metadata.get("feature_columns", []),
                "training_data": metadata.get("filename", "Unknown"),
                "target_column": metadata.get("target_column", "Unknown"),
            }
        else:
            return JSONResponse(
                {"error": "No metadata available for this model"}, status_code=404
            )
    except FileNotFoundError:
        return JSONResponse({"error": f"Model {model_name} not found"}, status_code=404)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
