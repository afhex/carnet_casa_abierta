# 🎬 Ejemplos de Uso - Interfaz Frontend

## Escenario 1: Usuario Nuevo - Análisis Completo

### Paso 1: Acceder a la Aplicación
```
URL: http://localhost:5173
Estado: Se ve la página principal con:
- Título: "✂️ Análisis de Cortes de Cabello"
- Subtítulo: "Descubre el corte de cabello perfecto para tu rostro con IA"
```

### Paso 2: Cargar Imagen
```javascript
// Usuario hace clic en "📁 Seleccionar archivo"
// Se abre selector de archivos del sistema
// Usuario selecciona: "mi_foto.jpg"

// EVENTO EMITIDO:
@image-selected({
  name: "mi_foto.jpg",
  size: 245120,
  type: "image/jpeg"
})
```

### Paso 3: Vista Previa
```
Se muestra:
- Miniatura de la imagen seleccionada
- Indicador de carga: "Analizando tu rostro..."
- Spinner girando
```

### Paso 4: Resultados del Análisis
```javascript
// Backend responde:
{
  "mensaje": "Análisis completado",
  "datos": {
    "tipo_rostro": "Ovalado",
    "corte_recomendado": "Fade Bajo",
    "emocion_detectada": "Sorprendido",
    "genero_detectado": "Masculino",
    "imagen_generada_url": "https://example.com/resultado.jpg"
  }
}

// Se muestra en tarjetas:
┌─────────────────────────┐
│ Tipo de Rostro: Ovalado │
├─────────────────────────┤
│ Corte: Fade Bajo        │ (destacado)
├─────────────────────────┤
│ Emoción: Sorprendido    │
├─────────────────────────┤
│ Género: Masculino       │
└─────────────────────────┘
```

### Paso 5: Ver Código QR
```javascript
// Usuario hace clic en "📱 Mostrar Código QR"
showQRCode.value = true

// Se genera QR con:
{
  tipo_rostro: "Ovalado",
  corte: "Fade Bajo",
  timestamp: "2026-01-31T10:30:00Z"
}
```

### Paso 6: Nuevo Análisis
```javascript
// Usuario hace clic en "Nuevo Análisis"
// Se resetea el estado:
selectedImage.value = null
analysisResults.value = null
error.value = null

// Se vuelve a mostrar el formulario de carga
```

---

## Escenario 2: Usar Cámara en Móvil

### Paso 1: Acceder desde Teléfono
```
URL: http://localhost:5173
Navegador: Chrome/Safari Mobile
```

### Paso 2: Hacer Clic en "📸 Usar Cámara"
```javascript
// Evento click en botón
@click="triggerCamera"

// Se abre el selector:
- Si es mobile: acceso directo a cámara
- Si es desktop: selector de archivo con capture
```

### Paso 3: Capturar Foto
```
Se abre cámara del dispositivo
Usuario toma foto
Se guarda en memoria
Se procesa como archivo
```

### Resultado
```
Todo igual al Escenario 1, desde el paso 3 en adelante
```

---

## Escenario 3: Error de Conexión

### Situación: Backend no disponible

```javascript
// Usuario carga imagen
// Se intenta POST a http://localhost:8000/analizar
// Error de conexión

// Respuesta:
error.value = "Error al analizar: Failed to fetch"

// Se muestra al usuario:
┌─────────────────────────┐
│ ❌ Error al analizar:   │
│ Failed to fetch         │
│                         │
│ Verifica que el         │
│ servidor esté corriendo │
└─────────────────────────┘
```

---

## Escenario 4: Navegación

### Desde Home a About
```javascript
// Usuario hace clic en "Acerca de" en navegación
// Router cambia a /about
// Se muestra la página con:
- Información del proyecto
- 4 pasos del proceso
- Tecnologías
- CTA para volver a análisis
```

### Desde About a Home
```javascript
// Usuario hace clic en "Ir al Análisis"
// Router cambia a /
// Se muestra página de análisis
```

---

## Escenario 5: Compartir Resultado

