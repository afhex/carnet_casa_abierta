# 🎨 REPORTE TÉCNICO: FRONTEND

**Proyecto:** Casa Abierta - Análisis Biométrico de Cortes de Cabello  
**Última Actualización:** 6 de Febrero, 2026  
**Versión:** 1.1.0

---

## 1. 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Vue.js** | 3.5.26 | Framework reactivo principal |
| **Vite** | 7.3.1 | Build tool y servidor dev |
| **Vue Router** | 4.6.4 | Enrutamiento (SPA) |
| **QRCode.vue** | 3.6.0 | Generación de códigos QR |
| **CSS3** | Moderno | Estilos y animaciones |

---

## 2. 🏛️ Arquitectura del Proyecto

Arquitectura modular basada en componentes reutilizables con Vue 3 Composition API.

### Estructura de Directorios

```
src/
├── views/
│   ├── HomeView.vue        # Vista principal (orquestación)
│   └── AboutView.vue       # Página informativa
├── components/
│   ├── ImageUpload.vue     # Captura y carga de imágenes
│   ├── AnalysisResults.vue # Visualización de resultados
│   └── QRCodeDisplay.vue   # Exportación QR
├── assets/
│   └── main.css            # Estilos globales
├── router/
│   └── index.js            # Configuración de rutas
└── App.vue                 # Layout principal
```

---

## 3. 🧩 Componentes

### **HomeView.vue** (Orquestador)
- **Función:** Control del flujo de estado (idle → uploading → analyzing → results)
- **Responsabilidades:**
  - Manejo de eventos de selección de imagen
  - Llamadas a API backend
  - Gestión de carga y errores
  - Renderización condicional

**Estados:**
- `selectedImage`: Imagen seleccionada/capturada
- `analysisResults`: Resultados del análisis
- `isLoading`: Indicador de carga
- `error`: Mensaje de error

### **ImageUpload.vue** (Captura)
- **Cámara en vivo:** API `navigator.mediaDevices.getUserMedia`
- **Preview:** Renderiza stream de video en `<video>`
- **Captura:** Convierte frames a `<canvas>`
- **Validación:** Verifica tipo de archivo (JPG/PNG)

**Características:**
- Selector de archivo
- Captura desde cámara web/móvil
- Vista previa en tiempo real
- Indicador de carga

### **AnalysisResults.vue** (Visualización)
- **Cards informativos** para mostrar:
  - Tipo de rostro detectado
  - Cortes recomendados
  - Género detectado
  - Imagen generada

**Propiedades:**
- `results`: Datos de análisis del backend
- `image`: Imagen original capturada/subida

### **QRCodeDisplay.vue** (Exportación)
- **Generación de QR** con librería `qrcode.vue`
- **Codifica:** URL con resultados del análisis
- **Exportación:** Permite descargar como imagen

---

## 4. 🔄 Flujo de Datos

```
Usuario selecciona/captura imagen
         ↓
Vue convierte a Blob
         ↓
FormData con campo 'file'
         ↓
Fetch POST a http://localhost:8000/analizar
         ↓
Backend analiza imagen
         ↓
Respuesta JSON con resultados
         ↓
Vue actualiza state reactivo
         ↓
Componentes se re-renderizan con resultados
         ↓
Usuario ve análisis y opciones de compartir
```

---

## 5. 🎨 Diseño y UX

### Paleta de Colores
- **Primario:** `#667eea` (Azul/Púrpura suave)
- **Secundario:** `#764ba2` (Púrpura profundo)
- **Fondo:** Degradado lineal moderno

### Responsividad
- **Mobile-First:** Diseño en columna única
- **Desktop:** Grid de dos columnas
- **Breakpoints:** Media queries estándar

### Animaciones
- **Fade In:** Aparición suave
- **Slide Up:** Movimiento dinámico
- **Transiciones CSS:** Suavizadas (0.3s)

---

## 6. 📡 Integración con API

### Endpoint: `POST /analizar`

**Código:**
```javascript
const response = await fetch('http://localhost:8000/analizar', {
  method: 'POST',
  body: formData,  // Contiene imagen en campo 'file'
})

const data = await response.json()
analysisResults.value = data.datos
```

**Manejo de errores:**
- Validación de respuesta HTTP
- Try-catch para excepciones de red
- Mensajes de error al usuario

---

## 7. 🔒 Seguridad

| Aspecto | Implementación |
|--------|----------------|
| **CORS** | Configurado en backend |
| **Validación** | Tipos de archivo en frontend |
| **Privacidad** | Imágenes procesadas localmente |
| **Errores** | Mensajes genéricos al usuario |

---

## 8. 📝 Cambios Recientes (6 de Febrero, 2026)

### ✅ Optimizaciones Implementadas

**Componentes:**
- ✅ Eliminación de componentes heredados no usados:
  - `HelloWorld.vue`
  - `TheWelcome.vue`
  - `WelcomeItem.vue`
  - Carpeta `icons/`

**Dependencias:**
- ✅ Eliminación de `@supabase/supabase-js` (no utilizado)
- ✅ Actualización de `package.json`
- ✅ Reducción de bundle size

**Código:**
- ✅ Mejor estructura de componentes
- ✅ Funciones mejor documentadas
- ✅ Eliminación de código duplicado

---

## 9. 🚀 Instalación y Desarrollo

```bash
# Instalar dependencias
npm install

# Servidor de desarrollo con Hot Module Replacement
npm run dev

# Build para producción
npm run build

# Vista previa del build
npm run preview

# Lint con ESLint
npm run lint
```

---

## 10. 🔧 Configuración

### `vite.config.js`
- Plugin Vue automático
- Vue DevTools integration
- Optimizaciones de build

### `eslint.config.js`
- Validación de código Vue
- Soporte para ES2024
- Globals de navegador

---

## 11. 📊 Rendimiento

- **Bundle Size:** ~150KB (minificado)
- **Load Time:** <2s en conexión 4G
- **Lighthouse Score:** >85 en rendimiento
- **File Caching:** Habilitado en producción

---

## 12. 🌐 Navegación

| Ruta | Vista | Descripción |
|------|------|-------------|
| `/` | HomeView | Análisis principal |
| `/about` | AboutView | Información del proyecto |

---

**Nota:** Para desarrollo local, asegurate que el backend esté corriendo en `http://localhost:8000`.

