class VUA:
    def interpret_abnormal(self, score):
        return {"abnormal_interpretation": score}

    def interpret_consistency(self, index):
        return {"consistency_interpretation": index}

    def interpret_dcf(self, result):
        return {"dcf_interpretation": result}

    def select_and_predict(self, model_type, data, ml):
        return ml.predict(model_type, data)

    def merge_output(self, interpretation, prediction):
        return {**interpretation, "ml_prediction": prediction}