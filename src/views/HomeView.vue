<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const userStats = ref({
  modulesCompleted: 3,
  totalModules: 12,
  accuracy: 87,
  timeSpent: 145
})

const recentActivities = ref([
  { title: 'Completed Financial Risk Assessment', time: '2 hours ago', type: 'completion' },
  { title: 'Started Portfolio Management Basics', time: '1 day ago', type: 'start' },
  { title: 'Scored 92% on Trading Fundamentals Quiz', time: '2 days ago', type: 'achievement' }
])

const quickActions = [
  { title: 'Continue Training', description: 'Resume your current module', icon: '📚', route: '/training' },
  { title: 'Practice Simulation', description: 'Test your skills in live scenarios', icon: '🎯', route: '/simulation' },
  { title: 'View Progress', description: 'Check your learning analytics', icon: '📊', route: '/progress' }
]

const navigateTo = (route: string) => {
  router.push(route)
}
</script>

<template>
  <div class="dashboard">
    <div class="container">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">Welcome to AI Fintech Training</h1>
          <p class="hero-description">
            Master financial technologies through interactive AI-powered training modules designed 
            for modern financial professionals and AI agents.
          </p>
          <button @click="navigateTo('/training')" class="cta-button">
            Start Learning 🚀
          </button>
        </div>
        <div class="hero-stats">
          <div class="stat-card">
            <div class="stat-number">{{ userStats.modulesCompleted }}</div>
            <div class="stat-label">Modules Completed</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ userStats.accuracy }}%</div>
            <div class="stat-label">Average Accuracy</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ userStats.timeSpent }}h</div>
            <div class="stat-label">Time Invested</div>
          </div>
        </div>
      </section>

      <!-- Quick Actions -->
      <section class="quick-actions-section">
        <h2 class="section-title">Quick Actions</h2>
        <div class="quick-actions-grid">
          <div 
            v-for="action in quickActions" 
            :key="action.title"
            @click="navigateTo(action.route)"
            class="action-card"
          >
            <div class="action-icon">{{ action.icon }}</div>
            <h3 class="action-title">{{ action.title }}</h3>
            <p class="action-description">{{ action.description }}</p>
          </div>
        </div>
      </section>

      <!-- Recent Activity -->
      <section class="recent-activity-section">
        <h2 class="section-title">Recent Activity</h2>
        <div class="activity-list">
          <div 
            v-for="activity in recentActivities" 
            :key="activity.title"
            class="activity-item"
          >
            <div class="activity-icon" :class="`activity-${activity.type}`">
              <span v-if="activity.type === 'completion'">✅</span>
              <span v-else-if="activity.type === 'start'">▶️</span>
              <span v-else-if="activity.type === 'achievement'">🏆</span>
            </div>
            <div class="activity-content">
              <h4 class="activity-title">{{ activity.title }}</h4>
              <p class="activity-time">{{ activity.time }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Progress Overview -->
      <section class="progress-overview-section">
        <h2 class="section-title">Learning Progress</h2>
        <div class="progress-card">
          <div class="progress-header">
            <h3>Overall Progress</h3>
            <span class="progress-percentage">{{ Math.round((userStats.modulesCompleted / userStats.totalModules) * 100) }}%</span>
          </div>
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: `${(userStats.modulesCompleted / userStats.totalModules) * 100}%` }"
            ></div>
          </div>
          <p class="progress-text">
            {{ userStats.modulesCompleted }} of {{ userStats.totalModules }} modules completed
          </p>
        </div>
      </section>
    </div>
  </div>
</template>
<style scoped>
.dashboard {
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Hero Section */
.hero-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  margin-bottom: 4rem;
  padding: 2rem 0;
  align-items: center;
}

.hero-content {
  color: white;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.hero-description {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-button {
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(238, 90, 36, 0.4);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(238, 90, 36, 0.6);
}

.hero-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 1rem;
  text-align: center;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Section Styles */
.section-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: white;
  text-align: center;
}

/* Quick Actions */
.quick-actions-section {
  margin-bottom: 4rem;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.action-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.action-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.action-description {
  color: #666;
  line-height: 1.5;
}

/* Recent Activity */
.recent-activity-section {
  margin-bottom: 4rem;
}

.activity-list {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 1.5rem;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #f8f9fa;
}

.activity-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.activity-time {
  color: #666;
  font-size: 0.9rem;
}

/* Progress Overview */
.progress-overview-section {
  margin-bottom: 2rem;
}

.progress-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.progress-header h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
}

.progress-percentage {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
}

.progress-bar {
  width: 100%;
  height: 1rem;
  background: #e9ecef;
  border-radius: 0.5rem;
  overflow: hidden;
  margin-bottom: 1rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(45deg, #667eea, #764ba2);
  border-radius: 0.5rem;
  transition: width 0.3s ease;
}

.progress-text {
  color: #666;
  text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2rem;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-stats {
    flex-direction: row;
    justify-content: center;
  }
  
  .stat-card {
    flex: 1;
    max-width: 120px;
  }
  
  .stat-number {
    font-size: 1.8rem;
  }
  
  .quick-actions-grid {
    grid-template-columns: 1fr;
  }
  
  .progress-header {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
}
</style>
