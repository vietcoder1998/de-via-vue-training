import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor

class MLModels:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.models = {
            "randomforest": RandomForest(),
            "neuralnetwork": NeuralNetwork(),
            "xgboost": XGBoost()
        }

    def predict(self, model_type, data):
        model_type = model_type.lower()
        model = self.models.get(model_type)
        if model:
            return model.predict(data)
        else:
            return {"error": f"Unknown model: {model_type}"}

    def train(self, model_type, csv_filename, target_column):
        model_type = model_type.lower()
        model = self.models.get(model_type)
        if model:
            return model.train(os.path.join(self.data_dir, csv_filename), target_column)
        else:
            return {"error": f"Unknown model: {model_type}"}

class RandomForest:
    def __init__(self):
        self.model = None

    def train(self, filepath, target_column):
        df = pd.read_csv(filepath)
        if target_column not in df.columns:
            return {"error": f"Target column '{target_column}' not found in {filepath}"}
        X = df.drop(columns=[target_column])
        y = df[target_column]
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        return {"message": "RandomForest trained successfully."}

    def predict(self, data):
        if self.model:
            # Assume data is a dict of features
            import numpy as np
            X = pd.DataFrame([data])
            pred = self.model.predict(X)[0]
            return {"rf_result": float(pred)}
        else:
            # Dummy logic if not trained
            values = [v for v in data.values() if isinstance(v, (int, float))]
            result = sum(values)
            return {"rf_result": result}

class NeuralNetwork:
    def __init__(self):
        self.model = None

    def train(self, filepath, target_column):
        df = pd.read_csv(filepath)
        if target_column not in df.columns:
            return {"error": f"Target column '{target_column}' not found in {filepath}"}
        X = df.drop(columns=[target_column])
        y = df[target_column]
        self.model = MLPRegressor(hidden_layer_sizes=(32, 16), max_iter=500, random_state=42)
        self.model.fit(X, y)
        return {"message": "NeuralNetwork trained successfully."}

    def predict(self, data):
        if self.model:
            X = pd.DataFrame([data])
            pred = self.model.predict(X)[0]
            return {"nn_result": float(pred)}
        else:
            result = len(data)
            return {"nn_result": result}

class XGBoost:
    def __init__(self):
        self.model = None

    def train(self, filepath, target_column):
        df = pd.read_csv(filepath)
        if target_column not in df.columns:
            return {"error": f"Target column '{target_column}' not found in {filepath}"}
        X = df.drop(columns=[target_column])
        y = df[target_column]
        self.model = XGBRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        return {"message": "XGBoost trained successfully."}

    def predict(self, data):
        if self.model:
            X = pd.DataFrame([data])
            pred = self.model.predict(X)[0]
            return {"xgb_result": float(pred)}
        else:
            values = [v for v in data.values() if isinstance(v, (int, float))]
            product = 1
            for v in values:
                product *= v
            if not values:
                product = 0
            return {"xgb_result": product}