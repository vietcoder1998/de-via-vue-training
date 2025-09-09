<template>
  <div class="about-view">
    <div class="container">
      <!-- Hero Section -->
      <section class="about-hero">
        <h1 class="hero-title">About AI Fintech Training</h1>
        <p class="hero-subtitle">
          Empowering the next generation of AI agents with comprehensive fintech knowledge
        </p>
      </section>

      <!-- Mission Section -->
      <section class="mission-section">
        <div class="mission-content">
          <h2 class="section-title">Our Mission</h2>
          <p class="mission-text">
            We believe that artificial intelligence agents need sophisticated understanding of financial 
            systems to operate effectively in modern fintech environments. Our platform provides 
            comprehensive, interactive training modules designed specifically for AI agents working 
            in financial services.
          </p>
        </div>
        <div class="mission-visual">
          <div class="visual-card">
            <div class="visual-icon">🤖</div>
            <h3>AI-Powered Learning</h3>
            <p>Advanced algorithms adapt to learning patterns</p>
          </div>
          <div class="visual-card">
            <div class="visual-icon">💼</div>
            <h3>Real-World Scenarios</h3>
            <p>Practice with actual fintech use cases</p>
          </div>
          <div class="visual-card">
            <div class="visual-icon">📊</div>
            <h3>Data-Driven Insights</h3>
            <p>Track progress with detailed analytics</p>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section class="features-section">
        <h2 class="section-title">Platform Features</h2>
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">📚</div>
            <h3 class="feature-title">Interactive Modules</h3>
            <p class="feature-description">
              Comprehensive training modules covering all aspects of fintech, from basic concepts 
              to advanced algorithmic trading strategies.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Live Simulations</h3>
            <p class="feature-description">
              Practice in realistic market conditions with real-time data and scenarios that 
              mirror actual financial environments.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">📈</div>
            <h3 class="feature-title">Progress Tracking</h3>
            <p class="feature-description">
              Monitor learning progress with detailed analytics, skill assessments, and 
              personalized learning path recommendations.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">🏆</div>
            <h3 class="feature-title">Achievement System</h3>
            <p class="feature-description">
              Earn badges and achievements as you master different aspects of fintech, 
              from risk management to blockchain technology.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">Adaptive Learning</h3>
            <p class="feature-description">
              AI-powered content adaptation that adjusts difficulty and focus areas based 
              on individual learning patterns and performance.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">🔒</div>
            <h3 class="feature-title">Secure Environment</h3>
            <p class="feature-description">
              Train safely in a sandbox environment that protects sensitive financial data 
              while providing realistic learning experiences.
            </p>
          </div>
        </div>
      </section>

      <!-- Curriculum Section -->
      <section class="curriculum-section">
        <h2 class="section-title">Training Curriculum</h2>
        <div class="curriculum-grid">
          <div class="curriculum-track">
            <h3 class="track-title">Foundation Track</h3>
            <ul class="track-modules">
              <li>Introduction to Fintech</li>
              <li>Financial Risk Assessment</li>
              <li>Basic Trading Principles</li>
              <li>Regulatory Compliance</li>
            </ul>
          </div>

          <div class="curriculum-track">
            <h3 class="track-title">Intermediate Track</h3>
            <ul class="track-modules">
              <li>Portfolio Management</li>
              <li>Algorithmic Trading</li>
              <li>Market Data Analysis</li>
              <li>Customer Service AI</li>
            </ul>
          </div>

          <div class="curriculum-track">
            <h3 class="track-title">Advanced Track</h3>
            <ul class="track-modules">
              <li>Blockchain & Cryptocurrency</li>
              <li>AI in Financial Services</li>
              <li>Quantitative Analysis</li>
              <li>RegTech Solutions</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Technology Section -->
      <section class="technology-section">
        <h2 class="section-title">Built with Modern Technology</h2>
        <div class="tech-stack">
          <div class="tech-item">
            <div class="tech-logo">⚡</div>
            <div class="tech-name">Vue.js 3</div>
            <div class="tech-description">Modern reactive framework</div>
          </div>
          <div class="tech-item">
            <div class="tech-logo">🎯</div>
            <div class="tech-name">TypeScript</div>
            <div class="tech-description">Type-safe development</div>
          </div>
          <div class="tech-item">
            <div class="tech-logo">🏪</div>
            <div class="tech-name">Pinia</div>
            <div class="tech-description">State management</div>
          </div>
          <div class="tech-item">
            <div class="tech-logo">🚀</div>
            <div class="tech-name">Vite</div>
            <div class="tech-description">Fast build tool</div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="cta-section">
        <div class="cta-content">
          <h2 class="cta-title">Ready to Start Learning?</h2>
          <p class="cta-text">
            Join thousands of AI agents already mastering fintech through our comprehensive training platform.
          </p>
          <router-link to="/training" class="cta-button">
            Begin Training Journey 🚀
          </router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.about-view {
  min-height: 100vh;
  color: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Hero Section */
.about-hero {
  text-align: center;
  padding: 4rem 0;
  margin-bottom: 4rem;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #fff, #fbbf24);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.3rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Section Styles */
.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 3rem;
  text-align: center;
}

/* Mission Section */
.mission-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  margin-bottom: 6rem;
  align-items: center;
}

.mission-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 3rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.mission-text {
  font-size: 1.1rem;
  line-height: 1.8;
  opacity: 0.9;
}

.mission-visual {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.visual-card {
  background: rgba(255, 255, 255, 0.95);
  color: #2c3e50;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.visual-card:hover {
  transform: translateY(-5px);
}

.visual-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.visual-card h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.visual-card p {
  color: #666;
  font-size: 0.9rem;
}

/* Features Section */
.features-section {
  margin-bottom: 6rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.feature-item {
  background: rgba(255, 255, 255, 0.95);
  color: #2c3e50;
  padding: 2.5rem;
  border-radius: 1rem;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.feature-item:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  display: block;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.feature-description {
  color: #666;
  line-height: 1.6;
  font-size: 1rem;
}

/* Curriculum Section */
.curriculum-section {
  margin-bottom: 6rem;
}

.curriculum-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.curriculum-track {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 2.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.curriculum-track:hover {
  transform: translateY(-5px);
}

.track-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #fbbf24;
  text-align: center;
}

.track-modules {
  list-style: none;
  padding: 0;
  margin: 0;
}

.track-modules li {
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  padding-left: 2rem;
}

.track-modules li:before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: 600;
}

.track-modules li:last-child {
  border-bottom: none;
}

/* Technology Section */
.technology-section {
  margin-bottom: 6rem;
}

.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.tech-item {
  background: rgba(255, 255, 255, 0.95);
  color: #2c3e50;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.tech-item:hover {
  transform: translateY(-5px);
}

.tech-logo {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.tech-name {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.tech-description {
  color: #666;
  font-size: 0.9rem;
}

/* CTA Section */
.cta-section {
  margin-bottom: 4rem;
}

.cta-content {
  background: linear-gradient(45deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
  backdrop-filter: blur(10px);
  padding: 4rem;
  border-radius: 2rem;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.cta-text {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-button {
  display: inline-block;
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
  text-decoration: none;
  padding: 1.25rem 2.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(238, 90, 36, 0.4);
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(238, 90, 36, 0.6);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .mission-section {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .features-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
  
  .curriculum-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .tech-stack {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .mission-content {
    padding: 2rem;
  }
  
  .cta-content {
    padding: 2rem;
  }
  
  .cta-title {
    font-size: 2rem;
  }
  
  .cta-text {
    font-size: 1rem;
  }
}
</style>
