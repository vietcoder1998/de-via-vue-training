<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface SimulationScenario {
  id: number
  title: string
  description: string
  difficulty: 'Easy' | 'Medium' | 'Hard'
  category: string
  estimatedTime: string
  isActive: boolean
}

interface MarketData {
  symbol: string
  price: number
  change: number
  changePercent: number
}

interface Transaction {
  id: number
  type: 'buy' | 'sell'
  symbol: string
  quantity: number
  price: number
  timestamp: Date
}

const currentScenario = ref<SimulationScenario | null>(null)
const isSimulationRunning = ref(false)
const simulationResults = ref<any>(null)

const scenarios = ref<SimulationScenario[]>([
  {
    id: 1,
    title: 'Market Volatility Response',
    description: 'Navigate through high market volatility and make optimal trading decisions.',
    difficulty: 'Medium',
    category: 'Trading',
    estimatedTime: '15 minutes',
    isActive: true
  },
  {
    id: 2,
    title: 'Risk Management Crisis',
    description: 'Handle a financial crisis scenario with proper risk management protocols.',
    difficulty: 'Hard',
    category: 'Risk Management',
    estimatedTime: '20 minutes',
    isActive: true
  },
  {
    id: 3,
    title: 'Portfolio Rebalancing',
    description: 'Optimize portfolio allocation based on changing market conditions.',
    difficulty: 'Easy',
    category: 'Portfolio Management',
    estimatedTime: '10 minutes',
    isActive: true
  },
  {
    id: 4,
    title: 'Algorithmic Trading Challenge',
    description: 'Develop and test trading algorithms in real-time market conditions.',
    difficulty: 'Hard',
    category: 'Algorithmic Trading',
    estimatedTime: '25 minutes',
    isActive: false
  },
  {
    id: 5,
    title: 'Customer Service AI',
    description: 'Handle customer inquiries and financial advisory requests.',
    difficulty: 'Medium',
    category: 'Customer Service',
    estimatedTime: '12 minutes',
    isActive: true
  }
])

const marketData = ref<MarketData[]>([
  { symbol: 'AAPL', price: 175.84, change: 2.34, changePercent: 1.35 },
  { symbol: 'GOOGL', price: 2745.25, change: -15.67, changePercent: -0.57 },
  { symbol: 'MSFT', price: 338.92, change: 5.21, changePercent: 1.58 },
  { symbol: 'TSLA', price: 242.18, change: -8.43, changePercent: -3.36 },
  { symbol: 'AMZN', price: 143.29, change: 1.87, changePercent: 1.32 }
])

const portfolio = ref({
  cash: 50000,
  totalValue: 75000,
  positions: [
    { symbol: 'AAPL', shares: 50, currentPrice: 175.84 },
    { symbol: 'GOOGL', shares: 5, currentPrice: 2745.25 },
    { symbol: 'MSFT', shares: 25, currentPrice: 338.92 }
  ]
})

const recentTransactions = ref<Transaction[]>([])

const simulationTimer = ref(0)
const timerInterval = ref<number | null>(null)

const difficultyColors = {
  'Easy': '#10b981',
  'Medium': '#f59e0b',
  'Hard': '#ef4444'
}

const startScenario = (scenario: SimulationScenario) => {
  if (!scenario.isActive) return
  
  currentScenario.value = scenario
  isSimulationRunning.value = true
  simulationTimer.value = 0
  simulationResults.value = null
  
  // Start timer
  timerInterval.value = setInterval(() => {
    simulationTimer.value++
  }, 1000)
  
  // Simulate market data updates
  startMarketDataSimulation()
}

const endSimulation = () => {
  isSimulationRunning.value = false
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
  
  // Generate simulation results
  generateResults()
}

const startMarketDataSimulation = () => {
  // Update market data every 3 seconds during simulation
  const marketInterval = setInterval(() => {
    if (!isSimulationRunning.value) {
      clearInterval(marketInterval)
      return
    }
    
    marketData.value.forEach(stock => {
      // Simulate price changes
      const changePercent = (Math.random() - 0.5) * 6 // ±3% change
      const change = stock.price * (changePercent / 100)
      stock.price = Math.max(0.01, stock.price + change)
      stock.change = change
      stock.changePercent = changePercent
    })
  }, 3000)
}

