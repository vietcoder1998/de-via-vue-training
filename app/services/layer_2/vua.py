class VUA:
    def interpret_abnormal(self, score):
        # Diễn giải điểm bất thường
        if score > 2:
            message = "Rất bất thường"
        elif score > 1:
            message = "Có dấu hiệu bất thường"
        else:
            message = "Bình thường"
        return {"abnormal_interpretation": score, "abnormal_message": message}

    def interpret_consistency(self, index):
        # Diễn giải chỉ số consistency
        if index > 0.9:
            message = "Rất nhất quán"
        elif index > 0.7:
            message = "Khá nhất quán"
        else:
            message = "Không nhất quán"
        return {"consistency_interpretation": index, "consistency_message": message}

    def interpret_dcf(self, result):
        # Diễn giải kết quả DCF
        if result > 1000:
            message = "Giá trị doanh nghiệp cao"
        elif result > 0:
            message = "Giá trị doanh nghiệp dương"
        else:
            message = "Giá trị doanh nghiệp âm"
        return {"dcf_interpretation": result, "dcf_message": message}

    def select_and_predict(self, model_type, data, ml):
        # Chọn và dự đoán với mô hình AI
        return ml.predict(model_type, data)

    def merge_output(self, interpretation, prediction):
        # Gộp kết quả diễn giải và dự đoán AI
        return {**interpretation, "ml_prediction": prediction}