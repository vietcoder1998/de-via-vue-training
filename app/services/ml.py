class MLModels:
    def predict(self, model_type, data):
        if model_type == "RandomForest":
            return RandomForest().predict(data)
        elif model_type == "NeuralNetwork":
            return NeuralNetwork().predict(data)
        elif model_type == "XGBoost":
            return XGBoost().predict(data)
        else:
            return {"error": "Unknown model"}

class RandomForest:
    def predict(self, data):
        return {"rf_result": 1}

class NeuralNetwork:
    def predict(self, data):
        return {"nn_result": 2}

class XGBoost:
    def predict(self, data):
        return {"xgb_result": 3}