```javascript
// Usuario ve resultados
// Hace clic en "📤 Compartir Resultado"

// Opciones (preparadas para implementar):
1. Compartir en WhatsApp
2. Compartir código QR por email
3. Copiar enlace
4. Descargar como PDF
```

---

## 🧪 Pruebas Manuales

### Test 1: Carga de Imagen Válida
```bash
✓ Seleccionar JPG
✓ Ver preview
✓ Enviar al backend
✓ Ver resultados
✓ Generar QR
```

### Test 2: Carga de Archivo Inválido
```bash
✓ Intentar seleccionar PDF
✓ Validación debe rechazarlo
✓ Mostrar error
```

### Test 3: Responsive Design
```bash
Desktop (1920x1080)
  ✓ Imagen grande
  ✓ Grid de 2 columnas
  ✓ Botones lado a lado

Tablet (768x1024)
  ✓ Imagen ajustada
  ✓ Grid de 1-2 columnas
  ✓ Botones apilados

Móvil (375x667)
  ✓ Imagen pequeña
  ✓ Grid de 1 columna
  ✓ Botones fullwidth
```

### Test 4: Animaciones
```bash
✓ Fade in de página
✓ Slide up de componentes
✓ Bounce del título de éxito
✓ Spin del loader
✓ Hover en botones
```

---

## 📱 Ejemplo de Respuesta del Backend

```json
{
  "mensaje": "Análisis completado",
  "datos": {
    "tipo_rostro": "Ovalado",
    "corte_recomendado": "Pompadour",
    "emocion_detectada": "Feliz",
    "genero_detectado": "Masculino",
    "imagen_generada_url": "https://api.example.com/img/resultado123.jpg"
  }
}
```

---

## 🔧 Modificar la Interfaz

### Cambiar Color Principal
```vue
<!-- En HomeView.vue -->
<style scoped>
.home-container {
  background: linear-gradient(135deg, #TU_COLOR_1 0%, #TU_COLOR_2 100%);
}
</style>
```

### Agregar Más Campos de Resultado
```vue
<!-- En AnalysisResults.vue -->
<div class="result-item">
  <div class="result-label">Tu Nuevo Campo</div>
  <div class="result-value">{{ results.tu_nuevo_campo }}</div>
</div>
```

### Cambiar Servidor Backend
```javascript
// En HomeView.vue, función analyzeImage()
const response = await fetch('http://TU_SERVIDOR:8000/analizar', {
  method: 'POST',
  body: formData,
})
```

---

## 📊 Datos que Fluyen

```
Usuario
  ↓ selecciona imagen
ImageUpload
  ↓ emite evento
HomeView
  ↓ POST /analizar
Backend (FastAPI)
  ↓ responde JSON
HomeView
  ↓ guarda en analysisResults
AnalysisResults
  ↓ renderiza datos
Usuario ve resultado
  ↓ visualiza QR
QRCodeDisplay
  ↓ muestra código
Usuario comparte con peluquero
```

---

## ⚡ Performance

### Tiempos Esperados
```
Carga inicial: ~1-2 segundos
Seleccionar imagen: <100ms
Envío al backend: depende del servidor
Renderizar resultados: ~200-300ms
Generar QR: <100ms
Animaciones totales: <600ms
```

---

## 🎯 Casos de Uso Reales

### Caso 1: Cliente en Barbería
```
1. Cliente accede con QR desde pared
2. Toma foto
3. Ve recomendación
4. Muestra código QR al barbero
5. Barbero compara estilos
```

### Caso 2: Usuario en Casa
```
1. Usuario entra a web
2. Selecciona foto actual
3. Ve qué corte le vendría bien
4. Descarga resultado
5. Va a la barbería con idea clara
```

### Caso 3: Redes Sociales
```
1. Usuario abre app
2. Hace análisis
3. Comparte resultado en Instagram
4. Usa hashtag #CasaAbierta
5. Se viral 📱
```

---

**Versión**: 1.0.0
**Actualizado**: 31 de enero de 2026
