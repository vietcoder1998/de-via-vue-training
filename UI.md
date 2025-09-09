# UI Guide - de-intern-ai Platform

<!-- filepath: d:\COMPANY\Freelancer\de-via-vue-training\UI.md -->

## Overview

This document provides a step-by-step guide for using the de-intern-ai platform user interface. The platform offers a web-based interface for financial analysis, machine learning model training, and advanced analytics.

## Accessing the UI

1. Ensure the server is running using `uvicorn run:run --host 127.0.0.1 --port 5001`
2. Open your browser and navigate to http://localhost:5001/analyze-ui

## UI Sections

The UI is organized into four main tabs:

1. **Analysis** - For single financial analysis requests
2. **Batch Analysis** - For processing multiple scenarios from a CSV file
3. **Model Training** - For training new ML models from data
4. **Advanced ML** - For specialized ML features like anomaly detection

---

## 1. Analysis Tab

This tab allows you to perform individual financial analyses using various models.

### How to use:

1. **Select a task** from the dropdown menu:

   - DCF Analysis
   - PE Analysis
   - Abnormal Finding
   - Model Consistency
   - Risk Mitigation

2. **Select a model type**:

   - RandomForest
   - NeuralNetwork
   - XGBoost

3. **Input data**:

   - Use the text area to provide input data in JSON format
   - For convenience, click the sample buttons to load pre-formatted examples

4. **Run the analysis**:

   - Click the "Analyze" button
   - Results will appear in the Result section below

### Example:

For a DCF Analysis, your input might look like:

```json
{
  "free_cash_flow": [100, 110, 121, 133.1, 146.41],
  "terminal_growth_rate": 0.02,
  "discount_rate": 0.1,
  "shares_outstanding": 10,
  "net_debt": 50,
  "historical_cash_flows": [80, 90, 100, 110, 121]
}
```

---

## 2. Batch Analysis Tab

This tab processes multiple analysis scenarios from a CSV file.

### How to use:

1. **Select a task and model type** as in the Analysis tab
2. **Upload a CSV file**:

   - The CSV should contain columns matching the expected input parameters
   - Each row represents a separate analysis scenario

3. **Run the batch analysis**:

   - Click the "Batch Analyze" button
   - Results for all scenarios will appear in the Batch Analysis Result section

### CSV Format Example (for DCF):

```
free_cash_flow,terminal_growth_rate,discount_rate,shares_outstanding,net_debt
"[100,110,121,133.1,146.41]",0.02,0.1,10,50
"[200,210,220,231,242.55]",0.03,0.12,20,100
```

---

## 3. Model Training Tab

This tab allows you to train new machine learning models using your own data.

### How to use:

1. **Select a model type**:

   - RandomForest
   - NeuralNetwork

2. **Specify the target column** in your CSV file
3. **Upload a training CSV file**:

   - The file should contain feature columns and a target column
   - Data should be preprocessed and ready for training

4. **Train the model**:

   - Click the "Upload & Train" button
   - Training results, including performance metrics, will appear below

5. **View available models**:

   - Click "Refresh Model List" to see all trained models
   - Models are saved for future use

### Training Data Format Example:

```
feature1,feature2,feature3,target
10.5,20.3,15.2,100.5
11.2,19.8,14.9,98.2
```

---

## 4. Advanced ML Tab

This tab provides specialized machine learning capabilities.

### Anomaly Detection:

1. **Upload a CSV file** containing data to analyze for anomalies
2. **Set the contamination rate** (0.01-0.5):
   - Higher values detect more anomalies
   - Lower values are more conservative
3. **Click "Train Anomaly Model"**
4. Review results showing detected anomalies and their scores

### Hyperparameter Tuning:

1. **Select a model type** to optimize:
   - RandomForest (rf)
   - NeuralNetwork (nn)
   - Ridge Regression (ridge)
   - Lasso Regression (lasso)
2. **Upload a CSV file** with training data
3. **Specify the target column**
4. **Click "Start Tuning"**
5. Review results showing the best parameters found

### Feature Importance:

1. **Select a trained model** from the dropdown
2. **Set the number of top features** to display
3. **Choose whether to include visualization**
4. **Click "Get Feature Importance"**
5. Review the importance scores and visualization of key features

---

## Tips for Best Results

1. **Data Preparation**:

   - Ensure your data is clean and properly formatted
   - For financial analysis, provide all relevant financial metrics
   - For ML training, normalize/standardize features when possible

2. **Model Selection**:

   - RandomForest works well for most financial predictions
   - NeuralNetwork may perform better with large, complex datasets
   - Use anomaly detection when looking for unusual patterns

3. **Interpretation**:

   - DCF and PE Analysis provide direct valuation estimates
   - Feature importance helps understand which factors drive predictions
   - Anomaly scores indicate how unusual a data point is

4. **Troubleshooting**:

   - If analysis fails, check your JSON format
   - For CSV uploads, ensure columns match expected parameters
   - For slow responses, consider reducing dataset size

---

## API Integration

All UI functionality is also available via direct API calls. See the API documentation at:

- http://localhost:5001/docs (Swagger UI)
- http://localhost:5001/redoc (ReDoc)