const buyStock = (symbol: string, quantity: number) => {
  const stock = marketData.value.find(s => s.symbol === symbol)
  if (!stock || portfolio.value.cash < stock.price * quantity) return
  
  const transaction: Transaction = {
    id: Date.now(),
    type: 'buy',
    symbol,
    quantity,
    price: stock.price,
    timestamp: new Date()
  }
  
  recentTransactions.value.unshift(transaction)
  portfolio.value.cash -= stock.price * quantity
  
  // Update portfolio positions
  const existingPosition = portfolio.value.positions.find(p => p.symbol === symbol)
  if (existingPosition) {
    existingPosition.shares += quantity
  } else {
    portfolio.value.positions.push({
      symbol,
      shares: quantity,
      currentPrice: stock.price
    })
  }
  
  updatePortfolioValue()
}

const sellStock = (symbol: string, quantity: number) => {
  const stock = marketData.value.find(s => s.symbol === symbol)
  const position = portfolio.value.positions.find(p => p.symbol === symbol)
  
  if (!stock || !position || position.shares < quantity) return
  
  const transaction: Transaction = {
    id: Date.now(),
    type: 'sell',
    symbol,
    quantity,
    price: stock.price,
    timestamp: new Date()
  }
  
  recentTransactions.value.unshift(transaction)
  portfolio.value.cash += stock.price * quantity
  position.shares -= quantity
  
  // Remove position if shares reach 0
  if (position.shares === 0) {
    const index = portfolio.value.positions.indexOf(position)
    portfolio.value.positions.splice(index, 1)
  }
  
  updatePortfolioValue()
}

const updatePortfolioValue = () => {
  const positionsValue = portfolio.value.positions.reduce((total, position) => {
    const currentStock = marketData.value.find(s => s.symbol === position.symbol)
    return total + (position.shares * (currentStock?.price || 0))
  }, 0)
  
  portfolio.value.totalValue = portfolio.value.cash + positionsValue
}

const generateResults = () => {
  const score = Math.floor(Math.random() * 40) + 60 // 60-100 score
  const profit = portfolio.value.totalValue - 75000 // Initial value was 75000
  
  simulationResults.value = {
    score,
    profit,
    timeElapsed: simulationTimer.value,
    decisions: recentTransactions.value.length,
    accuracy: Math.floor(Math.random() * 30) + 70 // 70-100%
  }
}

