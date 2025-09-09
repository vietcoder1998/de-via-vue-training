<script setup lang="ts">
import { ref, computed } from 'vue'

interface TrainingModule {
  id: number
  title: string
  description: string
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced'
  duration: string
  progress: number
  topics: string[]
  isCompleted: boolean
  isLocked: boolean
}

const currentModule = ref<TrainingModule | null>(null)
const showQuiz = ref(false)

const trainingModules = ref<TrainingModule[]>([
  {
    id: 1,
    title: 'Introduction to Fintech',
    description: 'Learn the fundamentals of financial technology and its impact on traditional banking.',
    difficulty: 'Beginner',
    duration: '2 hours',
    progress: 100,
    topics: ['Digital Banking', 'Payment Systems', 'Regulatory Framework'],
    isCompleted: true,
    isLocked: false
  },
  {
    id: 2,
    title: 'Financial Risk Assessment',
    description: 'Master techniques for evaluating and managing financial risks in digital environments.',
    difficulty: 'Beginner',
    duration: '3 hours',
    progress: 100,
    topics: ['Credit Risk', 'Market Risk', 'Operational Risk'],
    isCompleted: true,
    isLocked: false
  },
  {
    id: 3,
    title: 'Portfolio Management Basics',
    description: 'Understanding modern portfolio theory and asset allocation strategies.',
    difficulty: 'Intermediate',
    duration: '4 hours',
    progress: 60,
    topics: ['Asset Allocation', 'Diversification', 'Risk-Return Analysis'],
    isCompleted: false,
    isLocked: false
  },
  {
    id: 4,
    title: 'Algorithmic Trading',
    description: 'Introduction to automated trading systems and algorithm development.',
    difficulty: 'Intermediate',
    duration: '5 hours',
    progress: 0,
    topics: ['Trading Algorithms', 'Market Data', 'Execution Strategies'],
    isCompleted: false,
    isLocked: false
  },
  {
    id: 5,
    title: 'Blockchain & Cryptocurrency',
    description: 'Deep dive into blockchain technology and cryptocurrency markets.',
    difficulty: 'Advanced',
    duration: '6 hours',
    progress: 0,
    topics: ['Blockchain Fundamentals', 'Smart Contracts', 'DeFi'],
    isCompleted: false,
    isLocked: false
  },
  {
    id: 6,
    title: 'AI in Financial Services',
    description: 'Advanced applications of artificial intelligence in finance.',
    difficulty: 'Advanced',
    duration: '8 hours',
    progress: 0,
    topics: ['Machine Learning', 'Natural Language Processing', 'Predictive Analytics'],
    isCompleted: false,
    isLocked: true
  }
])

const currentQuiz = ref({
  question: 'What is the primary purpose of diversification in portfolio management?',
  options: [
    'To maximize returns',
    'To reduce risk without necessarily reducing expected returns',
    'To increase the number of assets',
    'To follow market trends'
  ],
  correctAnswer: 1,
  selectedAnswer: null as number | null,
  showResult: false
})

const difficultyColors = {
  'Beginner': '#10b981',
  'Intermediate': '#f59e0b',
  'Advanced': '#ef4444'
}

const startModule = (module: TrainingModule) => {
  if (module.isLocked) return
  currentModule.value = module
}

const startQuiz = () => {
  showQuiz.value = true
  currentQuiz.value.selectedAnswer = null
  currentQuiz.value.showResult = false
}

const selectAnswer = (index: number) => {
  currentQuiz.value.selectedAnswer = index
}

const submitQuiz = () => {
  currentQuiz.value.showResult = true
  if (currentQuiz.value.selectedAnswer === currentQuiz.value.correctAnswer) {
    // Correct answer - update progress
    if (currentModule.value) {
      currentModule.value.progress = Math.min(100, currentModule.value.progress + 20)
    }
  }
}

const continueTraining = () => {
  showQuiz.value = false
  if (currentModule.value && currentModule.value.progress >= 100) {
    currentModule.value.isCompleted = true
    // Unlock next module if exists
    const nextModule = trainingModules.value.find(m => m.id === currentModule.value!.id + 1)
    if (nextModule) {
      nextModule.isLocked = false
    }
  }
}

const closeModule = () => {
  currentModule.value = null
  showQuiz.value = false
}

const completedModules = computed(() => 
  trainingModules.value.filter(m => m.isCompleted).length
)

const totalProgress = computed(() => 
  Math.round(trainingModules.value.reduce((sum, m) => sum + m.progress, 0) / trainingModules.value.length)
)
</script>

