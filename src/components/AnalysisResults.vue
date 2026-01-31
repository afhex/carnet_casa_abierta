<script setup>
import { ref } from 'vue'
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
</script>

<template>
  <div class="results-container">
    <div class="results-card">
      <!-- Header con icono -->
      <div class="results-header">
        <div class="success-icon">✨</div>
        <h2>Análisis Completado</h2>
        <p>Te presentamos tu recomendación personalizada</p>
      </div>

      <!-- Grid de resultados -->
      <div class="results-grid">
        <!-- Tipo de Rostro -->
        <div class="result-item">
          <div class="result-label">Tipo de Rostro</div>
          <div class="result-value">{{ results.tipo_rostro }}</div>
          <div class="result-description">
            Tu estructura facial se caracteriza por estas proporciones
          </div>
        </div>

        <!-- Corte Recomendado -->
        <div class="result-item highlight">
          <div class="result-label">✂️ Corte Recomendado</div>
          <div class="result-value">{{ results.corte_recomendado }}</div>
          <div class="result-description">
            Este estilo potenciará tus rasgos faciales
          </div>
        </div>

        <!-- Emoción Detectada -->
        <div class="result-item">
          <div class="result-label">Emoción Detectada</div>
          <div class="result-value">{{ results.emocion_detectada }}</div>
          <div class="result-description">
            Estado emocional reconocido en el análisis
          </div>
        </div>

        <!-- Género Detectado -->
        <div class="result-item">
          <div class="result-label">Género Detectado</div>
          <div class="result-value">{{ results.genero_detectado }}</div>
          <div class="result-description">
            Información utilizada para personalizar recomendaciones
          </div>
        </div>
      </div>

      <!-- Imagen Generada -->
      <div v-if="results.imagen_generada_url" class="generated-image-section">
        <h3>Previsualización de tu nuevo look</h3>
        <img
          :src="results.imagen_generada_url"
          alt="Corte generado"
          class="generated-image"
        />
        <p class="image-description">
          Esta es una representación del corte recomendado para ti
        </p>
      </div>

      <!-- Botones de acción -->
      <div class="action-buttons">
        <button
          @click="showQRCode = !showQRCode"
          class="btn btn-qr"
        >
          📱 {{ showQRCode ? 'Ocultar' : 'Mostrar' }} Código QR
        </button>
        <button class="btn btn-share">
          📤 Compartir Resultado
        </button>
      </div>

      <!-- QR Code -->
      <QRCodeDisplay
        v-if="showQRCode"
        :results="results"
      />
    </div>
  </div>
</template>

<style scoped>
.results-container {
  width: 100%;
  padding: 2rem 0;
  animation: fadeIn 0.6s ease;
}

.results-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  overflow: hidden;
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
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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

.generated-image-section {
  margin-bottom: 2.5rem;
  padding: 2rem;
  background: linear-gradient(135deg, #faf5f0 0%, #f5ede4 100%);
  border-radius: 12px;
  text-align: center;
}

.generated-image-section h3 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.generated-image {
  max-width: 100%;
  max-height: 350px;
  border-radius: 10px;
  margin-bottom: 1rem;
  object-fit: cover;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.image-description {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

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

  .generated-image {
    max-height: 250px;
  }
}
</style>
