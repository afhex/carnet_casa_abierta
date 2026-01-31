<script setup>
import { ref, onUnmounted } from 'vue'

defineProps({
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['image-selected'])

const fileInput = ref(null)
const videoElement = ref(null)
const canvasElement = ref(null)
const previewImage = ref(null)
const showCamera = ref(false)
const cameraStream = ref(null)
const cameraError = ref(null)

// Seleccionar archivo
const triggerFileInput = () => {
  fileInput.value?.click()
}

// Iniciar cámara
const startCamera = async () => {
  cameraError.value = null

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'user',
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    })

    cameraStream.value = stream
    showCamera.value = true

    // Esperar a que el elemento video esté montado
    setTimeout(() => {
      if (videoElement.value) {
        videoElement.value.srcObject = stream
      }
    }, 100)
  } catch (err) {
    cameraError.value = `Error al acceder a la cámara: ${err.message}`
    console.error('Error accessing camera:', err)
  }
}

// Capturar foto
const capturePhoto = () => {
  if (!videoElement.value || !canvasElement.value) return

  const context = canvasElement.value.getContext('2d')
  canvasElement.value.width = videoElement.value.videoWidth
  canvasElement.value.height = videoElement.value.videoHeight

  // Espejo (flip) de la cámara frontal
  context.translate(canvasElement.value.width, 0)
  context.scale(-1, 1)

  // Dibujar video en canvas
  context.drawImage(videoElement.value, 0, 0)

  // Obtener imagen del canvas
  canvasElement.value.toBlob((blob) => {
    if (blob) {
      const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' })
      processImage(file)
      stopCamera()
    }
  }, 'image/jpeg', 0.95)
}

// Procesar imagen
const processImage = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    previewImage.value = e.target?.result
  }
  reader.readAsDataURL(file)

  emit('image-selected', file)
}

// Manejar cambio de archivo
const handleFileChange = (event) => {
  const file = event.target.files?.[0]
  if (file && file.type.startsWith('image/')) {
    processImage(file)
  }
}

// Detener cámara
const stopCamera = () => {
  if (cameraStream.value) {
    cameraStream.value.getTracks().forEach(track => track.stop())
    cameraStream.value = null
  }
  showCamera.value = false
  cameraError.value = null
}

// Cancelar cámara
const cancelCamera = () => {
  stopCamera()
  previewImage.value = null
}

// Limpiar al desmontar
onUnmounted(() => {
  stopCamera()
})
</script>

<template>
  <div class="upload-container">
    <!-- Preview de imagen capturada -->
    <div v-if="previewImage" class="preview-section">
      <img :src="previewImage" alt="Preview" class="preview-image">
      <button @click="previewImage = null" class="btn-reset">
        ↻ Capturar otra foto
      </button>
    </div>

    <!-- Vista de cámara activa -->
    <div v-else-if="showCamera" class="camera-section">
      <div class="camera-container">
        <video
          ref="videoElement"
          autoplay
          playsinline
          class="video-stream"
        ></video>

        <!-- Círculo guía para centrar rostro -->
        <div class="face-guide">
          <div class="face-circle"></div>
          <p>Centra tu rostro en el círculo</p>
        </div>
      </div>

      <!-- Controles de cámara -->
      <div class="camera-controls">
        <button @click="capturePhoto" class="btn btn-capture" title="Capturar foto">
          📸 Capturar
        </button>
        <button @click="cancelCamera" class="btn btn-cancel" title="Cerrar cámara">
          ✕ Cancelar
        </button>
      </div>

      <!-- Mostrar error si hay -->
      <div v-if="cameraError" class="error-message">
        ⚠️ {{ cameraError }}
      </div>
    </div>

    <!-- Área de carga principal -->
    <div v-else class="upload-area">
      <div class="upload-box">
        <div class="icon">📷</div>
        <h2>Sube o captura tu foto</h2>
        <p>Necesitamos una foto clara de tu rostro</p>

        <div class="button-group">
          <button
            @click="triggerFileInput"
            class="btn btn-primary"
            :disabled="isLoading"
          >
            📁 Seleccionar archivo
          </button>
          <button
            @click="startCamera"
            class="btn btn-secondary"
            :disabled="isLoading"
          >
            📸 Usar cámara
          </button>
        </div>

        <p class="info-text">
          Soportamos: JPG, PNG, WebP
        </p>
      </div>
    </div>

    <!-- Canvas oculto para captura -->
    <canvas ref="canvasElement" style="display: none;"></canvas>

    <!-- Input oculto para archivo -->
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      @change="handleFileChange"
      style="display: none"
    />
  </div>
</template>

<style scoped>
.upload-container {
  width: 100%;
}

.preview-section {
  text-align: center;
  padding: 2rem;
  animation: fadeIn 0.6s ease;
}

.preview-image {
  max-width: 100%;
  max-height: 400px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  object-fit: cover;
  margin-bottom: 1.5rem;
}

.btn-reset {
  padding: 0.6rem 1.5rem;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-reset:hover {
  background-color: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* Camera Section */
.camera-section {
  padding: 1.5rem;
  animation: fadeIn 0.6s ease;
}

.camera-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  margin: 0 auto 1.5rem;
  border-radius: 16px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.video-stream {
  width: 100%;
  display: block;
  transform: scaleX(-1);
}

.face-guide {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.face-circle {
  width: 200px;
  height: 200px;
  border: 3px solid rgba(139, 90, 43, 0.7);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.face-guide p {
  color: white;
  margin-top: 1rem;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.camera-controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.btn-capture {
  background-color: #4CAF50;
  color: white;
  padding: 0.9rem 2rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-capture:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.btn-cancel {
  background-color: #f44336;
  color: white;
  padding: 0.9rem 2rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  background-color: #da190b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  border-left: 4px solid #c33;
  text-align: center;
}

/* Upload Area */
.upload-area {
  padding: 2rem;
}

.upload-box {
  background: white;
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  animation: slideUp 0.6s ease;
}

.icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.upload-box h2 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.8rem;
}

.upload-box p {
  color: #666;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 160px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #8b5a2b;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #6b431f;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(139, 90, 43, 0.4);
}

.btn-secondary {
  background-color: white;
  color: #8b5a2b;
  border: 2px solid #8b5a2b;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #faf5f0;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(139, 90, 43, 0.2);
}

.info-text {
  font-size: 0.85rem;
  color: #999;
  margin-top: 1rem;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(139, 90, 43, 0.7);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(139, 90, 43, 0);
  }
}

@media (max-width: 768px) {
  .upload-box {
    padding: 2rem 1.5rem;
  }

  .button-group {
    flex-direction: column;
  }

  .btn {
    min-width: 100%;
  }

  .icon {
    font-size: 3rem;
  }

  .upload-box h2 {
    font-size: 1.5rem;
  }

  .camera-container {
    max-width: 100%;
  }

  .face-circle {
    width: 150px;
    height: 150px;
  }

  .camera-controls {
    flex-direction: column;
  }

  .btn-capture,
  .btn-cancel {
    min-width: 100%;
  }
}
</style>
