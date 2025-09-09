<script setup lang="ts">
import { ref, computed } from 'vue'

interface ProgressData {
  category: string
  completed: number
  total: number
  accuracy: number
}

interface Achievement {
  id: number
  title: string
  description: string
  icon: string
  dateEarned: Date | null
  isUnlocked: boolean
}

interface LearningPath {
  id: number
  name: string
  modules: string[]
  completed: number
  total: number
}

const selectedTimeframe = ref('week')
const timeframes = ['week', 'month', 'quarter', 'year']

const overallStats = ref({
  totalModules: 12,
  completedModules: 3,
  totalHours: 145,
  averageScore: 87,
  streak: 5,
  rank: 342
})

const progressData = ref<ProgressData[]>([
  { category: 'Trading', completed: 3, total: 4, accuracy: 92 },
  { category: 'Risk Management', completed: 2, total: 3, accuracy: 88 },
  { category: 'Portfolio Management', completed: 1, total: 2, accuracy: 85 },
  { category: 'Algorithmic Trading', completed: 0, total: 2, accuracy: 0 },
  { category: 'Blockchain & Crypto', completed: 0, total: 1, accuracy: 0 }
])

const weeklyProgress = ref([
  { day: 'Mon', hours: 2.5, score: 85 },
  { day: 'Tue', hours: 1.8, score: 90 },
  { day: 'Wed', hours: 3.2, score: 88 },
  { day: 'Thu', hours: 0, score: 0 },
  { day: 'Fri', hours: 2.1, score: 92 },
  { day: 'Sat', hours: 1.5, score: 87 },
  { day: 'Sun', hours: 0.8, score: 89 }
])

const achievements = ref<Achievement[]>([
  {
    id: 1,
    title: 'First Steps',
    description: 'Complete your first training module',
    icon: '🎯',
    dateEarned: new Date('2024-01-15'),
    isUnlocked: true
  },
  {
    id: 2,
    title: 'Trading Novice',
    description: 'Complete all beginner trading modules',
    icon: '📈',
    dateEarned: new Date('2024-01-20'),
    isUnlocked: true
  },
  {
    id: 3,
    title: 'Risk Expert',
    description: 'Master risk management fundamentals',
    icon: '🛡️',
    dateEarned: new Date('2024-01-25'),
    isUnlocked: true
  },
  {
    id: 4,
    title: 'Simulation Master',
    description: 'Score 90+ in 5 consecutive simulations',
    icon: '🏆',
    dateEarned: null,
    isUnlocked: false
  },
  {
    id: 5,
    title: 'Portfolio Pro',
    description: 'Complete all portfolio management modules',
    icon: '💼',
    dateEarned: null,
    isUnlocked: false
  },
  {
    id: 6,
    title: 'Algorithm Architect',
    description: 'Build your first trading algorithm',
    icon: '🤖',
    dateEarned: null,
    isUnlocked: false
  },
  {
    id: 7,
    title: 'Blockchain Pioneer',
    description: 'Complete all blockchain modules',
    icon: '⛓️',
    dateEarned: null,
    isUnlocked: false
  },
  {
    id: 8,
    title: 'Learning Streak',
    description: 'Maintain a 30-day learning streak',
    icon: '🔥',
    dateEarned: null,
    isUnlocked: false
  }
])

const learningPaths = ref<LearningPath[]>([
  {
    id: 1,
    name: 'Fintech Fundamentals',
    modules: ['Introduction to Fintech', 'Financial Risk Assessment', 'Basic Trading'],
    completed: 3,
    total: 3
  },
  {
    id: 2,
    name: 'Advanced Trading',
    modules: ['Portfolio Management', 'Algorithmic Trading', 'Market Analysis'],
    completed: 1,
    total: 3
  },
  {
    id: 3,
    name: 'Emerging Technologies',
    modules: ['Blockchain & Cryptocurrency', 'AI in Finance', 'RegTech'],
    completed: 0,
    total: 3
  }
])

const skillLevels = ref([
  { skill: 'Financial Analysis', level: 75, maxLevel: 100 },
  { skill: 'Risk Assessment', level: 82, maxLevel: 100 },
  { skill: 'Trading Strategies', level: 68, maxLevel: 100 },
  { skill: 'Portfolio Optimization', level: 45, maxLevel: 100 },
  { skill: 'Algorithmic Trading', level: 20, maxLevel: 100 },
  { skill: 'Blockchain Knowledge', level: 10, maxLevel: 100 }
])

