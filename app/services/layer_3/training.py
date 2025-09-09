import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from datetime import datetime


class ModelTrainer:
    def __init__(self, data_dir="data", models_dir="models"):
        self.data_dir = data_dir
        self.models_dir = models_dir

        # Create directories if they don't exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)

        # Dictionary to track training history
        self.training_history = {}

    def list_csv_files(self):
        """List all CSV files in the data directory."""
        if not os.path.exists(self.data_dir):
            return []
        return [f for f in os.listdir(self.data_dir) if f.endswith(".csv")]

    def load_data(self, filename):
        """Load a CSV file as a pandas DataFrame."""
        filepath = os.path.join(self.data_dir, filename)
        return pd.read_csv(filepath)

    def save_model(self, model, model_name, metadata=None):
        """Save a trained model with optional metadata."""
        model_path = os.path.join(self.models_dir, f"{model_name}.joblib")

        # If metadata provided, store it with the model
        if metadata:
            save_data = {
                "model": model,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat(),
            }
            joblib.dump(save_data, model_path)
        else:
            joblib.dump(model, model_path)

        return model_path

    def load_model(self, model_name):
        """Load a saved model."""
        model_path = os.path.join(self.models_dir, f"{model_name}.joblib")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model {model_name} not found")

        return joblib.load(model_path)

    def list_available_models(self):
        """List all available saved models."""
        if not os.path.exists(self.models_dir):
            return []
        return [
            f.replace(".joblib", "")
            for f in os.listdir(self.models_dir)
            if f.endswith(".joblib")
        ]

    def train_random_forest(self, filename, target_column, hyperparams=None, save=True):
        """
        Train a RandomForestRegressor on the given CSV file.
        Returns the trained model and test score.
        """
        df = self.load_data(filename)
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in {filename}")

        X = df.drop(columns=[target_column])
        y = df[target_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Default hyperparameters if none provided
        if hyperparams is None:
            hyperparams = {
                "n_estimators": 100,
                "max_depth": None,
                "min_samples_split": 2,
                "random_state": 42,
            }

        model = RandomForestRegressor(**hyperparams)
        model.fit(X_train, y_train)

        # Evaluate on test data
        y_pred = model.predict(X_test)
        score = model.score(X_test, y_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Create training metadata
        metadata = {
            "algorithm": "RandomForest",
            "filename": filename,
            "target_column": target_column,
            "hyperparameters": hyperparams,
            "feature_columns": X.columns.tolist(),
            "metrics": {"r2_score": r2, "mse": mse, "test_score": score},
            "feature_importance": dict(zip(X.columns, model.feature_importances_)),
        }

        model_name = f"rf_{target_column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.training_history[model_name] = metadata

        if save:
            self.save_model(model, model_name, metadata)

        return model, metadata

    def train_neural_network(
        self, filename, target_column, hidden_layers=(100, 50), save=True
    ):
        """
        Train a Neural Network (MLPRegressor) on the given CSV file.
        Returns the trained model and test score.
        """
        df = self.load_data(filename)
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in {filename}")

        X = df.drop(columns=[target_column])
        y = df[target_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Standardize features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Create and train the neural network
        model = MLPRegressor(
            hidden_layer_sizes=hidden_layers,
            activation="relu",
            solver="adam",
            alpha=0.0001,
            batch_size="auto",
            learning_rate="adaptive",
            max_iter=1000,
            random_state=42,
        )

        model.fit(X_train_scaled, y_train)

        # Evaluate on test data
        y_pred = model.predict(X_test_scaled)
        score = model.score(X_test_scaled, y_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Create training metadata
        metadata = {
            "algorithm": "MLPRegressor",
            "filename": filename,
            "target_column": target_column,
            "hyperparameters": {
                "hidden_layers": hidden_layers,
                "activation": "relu",
                "solver": "adam",
            },
            "feature_columns": X.columns.tolist(),
            "metrics": {"r2_score": r2, "mse": mse, "test_score": score},
        }

        # Create a pipeline with the scaler and model
        pipeline = Pipeline([("scaler", scaler), ("mlp", model)])

        model_name = f"nn_{target_column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.training_history[model_name] = metadata

        if save:
            self.save_model(pipeline, model_name, metadata)

        return pipeline, metadata

    def train_anomaly_detection(self, filename, contamination=0.1, save=True):
        """
        Train an anomaly detection model (Isolation Forest) on the given CSV file.
        Returns the trained model and outliers.
        """
        df = self.load_data(filename)

        # Use all columns for anomaly detection
        X = df.select_dtypes(include=["number"])

        # Create and train the isolation forest model
        model = IsolationForest(
            n_estimators=100, contamination=contamination, random_state=42
        )

        model.fit(X)

        # Predict anomalies
        predictions = model.predict(X)
        scores = model.decision_function(X)

        # Identify outliers (where prediction == -1)
        outliers = df[predictions == -1]

        # Create training metadata
        metadata = {
            "algorithm": "IsolationForest",
            "filename": filename,
            "hyperparameters": {"contamination": contamination, "n_estimators": 100},
            "feature_columns": X.columns.tolist(),
            "metrics": {
                "num_outliers": len(outliers),
                "outlier_percentage": (len(outliers) / len(df)) * 100,
            },
        }

        model_name = f"anomaly_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.training_history[model_name] = metadata

        if save:
            self.save_model(model, model_name, metadata)

        return model, metadata, outliers

    def hyperparameter_tuning(self, filename, target_column, model_type="rf"):
        """
        Perform hyperparameter tuning for the selected model type.
        Returns the best model and parameters.

        model_type: 'rf' (RandomForest), 'nn' (Neural Network), 'ridge', or 'lasso'
        """
        df = self.load_data(filename)
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in {filename}")

        X = df.drop(columns=[target_column])
        y = df[target_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Create parameter grids based on model type
        if model_type == "rf":
            model = RandomForestRegressor(random_state=42)
            param_grid = {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
            }
        elif model_type == "nn":
            model = MLPRegressor(random_state=42, max_iter=1000)
            param_grid = {
                "hidden_layer_sizes": [(50,), (100,), (50, 50), (100, 50)],
                "activation": ["relu", "tanh"],
                "alpha": [0.0001, 0.001, 0.01],
            }
        elif model_type == "ridge":
            model = Ridge(random_state=42)
            param_grid = {"alpha": [0.01, 0.1, 1.0, 10.0, 100.0]}
        elif model_type == "lasso":
            model = Lasso(random_state=42)
            param_grid = {"alpha": [0.01, 0.1, 1.0, 10.0, 100.0]}
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        # Perform grid search
        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=5,
            scoring="neg_mean_squared_error",
            n_jobs=-1,
            verbose=1,
        )

        grid_search.fit(X_train, y_train)

        # Get best model
        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_

        # Evaluate on test data
        y_pred = best_model.predict(X_test)
        score = best_model.score(X_test, y_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Create metadata
        metadata = {
            "algorithm": str(type(best_model).__name__),
            "filename": filename,
            "target_column": target_column,
            "best_hyperparameters": best_params,
            "feature_columns": X.columns.tolist(),
            "metrics": {"r2_score": r2, "mse": mse, "test_score": score},
        }

        # Add feature importance if available
        if hasattr(best_model, "feature_importances_"):
            metadata["feature_importance"] = dict(
                zip(X.columns, best_model.feature_importances_)
            )

        model_name = f"{model_type}_tuned_{target_column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.training_history[model_name] = metadata

        # Save the best model
        self.save_model(best_model, model_name, metadata)

        return best_model, metadata

    def plot_feature_importance(self, model_data, top_n=10):
        """
        Plot feature importance for a trained model.

        model_data can be:
        - A tuple of (model, metadata) as returned by train_*
        - A model with feature_importances_ attribute
        - A model name string (will load from saved models)
        """
        plt.figure(figsize=(10, 6))

        # Extract model and metadata
        if isinstance(model_data, tuple) and len(model_data) >= 2:
            model, metadata = model_data[0], model_data[1]
            feature_importance = metadata.get("feature_importance")
            if feature_importance is None and hasattr(model, "feature_importances_"):
                feature_columns = metadata.get("feature_columns", [])
                feature_importance = dict(
                    zip(feature_columns, model.feature_importances_)
                )
        elif isinstance(model_data, str):
            # Load saved model
            loaded_data = self.load_model(model_data)
            if isinstance(loaded_data, dict) and "metadata" in loaded_data:
                feature_importance = loaded_data["metadata"].get("feature_importance")
                model = loaded_data["model"]
            else:
                model = loaded_data
                feature_importance = None

            if feature_importance is None and hasattr(model, "feature_importances_"):
                # Try to reconstruct feature importance without column names
                feature_importance = {
                    f"Feature {i}": imp
                    for i, imp in enumerate(model.feature_importances_)
                }
        else:
            model = model_data
            if not hasattr(model, "feature_importances_"):
                raise ValueError("Model does not have feature_importances_ attribute")
            feature_importance = {
                f"Feature {i}": imp for i, imp in enumerate(model.feature_importances_)
            }

        # Plot top N features
        if feature_importance:
            # Sort features by importance
            sorted_features = sorted(
                feature_importance.items(), key=lambda x: x[1], reverse=True
            )
            top_features = sorted_features[:top_n]

            # Plot
            features, importances = zip(*top_features)
            plt.barh(range(len(features)), importances, align="center")
            plt.yticks(range(len(features)), features)
            plt.xlabel("Importance")
            plt.ylabel("Feature")
            plt.title(f"Top {len(features)} Feature Importances")
            plt.tight_layout()

            return plt.gcf()
        else:
            raise ValueError("Could not extract feature importance from model")

    def export_training_history(self):
        """Export training history to a CSV file."""
        if not self.training_history:
            return None

        # Flatten the nested dictionary structure
        records = []
        for model_name, metadata in self.training_history.items():
            record = {
                "model_name": model_name,
                "algorithm": metadata.get("algorithm", ""),
                "filename": metadata.get("filename", ""),
                "target_column": metadata.get("target_column", ""),
            }

            # Add metrics
            metrics = metadata.get("metrics", {})
            for metric_name, metric_value in metrics.items():
                record[f"metric_{metric_name}"] = metric_value

            records.append(record)

        # Create DataFrame and save
        history_df = pd.DataFrame(records)
        history_path = os.path.join(self.models_dir, "training_history.csv")
        history_df.to_csv(history_path, index=False)

        return history_path


# Example usage:
# trainer = ModelTrainer(data_dir="example/training/data", models_dir="example/training/models")
# rf_model, rf_metadata = trainer.train_random_forest("example.csv", "target_column")
# nn_model, nn_metadata = trainer.train_neural_network("example.csv", "target_column")
# anomaly_model, anomaly_metadata, outliers = trainer.train_anomaly_detection("example.csv")
# trainer.plot_feature_importance(rf_model, rf_metadata)