const resetSimulation = () => {
  currentScenario.value = null
  isSimulationRunning.value = false
  simulationResults.value = null
  simulationTimer.value = 0
  recentTransactions.value = []
  
  // Reset portfolio
  portfolio.value = {
    cash: 50000,
    totalValue: 75000,
    positions: [
      { symbol: 'AAPL', shares: 50, currentPrice: 175.84 },
      { symbol: 'GOOGL', shares: 5, currentPrice: 2745.25 },
      { symbol: 'MSFT', shares: 25, currentPrice: 338.92 }
    ]
  }
  
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

const activeScenarios = computed(() => scenarios.value.filter(s => s.isActive))
const lockedScenarios = computed(() => scenarios.value.filter(s => !s.isActive))

// Update market data and portfolio values periodically
onMounted(() => {
  updatePortfolioValue()
})
</script>

<template>
  <div class="simulation-view">
    <div class="container">
      <!-- Header -->
      <div class="simulation-header">
        <h1 class="page-title">AI Agent Simulation</h1>
        <p class="page-subtitle">Practice real-world fintech scenarios in a risk-free environment</p>
      </div>

      <!-- Scenario Selection -->
      <div v-if="!currentScenario" class="scenario-selection">
        <h2 class="section-title">Choose Your Simulation</h2>
        
        <div class="scenarios-grid">
          <div 
            v-for="scenario in activeScenarios" 
            :key="scenario.id"
            class="scenario-card"
            @click="startScenario(scenario)"
          >
            <div class="scenario-header">
              <div 
                class="difficulty-badge" 
                :style="{ backgroundColor: difficultyColors[scenario.difficulty] }"
              >
                {{ scenario.difficulty }}
              </div>
              <span class="category-tag">{{ scenario.category }}</span>
            </div>
            <h3 class="scenario-title">{{ scenario.title }}</h3>
            <p class="scenario-description">{{ scenario.description }}</p>
            <div class="scenario-footer">
              <span class="time-estimate">⏱️ {{ scenario.estimatedTime }}</span>
              <button class="start-button">Start Simulation</button>
            </div>
          </div>
        </div>

        <!-- Locked Scenarios -->
        <div v-if="lockedScenarios.length > 0" class="locked-scenarios">
          <h3 class="locked-title">🔒 Coming Soon</h3>
          <div class="locked-grid">
            <div 
              v-for="scenario in lockedScenarios" 
              :key="scenario.id"
              class="scenario-card locked"
            >
              <div class="scenario-header">
                <div 
                  class="difficulty-badge" 
                  :style="{ backgroundColor: difficultyColors[scenario.difficulty] }"
                >
                  {{ scenario.difficulty }}
                </div>
                <span class="category-tag">{{ scenario.category }}</span>
              </div>
              <h3 class="scenario-title">{{ scenario.title }}</h3>
              <p class="scenario-description">{{ scenario.description }}</p>
              <div class="scenario-footer">
                <span class="time-estimate">⏱️ {{ scenario.estimatedTime }}</span>
                <span class="locked-badge">Complete prerequisite modules</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Simulation -->
      <div v-if="currentScenario && isSimulationRunning && !simulationResults" class="active-simulation">
        <div class="simulation-controls">
          <div class="scenario-info">
            <h2 class="current-scenario">{{ currentScenario.title }}</h2>
            <div class="timer">Time: {{ formatTime(simulationTimer) }}</div>
          </div>
          <button @click="endSimulation" class="end-button">End Simulation</button>
        </div>

        <div class="simulation-dashboard">
          <!-- Market Data -->
          <div class="market-panel">
            <h3 class="panel-title">📈 Market Data</h3>
            <div class="market-list">
              <div 
                v-for="stock in marketData" 
                :key="stock.symbol"
                class="market-item"
                :class="{ 'positive': stock.change >= 0, 'negative': stock.change < 0 }"
              >
                <div class="stock-symbol">{{ stock.symbol }}</div>
                <div class="stock-price">{{ formatCurrency(stock.price) }}</div>
                <div class="stock-change">
                  {{ stock.change >= 0 ? '+' : '' }}{{ stock.change.toFixed(2) }}
                  ({{ stock.changePercent.toFixed(2) }}%)
                </div>
                <div class="stock-actions">
                  <button @click="buyStock(stock.symbol, 10)" class="buy-btn">Buy 10</button>
                  <button @click="sellStock(stock.symbol, 10)" class="sell-btn">Sell 10</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Portfolio -->
          <div class="portfolio-panel">
            <h3 class="panel-title">💼 Portfolio</h3>
            <div class="portfolio-summary">
              <div class="portfolio-stat">
                <span class="stat-label">Total Value</span>
                <span class="stat-value">{{ formatCurrency(portfolio.totalValue) }}</span>
              </div>
              <div class="portfolio-stat">
                <span class="stat-label">Cash</span>
                <span class="stat-value">{{ formatCurrency(portfolio.cash) }}</span>
              </div>
            </div>
            
            <div class="positions-list">
              <div 
                v-for="position in portfolio.positions" 
                :key="position.symbol"
                class="position-item"
              >
                <div class="position-symbol">{{ position.symbol }}</div>
                <div class="position-details">
                  <div>{{ position.shares }} shares</div>
                  <div>{{ formatCurrency(position.shares * position.currentPrice) }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Transactions -->
          <div class="transactions-panel">
            <h3 class="panel-title">📊 Recent Transactions</h3>
            <div class="transactions-list">
              <div 
                v-for="transaction in recentTransactions.slice(0, 5)" 
                :key="transaction.id"
                class="transaction-item"
                :class="transaction.type"
              >
                <div class="transaction-type">
                  {{ transaction.type.toUpperCase() }}
                </div>
                <div class="transaction-details">
                  <div>{{ transaction.symbol }} × {{ transaction.quantity }}</div>
                  <div>{{ formatCurrency(transaction.price) }}</div>
                </div>
                <div class="transaction-time">
                  {{ transaction.timestamp.toLocaleTimeString() }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Simulation Results -->
      <div v-if="simulationResults" class="simulation-results">
        <div class="results-header">
          <h2 class="results-title">🎯 Simulation Complete!</h2>
          <div class="overall-score">
            <span class="score-label">Overall Score</span>
            <span class="score-value">{{ simulationResults.score }}/100</span>
          </div>
        </div>

        <div class="results-grid">
          <div class="result-card">
            <div class="result-icon">💰</div>
            <div class="result-label">P&L</div>
            <div class="result-value" :class="{ 'positive': simulationResults.profit >= 0, 'negative': simulationResults.profit < 0 }">
              {{ formatCurrency(simulationResults.profit) }}
            </div>
          </div>

          <div class="result-card">
            <div class="result-icon">⏱️</div>
            <div class="result-label">Time</div>
            <div class="result-value">{{ formatTime(simulationResults.timeElapsed) }}</div>
          </div>

          <div class="result-card">
            <div class="result-icon">🎯</div>
            <div class="result-label">Accuracy</div>
            <div class="result-value">{{ simulationResults.accuracy }}%</div>
          </div>

          <div class="result-card">
            <div class="result-icon">📈</div>
            <div class="result-label">Decisions</div>
            <div class="result-value">{{ simulationResults.decisions }}</div>
          </div>
        </div>

        <div class="results-actions">
          <button @click="resetSimulation" class="retry-button">Try Another Scenario</button>
          <button @click="startScenario(currentScenario!)" class="restart-button">Restart This Scenario</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.simulation-view {
  min-height: 100vh;
  color: white;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Header */
.simulation-header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
}

.page-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
}

.page-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
}

/* Scenario Selection */
.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.scenario-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
}

