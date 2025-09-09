# de-intern-ai

## Overview

**de-intern-ai** is a modular FastAPI-based backend for financial and AI analysis, supporting:

- Financial analysis (DCF, Comparable, WACC, etc.)
- ML model training and prediction (RandomForest, NeuralNetwork, XGBoost)
- Interactive API docs and a simple web UI for testing

---

## Project Structure

2. Run the API server (recommended)
   Or, for Flask-style dev mode (not recommended for FastAPI):
3. Access API Docs & UI
   Swagger UI: http://localhost:5001/docs
   ReDoc: http://localhost:5001/redoc
   Demo UI: http://localhost:5001/analyze-ui
   Example: Analyze API
   POST /analyze

Sample request:

Sample response:

Example: Train Model API
POST /train

Sample request:

Or upload a new CSV file via /train-with-file in Swagger UI.

Development Notes
Place your training data in app/data/.
All routers are modular: see app/routes/api.py, app/routes/ui.py, app/routes/training.py.
Extend business logic in app/services/layer_2/ and ML logic in app/services/layer_3/.
License
MIT License

Authors
Your Name Here
update to file

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
uvicorn run:run --host 127.0.0.1 --port 5001

3. Access API Docs & UI
Swagger UI: http://localhost:5001/docs
ReDoc: http://localhost:5001/redoc
Demo UI: http://localhost:5001/analyze-ui
Example: Analyze API

Example: Analyze API
POST /analyze

## Sample request:
```

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

```

{
"result": {
"enterprise_value": 1500.0,
"equity_value": 1450.0,
"equity_value_per_share": 145.0
}
}

```

Example: Train Model API
POST /train

Sample request:
{
  "model_type": "RandomForest",
  "csv_filename": "dcf.csv",
  "target_column": "target"
}
```