<template>
  <div class="training-view">
    <div class="container">
      <!-- Header -->
      <div class="training-header">
        <h1 class="page-title">AI Fintech Training Modules</h1>
        <div class="training-stats">
          <div class="stat">
            <span class="stat-number">{{ completedModules }}</span>
            <span class="stat-label">Completed</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ totalProgress }}%</span>
            <span class="stat-label">Overall Progress</span>
          </div>
        </div>
      </div>

      <!-- Training Modules Grid -->
      <div v-if="!currentModule" class="modules-grid">
        <div 
          v-for="module in trainingModules" 
          :key="module.id"
          class="module-card"
          :class="{ 
            'completed': module.isCompleted, 
            'locked': module.isLocked,
            'in-progress': module.progress > 0 && !module.isCompleted 
          }"
          @click="startModule(module)"
        >
          <div class="module-header">
            <div class="module-status">
              <span v-if="module.isCompleted" class="status-icon completed">✓</span>
              <span v-else-if="module.isLocked" class="status-icon locked">🔒</span>
              <span v-else-if="module.progress > 0" class="status-icon in-progress">▶️</span>
              <span v-else class="status-icon available">🎯</span>
            </div>
            <div 
              class="difficulty-badge" 
              :style="{ backgroundColor: difficultyColors[module.difficulty] }"
            >
              {{ module.difficulty }}
            </div>
          </div>

          <h3 class="module-title">{{ module.title }}</h3>
          <p class="module-description">{{ module.description }}</p>
          
          <div class="module-details">
            <span class="duration">⏱️ {{ module.duration }}</span>
            <div class="topics">
              <span v-for="topic in module.topics.slice(0, 2)" :key="topic" class="topic-tag">
                {{ topic }}
              </span>
              <span v-if="module.topics.length > 2" class="topic-more">
                +{{ module.topics.length - 2 }} more
              </span>
            </div>
          </div>

          <div class="module-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: `${module.progress}%` }"
              ></div>
            </div>
            <span class="progress-text">{{ module.progress }}%</span>
          </div>
        </div>
      </div>

      <!-- Module Content -->
      <div v-if="currentModule && !showQuiz" class="module-content">
        <div class="content-header">
          <button @click="closeModule" class="back-button">← Back to Modules</button>
          <h2 class="content-title">{{ currentModule.title }}</h2>
        </div>

        <div class="content-body">
          <div class="lesson-content">
            <h3>Learning Objectives</h3>
            <ul>
              <li v-for="topic in currentModule.topics" :key="topic">
                Understanding {{ topic }}
              </li>
            </ul>

            <div class="lesson-section">
              <h4>Key Concepts</h4>
              <p>
                This module covers essential concepts in {{ currentModule.title.toLowerCase() }}. 
                You'll learn practical applications and real-world scenarios that AI agents 
                encounter in financial services.
              </p>
            </div>

            <div class="interactive-elements">
              <div class="case-study">
                <h4>📊 Case Study</h4>
                <p>
                  Analyze a real-world scenario where these concepts are applied in 
                  modern financial institutions. Consider the challenges and solutions 
                  implemented by AI systems.
                </p>
              </div>
            </div>
          </div>

          <div class="lesson-sidebar">
            <div class="progress-card">
              <h4>Module Progress</h4>
              <div class="circular-progress">
                <div class="progress-circle">
                  <span class="progress-percentage">{{ currentModule.progress }}%</span>
                </div>
              </div>
            </div>

            <div class="action-buttons">
              <button @click="startQuiz" class="quiz-button">
                Take Quiz 📝
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Quiz Section -->
      <div v-if="showQuiz" class="quiz-section">
        <div class="quiz-header">
          <button @click="showQuiz = false" class="back-button">← Back to Module</button>
          <h2 class="quiz-title">Knowledge Check</h2>
        </div>

        <div class="quiz-content">
          <div class="question-card">
            <h3 class="question-text">{{ currentQuiz.question }}</h3>
            
            <div class="options-list">
              <div 
                v-for="(option, index) in currentQuiz.options" 
                :key="index"
                class="option-item"
                :class="{ 
                  'selected': currentQuiz.selectedAnswer === index,
                  'correct': currentQuiz.showResult && index === currentQuiz.correctAnswer,
                  'incorrect': currentQuiz.showResult && currentQuiz.selectedAnswer === index && index !== currentQuiz.correctAnswer
                }"
                @click="selectAnswer(index)"
              >
                <span class="option-letter">{{ String.fromCharCode(65 + index) }}</span>
                <span class="option-text">{{ option }}</span>
              </div>
            </div>

            <div class="quiz-actions">
              <button 
                v-if="!currentQuiz.showResult"
                @click="submitQuiz" 
                :disabled="currentQuiz.selectedAnswer === null"
                class="submit-button"
              >
                Submit Answer
              </button>
              <button 
                v-else
                @click="continueTraining" 
                class="continue-button"
              >
                Continue Training
              </button>
            </div>

            <div v-if="currentQuiz.showResult" class="quiz-result">
              <div v-if="currentQuiz.selectedAnswer === currentQuiz.correctAnswer" class="result-correct">
                <span class="result-icon">🎉</span>
                <span class="result-text">Correct! Well done!</span>
              </div>
              <div v-else class="result-incorrect">
                <span class="result-icon">💡</span>
                <span class="result-text">Not quite right. The correct answer was option {{ String.fromCharCode(65 + currentQuiz.correctAnswer) }}.</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.training-view {
  min-height: 100vh;
  color: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Header */
.training-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0;
}

