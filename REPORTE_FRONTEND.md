# 🎨 REPORTE TÉCNICO: FRONTEND
**Proyecto: Casa Abierta - Análisis Biométrico de Cortes de Cabello**
**Fecha:** 1 de Febrero, 2026
**Versión:** 1.0.0

---

## 1. 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Vue.js** | 3.5.26 | Framework reactivo principal |
| **Vite** | 7.3.1 | Build tool y servidor de desarrollo rápido |
| **Vue Router** | 4.6.4 | Manejo de rutas y navegación (SPA) |
| **QRCode.vue** | 3.6.0 | Generación de códigos QR en el cliente |
| **CSS3** | N/A | Estilizado moderno con variables y animaciones |

---

## 2. 🏛️ Arquitectura del Proyecto

El frontend sigue una arquitectura basada en componentes modulares gestionados por Vue 3 (Composition API).

### Estructura de Directorios Clave
```bash
src/
├── views/                  # Páginas completas
│   ├── HomeView.vue        # Vista principal (Lógica de orquestación)
│   └── AboutView.vue       # Vista informativa
├── components/             # Piezas reutilizables
│   ├── ImageUpload.vue     # Captura (Cámara) y Selección de archivos
│   ├── AnalysisResults.vue # Grid de resultados y visualización
│   └── QRCodeDisplay.vue   # Componente de exportación QR
├── assets/                 # Recursos estáticos
│   └── main.css            # Estilos globales y paleta de colores
└── App.vue                 # Layout principal (Header/Footer)
```

---

## 3. 🧩 Componentes y Funcionalidades

### A. HomeView.vue (Orquestador)
- **Función:** Controla el flujo de estado de la aplicación (`idle` -> `uploading` -> `analyzing` -> `results`).
- **Integración API:** Realiza la petición `POST` al backend (`/analizar`).
- **Manejo de Errores:** Visualiza alertas si el backend falla o la imagen es inválida.

### B. ImageUpload.vue (Captura)
- **Cámara en Vivo:** Utiliza la API `navigator.mediaDevices.getUserMedia` para acceder a la cámara web/móvil.
- **Preview:** Renderiza el stream de video en un `<video>` y captura frames en un `<canvas>`.
- **Validación:** Asegura que los archivos subidos sean imágenes (JPG/PNG).

### C. AnalysisResults.vue (Visualización)
- **Diseño:** Cards informativas para mostrar:
    - Tipo de Rostro (Detectado)
    - Corte Recomendado (IA)
    - Emoción y Género
- **Feedback Visual:** Muestra la imagen generada por el backend en base64.

---

## 4. 🔄 Flujo de Datos (Usuario -> Sistema)

1.  **Input:** Usuario selecciona archivo o captura foto en el navegador.
2.  **Procesamiento Local:** Vue convierte el blob de la imagen y genera un preview.
3.  **Envío:** Se empaqueta en un `FormData` (campo `file`) y se envía vía `fetch`.
4.  **Recepción:** El JSON de respuesta actualiza las variables reactivas (`reactive()`).
5.  **Renderizado:** La UI se actualiza automáticamente con los resultados y el QR generado.

---

## 5. 🎨 Diseño y UX

- **Paleta de Colores:**
    - Primario: `#667eea` (Azul/Púrpura suave)
    - Secundario: `#764ba2` (Púrpura profundo)
    - Fondo: Degradado linear moderno.
- **Responsividad:** Diseño "Mobile-First" que se adapta a celulares (columna única) y desktops (grid de 2 columnas).
- **Animaciones:** Transiciones CSS (`fade`, `slide-up`) para suavizar la aparición de resultados.