const recentActivity = ref([
  { date: '2024-01-25', activity: 'Completed "Risk Management Crisis" simulation', score: 92 },
  { date: '2024-01-24', activity: 'Finished "Financial Risk Assessment" module', score: 88 },
  { date: '2024-01-23', activity: 'Started "Portfolio Management Basics"', score: null },
  { date: '2024-01-22', activity: 'Achieved "Risk Expert" badge', score: null },
  { date: '2024-01-21', activity: 'Completed practice quiz with 95% accuracy', score: 95 }
])

const overallProgress = computed(() => {
  return Math.round((overallStats.value.completedModules / overallStats.value.totalModules) * 100)
})

const unlockedAchievements = computed(() => 
  achievements.value.filter(a => a.isUnlocked && a.dateEarned)
)

const lockedAchievements = computed(() => 
  achievements.value.filter(a => !a.isUnlocked || !a.dateEarned)
)

const averageWeeklyHours = computed(() => {
  const totalHours = weeklyProgress.value.reduce((sum, day) => sum + day.hours, 0)
  return Math.round((totalHours / 7) * 10) / 10
})

const averageWeeklyScore = computed(() => {
  const scoresWithData = weeklyProgress.value.filter(day => day.score > 0)
  if (scoresWithData.length === 0) return 0
  const totalScore = scoresWithData.reduce((sum, day) => sum + day.score, 0)
  return Math.round(totalScore / scoresWithData.length)
})

const getSkillColor = (level: number) => {
  if (level >= 80) return '#10b981'
  if (level >= 60) return '#f59e0b'
  if (level >= 40) return '#3b82f6'
  return '#6b7280'
}

const getProgressColor = (percentage: number) => {
  if (percentage >= 80) return '#10b981'
  if (percentage >= 60) return '#f59e0b'
  return '#3b82f6'
}

const formatDate = (date: Date) => {
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  })
}

const maxHours = computed(() => Math.max(...weeklyProgress.value.map(d => d.hours)))
const maxScore = computed(() => Math.max(...weeklyProgress.value.map(d => d.score)))
</script>