.scenario-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.scenario-card.locked {
  opacity: 0.6;
  cursor: not-allowed;
}

.scenario-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.difficulty-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  color: white;
  font-size: 0.8rem;
  font-weight: 600;
}

.category-tag {
  background: #e5e7eb;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  color: #555;
}

.scenario-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.scenario-description {
  color: #666;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.scenario-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.time-estimate {
  color: #666;
  font-size: 0.9rem;
}

.start-button {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.start-button:hover {
  transform: translateY(-2px);
}

.locked-badge {
  background: #fbbf24;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
}

/* Locked Scenarios */
.locked-scenarios {
  margin-top: 4rem;
}

.locked-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  text-align: center;
  color: #fbbf24;
}

.locked-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

/* Active Simulation */
.simulation-controls {
  background: rgba(255, 255, 255, 0.95);
  padding: 1.5rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #2c3e50;
}

.scenario-info {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.current-scenario {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.timer {
  font-size: 1.2rem;
  font-weight: 700;
  color: #667eea;
}

.end-button {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.end-button:hover {
  background: #dc2626;
}

/* Simulation Dashboard */
.simulation-dashboard {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 2rem;
}

.market-panel, .portfolio-panel, .transactions-panel {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 1.5rem;
  color: #2c3e50;
}

.panel-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Market Data */
.market-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.market-item {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 0.5rem;
  background: #f8f9fa;
}

.market-item.positive {
  border-left: 4px solid #10b981;
}

.market-item.negative {
  border-left: 4px solid #ef4444;
}

.stock-symbol {
  font-weight: 600;
}

.stock-change.positive {
  color: #10b981;
}

.stock-change.negative {
  color: #ef4444;
}

.stock-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.buy-btn, .sell-btn {
  flex: 1;
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.buy-btn {
  background: #10b981;
  color: white;
}

.buy-btn:hover {
  background: #059669;
}

.sell-btn {
  background: #ef4444;
  color: white;
}

.sell-btn:hover {
  background: #dc2626;
}

/* Portfolio */
.portfolio-summary {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
}

.portfolio-stat {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-weight: 700;
  color: #2c3e50;
}

.positions-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.position-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
}

.position-symbol {
  font-weight: 600;
}

.position-details {
  text-align: right;
  font-size: 0.9rem;
}

/* Transactions */
.transactions-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.transaction-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  background: #f8f9fa;
  align-items: center;
}

.transaction-item.buy {
  border-left: 4px solid #10b981;
}

.transaction-item.sell {
  border-left: 4px solid #ef4444;
}

.transaction-type {
  font-weight: 600;
  font-size: 0.8rem;
}

.transaction-details {
  font-size: 0.9rem;
}

.transaction-time {
  font-size: 0.8rem;
  color: #666;
}

/* Simulation Results */
.simulation-results {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 3rem;
  text-align: center;
  color: #2c3e50;
}

.results-header {
  margin-bottom: 3rem;
}

.results-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.overall-score {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.score-label {
  font-size: 1.2rem;
  color: #666;
}

.score-value {
  font-size: 3rem;
  font-weight: 800;
  color: #667eea;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.result-card {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 1rem;
}

.result-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.result-label {
  font-size: 1rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.result-value {
  font-size: 1.5rem;
  font-weight: 700;
}

.result-value.positive {
  color: #10b981;
}

.result-value.negative {
  color: #ef4444;
}

.results-actions {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.retry-button, .restart-button {
  padding: 1rem 2rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.retry-button {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
}

.restart-button {
  background: #6b7280;
  color: white;
}

.retry-button:hover, .restart-button:hover {
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .simulation-dashboard {
    grid-template-columns: 1fr;
  }
  
  .simulation-controls {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .scenario-info {
    flex-direction: column;
    gap: 0.5rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .scenarios-grid, .locked-grid {
    grid-template-columns: 1fr;
  }
  
  .results-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .portfolio-summary {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>