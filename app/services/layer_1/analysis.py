from typing import Any, Dict, List, Optional
import pandas as pd
import os
from app.services.layer_1.transformer import DataTransformer
from app.services.layer_2.via import VIA
from app.services.layer_2.vua import VUA
from app.services.layer_3.ml import MLModels
from app.services.layer_3.training import ModelTrainer


class AnalysisService:
    def __init__(self):
        self.transformer = DataTransformer()
        self.via = VIA()
        self.vua = VUA()
        self.ml = MLModels()
        self.trainer = ModelTrainer(data_dir="data", models_dir="models")

    async def handle_request(self, request_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle analysis requests with enhanced AI-driven capabilities
        """
        # Transform and normalize data
        data = self.transformer.transform_xxx(request_json)
        task = request_json.get("task")
        model_type = request_json.get("model_type", "RandomForest")

        # Task-specific processing using enhanced VIA methods
        if task == "Abnormal Finding":
            # Use the AI-driven abnormal finding method if sufficient data is available
            if self._has_sufficient_data(
                data, ["historical_prices", "trading_volumes"]
            ):
                result = self.via.run_ai_driven_abnormal_finding(data)
            else:
                # Fall back to simpler method if data is insufficient
                score = self.via.run_abnormal(data)
                result = {
                    "abnormal_score": score,
                    "interpretation": self.vua.interpret_abnormal(score),
                }

        elif task == "Model Consistency":
            # Use AI-driven consistency analysis if model predictions are available
            if self._has_sufficient_data(data, ["model_predictions"]):
                result = self.via.run_ai_driven_model_consistency(data)
            else:
                # Fall back to simple consistency check
                index = self.via.run_consistency(data)
                result = {
                    "consistency_index": index,
                    "interpretation": self.vua.interpret_consistency(index),
                }

        elif task == "DCF":
            # Use AI-driven DCF if we have sufficient financial data
            if self._has_sufficient_data(
                data, ["historical_cash_flows", "financial_statements"]
            ):
                result = self.via.run_ai_driven_dcf(data)
            else:
                # Fall back to traditional DCF
                result = self.via.run_dcf(data)
                result = {**result, "interpretation": self.vua.interpret_dcf(result)}

        elif task == "PE Analysis":
            # Use neural PE analysis if growth and financial health data are available
            if self._has_sufficient_data(data, ["growth_metrics", "financial_health"]):
                result = self.via.run_neural_pe_analysis(data)
            else:
                # Fall back to standard PE analysis
                result = self.via.run_pe_analysis(data)

        elif task == "Risk Mitigation":
            # Use AI-driven risk analysis with Z-score and Monte Carlo if data available
            if self._has_sufficient_data(
                data, ["financial_statements", "stock_price_history"]
            ):
                result = self.via.run_risk_mitigation(data)
            else:
                return {"error": "Insufficient data for Risk Mitigation analysis"}

        else:
            return {"error": f"Unknown task: {task}"}

        # Augment result with AI prediction if appropriate for this task
        if self._should_apply_ai_prediction(task):
            prediction = self.vua.select_and_predict(model_type, data, self.ml)
            output = self.vua.merge_output(result, prediction)
        else:
            output = result

        return output

    def _has_sufficient_data(
        self, data: Dict[str, Any], required_fields: List[str]
    ) -> bool:
        """
        Check if the data contains sufficient information for advanced analysis
        """
        return all(field in data and data[field] for field in required_fields)

    def _should_apply_ai_prediction(self, task: str) -> bool:
        """
        Determine if AI prediction should be applied to this task
        """
        # Tasks that benefit from additional AI prediction
        ai_prediction_tasks = ["DCF", "PE Analysis"]
        return task in ai_prediction_tasks

    async def handle_batch_request(self, csv_file_path: str) -> List[Dict[str, Any]]:
        """
        Process multiple analysis requests from a CSV file
        """
        results = []
        try:
            # Read CSV file
            df = pd.read_csv(csv_file_path)

            # Process each row
            for _, row in df.iterrows():
                # Convert row to dict
                row_dict = row.to_dict()

                # Extract task from row or use default
                task = row_dict.get("task", "DCF")

                # Process request
                result = await self.handle_request(row_dict)
                results.append(result)

            return results
        except Exception as e:
            return [{"error": f"Error processing batch request: {str(e)}"}]

    async def train_model(
        self, model_type: str, data_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Train a model using the ModelTrainer
        """
        try:
            if model_type.lower() == "dcf":
                result = self.trainer.train_random_forest(
                    data_path or "default_dcf.csv", "target_value"
                )
            elif model_type.lower() == "pe":
                result = self.trainer.train_neural_network(
                    data_path or "default_pe.csv", "target_value"
                )
            elif model_type.lower() == "anomaly":
                result = self.trainer.train_anomaly_detection(
                    data_path or "default_anomaly.csv"
                )
            else:
                return {"error": f"Unsupported model type: {model_type}"}

            return {"success": True, "model": model_type, "result": result}
        except Exception as e:
            return {"error": f"Error training model: {str(e)}"}
