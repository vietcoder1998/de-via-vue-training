import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class ModelTrainer:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def list_csv_files(self):
        """List all CSV files in the data directory."""
        return [f for f in os.listdir(self.data_dir) if f.endswith(".csv")]

    def load_data(self, filename):
        """Load a CSV file as a pandas DataFrame."""
        filepath = os.path.join(self.data_dir, filename)
        return pd.read_csv(filepath)

    def train_random_forest(self, filename, target_column):
        """
        Train a RandomForestRegressor on the given CSV file.
        Returns the trained model and test score.
        """
        df = self.load_data(filename)
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in {filename}")

        X = df.drop(columns=[target_column])
        y = df[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        return model, score

# Example usage:
# trainer = ModelTrainer()
# print(trainer.list_csv_files())
# model, score = trainer.train_random_forest("your_data.csv", "target_column")
# print("Test score:", score)