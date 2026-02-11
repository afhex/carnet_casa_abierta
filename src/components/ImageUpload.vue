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

        <!-- Círculo guía para centrar rostro con efectos futuristas -->
        <div class="face-guide">
          <div class="scanner-line"></div>
          <div class="face-circle">
            <div class="inner-ring"></div>
            <div class="outer-ring"></div>
          </div>

          <!-- Esquinas tecnológicas -->
          <div class="tech-corners">
            <div class="corner top-left"></div>
            <div class="corner top-right"></div>
            <div class="corner bottom-left"></div>
            <div class="corner bottom-right"></div>
          </div>

          <p class="status-text">ANALIZANDO BIOMETRÍA...</p>
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
  opacity: 0.9;
}

.face-guide {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  background: radial-gradient(circle, transparent 30%, rgba(0,0,0,0.5) 80%);
}

/* --- EFECTOS FUTURISTAS --- */

/* Círculo Central */
.face-circle {
  width: 240px;
  height: 300px; /* Más ovalado para rostro */
  position: relative;
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 50% 50% 45% 45%; /* Forma de rostro */
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.2), inset 0 0 20px rgba(0, 255, 255, 0.1);
}

/* Anillos Giratorios */
.inner-ring, .outer-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  border: 2px dashed rgba(0, 255, 255, 0.4);
}

.inner-ring {
  width: 90%;
  height: 90%;
  animation: spin 10s linear infinite reverse;
}

.outer-ring {
  width: 110%;
  height: 110%;
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-left-color: transparent;
  border-right-color: transparent;
  animation: spin 8s linear infinite;
}

/* Línea de Escáner */
.scanner-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00ffff, transparent);
  box-shadow: 0 0 10px #00ffff;
  animation: scan 3s ease-in-out infinite;
  z-index: 10;
}

/* Esquinas Tecnológicas */
.tech-corners {
  position: absolute;
  inset: 20px;
}

.corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 3px solid rgba(0, 255, 255, 0.6);
  filter: drop-shadow(0 0 5px rgba(0, 255, 255, 0.5));
}

.top-left { top: 0; left: 0; border-right: none; border-bottom: none; }
.top-right { top: 0; right: 0; border-left: none; border-bottom: none; }
.bottom-left { bottom: 0; left: 0; border-right: none; border-top: none; }
.bottom-right { bottom: 0; right: 0; border-left: none; border-top: none; }

/* Texto de Estado */
.status-text {
  color: #00ffff;
  margin-top: 1.5rem;
  font-family: 'Courier New', monospace;
  font-weight: bold;
  font-size: 0.9rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.8);
  animation: blink 2s infinite;
  background: rgba(0, 0, 0, 0.6);
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
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
  padding: 1rem;
}

.upload-box {
  background: white;
  border-radius: 18px;
  padding: 2.6rem 2.4rem 2.2rem;
  text-align: center;
  box-shadow: 0 16px 40px rgba(9, 30, 66, 0.18);
  animation: slideUp 0.6s ease;
  border: 1px solid rgba(15, 39, 66, 0.08);
}

.icon {
  width: 44px;
  height: 44px;
  margin: 0 auto 1.2rem;
  display: grid;
  place-items: center;
  font-size: 1.4rem;
  color: #1e4c7a;
  background: #eef4fb;
  border-radius: 12px;
  border: 1px solid #d7e6f8;
}

.upload-box h2 {
  color: #0f2742;
  margin-bottom: 0.6rem;
  font-size: 1.7rem;
  font-weight: 700;
}

.upload-box p {
  color: #5b6b7a;
  margin-bottom: 1.8rem;
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
  padding: 0.7rem 1.4rem;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 160px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #1e4c7a;
  color: white;
  box-shadow: 0 8px 18px rgba(30, 76, 122, 0.25);
}

.btn-primary:hover:not(:disabled) {
  background-color: #173e64;
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(30, 76, 122, 0.3);
}

.btn-secondary {
  background-color: white;
  color: #1e4c7a;
  border: 1px solid #9fc0e4;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #eef4fb;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(30, 76, 122, 0.15);
}

.info-text {
  font-size: 0.82rem;
  color: #6f7f90;
  margin-top: 0.9rem;
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

@keyframes spin {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes scan {
  0% { top: 10%; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 90%; opacity: 0; }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@media (max-width: 768px) {
  .upload-box {
    padding: 2.2rem 1.6rem;
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
    font-size: 1.4rem;
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
