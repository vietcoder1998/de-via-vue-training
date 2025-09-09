class VIA:
    def run_abnormal(self, data):
        """
        Xử lý abnormal: Tính điểm bất thường dựa trên trung bình và độ lệch chuẩn.
        """
        values = [v for v in data.values() if isinstance(v, (int, float))]
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std = variance ** 0.5
        # Điểm bất thường: max khoảng cách so với trung bình, chia cho std (nếu std > 0)
        abnormal_score = max(abs(x - mean) for x in values) / std if std > 0 else 0.0
        return round(abnormal_score, 4)

    def run_consistency(self, data):
        """
        Xử lý consistency: Tính chỉ số consistency dựa trên tỉ lệ giá trị giống nhau.
        """
        values = [v for v in data.values() if isinstance(v, (int, float, str))]
        if not values:
            return 1.0
        most_common = max(set(values), key=values.count)
        consistency_index = values.count(most_common) / len(values)
        return round(consistency_index, 4)

    def run_dcf(self, data):
        """
        Xử lý DCF: Tính giá trị hiện tại ròng (Discounted Cash Flow).
        Giả sử data có các trường: 'cash_flows' (list), 'discount_rate' (float)
        """
        cash_flows = data.get("cash_flows", [])
        discount_rate = data.get("discount_rate", 0.1)
        if not isinstance(cash_flows, list) or not cash_flows:
            return 0.0
        dcf = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows, start=1))
        return round(dcf, 2)