<template>
  <div class="progress-view">
    <div class="container">
      <!-- Header -->
      <div class="progress-header">
        <h1 class="page-title">Learning Progress</h1>
        <p class="page-subtitle">Track your journey to becoming a fintech AI expert</p>
      </div>

      <!-- Overall Stats -->
      <div class="stats-overview">
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-content">
            <div class="stat-number">{{ overallStats.completedModules }}/{{ overallStats.totalModules }}</div>
            <div class="stat-label">Modules Completed</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">⏱️</div>
          <div class="stat-content">
            <div class="stat-number">{{ overallStats.totalHours }}h</div>
            <div class="stat-label">Time Invested</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">🎯</div>
          <div class="stat-content">
            <div class="stat-number">{{ overallStats.averageScore }}%</div>
            <div class="stat-label">Average Score</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">🔥</div>
          <div class="stat-content">
            <div class="stat-number">{{ overallStats.streak }}</div>
            <div class="stat-label">Day Streak</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">🏅</div>
          <div class="stat-content">
            <div class="stat-number">#{{ overallStats.rank }}</div>
            <div class="stat-label">Global Rank</div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="content-grid">
        <!-- Progress by Category -->
        <div class="panel category-progress">
          <h2 class="panel-title">Progress by Category</h2>
          <div class="category-list">
            <div v-for="category in progressData" :key="category.category" class="category-item">
              <div class="category-header">
                <h3 class="category-name">{{ category.category }}</h3>
                <span class="category-ratio">{{ category.completed }}/{{ category.total }}</span>
              </div>
              <div class="category-progress-bar">
                <div 
                  class="category-progress-fill" 
                  :style="{ 
                    width: `${(category.completed / category.total) * 100}%`,
                    backgroundColor: getProgressColor((category.completed / category.total) * 100)
                  }"
                ></div>
              </div>
              <div class="category-stats">
                <span class="accuracy">Accuracy: {{ category.accuracy }}%</span>
                <span class="completion">{{ Math.round((category.completed / category.total) * 100) }}% Complete</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Weekly Activity -->
        <div class="panel weekly-activity">
          <h2 class="panel-title">Weekly Activity</h2>
          <div class="weekly-stats">
            <div class="weekly-stat">
              <span class="weekly-stat-value">{{ averageWeeklyHours }}h</span>
              <span class="weekly-stat-label">Avg Daily</span>
            </div>
            <div class="weekly-stat">
              <span class="weekly-stat-value">{{ averageWeeklyScore }}%</span>
              <span class="weekly-stat-label">Avg Score</span>
            </div>
          </div>
          
          <div class="activity-chart">
            <div class="chart-container">
              <div class="chart-bars">
                <div 
                  v-for="day in weeklyProgress" 
                  :key="day.day"
                  class="chart-bar"
                >
                  <div 
                    class="hours-bar"
                    :style="{ 
                      height: maxHours > 0 ? `${(day.hours / maxHours) * 100}%` : '0%',
                      backgroundColor: day.hours > 0 ? '#667eea' : '#e5e7eb'
                    }"
                    :title="`${day.hours} hours`"
                  ></div>
                  <div class="day-label">{{ day.day }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Skill Levels -->
        <div class="panel skill-levels">
          <h2 class="panel-title">Skill Development</h2>
          <div class="skills-list">
            <div v-for="skill in skillLevels" :key="skill.skill" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ skill.skill }}</span>
                <span class="skill-percentage">{{ skill.level }}%</span>
              </div>
              <div class="skill-progress-bar">
                <div 
                  class="skill-progress-fill"
                  :style="{ 
                    width: `${skill.level}%`,
                    backgroundColor: getSkillColor(skill.level)
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Learning Paths -->
        <div class="panel learning-paths">
          <h2 class="panel-title">Learning Paths</h2>
          <div class="paths-list">
            <div v-for="path in learningPaths" :key="path.id" class="path-item">
              <div class="path-header">
                <h3 class="path-name">{{ path.name }}</h3>
                <div class="path-progress">
                  <span class="path-ratio">{{ path.completed }}/{{ path.total }}</span>
                  <div class="path-progress-bar">
                    <div 
                      class="path-progress-fill"
                      :style="{ 
                        width: `${(path.completed / path.total) * 100}%`,
                        backgroundColor: getProgressColor((path.completed / path.total) * 100)
                      }"
                    ></div>
                  </div>
                </div>
              </div>
              <div class="path-modules">
                <div 
                  v-for="(module, index) in path.modules" 
                  :key="module"
                  class="module-chip"
                  :class="{ 'completed': index < path.completed }"
                >
                  <span v-if="index < path.completed" class="module-check">✓</span>
                  {{ module }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Achievements -->
        <div class="panel achievements">
          <h2 class="panel-title">Achievements</h2>
          
          <!-- Unlocked Achievements -->
          <div class="achievements-section">
            <h3 class="achievements-subtitle">Earned ({{ unlockedAchievements.length }})</h3>
            <div class="achievements-grid">
              <div 
                v-for="achievement in unlockedAchievements" 
                :key="achievement.id"
                class="achievement-item earned"
              >
                <div class="achievement-icon">{{ achievement.icon }}</div>
                <div class="achievement-content">
                  <h4 class="achievement-title">{{ achievement.title }}</h4>
                  <p class="achievement-description">{{ achievement.description }}</p>
                  <span class="achievement-date">{{ formatDate(achievement.dateEarned!) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Locked Achievements -->
          <div class="achievements-section">
            <h3 class="achievements-subtitle">Available ({{ lockedAchievements.length }})</h3>
            <div class="achievements-grid">
              <div 
                v-for="achievement in lockedAchievements" 
                :key="achievement.id"
                class="achievement-item locked"
              >
                <div class="achievement-icon">{{ achievement.icon }}</div>
                <div class="achievement-content">
                  <h4 class="achievement-title">{{ achievement.title }}</h4>
                  <p class="achievement-description">{{ achievement.description }}</p>
                  <span class="achievement-status">Not earned yet</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="panel recent-activity">
          <h2 class="panel-title">Recent Activity</h2>
          <div class="activity-list">
            <div v-for="activity in recentActivity" :key="activity.date + activity.activity" class="activity-item">
              <div class="activity-date">{{ formatDate(new Date(activity.date)) }}</div>
              <div class="activity-content">
                <div class="activity-text">{{ activity.activity }}</div>
                <div v-if="activity.score" class="activity-score">Score: {{ activity.score }}%</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.progress-view {
  min-height: 100vh;
  color: white;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Header */
.progress-header {
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

/* Stats Overview */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #2c3e50;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 3rem;
  width: 4rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, #667eea, #764ba2);
  border-radius: 50%;
  flex-shrink: 0;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: #2c3e50;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.panel {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 2rem;
  color: #2c3e50;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.panel-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

/* Category Progress */
.category-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.category-item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.category-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

.category-ratio {
  font-weight: 600;
  color: #666;
}

.category-progress-bar {
  width: 100%;
  height: 0.75rem;
  background: #e5e7eb;
  border-radius: 0.375rem;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.category-progress-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 0.375rem;
}

.category-stats {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
}

/* Weekly Activity */
.weekly-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
}

.weekly-stat {
  text-align: center;
}

.weekly-stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
}

.weekly-stat-label {
  font-size: 0.9rem;
  color: #666;
}

.activity-chart {
  height: 200px;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
}

.chart-container {
  height: 100%;
  display: flex;
  align-items: end;
}

.chart-bars {
  display: flex;
  justify-content: space-between;
  align-items: end;
  width: 100%;
  height: 100%;
  gap: 0.5rem;
}

.chart-bar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}

.hours-bar {
  width: 100%;
  border-radius: 0.25rem 0.25rem 0 0;
  transition: all 0.3s ease;
  cursor: pointer;
}

.day-label {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #666;
  font-weight: 600;
}

/* Skill Levels */
.skills-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.skill-item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.skill-name {
  font-weight: 600;
}

.skill-percentage {
  font-weight: 700;
  color: #667eea;
}

.skill-progress-bar {
  width: 100%;
  height: 0.5rem;
  background: #e5e7eb;
  border-radius: 0.25rem;
  overflow: hidden;
}

.skill-progress-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 0.25rem;
}

/* Learning Paths */
.paths-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.path-item {
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
}

.path-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.path-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

.path-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.path-ratio {
  font-weight: 600;
  color: #666;
  min-width: 3rem;
}

.path-progress-bar {
  width: 100px;
  height: 0.5rem;
  background: #e5e7eb;
  border-radius: 0.25rem;
  overflow: hidden;
}

.path-progress-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 0.25rem;
}

