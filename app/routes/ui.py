from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse

ui_router = APIRouter()

@ui_router.get("/analyze-ui", response_class=HTMLResponse, summary="Demo UI for /analyze")
async def analyze_ui():
    """A simple HTML UI for trying the /analyze endpoint."""
    return """
    <html>
    <head>
        <title>Analyze Demo UI</title>
    </head>
    <body>
        <h2>Demo: /analyze endpoint</h2>
        <form id="analyzeForm">
            <label>Task:</label>
            <select name="task">
                <option value="DCF">DCF</option>
                <option value="Abnormal Finding">Abnormal Finding</option>
                <option value="Model Consistency">Model Consistency</option>
                <option value="WACC">WACC</option>
            </select><br/>
            <label>Model Type:</label>
            <select name="model_type">
                <option value="RandomForest">RandomForest</option>
                <option value="NeuralNetwork">NeuralNetwork</option>
                <option value="XGBoost">XGBoost</option>
            </select><br/>
            <label>Data (JSON):</label><br/>
            <textarea name="data" rows="10" cols="60">{ "free_cash_flow": [100, 110, 121, 133.1, 146.41], "terminal_growth_rate": 0.02, "discount_rate": 0.1, "shares_outstanding": 10, "net_debt": 50 }</textarea><br/>
            <button type="button" onclick="submitForm()">Submit</button>
        </form>
        <h3>Result:</h3>
        <pre id="result"></pre>
        <hr>
        <h2>Batch Analyze CSV</h2>
        <form id="batchForm" enctype="multipart/form-data">
            <label>Task:</label>
            <select name="task">
                <option value="DCF">DCF</option>
                <option value="Abnormal Finding">Abnormal Finding</option>
                <option value="Model Consistency">Model Consistency</option>
                <option value="WACC">WACC</option>
            </select><br/>
            <label>Model Type:</label>
            <select name="model_type">
                <option value="RandomForest">RandomForest</option>
                <option value="NeuralNetwork">NeuralNetwork</option>
                <option value="XGBoost">XGBoost</option>
            </select><br/>
            <label>CSV File:</label>
            <input type="file" name="file" accept=".csv" /><br/>
            <button type="button" onclick="batchAnalyze()">Batch Analyze</button>
        </form>
        <h3>Batch Analyze Result:</h3>
        <pre id="batchResult"></pre>
        <hr>
        <h2>Update Training Data</h2>
        <form id="uploadForm" enctype="multipart/form-data">
            <label>Model Type:</label>
            <select name="model_type">
                <option value="RandomForest">RandomForest</option>
                <option value="NeuralNetwork">NeuralNetwork</option>
                <option value="XGBoost">XGBoost</option>
            </select><br/>
            <label>Target Column:</label>
            <input type="text" name="target_column" value="target" /><br/>
            <label>CSV File:</label>
            <input type="file" name="file" accept=".csv" /><br/>
            <button type="button" onclick="uploadFile()">Upload & Train</button>
        </form>
        <h3>Training Result:</h3>
        <pre id="trainResult"></pre>
        <script>
        async function submitForm() {
            const form = document.getElementById('analyzeForm');
            const task = form.task.value;
            const model_type = form.model_type.value;
            let data;
            try {
                data = JSON.parse(form.data.value);
            } catch (e) {
                document.getElementById('result').innerText = "Invalid JSON in data field!";
                return;
            }
            const payload = { task, model_type, data };
            const res = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await res.json();
            document.getElementById('result').innerText = JSON.stringify(result, null, 2);
        }

        async function batchAnalyze() {
            const form = document.getElementById('batchForm');
            const task = form.task.value;
            const model_type = form.model_type.value;
            const fileInput = form.file;
            if (!fileInput.files.length) {
                document.getElementById('batchResult').innerText = "Please select a CSV file!";
                return;
            }
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("task", task);
            formData.append("model_type", model_type);
            formData.append("file", file);

            const res = await fetch('/analyze-csv', {
                method: 'POST',
                body: formData
            });
            const result = await res.json();
            document.getElementById('batchResult').innerText = JSON.stringify(result, null, 2);
        }

        async function uploadFile() {
            const form = document.getElementById('uploadForm');
            const model_type = form.model_type.value;
            const target_column = form.target_column.value;
            const fileInput = form.file;
            if (!fileInput.files.length) {
                document.getElementById('trainResult').innerText = "Please select a CSV file!";
                return;
            }
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("model_type", model_type);
            formData.append("target_column", target_column);
            formData.append("file", file);

            const res = await fetch('/train-with-file', {
                method: 'POST',
                body: formData
            });
            const result = await res.json();
            document.getElementById('trainResult').innerText = JSON.stringify(result, null, 2);
        }
        </script>
    </body>
    </html>
    """