<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="container">
        <div class="logo-section">
          <h1 class="app-title">🤖 AI Agent Fintech Training</h1>
          <p class="app-subtitle">Interactive Training System for Financial AI Agents</p>
        </div>
        
        <nav class="main-nav">
          <RouterLink to="/" class="nav-link">Dashboard</RouterLink>
          <RouterLink to="/training" class="nav-link">Training</RouterLink>
          <RouterLink to="/simulation" class="nav-link">Simulation</RouterLink>
          <RouterLink to="/progress" class="nav-link">Progress</RouterLink>
          <RouterLink to="/about" class="nav-link">About</RouterLink>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.logo-section {
  flex: 1;
}

.app-title {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-subtitle {
  margin: 0.25rem 0 0 0;
  font-size: 0.9rem;
  color: #666;
  font-weight: 400;
}

.main-nav {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.nav-link {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  text-decoration: none;
  color: #555;
  font-weight: 500;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.nav-link:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  transform: translateY(-1px);
}

.nav-link.router-link-active {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.main-content {
  min-height: calc(100vh - 100px);
  padding: 2rem;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    text-align: center;
  }
  
  .main-nav {
    justify-content: center;
  }
  
  .app-title {
    font-size: 1.5rem;
  }
  
  .main-content {
    padding: 1rem;
  }
}
</style>
