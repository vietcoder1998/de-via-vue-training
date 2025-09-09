class DataTransformer:
    def transform_xxx(self, request_json):
        """
        Chuẩn hoá dữ liệu đầu vào:
        - Chuyển tất cả key về dạng snake_case
        - Loại bỏ các trường không cần thiết (nếu có)
        - Chuyển các giá trị số về float (nếu có thể)
        """
        import re

        def to_snake_case(s):
            return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

        data = request_json.get("data", {}) if "data" in request_json else request_json
        transformed = {}
        for k, v in data.items():
            key = to_snake_case(k)
            # Convert numeric strings to float if possible
            if isinstance(v, str) and v.replace('.', '', 1).isdigit():
                try:
                    v = float(v)
                except Exception:
                    pass
            transformed[key] = v
        return transformed