from fastapi import APIRouter
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
        </script>
    </body>
    </html>
    """