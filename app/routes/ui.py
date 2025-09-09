from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse

ui_router = APIRouter()


@ui_router.get(
    "/analyze-ui", response_class=HTMLResponse, summary="Demo UI for /analyze"
)
async def analyze_ui():
    """A simple HTML UI for trying the /analyze endpoint."""
    return """
    <html>
    <head>
        <title>AI Financial Analysis Platform</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
            h1, h2, h3 { color: #2c3e50; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { background: #f9f9f9; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            label { font-weight: bold; display: block; margin-bottom: 5px; }
            select, input, textarea { width: 100%; padding: 8px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            textarea { resize: vertical; font-family: monospace; }
            button { background: #3498db; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
            button:hover { background: #2980b9; }
            pre { background: #f1f1f1; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
            .tabs { display: flex; margin-bottom: 20px; }
            .tab { padding: 10px 20px; cursor: pointer; border-bottom: 2px solid transparent; }
            .tab.active { border-bottom: 2px solid #3498db; font-weight: bold; }
            .tab-content { display: none; }
            .tab-content.active { display: block; }
            .loading { display: none; margin: 20px 0; text-align: center; }
            .loading:after { content: " ⟳"; animation: spin 1s linear infinite; display: inline-block; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .info-box { background: #e8f4fc; border-left: 4px solid #3498db; padding: 10px 15px; margin-bottom: 15px; }
            .sample-btn { background: #95a5a6; margin-right: 5px; font-size: 12px; padding: 5px 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Financial Analysis Platform</h1>
            
            <div class="tabs">
                <div class="tab active" onclick="showTab('analyze')">Analysis</div>
                <div class="tab" onclick="showTab('batch')">Batch Analysis</div>
                <div class="tab" onclick="showTab('training')">Model Training</div>
                <div class="tab" onclick="showTab('advanced')">Advanced ML</div>
            </div>
            
            <!-- Analysis Tab -->
            <div id="analyze" class="tab-content active card">
                <h2>Financial Analysis</h2>
                <div class="info-box">
                    Select a task and model type, then provide the required input data in JSON format.
                </div>
                
                <form id="analyzeForm">
                    <label>Task:</label>
                    <select name="task" onchange="updateSampleData()">
                        <option value="DCF">DCF Analysis</option>
                        <option value="PE Analysis">PE Analysis</option>
                        <option value="Abnormal Finding">Abnormal Finding</option>
                        <option value="Model Consistency">Model Consistency</option>
                        <option value="Risk Mitigation">Risk Mitigation</option>
                    </select>
                    
                    <label>Model Type:</label>
                    <select name="model_type">
                        <option value="RandomForest">RandomForest</option>
                        <option value="NeuralNetwork">NeuralNetwork</option>
                        <option value="XGBoost">XGBoost</option>
                    </select>
                    
                    <label>
                        Data (JSON):
                        <button type="button" class="sample-btn" onclick="loadSample('dcf')">DCF Sample</button>
                        <button type="button" class="sample-btn" onclick="loadSample('pe')">PE Sample</button>
                        <button type="button" class="sample-btn" onclick="loadSample('abnormal')">Abnormal Sample</button>
                    </label>
                    <textarea name="data" rows="12" cols="60" id="dataInput">{ 
    "free_cash_flow": [100, 110, 121, 133.1, 146.41], 
    "terminal_growth_rate": 0.02, 
    "discount_rate": 0.1, 
    "shares_outstanding": 10, 
    "net_debt": 50 
}</textarea>
                    
                    <button type="button" onclick="submitForm()">Analyze</button>
                </form>
                
                <div id="analyzeLoading" class="loading">Processing analysis...</div>
                
                <h3>Result:</h3>
                <pre id="result"></pre>
            </div>
            
            <!-- Batch Analysis Tab -->
            <div id="batch" class="tab-content card">
                <h2>Batch Analysis with CSV</h2>
                <div class="info-box">
                    Upload a CSV file with multiple rows to analyze many scenarios at once.
                </div>
                
                <form id="batchForm" enctype="multipart/form-data">
                    <label>Task:</label>
                    <select name="task">
                        <option value="DCF">DCF Analysis</option>
                        <option value="PE Analysis">PE Analysis</option>
                        <option value="Abnormal Finding">Abnormal Finding</option>
                        <option value="Model Consistency">Model Consistency</option>
                        <option value="Risk Mitigation">Risk Mitigation</option>
                    </select>
                    
                    <label>Model Type:</label>
                    <select name="model_type">
                        <option value="RandomForest">RandomForest</option>
                        <option value="NeuralNetwork">NeuralNetwork</option>
                        <option value="XGBoost">XGBoost</option>
                    </select>
                    
                    <label>CSV File:</label>
                    <input type="file" name="file" accept=".csv" />
                    
                    <button type="button" onclick="batchAnalyze()">Batch Analyze</button>
                </form>
                
                <div id="batchLoading" class="loading">Processing batch analysis...</div>
                
                <h3>Batch Analysis Result:</h3>
                <pre id="batchResult"></pre>
            </div>
            
            <!-- Training Tab -->
            <div id="training" class="tab-content card">
                <h2>Model Training</h2>
                <div class="info-box">
                    Upload a CSV file to train a new machine learning model.
                </div>
                
                <form id="uploadForm" enctype="multipart/form-data">
                    <label>Model Type:</label>
                    <select name="model_type">
                        <option value="RandomForest">RandomForest</option>
                        <option value="NeuralNetwork">NeuralNetwork</option>
                    </select>
                    
                    <label>Target Column:</label>
                    <input type="text" name="target_column" value="target" />
                    
                    <label>CSV File:</label>
                    <input type="file" name="file" accept=".csv" />
                    
                    <button type="button" onclick="uploadAndTrain()">Upload & Train</button>
                </form>
                
                <div id="trainingLoading" class="loading">Training model...</div>
                
                <h3>Training Result:</h3>
                <pre id="trainResult"></pre>
                
                <h3>Available Models</h3>
                <button type="button" onclick="listModels()">Refresh Model List</button>
                <pre id="modelsList"></pre>
            </div>
            
            <!-- Advanced ML Tab -->
            <div id="advanced" class="tab-content card">
                <h2>Advanced Machine Learning</h2>
                
                <div class="card">
                    <h3>Anomaly Detection</h3>
                    <div class="info-box">
                        Train a model to detect anomalies in your financial data.
                    </div>
                    
                    <form id="anomalyForm" enctype="multipart/form-data">
                        <label>CSV File:</label>
                        <input type="file" name="file" accept=".csv" />
                        
                        <label>Contamination Rate (0.0-0.5):</label>
                        <input type="number" name="contamination" value="0.1" min="0.01" max="0.5" step="0.01" />
                        
                        <button type="button" onclick="trainAnomaly()">Train Anomaly Model</button>
                    </form>
                    
                    <div id="anomalyLoading" class="loading">Training anomaly detection model...</div>
                    <pre id="anomalyResult"></pre>
                </div>
                
                <div class="card">
                    <h3>Hyperparameter Tuning</h3>
                    <div class="info-box">
                        Optimize your model parameters for best performance.
                    </div>
                    
                    <form id="tuningForm" enctype="multipart/form-data">
                        <label>Model Type:</label>
                        <select name="model_type">
                            <option value="rf">RandomForest</option>
                            <option value="nn">NeuralNetwork</option>
                            <option value="ridge">Ridge Regression</option>
                            <option value="lasso">Lasso Regression</option>
                        </select>
                        
                        <label>CSV File:</label>
                        <input type="file" name="file" accept=".csv" />
                        
                        <label>Target Column:</label>
                        <input type="text" name="target_column" value="target" />
                        
                        <button type="button" onclick="tuneHyperparameters()">Start Tuning</button>
                    </form>
                    
                    <div id="tuningLoading" class="loading">Optimizing hyperparameters (this may take a while)...</div>
                    <pre id="tuningResult"></pre>
                </div>
                
                <div class="card">
                    <h3>Feature Importance</h3>
                    <div class="info-box">
                        Analyze which features have the most impact on your model's predictions.
                    </div>
                    
                    <form id="featureForm">
                        <label>Model Name:</label>
                        <select id="modelSelector" name="model_name">
                            <option value="">Select a model</option>
                        </select>
                        
                        <label>Top N Features:</label>
                        <input type="number" name="top_n" value="10" min="1" max="50" />
                        
                        <label>Include Visualization:</label>
                        <input type="checkbox" name="include_plot" checked />
                        
                        <button type="button" onclick="getFeatureImportance()">Get Feature Importance</button>
                    </form>
                    
                    <div id="featureLoading" class="loading">Analyzing features...</div>
                    <div id="featureResult">
                        <pre id="featureData"></pre>
                        <div id="featureImage"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // Tab functionality
            function showTab(tabId) {
                // Hide all tabs
                document.querySelectorAll('.tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Show selected tab
                document.getElementById(tabId).classList.add('active');
                
                // Update active tab highlight
                document.querySelectorAll('.tab').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Find the clicked tab and add active class
                Array.from(document.querySelectorAll('.tab')).find(
                    tab => tab.textContent.toLowerCase().includes(tabId)
                ).classList.add('active');
                
                // If showing advanced tab, refresh model list for the feature importance dropdown
                if (tabId === 'advanced') {
                    refreshModelSelector();
                }
            }
            
            // Sample data templates
            function loadSample(type) {
                const input = document.getElementById('dataInput');
                
                if (type === 'dcf') {
                    input.value = JSON.stringify({
                        free_cash_flow: [100, 110, 121, 133.1, 146.41],
                        terminal_growth_rate: 0.02,
                        discount_rate: 0.1,
                        shares_outstanding: 10,
                        net_debt: 50,
                        historical_cash_flows: [80, 90, 100, 110, 121],
                        financial_statements: {
                            beta: 1.2,
                            tax_rate: 0.25,
                            interest_rate: 0.045
                        },
                        growth_rates: {
                            revenue_growth: 0.08,
                            profit_margin: 0.15,
                            projected_growth: 0.06
                        }
                    }, null, 4);
                } else if (type === 'pe') {
                    input.value = JSON.stringify({
                        price: 100,
                        earnings: 5,
                        sector_avg_pe: 15,
                        market_avg_pe: 18,
                        historical_pe: [14, 16, 15, 17, 19],
                        sector_data: {
                            avg_pe: 15,
                            avg_growth: 0.05,
                            high_pe: 25,
                            low_pe: 10
                        },
                        growth_metrics: {
                            revenue_growth: 0.08,
                            earnings_growth: 0.10,
                            projected_growth: 0.07
                        },
                        financial_health: {
                            debt_to_equity: 0.8,
                            current_ratio: 1.8,
                            roe: 0.15
                        }
                    }, null, 4);
                } else if (type === 'abnormal') {
                    input.value = JSON.stringify({
                        historical_prices: [100, 102, 105, 103, 106, 110, 108, 112, 115, 140],
                        trading_volumes: [1000, 1100, 950, 1050, 1200, 1300, 1100, 1050, 1200, 3000],
                        sector_metrics: {
                            avg_pe: 15,
                            avg_growth: 0.05
                        },
                        market_indicators: {
                            index_change: 0.02,
                            volatility: 0.1
                        },
                        financial_ratios: {
                            pe_ratio: 20,
                            pb_ratio: 3.5,
                            debt_to_equity: 0.75
                        }
                    }, null, 4);
                }
            }
            
            // Update sample data when task changes
            function updateSampleData() {
                const task = document.getElementById('analyzeForm').task.value;
                if (task === 'DCF') {
                    loadSample('dcf');
                } else if (task === 'PE Analysis') {
                    loadSample('pe');
                } else if (task === 'Abnormal Finding') {
                    loadSample('abnormal');
                }
            }
            
            // Refresh model selector
            async function refreshModelSelector() {
                try {
                    const res = await fetch('/models');
                    const data = await res.json();
                    
                    const select = document.getElementById('modelSelector');
                    // Clear existing options
                    select.innerHTML = '<option value="">Select a model</option>';
                    
                    // Add new options
                    if (data.models && data.models.length) {
                        data.models.forEach(model => {
                            const option = document.createElement('option');
                            option.value = model;
                            option.textContent = model;
                            select.appendChild(option);
                        });
                    }
                } catch (error) {
                    console.error('Error fetching models:', error);
                }
            }
            
            // Analysis submission
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
                
                // Show loading indicator
                document.getElementById('analyzeLoading').style.display = 'block';
                document.getElementById('result').innerText = '';
                
                try {
                    const res = await fetch('/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                    
                    const result = await res.json();
                    document.getElementById('result').innerText = JSON.stringify(result, null, 2);
                } catch (error) {
                    document.getElementById('result').innerText = `Error: ${error.message}`;
                } finally {
                    document.getElementById('analyzeLoading').style.display = 'none';
                }
            }
            
            // Batch analysis
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
                
                // Show loading indicator
                document.getElementById('batchLoading').style.display = 'block';
                document.getElementById('batchResult').innerText = '';
                
                try {
                    const res = await fetch('/analyze-csv', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await res.json();
                    document.getElementById('batchResult').innerText = JSON.stringify(result, null, 2);
                } catch (error) {
                    document.getElementById('batchResult').innerText = `Error: ${error.message}`;
                } finally {
                    document.getElementById('batchLoading').style.display = 'none';
                }
            }
            
            // Upload and train
            async function uploadAndTrain() {
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
                
                // Show loading indicator
                document.getElementById('trainingLoading').style.display = 'block';
                document.getElementById('trainResult').innerText = '';
                
                try {
                    const res = await fetch('/train-with-file', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await res.json();
                    document.getElementById('trainResult').innerText = JSON.stringify(result, null, 2);
                    
                    // Refresh model list after successful training
                    listModels();
                } catch (error) {
                    document.getElementById('trainResult').innerText = `Error: ${error.message}`;
                } finally {
                    document.getElementById('trainingLoading').style.display = 'none';
                }
            }
            
            // List available models
            async function listModels() {
                try {
                    const res = await fetch('/models');
                    const result = await res.json();
                    document.getElementById('modelsList').innerText = JSON.stringify(result, null, 2);
                    
                    // Also refresh model selector for feature importance
                    refreshModelSelector();
                } catch (error) {
                    document.getElementById('modelsList').innerText = `Error: ${error.message}`;
                }
            }
            
            // Train anomaly detection model
            async function trainAnomaly() {
                const form = document.getElementById('anomalyForm');
                const contamination = form.contamination.value;
                const fileInput = form.file;
                
                if (!fileInput.files.length) {
                    document.getElementById('anomalyResult').innerText = "Please select a CSV file!";
                    return;
                }
                
                const file = fileInput.files[0];
                const formData = new FormData();
                formData.append("contamination", contamination);
                formData.append("file", file);
                
                // Show loading indicator
                document.getElementById('anomalyLoading').style.display = 'block';
                document.getElementById('anomalyResult').innerText = '';
                
                try {
                    const res = await fetch('/anomaly-detection', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await res.json();
                    document.getElementById('anomalyResult').innerText = JSON.stringify(result, null, 2);
                } catch (error) {
                    document.getElementById('anomalyResult').innerText = `Error: ${error.message}`;
                } finally {
                    document.getElementById('anomalyLoading').style.display = 'none';
                }
            }
            
            // Hyperparameter tuning
            async function tuneHyperparameters() {
                const form = document.getElementById('tuningForm');
                const model_type = form.model_type.value;
                const target_column = form.target_column.value;
                const fileInput = form.file;
                
                if (!fileInput.files.length) {
                    document.getElementById('tuningResult').innerText = "Please select a CSV file!";
                    return;
                }
                
                const file = fileInput.files[0];
                const formData = new FormData();
                formData.append("model_type", model_type);
                formData.append("target_column", target_column);
                formData.append("file", file);
                
                // Show loading indicator
                document.getElementById('tuningLoading').style.display = 'block';
                document.getElementById('tuningResult').innerText = '';
                
                try {
                    const res = await fetch('/hyperparameter-tuning', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await res.json();
                    document.getElementById('tuningResult').innerText = JSON.stringify(result, null, 2);
                } catch (error) {
                    document.getElementById('tuningResult').innerText = `Error: ${error.message}`;
                } finally {
                    document.getElementById('tuningLoading').style.display = 'none';
                }
            }
            
            // Get feature importance
            async function getFeatureImportance() {
                const form = document.getElementById('featureForm');
                const model_name = form.model_name.value;
                const top_n = form.top_n.value;
                const include_plot = form.include_plot.checked;
                
                if (!model_name) {
                    document.getElementById('featureData').innerText = "Please select a model!";
                    return;
                }
                
                // Show loading indicator
                document.getElementById('featureLoading').style.display = 'block';
                document.getElementById('featureData').innerText = '';
                document.getElementById('featureImage').innerHTML = '';
                
                try {
                    const res = await fetch(`/feature-importance/${model_name}?top_n=${top_n}&include_plot=${include_plot}`);
                    const result = await res.json();
                    
                    document.getElementById('featureData').innerText = JSON.stringify(result.feature_importance, null, 2);
                    
                    // Display image if available
                    if (result.image_base64) {
                        const img = document.createElement('img');
                        img.src = `data:image/png;base64,${result.image_base64}`;
                        img.alt = 'Feature Importance';
                        img.style.maxWidth = '100%';
                        document.getElementById('featureImage').appendChild(img);
                    }
                } catch (error) {
                    document.getElementById('featureData').innerText = `Error: ${error.message}`;
                } finally {
                    document.getElementById('featureLoading').style.display = 'none';
                }
            }
            
            // Initial model list load
            listModels();
        </script>
    </body>
    </html>
    """
