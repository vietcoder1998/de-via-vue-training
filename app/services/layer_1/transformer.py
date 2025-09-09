import re
import csv

class DataTransformer:
    def transform_xxx(self, request_json):
        """
        Chuẩn hoá dữ liệu đầu vào:
        - Chuyển tất cả key về dạng snake_case
        - Loại bỏ các trường không cần thiết (nếu có)
        - Chuyển các giá trị số về float (nếu có thể)
        """
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

    def csv_to_json_consistency(self, csv_file):
        """
        Nhận vào file-like object (StringIO hoặc file path), trả về list dict JSON consistency.
        """
        result = []
        # Nếu là file path thì mở file, nếu là file-like thì dùng trực tiếp
        if isinstance(csv_file, str):
            f = open(csv_file, encoding="utf-8")
            close_f = True
        else:
            f = csv_file
            close_f = False
        reader = csv.DictReader(f)
        for row in reader:
            base = {}
            comparable_companies = []
            for k, v in row.items():
                if k.startswith("comparable_name_"):
                    idx = k.split("_")[-1]
                    name = v
                    pe_key = f"comparable_pe_{idx}"
                    pe_ratio = row.get(pe_key)
                    if name and pe_ratio:
                        try:
                            pe_ratio = float(pe_ratio)
                        except Exception:
                            pass
                        comparable_companies.append({"name": name, "pe_ratio": pe_ratio})
                elif not k.startswith("comparable_pe_"):
                    try:
                        base[k] = float(v)
                    except Exception:
                        base[k] = v
            base["comparable_companies"] = comparable_companies
            result.append(base)
        if close_f:
            f.close()
        return result

    def csv_to_json_wacc(self, csv_file):
        """
        Nhận vào file-like object (StringIO hoặc file path), trả về list dict JSON WACC.
        """
        result = []
        if isinstance(csv_file, str):
            f = open(csv_file, encoding="utf-8")
            close_f = True
        else:
            f = csv_file
            close_f = False
        reader = csv.DictReader(f)
        for row in reader:
            item = {}
            for k, v in row.items():
                try:
                    item[k] = float(v)
                except Exception:
                    item[k] = v
            result.append(item)
        if close_f:
            f.close()
        return result

    def csv_to_json_abnormal(self, csv_file):
        """
        Nhận vào file-like object (StringIO hoặc file path), trả về list dict JSON abnormal/dcf.
        """
        result = []
        if isinstance(csv_file, str):
            f = open(csv_file, encoding="utf-8")
            close_f = True
        else:
            f = csv_file
            close_f = False
        reader = csv.DictReader(f)
        for row in reader:
            item = {}
            for k, v in row.items():
                try:
                    item[k] = float(v)
                except Exception:
                    item[k] = v
            result.append(item)
        if close_f:
            f.close()
        return result