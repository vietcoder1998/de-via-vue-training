# de-intern-ai

## Overview

**de-intern-ai** is a modular FastAPI-based backend for financial and AI analysis, supporting:

- Financial analysis (DCF, Comparable, WACC, etc.)
- ML model training and prediction (RandomForest, NeuralNetwork, XGBoost)
- Advanced anomaly detection using Isolation Forest
- Hyperparameter tuning for optimal model performance
- Interactive API docs and a simple web UI for testing

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API server

```bash
uvicorn run:run --host 127.0.0.1 --port 5001
```

Or, for development mode with auto-reload:

```bash
uvicorn run:run --host 127.0.0.1 --port 5001 --reload
```

### 3. Access API Docs & UI

- **Swagger UI**: http://localhost:5001/docs
- **ReDoc**: http://localhost:5001/redoc
- **Demo UI**: http://localhost:5001/analyze-ui

---

## Key APIs

### Financial Analysis

#### Example: Analyze API

**POST /analyze**

Sample request:

```json
{
  "task": "DCF",
  "model_type": "RandomForest",
  "data": {
    "free_cash_flow": [100, 110, 121, 133.1, 146.41],
    "terminal_growth_rate": 0.02,
    "discount_rate": 0.1,
    "shares_outstanding": 10,
    "net_debt": 50
  }
}
```

Sample response:

```json
{
  "result": {
    "enterprise_value": 1500.0,
    "equity_value": 1450.0,
    "equity_value_per_share": 145.0
  }
}
```

#### Batch Analysis

**POST /analyze-csv**

Upload a CSV file for batch analysis of multiple scenarios.

### Model Training

#### Example: Train Model API

**POST /train**

Sample request:

```json
{
  "model_type": "RandomForest",
  "csv_filename": "dcf.csv",
  "target_column": "target"
}
```

#### Direct File Upload Training

**POST /train-with-file**

Upload a CSV file directly to train a model without saving it to the data directory first.

#### Advanced ML Features

- **POST /anomaly-detection**: Train anomaly detection models using Isolation Forest
- **POST /hyperparameter-tuning**: Optimize model parameters for best performance
- **GET /feature-importance/{model_name}**: Analyze and visualize feature importance
- **GET /model-details/{model_name}**: Get comprehensive information about trained models
- **GET /history**: Export complete training history as CSV

---

## Project Structure

```
de-intern-ai/
├── app/
│   ├── routes/
│   │   ├── api.py         # Main analysis endpoints
│   │   ├── training.py    # ML training endpoints
│   │   └── ui.py          # Simple web UI endpoints
│   │
│   ├── services/
│   │   ├── layer_1/       # Core services
│   │   ├── layer_2/       # Business logic (VIA, DCF, etc.)
│   │   └── layer_3/       # ML training and modeling
│   │
│   ├── models/            # Saved trained models
│   └── data/              # Training data directory
│
├── example/
│   └── 200cases/          # Example datasets
│
├── run.py                 # Application entry point
└── requirements.txt       # Project dependencies
```

---

## Development Notes

- Place your training data in `app/data/`.
- All routers are modular: see `app/routes/api.py`, `app/routes/ui.py`, `app/routes/training.py`.
- Extend business logic in `app/services/layer_2/` and ML logic in `app/services/layer_3/`.
- The system supports:
  - Financial modeling (DCF, WACC, Comparables)
  - Risk assessment and anomaly detection
  - ML-driven prediction and analysis
  - Feature importance analysis

---

## API Documentation

Full API documentation is available via Swagger UI at http://localhost:5001/docs when the server is running. This includes:

- Request and response schemas
- Example payloads
- Try-it-out functionality for all endpoints

---

## License

MIT License

---

## Authors

Your Name Here
