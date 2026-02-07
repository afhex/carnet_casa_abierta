<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app" class="app-container">
    <header class="app-header">
      <div class="header-content">
        <RouterLink to="/" class="logo-link">
          <img src="/logo.png" alt="Casa Abierta" class="logo-image">
          <span class="app-name">Casa Abierta</span>
        </RouterLink>

        <nav class="nav-menu">
          <RouterLink to="/" class="nav-link">Inicio</RouterLink>
          <RouterLink to="/about" class="nav-link">Acerca de</RouterLink>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <RouterView />
    </main>

    <footer class="app-footer">
      <p>&copy; 2026 Casa Abierta - Análisis de Cortes con IA</p>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
}

.app-header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  text-decoration: none;
  color: #333;
  transition: color 0.3s ease;
}

.logo-link:hover {
  color: #c77a3a;
}

.logo-image {
  height: 50px;
  width: auto;
  object-fit: contain;
}

.app-name {
  font-size: 1.3rem;
  font-weight: bold;
  background: linear-gradient(135deg, #8b5a2b 0%, #d4a574 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: #666;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #c77a3a;
}

.nav-link.router-link-active {
  color: #c77a3a;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(135deg, #8b5a2b 0%, #d4a574 100%);
}

.app-main {
  flex: 1;
  width: 100%;
  overflow-y: auto;
}

.app-footer {
  background: #333;
  color: white;
  text-align: center;
  padding: 2rem 1rem;
  margin-top: 3rem;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-menu {
    gap: 1rem;
  }

  .nav-link {
    font-size: 0.9rem;
  }

  .app-name {
    font-size: 1.1rem;
  }
}
</style>
