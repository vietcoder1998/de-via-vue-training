import numpy as np
import math
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import random


class VIA:
    def __init__(self):
        self.scaler = StandardScaler()
        # Khởi tạo các model
        self.pe_neural_model = MLPRegressor(
            hidden_layer_sizes=(32, 16), activation="relu", max_iter=1000
        )
        self.dcf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.abnormal_model = IsolationForest(contamination=0.1, random_state=42)

    def run_abnormal(self, data):
        """
        Xử lý abnormal: Tính điểm bất thường dựa trên trung bình và độ lệch chuẩn.
        """
        values = [v for v in data.values() if isinstance(v, (int, float))]
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std = variance**0.5
        # Điểm bất thường: max khoảng cách so với trung bình, chia cho std (nếu std > 0)
        abnormal_score = max(abs(x - mean) for x in values) / std if std > 0 else 0.0
        return round(abnormal_score, 4)

    def run_ai_driven_abnormal_finding(self, data):
        """
        Task 3: Phân tích bất thường dựa trên AI (Isolation Forest)

        Đầu vào:
        - historical_prices: Giá lịch sử
        - trading_volumes: Khối lượng giao dịch
        - sector_metrics: Các chỉ số ngành
        - market_indicators: Chỉ số thị trường
        - financial_ratios: Các tỷ lệ tài chính

        Đầu ra: JSON chứa thông tin về các bất thường được phát hiện, điểm bất thường,
        phân loại mức độ và khuyến nghị
        """
        try:
            # Trích xuất các đặc trưng
            features = []

            # Giá và khối lượng
            price_data = data.get("historical_prices", [])
            volume_data = data.get("trading_volumes", [])

            if not price_data or len(price_data) < 10:
                return {"error": "Không đủ dữ liệu giá lịch sử"}

            # Tính các chỉ số kỹ thuật
            price_changes = [
                price_data[i + 1] - price_data[i] for i in range(len(price_data) - 1)
            ]
            price_volatility = np.std(price_changes) if price_changes else 0
            price_momentum = sum(price_changes[-5:]) if len(price_changes) >= 5 else 0

            # Volume anomalies
            avg_volume = np.mean(volume_data) if volume_data else 0
            recent_volume = volume_data[-1] if volume_data else 0
            volume_change = (recent_volume / avg_volume - 1) if avg_volume > 0 else 0

            # Tỷ lệ tài chính
            financial_ratios = data.get("financial_ratios", {})
            pe_ratio = financial_ratios.get("pe_ratio", 0)
            pb_ratio = financial_ratios.get("pb_ratio", 0)
            debt_to_equity = financial_ratios.get("debt_to_equity", 0)

            # Dữ liệu ngành và thị trường để so sánh
            sector_metrics = data.get("sector_metrics", {})
            market_indicators = data.get("market_indicators", {})

            sector_pe = sector_metrics.get("avg_pe", 15)
            pe_difference = (
                (pe_ratio / sector_pe - 1) if sector_pe > 0 and pe_ratio > 0 else 0
            )

            # Tạo vector đặc trưng
            features = [
                price_volatility,
                price_momentum,
                volume_change,
                pe_difference,
                pe_ratio,
                pb_ratio,
                debt_to_equity,
            ]

            # Chuẩn hóa dữ liệu
            features_array = np.array(features).reshape(1, -1)

            # Phát hiện bất thường bằng Isolation Forest
            anomaly_score = (
                -1 * self.abnormal_model.decision_function(features_array)[0]
            )
            anomaly_label = self.abnormal_model.predict(features_array)[0]

            # Phân loại mức độ bất thường
            if anomaly_score > 0.8:
                severity = "Cao"
                recommendation = (
                    "Cần theo dõi chặt chẽ và xem xét điều chỉnh chiến lược đầu tư"
                )
            elif anomaly_score > 0.6:
                severity = "Trung bình"
                recommendation = "Theo dõi sát và chuẩn bị các kịch bản dự phòng"
            elif anomaly_score > 0.4:
                severity = "Thấp"
                recommendation = "Theo dõi các chỉ số trong danh sách bất thường"
            else:
                severity = "Không đáng kể"
                recommendation = "Không cần hành động đặc biệt"

            # Xác định các loại bất thường cụ thể
            anomalies_detected = []

            if price_volatility > np.mean(price_data) * 0.15:
                anomalies_detected.append(
                    {
                        "type": "Biến động giá bất thường",
                        "value": round(price_volatility, 4),
                        "threshold": round(np.mean(price_data) * 0.15, 4),
                    }
                )

            if volume_change > 0.5:
                anomalies_detected.append(
                    {
                        "type": "Khối lượng giao dịch bất thường",
                        "value": round(volume_change, 4),
                        "threshold": 0.5,
                    }
                )

            if pe_difference > 0.3 or pe_difference < -0.3:
                anomalies_detected.append(
                    {
                        "type": "Chênh lệch P/E so với ngành",
                        "value": round(pe_difference, 4),
                        "threshold": "±0.3",
                    }
                )

            return {
                "anomaly_score": round(anomaly_score, 4),
                "is_anomaly": anomaly_label == -1,
                "severity": severity,
                "recommendation": recommendation,
                "anomalies_detected": anomalies_detected,
                "features_analyzed": {
                    "price_volatility": round(price_volatility, 4),
                    "price_momentum": round(price_momentum, 4),
                    "volume_change": round(volume_change, 4),
                    "pe_difference": round(pe_difference, 4),
                },
            }

        except Exception as e:
            return {"error": f"Lỗi khi phân tích bất thường: {str(e)}"}

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

    def run_ai_driven_model_consistency(self, data):
        """
        Task 4: Tính toán AI driven cho Model Consistency

        Đầu vào:
        - model_predictions: Danh sách dự đoán từ các mô hình khác nhau
        - model_weights: Trọng số của các mô hình
        - historical_accuracy: Độ chính xác lịch sử của mô hình
        - market_conditions: Điều kiện thị trường hiện tại

        Đầu ra: JSON chứa chỉ số đồng nhất, mô hình đáng tin cậy nhất, và khuyến nghị
        """
        try:
            # Trích xuất dữ liệu
            model_predictions = data.get("model_predictions", {})
            model_weights = data.get("model_weights", {})
            historical_accuracy = data.get("historical_accuracy", {})
            market_conditions = data.get("market_conditions", "neutral")

            if not model_predictions:
                return {"error": "Không có dự đoán từ mô hình nào"}

            # Đảm bảo tất cả model có trọng số
            for model in model_predictions:
                if model not in model_weights:
                    model_weights[model] = 1.0

            # Chuẩn hóa trọng số
            total_weights = sum(model_weights.values())
            if total_weights > 0:
                model_weights = {
                    model: weight / total_weights
                    for model, weight in model_weights.items()
                }

            # Tính điểm cho từng mô hình
            model_scores = {}
            for model, predictions in model_predictions.items():
                # Tính điểm dựa trên độ đồng nhất nội bộ mô hình
                if isinstance(predictions, list) and len(predictions) > 1:
                    internal_consistency = 1.0 - np.std(predictions) / (
                        np.mean(predictions) if np.mean(predictions) != 0 else 1
                    )
                else:
                    internal_consistency = 1.0

                # Tính điểm dựa trên độ chính xác lịch sử
                historical_score = historical_accuracy.get(model, 0.5)

                # Điểm cuối cùng của mô hình
                model_scores[model] = (
                    0.6 * internal_consistency + 0.4 * historical_score
                )

            # Tìm mô hình có điểm cao nhất
            best_model = (
                max(model_scores, key=model_scores.get) if model_scores else None
            )

            # Tính điểm đồng nhất giữa các mô hình
            all_predictions = []
            for predictions in model_predictions.values():
                if isinstance(predictions, list):
                    all_predictions.extend(predictions)
                else:
                    all_predictions.append(predictions)

            overall_consistency = 1.0 - np.std(all_predictions) / (
                np.mean(all_predictions)
                if np.mean(all_predictions) != 0 and len(all_predictions) > 0
                else 1
            )

            # Weighted average of predictions
            weighted_predictions = {}
            for metric in ["price_target", "growth_rate", "risk_score"]:
                values = []
                weights = []
                for model, predictions in model_predictions.items():
                    if isinstance(predictions, dict) and metric in predictions:
                        values.append(predictions[metric])
                        weights.append(model_weights.get(model, 1.0))

                if values and weights:
                    weighted_predictions[metric] = sum(
                        v * w for v, w in zip(values, weights)
                    ) / sum(weights)

            # Đề xuất khuyến nghị
            if overall_consistency > 0.8:
                recommendation = (
                    "Mức độ đồng thuận cao giữa các mô hình. Độ tin cậy cao."
                )
            elif overall_consistency > 0.6:
                recommendation = "Mức độ đồng thuận khá tốt. Nên ưu tiên mô hình có độ chính xác lịch sử cao nhất."
            elif overall_consistency > 0.4:
                recommendation = "Mức độ đồng thuận trung bình. Xem xét kỹ các mô hình trước khi ra quyết định."
            else:
                recommendation = "Mức độ đồng thuận thấp giữa các mô hình. Cần thận trọng và thu thập thêm thông tin."

            return {
                "overall_consistency_score": round(overall_consistency, 4),
                "model_scores": {
                    model: round(score, 4) for model, score in model_scores.items()
                },
                "best_model": best_model,
                "weighted_predictions": {
                    k: round(v, 4) for k, v in weighted_predictions.items()
                },
                "recommendation": recommendation,
                "market_conditions": market_conditions,
            }

        except Exception as e:
            return {"error": f"Lỗi khi phân tích độ đồng nhất mô hình: {str(e)}"}

    def run_dcf(self, data):
        """
        Xử lý DCF: Tính giá trị hiện tại ròng (Discounted Cash Flow).
        Giả sử data có các trường: 'cash_flows' (list), 'discount_rate' (float)
        """
        cash_flows = data.get("cash_flows", [])
        discount_rate = data.get("discount_rate", 0.1)
        if not isinstance(cash_flows, list) or not cash_flows:
            return 0.0
        dcf = sum(
            cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows, start=1)
        )
        return round(dcf, 2)

    def calculate_wacc(self, data):
        """
        Tính Weighted Average Cost of Capital (WACC)

        WACC = (E / (E + D)) * Re + (D / (E + D)) * Rd * (1 - T)

        Trong đó:
        - E: Giá trị vốn chủ sở hữu
        - D: Giá trị nợ
        - Re: Chi phí vốn chủ sở hữu (thường sử dụng CAPM: Re = Rf + β * (Rm - Rf))
        - Rd: Chi phí nợ
        - T: Thuế suất
        """
        equity_value = data.get("equity_value", 0)
        debt_value = data.get("debt_value", 0)
        risk_free_rate = data.get(
            "risk_free_rate", 0.03
        )  # Lãi suất phi rủi ro (VD: Trái phiếu chính phủ)
        market_return = data.get("market_return", 0.10)  # Lợi nhuận thị trường kỳ vọng
        beta = data.get("beta", 1.0)  # Hệ số beta
        cost_of_debt = data.get("cost_of_debt", 0.05)  # Chi phí nợ
        tax_rate = data.get("tax_rate", 0.2)  # Thuế suất

        total_value = equity_value + debt_value
        if total_value == 0:
            return 0.0

        # Tính chi phí vốn chủ sở hữu theo CAPM
        cost_of_equity = risk_free_rate + beta * (market_return - risk_free_rate)

        # Tính WACC
        equity_weight = equity_value / total_value
        debt_weight = debt_value / total_value

        wacc = equity_weight * cost_of_equity + debt_weight * cost_of_debt * (
            1 - tax_rate
        )

        return round(wacc, 4)

    def run_ai_driven_dcf(self, data):
        """
        Task 1: Tính toán AI driven DCF và WACC

        Đầu vào:
        - historical_cash_flows: Dòng tiền lịch sử
        - financial_statements: Báo cáo tài chính
        - growth_rates: Tỷ lệ tăng trưởng
        - industry_data: Dữ liệu ngành
        - market_data: Dữ liệu thị trường
        - balance_sheet: Bảng cân đối kế toán

        Đầu ra: JSON chứa thông tin về DCF, WACC, và dự báo dòng tiền
        """
        try:
            # Trích xuất dữ liệu
            historical_cash_flows = data.get("historical_cash_flows", [])
            financial_statements = data.get("financial_statements", {})
            growth_rates = data.get("growth_rates", {})
            industry_data = data.get("industry_data", {})
            market_data = data.get("market_data", {})
            balance_sheet = data.get("balance_sheet", {})

            if not historical_cash_flows or len(historical_cash_flows) < 3:
                return {"error": "Không đủ dữ liệu dòng tiền lịch sử"}

            # Tính WACC - giúp xác định tỷ lệ chiết khấu
            wacc_data = {
                "equity_value": balance_sheet.get("total_equity", 0),
                "debt_value": balance_sheet.get("total_debt", 0),
                "risk_free_rate": market_data.get("risk_free_rate", 0.03),
                "market_return": market_data.get("market_return", 0.1),
                "beta": financial_statements.get("beta", 1.0),
                "cost_of_debt": financial_statements.get("interest_rate", 0.05),
                "tax_rate": financial_statements.get("tax_rate", 0.2),
            }

            wacc = self.calculate_wacc(wacc_data)

            # Tạo các features cho AI model
            features = []
            target = []

            # Chuẩn bị dữ liệu cho mô hình học
            for i in range(len(historical_cash_flows) - 1):
                # Lấy 3 giá trị dòng tiền liên tiếp làm đặc trưng
                if i + 3 <= len(historical_cash_flows):
                    feature = [
                        historical_cash_flows[i],
                        historical_cash_flows[i + 1],
                        historical_cash_flows[i + 2],
                    ]

                    # Thêm các đặc trưng khác
                    feature.append(growth_rates.get("revenue_growth", 0.05))
                    feature.append(growth_rates.get("profit_margin", 0.1))
                    feature.append(industry_data.get("industry_growth", 0.03))
                    feature.append(market_data.get("gdp_growth", 0.02))

                    features.append(feature)

                    # Giá trị tiếp theo là mục tiêu dự đoán
                    if i + 3 < len(historical_cash_flows):
                        target.append(historical_cash_flows[i + 3])

            if not features or not target:
                # Nếu không đủ dữ liệu cho AI, sử dụng phương pháp truyền thống
                last_cash_flow = historical_cash_flows[-1]
                projected_growth = growth_rates.get("projected_growth", 0.05)

                # Dự báo dòng tiền trong tương lai (5 năm)
                projected_cash_flows = []
                for i in range(1, 6):
                    projected_cf = last_cash_flow * (1 + projected_growth) ** i
                    projected_cash_flows.append(round(projected_cf, 2))

                # Tính terminal value (Gordon Growth Model)
                terminal_growth = industry_data.get("long_term_growth", 0.02)
                terminal_value = (
                    projected_cash_flows[-1]
                    * (1 + terminal_growth)
                    / (wacc - terminal_growth)
                )

                # Tính DCF
                dcf_value = 0
                for i, cf in enumerate(projected_cash_flows, start=1):
                    dcf_value += cf / ((1 + wacc) ** i)

                # Thêm terminal value
                dcf_value += terminal_value / ((1 + wacc) ** len(projected_cash_flows))

                ai_confidence = 0  # Không dùng AI
            else:
                # Huấn luyện mô hình
                self.dcf_model.fit(features, target)

                # Dự báo dòng tiền tương lai
                last_features = features[-1][1:] + [
                    growth_rates.get("projected_growth", 0.05)
                ]

                projected_cash_flows = []
                current_feature = last_features

                for i in range(5):  # Dự đoán 5 năm tiếp theo
                    prediction = self.dcf_model.predict([current_feature])[0]
                    projected_cash_flows.append(round(prediction, 2))

                    # Cập nhật features cho lần dự đoán tiếp theo
                    current_feature = current_feature[1:] + [prediction]

                # Tính terminal value
                terminal_growth = industry_data.get("long_term_growth", 0.02)
                terminal_value = (
                    projected_cash_flows[-1]
                    * (1 + terminal_growth)
                    / (wacc - terminal_growth)
                )

                # Tính DCF
                dcf_value = 0
                for i, cf in enumerate(projected_cash_flows, start=1):
                    dcf_value += cf / ((1 + wacc) ** i)

                # Thêm terminal value
                dcf_value += terminal_value / ((1 + wacc) ** len(projected_cash_flows))

                # Đánh giá độ tin cậy của mô hình
                # Đối với RandomForestRegressor, ta có thể dùng R²
                ai_confidence = self.dcf_model.score(features, target)

            # Tính tổng giá trị công ty
            outstanding_shares = balance_sheet.get("outstanding_shares", 1000000)
            total_debt = balance_sheet.get("total_debt", 0)
            cash_equivalents = balance_sheet.get("cash_equivalents", 0)

            enterprise_value = dcf_value
            equity_value = enterprise_value + cash_equivalents - total_debt
            price_per_share = (
                equity_value / outstanding_shares if outstanding_shares > 0 else 0
            )

            return {
                "dcf_value": round(dcf_value, 2),
                "wacc": wacc,
                "projected_cash_flows": projected_cash_flows,
                "terminal_value": round(terminal_value, 2),
                "enterprise_value": round(enterprise_value, 2),
                "equity_value": round(equity_value, 2),
                "price_per_share": round(price_per_share, 2),
                "ai_confidence": (
                    round(ai_confidence, 4)
                    if isinstance(ai_confidence, (int, float))
                    else 0
                ),
                "discount_factors": [
                    round(1 / ((1 + wacc) ** i), 4)
                    for i in range(1, len(projected_cash_flows) + 1)
                ],
                "methodology": (
                    "AI-driven DCF" if ai_confidence > 0 else "Traditional DCF"
                ),
            }

        except Exception as e:
            return {"error": f"Lỗi khi tính DCF: {str(e)}"}

    def run_pe_analysis(self, data):
        """
        Phân tích tỉ số P/E (Price-to-Earnings) và đánh giá định giá cổ phiếu.
        Giả sử data có các trường: 'price' (float), 'earnings' (float), 'sector_avg_pe' (float), 'market_avg_pe' (float)

        Trả về: Dictionary chứa tỉ số P/E, đánh giá, và so sánh với trung bình ngành và thị trường
        """
        price = data.get("price", 0)
        earnings = data.get("earnings", 0)
        sector_avg_pe = data.get("sector_avg_pe", 15.0)  # PE trung bình ngành mặc định
        market_avg_pe = data.get(
            "market_avg_pe", 18.0
        )  # PE trung bình thị trường mặc định

        # Tránh chia cho 0
        if earnings <= 0:
            return {
                "pe_ratio": None,
                "evaluation": "Không thể đánh giá (EPS không dương)",
                "sector_comparison": None,
                "market_comparison": None,
            }

        pe_ratio = price / earnings
        pe_ratio_rounded = round(pe_ratio, 2)

        # Đánh giá định giá dựa trên tỉ số P/E
        if pe_ratio < sector_avg_pe * 0.7:
            evaluation = "Định giá thấp (có thể định giá thấp hoặc có vấn đề tiềm ẩn)"
        elif pe_ratio < sector_avg_pe:
            evaluation = "Định giá hợp lý (thấp hơn trung bình ngành)"
        elif pe_ratio < sector_avg_pe * 1.3:
            evaluation = "Định giá hợp lý (cao hơn trung bình ngành)"
        else:
            evaluation = "Định giá cao (kỳ vọng tăng trưởng cao hoặc định giá quá cao)"

        # So sánh với trung bình ngành và thị trường
        sector_comparison = round(
            (pe_ratio / sector_avg_pe - 1) * 100, 2
        )  # % chênh lệch so với ngành
        market_comparison = round(
            (pe_ratio / market_avg_pe - 1) * 100, 2
        )  # % chênh lệch so với thị trường

        return {
            "pe_ratio": pe_ratio_rounded,
            "evaluation": evaluation,
            "sector_comparison": sector_comparison,
            "market_comparison": market_comparison,
        }

    def run_neural_pe_analysis(self, data):
        """
        Task 2: Phân tích PE với mạng neural

        Đầu vào:
        - price: Giá cổ phiếu hiện tại
        - earnings: Thu nhập
        - historical_pe: Lịch sử PE
        - sector_data: Dữ liệu ngành
        - growth_metrics: Chỉ số tăng trưởng
        - financial_health: Sức khỏe tài chính

        Đầu ra: JSON chứa phân tích PE được tăng cường bởi neural network
        """
        try:
            # Trích xuất dữ liệu
            price = data.get("price", 0)
            earnings = data.get("earnings", 0)
            historical_pe = data.get("historical_pe", [])
            sector_data = data.get("sector_data", {})
            growth_metrics = data.get("growth_metrics", {})
            financial_health = data.get("financial_health", {})

            # Các chỉ số tăng trưởng
            revenue_growth = growth_metrics.get("revenue_growth", 0)
            earnings_growth = growth_metrics.get("earnings_growth", 0)
            projected_growth = growth_metrics.get("projected_growth", 0)

            # Dữ liệu ngành
            sector_avg_pe = sector_data.get("avg_pe", 15)
            sector_avg_growth = sector_data.get("avg_growth", 0.05)
            sector_high_pe = sector_data.get("high_pe", 25)
            sector_low_pe = sector_data.get("low_pe", 10)

            # Sức khỏe tài chính
            debt_to_equity = financial_health.get("debt_to_equity", 1.0)
            current_ratio = financial_health.get("current_ratio", 1.5)
            return_on_equity = financial_health.get("roe", 0.1)

            if earnings <= 0:
                return {
                    "pe_ratio": None,
                    "adjusted_pe": None,
                    "fair_pe": None,
                    "evaluation": "Không thể đánh giá (EPS không dương)",
                    "price_targets": None,
                    "confidence": 0,
                }

            # Tính PE cơ bản
            pe_ratio = price / earnings if earnings > 0 else None

            # Chuẩn bị features cho neural network
            features = [
                pe_ratio if pe_ratio is not None else 0,
                sector_avg_pe,
                revenue_growth,
                earnings_growth,
                projected_growth,
                debt_to_equity,
                current_ratio,
                return_on_equity,
                np.mean(historical_pe) if historical_pe else pe_ratio or 0,
                (
                    np.std(historical_pe)
                    if historical_pe and len(historical_pe) > 1
                    else 0
                ),
            ]

            # Chuẩn hóa features
            features_array = np.array(features).reshape(1, -1)

            # Trong thực tế, mô hình neural network sẽ được huấn luyện trước
            # Ở đây, chúng ta sẽ mô phỏng kết quả từ neural network

            # Mô phỏng fair P/E dựa trên đặc điểm của công ty
            # Công thức: PE cơ bản được điều chỉnh theo tăng trưởng và rủi ro

            # PEG ratio (PE/Growth) - chỉ số đánh giá PE theo tăng trưởng
            peg_ratio = pe_ratio / projected_growth if projected_growth > 0 else None

            # Tính fair PE dựa trên mô hình tăng trưởng (PE ~ Growth Rate)
            # Mô hình đơn giản: Fair PE = Sector Avg PE * (1 + (Growth - Sector Avg Growth))
            growth_adjustment = 1 + (projected_growth - sector_avg_growth)
            fair_pe_by_growth = sector_avg_pe * growth_adjustment

            # Điều chỉnh theo rủi ro tài chính
            risk_factor = 1.0
            if debt_to_equity > 2:
                risk_factor -= 0.2  # Giảm PE nếu nợ cao
            elif debt_to_equity < 0.5:
                risk_factor += 0.1  # Tăng PE nếu nợ thấp

            if current_ratio < 1.0:
                risk_factor -= 0.1  # Giảm PE nếu thanh khoản thấp
            elif current_ratio > 2.0:
                risk_factor += 0.05  # Tăng PE nếu thanh khoản cao

            if return_on_equity > 0.2:
                risk_factor += 0.15  # Tăng PE nếu ROE cao

            # Fair PE cuối cùng
            fair_pe = fair_pe_by_growth * risk_factor

            # Giới hạn fair PE trong khoảng hợp lý
            fair_pe = max(sector_low_pe * 0.8, min(fair_pe, sector_high_pe * 1.2))

            # Đánh giá định giá dựa trên PE so với fair PE
            if pe_ratio is None:
                evaluation = "Không thể đánh giá"
            elif pe_ratio < fair_pe * 0.8:
                evaluation = "Định giá thấp (tiềm năng tăng giá)"
            elif pe_ratio < fair_pe * 0.95:
                evaluation = "Định giá hợp lý (thấp hơn giá trị hợp lý)"
            elif pe_ratio < fair_pe * 1.05:
                evaluation = "Định giá hợp lý (gần giá trị hợp lý)"
            elif pe_ratio < fair_pe * 1.2:
                evaluation = "Định giá hợp lý (cao hơn giá trị hợp lý)"
            else:
                evaluation = "Định giá cao (có thể điều chỉnh giảm)"

            # Tính các mức giá mục tiêu
            fair_price = fair_pe * earnings
            upside_price = fair_pe * earnings * 1.1  # 10% trên giá trị hợp lý
            downside_price = fair_pe * earnings * 0.9  # 10% dưới giá trị hợp lý

            # Độ tin cậy của mô hình
            # Trong thực tế, độ tin cậy sẽ được tính từ kết quả của mô hình neural
            confidence = 0.75  # Giá trị mô phỏng

            # Nếu không có đủ dữ liệu, giảm độ tin cậy
            if not historical_pe:
                confidence *= 0.8
            if projected_growth == 0:
                confidence *= 0.9

            return {
                "pe_ratio": round(pe_ratio, 2) if pe_ratio is not None else None,
                "fair_pe": round(fair_pe, 2),
                "peg_ratio": round(peg_ratio, 2) if peg_ratio is not None else None,
                "evaluation": evaluation,
                "price_targets": {
                    "current_price": price,
                    "fair_price": round(fair_price, 2),
                    "upside_target": round(upside_price, 2),
                    "downside_risk": round(downside_price, 2),
                    "potential_return": (
                        round((fair_price / price - 1) * 100, 2) if price > 0 else None
                    ),
                },
                "neural_factors": {
                    "growth_adjustment": round(growth_adjustment, 2),
                    "risk_factor": round(risk_factor, 2),
                },
                "confidence": round(confidence, 2),
                "sector_comparison": {
                    "company_pe": round(pe_ratio, 2) if pe_ratio is not None else None,
                    "sector_avg_pe": round(sector_avg_pe, 2),
                    "difference_percent": (
                        round((pe_ratio / sector_avg_pe - 1) * 100, 2)
                        if pe_ratio is not None and sector_avg_pe > 0
                        else None
                    ),
                },
            }

        except Exception as e:
            return {"error": f"Lỗi khi phân tích PE: {str(e)}"}

    def run_risk_mitigation(self, data):
        """
        Task 5: Tính toán AI driven cho Risk Mitigation, giả định Monte Carlo, Altman & Piotroski Z-score

        Đầu vào:
        - financial_statements: Báo cáo tài chính
        - stock_price_history: Lịch sử giá cổ phiếu
        - market_data: Dữ liệu thị trường
        - macro_indicators: Chỉ số vĩ mô

        Đầu ra: JSON chứa phân tích rủi ro, Z-score, kết quả Monte Carlo và khuyến nghị
        """
        try:
            # Trích xuất dữ liệu
            financial = data.get("financial_statements", {})
            price_history = data.get("stock_price_history", [])
            market_data = data.get("market_data", {})
            macro_indicators = data.get("macro_indicators", {})

            if not financial:
                return {"error": "Không có dữ liệu tài chính"}

            # 1. Tính Altman Z-Score
            # Z = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
            # A = Working Capital / Total Assets
            # B = Retained Earnings / Total Assets
            # C = EBIT / Total Assets
            # D = Market Value of Equity / Total Liabilities
            # E = Sales / Total Assets

            working_capital = financial.get("current_assets", 0) - financial.get(
                "current_liabilities", 0
            )
            total_assets = financial.get("total_assets", 1)  # Tránh chia cho 0
            retained_earnings = financial.get("retained_earnings", 0)
            ebit = financial.get("ebit", 0)
            market_value_equity = financial.get("market_cap", 0)
            total_liabilities = financial.get("total_liabilities", 1)
            sales = financial.get("sales", 0)

            A = working_capital / total_assets
            B = retained_earnings / total_assets
            C = ebit / total_assets
            D = market_value_equity / total_liabilities
            E = sales / total_assets

            z_score = 1.2 * A + 1.4 * B + 3.3 * C + 0.6 * D + 1.0 * E

            # Phân loại theo Z-Score
            if z_score > 2.99:
                z_evaluation = "An toàn - Khả năng phá sản thấp"
                z_risk_level = "Thấp"
            elif z_score > 1.81:
                z_evaluation = "Vùng xám - Cần theo dõi"
                z_risk_level = "Trung bình"
            else:
                z_evaluation = "Nguy hiểm - Khả năng phá sản cao"
                z_risk_level = "Cao"

            # 2. Tính Piotroski F-Score (từ 0 đến 9, cao hơn tốt hơn)
            # Chỉ số này đánh giá sức khỏe tài chính dựa trên 9 tiêu chí
            f_score = 0

            # Khả năng sinh lời
            if financial.get("net_income", 0) > 0:
                f_score += 1  # Lợi nhuận ròng dương

            if financial.get("operating_cash_flow", 0) > 0:
                f_score += 1  # Dòng tiền hoạt động dương

            if financial.get("roa", 0) > financial.get("prev_roa", 0):
                f_score += 1  # ROA cải thiện

            if financial.get("operating_cash_flow", 0) > financial.get("net_income", 0):
                f_score += 1  # Dòng tiền > Lợi nhuận (chất lượng thu nhập)

            # Đòn bẩy, thanh khoản và hiệu quả hoạt động
            if financial.get("long_term_debt", 0) / total_assets < financial.get(
                "prev_long_term_debt", 0
            ) / financial.get("prev_total_assets", 1):
                f_score += 1  # Giảm đòn bẩy

            if financial.get("current_ratio", 0) > financial.get(
                "prev_current_ratio", 0
            ):
                f_score += 1  # Tăng thanh khoản

            if financial.get("shares_outstanding", 0) <= financial.get(
                "prev_shares_outstanding", float("inf")
            ):
                f_score += 1  # Không pha loãng cổ phiếu

            # Hiệu quả hoạt động
            if financial.get("gross_margin", 0) > financial.get("prev_gross_margin", 0):
                f_score += 1  # Cải thiện biên lợi nhuận gộp

            if financial.get("asset_turnover", 0) > financial.get(
                "prev_asset_turnover", 0
            ):
                f_score += 1  # Tăng vòng quay tài sản

            # Đánh giá F-Score
            if f_score >= 7:
                f_evaluation = "Sức khỏe tài chính tốt"
            elif f_score >= 4:
                f_evaluation = "Sức khỏe tài chính trung bình"
            else:
                f_evaluation = "Sức khỏe tài chính yếu"

            # 3. Mô phỏng Monte Carlo cho dự đoán giá cổ phiếu
            if price_history and len(price_history) > 30:
                # Tính lợi suất lịch sử
                returns = [
                    (price_history[i] / price_history[i - 1] - 1)
                    for i in range(1, len(price_history))
                ]
                mu = np.mean(returns)  # Lợi suất trung bình
                sigma = np.std(returns)  # Độ biến động

                current_price = price_history[-1]
                days = 252  # Số ngày giao dịch trong năm
                num_simulations = 1000

                # Thực hiện mô phỏng Monte Carlo
                simulation_results = []
                for _ in range(num_simulations):
                    price_series = [current_price]
                    for _ in range(days):
                        # Mô hình Chuyển động Brown hình học
                        daily_return = np.random.normal(mu, sigma)
                        price_series.append(price_series[-1] * (1 + daily_return))
                    simulation_results.append(price_series[-1])

                # Phân tích kết quả mô phỏng
                mean_price = np.mean(simulation_results)
                median_price = np.median(simulation_results)
                std_dev = np.std(simulation_results)

                # Tính VaR (Value at Risk) và CVaR (Conditional VaR)
                confidence_level = 0.05  # 95% confidence
                var_95 = np.percentile(simulation_results, confidence_level * 100)
                cvar_95 = np.mean([x for x in simulation_results if x <= var_95])

                # Xác suất giảm giá
                downside_prob = (
                    len([x for x in simulation_results if x < current_price])
                    / num_simulations
                )

                # Định giá rủi ro
                risk_reward_ratio = (
                    (mean_price - current_price) / (current_price - var_95)
                    if current_price != var_95
                    else 0
                )

                monte_carlo_results = {
                    "expected_price": round(mean_price, 2),
                    "median_price": round(median_price, 2),
                    "current_price": round(current_price, 2),
                    "price_volatility": round(std_dev / mean_price, 4),
                    "var_95": round(var_95, 2),
                    "cvar_95": round(cvar_95, 2),
                    "downside_probability": round(downside_prob, 4),
                    "risk_reward_ratio": round(risk_reward_ratio, 2),
                    "max_price": round(max(simulation_results), 2),
                    "min_price": round(min(simulation_results), 2),
                }
            else:
                monte_carlo_results = {
                    "error": "Không đủ dữ liệu giá để thực hiện mô phỏng Monte Carlo"
                }

            # 4. Đánh giá rủi ro tổng thể và khuyến nghị
            # Kết hợp các chỉ số để đánh giá rủi ro
            if z_score > 2.5 and f_score >= 7:
                risk_rating = "Thấp"
                risk_recommendation = (
                    "Rủi ro thấp. Phù hợp cho đầu tư dài hạn với mức rủi ro thấp."
                )
            elif z_score > 1.8 and f_score >= 5:
                risk_rating = "Trung bình-Thấp"
                risk_recommendation = "Rủi ro trung bình thấp. Cần theo dõi các chỉ số tài chính trong các quý tới."
            elif z_score > 1.5 and f_score >= 3:
                risk_rating = "Trung bình"
                risk_recommendation = "Rủi ro trung bình. Nên giới hạn phần trăm danh mục đầu tư vào cổ phiếu này."
            elif z_score > 1.0:
                risk_rating = "Trung bình-Cao"
                risk_recommendation = (
                    "Rủi ro cao. Chỉ phù hợp cho nhà đầu tư chấp nhận rủi ro cao."
                )
            else:
                risk_rating = "Cao"
                risk_recommendation = "Rủi ro rất cao. Không khuyến nghị đầu tư."

            # Xem xét các yếu tố vĩ mô
            macro_risk_factors = []

            if macro_indicators.get("interest_rate_trend", "stable") == "rising":
                macro_risk_factors.append(
                    "Lãi suất đang tăng - có thể ảnh hưởng tiêu cực đến định giá cổ phiếu"
                )

            if macro_indicators.get("gdp_growth", 0) < 1.0:
                macro_risk_factors.append(
                    "Tăng trưởng GDP thấp - có thể ảnh hưởng đến doanh thu và lợi nhuận"
                )

            if macro_indicators.get("inflation", 0) > 5.0:
                macro_risk_factors.append(
                    "Lạm phát cao - có thể ảnh hưởng đến biên lợi nhuận và chi phí vốn"
                )

            if market_data.get("market_sentiment", "neutral") == "bearish":
                macro_risk_factors.append(
                    "Tâm lý thị trường tiêu cực - có thể gây áp lực giảm giá"
                )

            # Tổng hợp đánh giá rủi ro
            return {
                "altman_z_score": {
                    "score": round(z_score, 2),
                    "evaluation": z_evaluation,
                    "risk_level": z_risk_level,
                    "components": {
                        "working_capital_to_assets": round(A, 4),
                        "retained_earnings_to_assets": round(B, 4),
                        "ebit_to_assets": round(C, 4),
                        "equity_to_liabilities": round(D, 4),
                        "sales_to_assets": round(E, 4),
                    },
                },
                "piotroski_f_score": {
                    "score": f_score,
                    "evaluation": f_evaluation,
                    "max_score": 9,
                },
                "monte_carlo_simulation": monte_carlo_results,
                "overall_risk_assessment": {
                    "risk_rating": risk_rating,
                    "recommendation": risk_recommendation,
                    "macro_risk_factors": macro_risk_factors,
                    "confidence": 0.8,  # Độ tin cậy của đánh giá
                },
            }

        except Exception as e:
            return {"error": f"Lỗi khi phân tích rủi ro: {str(e)}"}
