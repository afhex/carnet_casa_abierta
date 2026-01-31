<script setup>
import { ref } from 'vue'

defineProps({
  results: {
    type: Object,
    required: true
  }
})

const qrValue = ref(JSON.stringify({
  tipo_rostro: 'results.tipo_rostro',
  corte: 'results.corte_recomendado',
  timestamp: new Date().toISOString()
}))
</script>

<template>
  <div class="qr-container">
    <div class="qr-content">
      <h3>Código QR de tu Recomendación</h3>
      <p>Escanea este código para guardar tu análisis</p>

      <div class="qr-box">
        <qrcode-vue
          :value="qrValue"
          :options="{ width: 200, margin: 2, color: { dark: '#333333', light: '#ffffff' } }"
        />
      </div>

      <p class="qr-description">
        Comparte este código con tu barbero o peluquero
      </p>
    </div>
  </div>
</template>

<script>
import QrcodeVue from 'qrcode.vue'

export default {
  components: {
    QrcodeVue
  }
}
</script>

<style scoped>
.qr-container {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e0e8ff;
  animation: fadeInUp 0.6s ease;
}

.qr-content {
  text-align: center;
}

.qr-content h3 {
  color: #333;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.qr-content > p {
  color: #666;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.qr-box {
  display: flex;
  justify-content: center;
  margin: 1.5rem 0;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f5f7ff 0%, #f0f4ff 100%);
  border-radius: 12px;
  border: 2px solid #e0e8ff;
}

.qr-description {
  color: #999;
  font-size: 0.85rem;
  margin-top: 1rem;
}

@keyframes fadeInUp {
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
  .qr-box {
    padding: 1rem;
  }
}
</style>
