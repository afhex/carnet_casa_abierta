<script setup>
import { ref } from "vue";
import ImageUpload from "../components/ImageUpload.vue";
import AnalysisResults from "../components/AnalysisResults.vue";

const selectedImage = ref(null);
const analysisResults = ref(null);
const isLoading = ref(false);
const error = ref(null);

const handleImageSelected = async (file) => {
  selectedImage.value = file;
  error.value = null;

  // Enviar al backend para análisis
  await analyzeImage(file);
};

const analyzeImage = async (file) => {
  isLoading.value = true;
  error.value = null;

  const formData = new FormData();
  formData.append("file", file);

  try {
    // Cambiar URL según tu servidor backend
    const response = await fetch("http://localhost:8000/analizar", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      let errorMessage = `Error: ${response.status}`;
      try {
        const errorData = await response.json();
        if (errorData && errorData.error) {
          errorMessage = errorData.error;
        }
      } catch (e) {
        // Si no se puede parsear JSON, usar status por defecto
      }
      throw new Error(errorMessage);
    }

    const data = await response.json();
    analysisResults.value = data.datos;
  } catch (err) {
    error.value = `Error al analizar: ${err.message}`;
    console.error("Error:", err);
  } finally {
    isLoading.value = false;
  }
};

const resetAnalysis = () => {
  selectedImage.value = null;
  analysisResults.value = null;
  error.value = null;
};
</script>

<template>
  <main class="home-container">
    <div class="content-wrapper">
      <!-- Mostrar componente de carga de imagen si no hay resultados -->
      <div v-if="!analysisResults" class="upload-section">
        <ImageUpload
          @image-selected="handleImageSelected"
          :is-loading="isLoading"
        />

        <!-- Mostrar error si hay -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </div>

      <!-- Mostrar resultados si los hay -->
      <div v-if="analysisResults && !isLoading" class="results-section">
        <AnalysisResults :results="analysisResults" :image="selectedImage" />
        <button @click="resetAnalysis" class="btn-new-analysis">
          Nuevo Análisis
        </button>
      </div>

      <!-- Indicador de carga -->
      <div v-if="isLoading" class="loading-section">
        <div class="spinner"></div>
        <p>Analizando tu rostro...</p>
      </div>
    </div>
  </main>
</template>

<style scoped>
.home-container {
  min-height: calc(100vh - 140px);
  background: linear-gradient(
    120deg,
    #1f6fb2 0%,
    #2e7cc4 40%,
    #c07a33 75%,
    #e6a354 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1rem 3rem;
}

.content-wrapper {
  width: 100%;
  max-width: 860px;
  margin: 0 auto;
}

.upload-section,
.results-section {
  padding-top: 0;
  animation: fadeIn 0.6s ease;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  border-left: 4px solid #c33;
}

.loading-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  padding: 3rem;
  color: white;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.btn-new-analysis {
  display: block;
  margin: 2rem auto 0;
  padding: 0.8rem 2rem;
  background-color: white;
  color: #1e4c7a;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-new-analysis:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
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
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .home-container {
    padding: 2rem 0.8rem 2.5rem;
  }
}
</style>
