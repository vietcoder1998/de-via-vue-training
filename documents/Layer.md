+-------------------+
|   AnalysisController   |
+-------------------+
| - service: AnalysisService |
+-------------------+
| + handle_request(request_json: dict): dict |
+-------------------+
                |
                v
+-------------------+
|   AnalysisService   |
+-------------------+
| - transformer: DataTransformer |
| - via: VIA |
| - vua: VUA |
+-------------------+
| + process(task_type: str, request_json: dict): dict |
+-------------------+
   |               |               |
   v               v               v
+-------------------+     +-------------------+     +-------------------+
| DataTransformer   |     |        VIA        |     |        VUA        |
+-------------------+     +-------------------+     +-------------------+
| + transform_financial()| | + run_dcf()       |    | + interpret_dcf()  |
| + transform_transaction()|+ run_abnormal()  |    | + interpret_abnormal()|
|                       | | + run_consistency()|    | + interpret_consistency()|
+-------------------+     +-------------------+     +-------------------+
                                |
                                v
                       +-------------------+
                       |  ML Models (AI)   |
                       +-------------------+
                       | RandomForest, NN, |
                       | XGBoost, etc.     |
                       +-------------------+