.path-modules {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.module-chip {
  padding: 0.25rem 0.75rem;
  background: #e5e7eb;
  border-radius: 1rem;
  font-size: 0.8rem;
  color: #555;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.module-chip.completed {
  background: #d1fae5;
  color: #065f46;
}

.module-check {
  font-weight: 600;
}

/* Achievements */
.achievements-section {
  margin-bottom: 2rem;
}

.achievements-section:last-child {
  margin-bottom: 0;
}

.achievements-subtitle {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #666;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.achievement-item {
  display: flex;
  align-items: start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.achievement-item.earned {
  background: #d1fae5;
  border: 1px solid #10b981;
}

.achievement-item.locked {
  background: #f3f4f6;
  opacity: 0.7;
}

.achievement-icon {
  font-size: 2rem;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: white;
  flex-shrink: 0;
}

.achievement-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
}

.achievement-description {
  font-size: 0.9rem;
  color: #666;
  margin: 0 0 0.25rem 0;
  line-height: 1.4;
}

.achievement-date {
  font-size: 0.8rem;
  color: #10b981;
  font-weight: 600;
}

.achievement-status {
  font-size: 0.8rem;
  color: #6b7280;
  font-style: italic;
}

/* Recent Activity */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
}

.activity-date {
  font-size: 0.8rem;
  color: #666;
  font-weight: 600;
  min-width: 80px;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 0.25rem;
}

.activity-score {
  font-size: 0.8rem;
  color: #10b981;
  font-weight: 600;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-overview {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }
  
  .stat-icon {
    margin-bottom: 1rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .path-header {
    flex-direction: column;
    align-items: start;
    gap: 0.5rem;
  }
  
  .category-header {
    flex-direction: column;
    align-items: start;
    gap: 0.25rem;
  }
  
  .activity-item {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .activity-date {
    min-width: auto;
  }
}
</style>