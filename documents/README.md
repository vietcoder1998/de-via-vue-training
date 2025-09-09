# de-intern-ai

## Description
This project provides a FastAPI-based backend for AI analysis tasks, including abnormal finding, model consistency, and DCF valuation, with support for multiple ML models.

## Requirements
- Python 3.9+
- FastAPI
- Uvicorn

## Installation

```bash
pip install -r requirements.txt
```
## run app
uvicorn run:app --reload --host 0.0.0.0 --port 5001

## Update dependencies and sync Uvicorn

To update your dependencies and ensure Uvicorn is installed and up-to-date, run:

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
pip install --upgrade uvicorn
```