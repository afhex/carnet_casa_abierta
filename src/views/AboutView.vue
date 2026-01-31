<template>
  <div class="about-container">
    <div class="about-content">
      <h1>Acerca de Casa Abierta</h1>

      <section class="about-section">
        <h2>🎯 Nuestra Misión</h2>
        <p>
          Revolucionar la experiencia de encontrar el corte de cabello perfecto
          usando inteligencia artificial y análisis biométrico. Queremos que cada
          persona descubra el estilo que mejor se adapta a su tipo de rostro y personalidad.
        </p>
      </section>

      <section class="about-section">
        <h2>🚀 Cómo Funciona</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon">📷</div>
            <h3>1. Captura</h3>
            <p>Sube una foto clara de tu rostro</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>2. Análisis</h3>
            <p>IA analiza tu tipo de rostro y rasgos</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">✂️</div>
            <h3>3. Recomendación</h3>
            <p>Obtén tu corte de cabello ideal</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3>4. Comparte</h3>
            <p>Comparte el código QR con tu peluquero</p>
          </div>
        </div>
      </section>

      <section class="about-section">
        <h2>💡 Tecnología</h2>
        <p>
          Utilizamos tecnologías avanzadas como:
        </p>
        <ul class="tech-list">
          <li>MediaPipe para detección de rostros en tiempo real</li>
          <li>Análisis biométrico de proporcionesiaciales</li>
          <li>Generación de imágenes con IA (Replicate)</li>
          <li>Vue 3 + FastAPI para una experiencia rápida y fluida</li>
        </ul>
      </section>

      <section class="about-section cta-section">
        <h2>¿Listo para encontrar tu estilo perfecto?</h2>
        <p>Comienza tu análisis ahora mismo</p>
        <router-link to="/" class="btn-cta">
          Ir al Análisis
        </router-link>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>

<style scoped>
.about-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #8b5a2b 0%, #d4a574 100%);
  padding: 3rem 1rem;
}

.about-content {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  animation: slideInUp 0.8s ease;
}

h1 {
  color: #8b5a2b;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
}

.about-section {
  margin-bottom: 3rem;
}

.about-section h2 {
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.about-section p {
  color: #666;
  line-height: 1.8;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.feature-card {
  background: linear-gradient(135deg, #faf5f0 0%, #f5ede4 100%);
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #e8ddd0;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(139, 90, 43, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #8b5a2b;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.feature-card p {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.tech-list {
  list-style: none;
  margin-left: 0;
  padding-left: 0;
  margin-top: 1rem;
}

.tech-list li {
  color: #666;
  padding: 0.8rem 0 0.8rem 2rem;
  position: relative;
  line-height: 1.6;
}

.tech-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #c77a3a;
  font-weight: bold;
  font-size: 1.2rem;
}

.cta-section {
  text-align: center;
  background: linear-gradient(135deg, #8b5a2b 0%, #d4a574 100%);
  padding: 2rem;
  border-radius: 12px;
  color: white;
  margin-bottom: 0;
}

.cta-section h2,
.cta-section p {
  color: white;
}

.btn-cta {
  display: inline-block;
  background: white;
  color: #8b5a2b;
  padding: 0.9rem 2rem;
  border-radius: 25px;
  font-weight: bold;
  margin-top: 1.5rem;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .about-container {
    padding: 1.5rem 0.5rem;
  }

  .about-content {
    padding: 2rem 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }

  .about-section h2 {
    font-size: 1.4rem;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>
