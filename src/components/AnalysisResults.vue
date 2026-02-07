<script setup>
import { ref, nextTick } from 'vue'
import QRCodeDisplay from './QRCodeDisplay.vue'

defineProps({
  results: {
    type: Object,
    required: true
  },
  image: {
    type: [File, null],
    default: null
  }
})

const showQRCode = ref(false)
const showTelemetry = ref(false)

// Función para alternar telemetría sin auto-scroll
const toggleTelemetry = async () => {
  const scrollPos = window.scrollY
  showTelemetry.value = !showTelemetry.value
  await nextTick()
  window.scrollTo(0, scrollPos)
}

// Función para alternar QR sin auto-scroll
const toggleQRCode = async () => {
  const scrollPos = window.scrollY
  showQRCode.value = !showQRCode.value
  await nextTick()
  window.scrollTo(0, scrollPos)
}

// Función para descargar las imágenes al hacer clic
const downloadImage = async (url, name) => {
  try {
    const response = await fetch(url);
    const blob = await response.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `Corte-${name}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error('Error descargando:', error);
  }
}
</script>

<template>
  <div class="results-container">
    <div class="results-card">
      <div class="results-header">
        <div class="success-icon">✨</div>
        <h2>Análisis Completado</h2>
        <p>Te presentamos tu recomendación personalizada</p>
      </div>

      <div class="results-grid">
        <div class="result-item">
          <div class="result-label">Tipo de Rostro</div>
          <div class="result-value">{{ results.tipo_rostro }}</div>
          <div class="result-description">
            Tu estructura facial detectada
          </div>
        </div>

        <div class="result-item highlight">
          <div class="result-label">✂️ Corte Recomendado</div>
          <div class="result-value">{{ results.corte_recomendado }}</div>
          <div class="result-description">
            Este estilo potenciará tus rasgos faciales
          </div>
        </div>

        <div class="result-item">
          <div class="result-label">Género Detectado</div>
          <div class="result-value">{{ results.genero_detectado }}</div>
          <div class="result-description">
            Base para la personalización
          </div>
        </div>
      </div>

      <div v-if="results.imagen_generada_url || results.imagen_graciosa_url" class="comparison-images-section">
        <h3 class="section-title">✨ Resultados Generados</h3>
        
        <div class="generated-images-grid">
          <!-- Imagen del corte recomendado -->
          <div v-if="results.imagen_generada_url" class="generated-card">
            <div class="card-badge">Recomendado</div>
            <div class="image-wrapper">
              <img
                :src="results.imagen_generada_url"
                alt="Corte generado"
                class="generated-image"
              />
            </div>
            <h4>{{ results.corte_recomendado }}</h4>
            <p class="card-description">
              Tu nuevo look profesional
            </p>
            <button @click="downloadImage(results.imagen_generada_url, results.corte_recomendado)" class="btn-download">
              ⬇️ Descargar
            </button>
          </div>

          <!-- Imagen graciosa -->
          <div v-if="results.imagen_graciosa_url" class="generated-card">
            <div class="card-badge funny-badge">🎭 Divertido</div>
            <div class="image-wrapper">
              <img 
                :src="results.imagen_graciosa_url" 
                :alt="results.corte_gracioso_nombre" 
                class="generated-image"
              />
            </div>
            <h4>{{ results.corte_gracioso_nombre }}</h4>
            <p class="card-description">
              ¡Porque no todo tiene que ser serio!
            </p>
            <button @click="downloadImage(results.imagen_graciosa_url, results.corte_gracioso_nombre)" class="btn-download">
              ⬇️ Descargar
            </button>
          </div>
        </div>
      </div>

      <!-- Sección de Telemetría (Modo Ingeniero) -->
      <div v-if="results.telemetria" class="telemetry-section">
        <button 
          @click="toggleTelemetry" 
          class="btn-toggle-telemetry"
        >
          {{ showTelemetry ? '🔽 Ocultar' : 'Ver' }} Telemetría Biométrica
        </button>
        
        <transition name="slide-fade">
          <div v-if="showTelemetry" class="telemetry-console">
            <div class="console-header">
              <span class="dot red"></span>
              <span class="dot yellow"></span>
              <span class="dot green"></span>
              <span class="console-title">root@biometric-core:~</span>
            </div>
            <div class="console-body">
              <div class="log-line"> > VERIFICACIÓN_INTEGRIDAD... <span class="success">APROBADA</span></div>
              <div class="log-line"> > OBJETIVO_ADQUIRIDO: <span class="highlight">VERDADERO</span></div>
              <div class="log-line"> > ANCHO_ROSTRO: {{ results.telemetria.face_width }} px</div>
              <div class="log-line"> > ALTO_ROSTRO: {{ results.telemetria.face_height }} px</div>
              <div class="log-line highlight-row"> > PROPORCIÓN_A/A: {{ results.telemetria.ratio_width_height }} [INDICADOR: {{ results.tipo_rostro.toUpperCase() }}]</div>
              <div class="log-line"> > ESTRUCTURA_MANDÍBULA: {{ results.telemetria.ratio_jaw }}</div>
              <div class="log-line"> > ÍNDICE_FRENTE: {{ results.telemetria.ratio_forehead }}</div>
              <div class="log-line flashing"> > CALCULANDO_MEJOR_COINCIDENCIA... COMPLETADO_</div>
            </div>
          </div>
        </transition>
      </div>

      <div class="action-buttons">
        <button
          @click="toggleQRCode"
          class="btn btn-qr"
        >
          📱 {{ showQRCode ? 'Ocultar' : 'Mostrar' }} Código QR
        </button>
        <button class="btn btn-share">
          📤 Compartir Resultado
        </button>
      </div>

      <QRCodeDisplay
        v-if="showQRCode"
        :results="results"
      />
    </div>
  </div>
</template>

<style scoped>
/* Telemetry Section */
.telemetry-section {
  margin-bottom: 2rem;
  text-align: center;
}

.btn-toggle-telemetry {
  background: none;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  color: #666;
  transition: all 0.3s;
}

.btn-toggle-telemetry:hover {
  background: #f0f0f0;
  color: #333;
  border-color: #bbb;
}

.telemetry-console {
  margin-top: 1rem;
  background-color: #1e1e1e;
  border-radius: 8px;
  overflow: hidden;
  text-align: left;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.console-header {
  background-color: #2d2d2d;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.red { background-color: #ff5f56; }
.yellow { background-color: #ffbd2e; }
.green { background-color: #27c93f; }

.console-title {
  color: #aaa;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  margin-left: 1rem;
}

.console-body {
  padding: 1rem;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: #00ff00; /* Hacker Green */
  line-height: 1.5;
}

.log-line {
  margin-bottom: 0.2rem;
}

.success { color: #00ff00; font-weight: bold; }
.highlight { color: #00ffff; font-weight: bold; }
.highlight-row { color: #fff; background-color: rgba(255, 255, 255, 0.1); }

.flashing {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

.results-container {
  width: 100%;
  min-height: 100%;
  padding: 2rem 0;
  animation: fadeIn 0.6s ease;
}

.results-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  overflow: visible;
}

.results-header {
  text-align: center;
  margin-bottom: 3rem;
}

.success-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  animation: bounce 1s ease;
}

.results-header h2 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.results-header p {
  color: #666;
  font-size: 1rem;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.result-item {
  background: linear-gradient(135deg, #faf5f0 0%, #f5ede4 100%);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e8ddd0;
  transition: all 0.3s ease;
}

.result-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(139, 90, 43, 0.15);
}

.result-item.highlight {
  background: linear-gradient(135deg, #8b5a2b 0%, #d4a574 100%);
  color: white;
  border: none;
}

.result-item.highlight .result-label,
.result-item.highlight .result-description {
  color: rgba(255, 255, 255, 0.9);
}

.result-label {
  font-size: 0.85rem;
  color: #8b5a2b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
}

.result-item.highlight .result-label {
  color: rgba(255, 255, 255, 0.95);
}

.result-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.result-item.highlight .result-value {
  color: white;
}

.result-description {
  font-size: 0.85rem;
  color: #999;
  line-height: 1.4;
}

/* --- ESTILOS DE IMÁGENES GENERADAS --- */
.comparison-images-section {
  margin-bottom: 3rem;
}

.section-title {
  color: #8b5a2b;
  font-size: 1.6rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 2rem;
}

.generated-images-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.generated-card {
  background: linear-gradient(135deg, #faf5f0 0%, #f5ede4 100%);
  border: 1px solid #e8ddd0;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  position: relative;
  transition: all 0.3s ease;
  overflow: hidden;
}

.generated-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

/* Estilo especial para la tarjeta graciosa */
.generated-card:has(.funny-badge) {
  background: linear-gradient(135deg, #f8f5fa 0%, #f0e8f8 100%);
  border-color: #d8c0e8;
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: rgba(139, 90, 43, 0.9);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
  z-index: 10;
}

.card-badge.funny-badge {
  background-color: rgba(211, 84, 0, 0.9);
}

.generated-card .image-wrapper {
  margin: 1rem 0;
  height: 300px;
  overflow: hidden;
  border-radius: 10px;
}

.generated-card .generated-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.generated-card h4 {
  color: #333;
  font-size: 1.2rem;
  margin: 1rem 0 0.5rem;
  font-weight: bold;
}

.card-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.generated-image-section {
  margin-bottom: 2.5rem;
  padding: 2rem;
  background: linear-gradient(135deg, #faf5f0 0%, #f5ede4 100%);
  border-radius: 12px;
  text-align: center;
  border: 1px solid #e8ddd0;
}

.generated-image-section h3 {
  color: #8b5a2b;
  margin-bottom: 1rem;
  font-size: 1.4rem;
  font-weight: bold;
}

.generated-image {
  max-width: 100%;
  border-radius: 10px;
  object-fit: cover;
}

.main-image {
  max-height: 400px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}

.image-description {
  color: #666;
  font-size: 0.9rem;
  margin: 1rem 0;
}

/* --- ESTILOS NUEVA SECCIÓN GRACIOSA --- */
.funny-section {
  margin-top: 3rem;
  margin-bottom: 3rem;
  text-align: center;
  padding-top: 2rem;
  border-top: 2px dashed #e8ddd0;
}

.funny-section h3 {
  color: #d35400;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #777;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.funny-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.funny-card-small {
  background: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  transition: transform 0.3s ease;
  border: 1px solid #eee;
}

.funny-card-small:hover {
  transform: translateY(-5px);
}

.funny-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.funny-card h4 {
  color: #8b5a2b;
  margin: 0.5rem 0;
  font-size: 1.1rem;
}

/* --- BOTONES DE DESCARGA --- */
.btn-download {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
}

.btn-download:hover {
  background-color: #34495e;
}

.btn-download-small {
  background-color: #e67e22;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.btn-download-small:hover {
  background-color: #d35400;
}


/* --- BOTONES DE ACCIÓN PRINCIPALES --- */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.9rem 1.8rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 160px;
}

.btn-qr {
  background-color: #8b5a2b;
  color: white;
}

.btn-qr:hover {
  background-color: #6b431f;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(139, 90, 43, 0.4);
}

.btn-share {
  background-color: #c77a3a;
  color: white;
}

.btn-share:hover {
  background-color: #b6682c;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(199, 122, 58, 0.4);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@media (max-width: 768px) {
  .results-card {
    padding: 1.5rem;
  }

  .results-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .results-header h2 {
    font-size: 1.5rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    min-width: 100%;
  }

  .generated-images-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .generated-card .image-wrapper {
    height: 250px;
  }

  .main-image {
    max-height: 250px;
  }

  .funny-grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* Telemetry Section */
.telemetry-section {
  margin-bottom: 2rem;
  text-align: center;
}

.btn-toggle-telemetry {
  background: none;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  color: #666;
  transition: all 0.3s;
}

.btn-toggle-telemetry:hover {
  background: #f0f0f0;
  color: #333;
  border-color: #bbb;
}

.telemetry-console {
  margin-top: 1rem;
  background-color: #1e1e1e;
  border-radius: 8px;
  overflow: hidden;
  text-align: left;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.console-header {
  background-color: #2d2d2d;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.red { background-color: #ff5f56; }
.yellow { background-color: #ffbd2e; }
.green { background-color: #27c93f; }

.console-title {
  color: #aaa;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  margin-left: 1rem;
}

.console-body {
  padding: 1rem;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: #00ff00; /* Hacker Green */
  line-height: 1.5;
}

.log-line {
  margin-bottom: 0.2rem;
}

.success { color: #00ff00; font-weight: bold; }
.highlight { color: #00ffff; font-weight: bold; }
.highlight-row { color: #fff; background-color: rgba(255, 255, 255, 0.1); }

.flashing {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>