from typing import Any, Dict
from app.services.layer_1.transformer import DataTransformer
from app.services.layer_2.via import VIA
from app.services.layer_2.vua import VUA
from app.services.layer_3.ml import MLModels


class AnalysisService:
    def __init__(self):
        self.transformer = DataTransformer()
        self.via = VIA()
        self.vua = VUA()
        self.ml = MLModels()

    async def handle_request(self, request_json: Dict[str, Any]) -> Dict[str, Any]:
        # Chuẩn hoá dữ liệu
        data = self.transformer.transform_xxx(request_json)
        task = request_json.get("task")

        if task == "Abnormal Finding":
            score = self.via.run_abnormal(data)
            interpretation = self.vua.interpret_abnormal(score)
        elif task == "Model Consistency":
            index = self.via.run_consistency(data)
            interpretation = self.vua.interpret_consistency(index)
        elif task == "DCF":
            result = self.via.run_dcf(data)
            interpretation = self.vua.interpret_dcf(result)
        else:
            return {"error": "Unknown task"}

        # Chọn model AI và dự đoán
        model_type = request_json.get("model_type", "RandomForest")
        prediction = self.vua.select_and_predict(model_type, data, self.ml)

        # Diễn giải và merge kết quả
        output = self.vua.merge_output(interpretation, prediction)
        return output
