<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app" class="app-container">
    <header class="app-header">
      <div class="header-content">
        <RouterLink to="/" class="logo-link" aria-label="Casa Abierta">
          <img src="/logo.png" alt="Casa Abierta" class="logo-image">
        </RouterLink>

        <div class="title-block">
          <span class="title-main">CASA ABIERTA 2026</span>
          <span class="title-sub">SISTEMAS Y GESTION DE DATA</span>
        </div>

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
      <p>&copy; 2026 Casa Abierta</p>
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
  padding: 1rem 0.5rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: grid;
  grid-template-columns: 140px 1fr 200px;
  align-items: center;
  gap: 1rem;
}

.logo-link {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
}

.logo-image {
  height: 56px;
  width: auto;
  object-fit: contain;
}

.title-block {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.title-main {
  font-weight: 700;
  font-size: 1.3rem;
  color: #0b2a4a;
  letter-spacing: 0.2rem;
}

.title-sub {
  font-weight: 600;
  font-size: 0.85rem;
  color: #3a6ea5;
  letter-spacing: 0.25rem;
}

.nav-menu {
  display: flex;
  gap: 1.5rem;
  justify-content: flex-end;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: #35506b;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #1e4c7a;
}

.nav-link.router-link-active {
  color: #1e4c7a;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  right: 0;
  height: 2px;
  background: #1e4c7a;
}

.app-main {
  flex: 1;
  width: 100%;
  overflow-y: auto;
}

.app-footer {
  background: #0f2742;
  color: white;
  text-align: center;
  padding: 1.5rem 1rem;
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .header-content {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 0.7rem;
  }

  .nav-menu {
    gap: 1rem;
    justify-content: center;
  }

  .nav-link {
    font-size: 0.9rem;
  }

  .title-main {
    font-size: 1.1rem;
    letter-spacing: 0.12rem;
  }

  .title-sub {
    font-size: 0.75rem;
    letter-spacing: 0.12rem;
  }
}
</style>