.training-stats {
  display: flex;
  gap: 2rem;
}

.stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #fbbf24;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Modules Grid */
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.module-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
}

.module-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.module-card.locked {
  opacity: 0.6;
  cursor: not-allowed;
}

.module-card.completed {
  border: 2px solid #10b981;
}

.module-card.in-progress {
  border: 2px solid #f59e0b;
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.status-icon {
  font-size: 1.5rem;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #f8f9fa;
}

.status-icon.completed {
  background: #10b981;
  color: white;
}

.status-icon.in-progress {
  background: #f59e0b;
  color: white;
}

.difficulty-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  color: white;
  font-size: 0.8rem;
  font-weight: 600;
}

.module-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.module-description {
  color: #666;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.module-details {
  margin-bottom: 1rem;
}

.duration {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  display: block;
}

.topics {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.topic-tag {
  background: #e5e7eb;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  color: #555;
}

.topic-more {
  color: #666;
  font-size: 0.8rem;
  font-style: italic;
}

.module-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-bar {
  flex: 1;
  height: 0.5rem;
  background: #e5e7eb;
  border-radius: 0.25rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(45deg, #667eea, #764ba2);
  transition: width 0.3s ease;
}

.progress-text {
  font-weight: 600;
  color: #667eea;
}

/* Module Content */
.module-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 2rem;
  color: #2c3e50;
}

.content-header {
  margin-bottom: 2rem;
}

.back-button {
  background: #6b7280;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  margin-bottom: 1rem;
  transition: background 0.3s ease;
}

.back-button:hover {
  background: #4b5563;
}

.content-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.content-body {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

.lesson-content h3, .lesson-content h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.lesson-content ul {
  margin-left: 1.5rem;
  margin-bottom: 2rem;
}

.lesson-content li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.lesson-section {
  margin-bottom: 2rem;
}

.case-study {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border-left: 4px solid #667eea;
}

.lesson-sidebar {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.progress-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.5rem;
  text-align: center;
}

.circular-progress {
  margin: 1rem 0;
}

.progress-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  position: relative;
}

.progress-percentage {
  font-size: 1.2rem;
  font-weight: 700;
  color: #667eea;
}

.quiz-button {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  transition: transform 0.3s ease;
}

.quiz-button:hover {
  transform: translateY(-2px);
}

/* Quiz Section */
.quiz-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 2rem;
  color: #2c3e50;
}

.quiz-header {
  margin-bottom: 2rem;
}

.quiz-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 1rem 0 0 0;
}

.question-card {
  max-width: 800px;
  margin: 0 auto;
}

.question-text {
  font-size: 1.3rem;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.options-list {
  margin-bottom: 2rem;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-item:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.option-item.selected {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.option-item.correct {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.option-item.incorrect {
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.option-letter {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.option-text {
  flex: 1;
  line-height: 1.5;
}

.quiz-actions {
  text-align: center;
  margin-bottom: 2rem;
}

.submit-button, .continue-button {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-button:hover:not(:disabled), .continue-button:hover {
  transform: translateY(-2px);
}

.quiz-result {
  text-align: center;
  padding: 1rem;
  border-radius: 0.5rem;
}

.result-correct {
  color: #10b981;
}

.result-incorrect {
  color: #ef4444;
}

.result-icon {
  font-size: 2rem;
  margin-right: 0.5rem;
}

.result-text {
  font-weight: 600;
}

/* Responsive Design */
@media (max-width: 768px) {
  .training-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .training-stats {
    justify-content: center;
  }
  
  .content-body {
    grid-template-columns: 1fr;
  }
  
  .modules-grid {
    grid-template-columns: 1fr;
  }
}
</style>