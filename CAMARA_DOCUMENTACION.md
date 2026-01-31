# 📸 Acceso a Cámara - Documentación

## ✨ Nueva Funcionalidad Implementada

El botón **"📸 Usar cámara"** ahora se conecta **REALMENTE** con la cámara del equipo y permite tomar fotografías directamente desde la interfaz.

---

## 🎯 ¿Qué Hace?

### 1. **Acceso a la Cámara**
- Clic en "📸 Usar cámara"
- Se solicita permiso al navegador
- La cámara frontal se activa automáticamente

### 2. **Vista Previa en Vivo**
- Ves la transmisión en directo de la cámara
- Espejo (invertido) como una selfie
- Circle guide para centrar tu rostro

### 3. **Captura de Foto**
- Clic en "📸 Capturar"
- Se toma la foto de la transmisión
- Se convierte a imagen JPEG (0.95 calidad)

### 4. **Usar la Foto**
- La foto se muestra en preview
- Se puede enviar al backend para análisis
- O capturar otra foto si lo deseas

---

## 🔧 Tecnología Utilizada

### **APIs del Navegador**
```javascript
// getUserMedia API - Acceso a dispositivos multimedia
navigator.mediaDevices.getUserMedia({
  video: {
    facingMode: 'user',
    width: { ideal: 1280 },
    height: { ideal: 720 }
  },
  audio: false
})
```

### **Canvas API**
```javascript
// Captura de frame de video
const context = canvas.getContext('2d')
context.drawImage(videoElement, 0, 0)
canvas.toBlob(blob => {
  // Convertir a archivo
})
```

---

## 📱 Flujo Completo

```
Usuario hace clic en "📸 Usar cámara"
           ↓
[Navigator] Solicita permiso
           ↓
Usuario aprueba acceso
           ↓
[Video Element] Cámara se inicia
           ↓
[Face Guide] Muestra círculo de guía
           ↓
Usuario centra su rostro
           ↓
Usuario hace clic en "📸 Capturar"
           ↓
[Canvas] Captura frame actual
           ↓
[Convert] Convierte a JPEG
           ↓
[File] Crea objeto File
           ↓
[Preview] Muestra foto capturada
           ↓
Usuario puede:
  ├─ Enviar al análisis
  └─ Capturar otra foto
```

---

## 🎨 Interfaz Visual

### **Pantalla de Cámara**

```
┌─────────────────────────────┐
│    📹 CÁMARA EN VIVO       │
│                             │
│  ╔═════════════════════╗   │
│  ║                     ║   │
│  ║   TRANSMISIÓN      ║   │
│  ║                     ║   │
│  ║   ○ GUÍA CIRCULAR   ║   │
│  ║                     ║   │
│  ║                     ║   │
│  ╚═════════════════════╝   │
│                             │
│  [📸 Capturar] [✕ Cancelar]│
└─────────────────────────────┘
```

### **Elementos**

| Elemento | Propósito |
|----------|-----------|
| Video Stream | Transmisión en vivo |
| Face Circle | Guía para centrar rostro |
| Capturar | Toma la foto |
| Cancelar | Cierra cámara |

---

## 🔐 Permisos y Seguridad

### **Primer Uso**
```
Navegador muestra:
"¿Casa Abierta quiere acceder a tu cámara?"
[Permitir] [Denegar]
```

### **Importante**
- ✅ Solo acceso a cámara (sin audio)
- ✅ HTTPS requerido en producción
- ✅ Usuario debe aprobar explícitamente
- ✅ Puede revocar permisos en configuración

---

## 💻 Código Principal

### **Iniciar Cámara**
```javascript
const startCamera = async () => {
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
    
    videoElement.value.srcObject = stream
  } catch (err) {
    cameraError.value = err.message
  }
}
```

### **Capturar Foto**
```javascript
const capturePhoto = () => {
  const context = canvasElement.value.getContext('2d')
  const width = videoElement.value.videoWidth
  const height = videoElement.value.videoHeight
  
  canvasElement.value.width = width
  canvasElement.value.height = height
  
  // Espejo (flip)
  context.translate(width, 0)
  context.scale(-1, 1)
  
  // Dibujar
  context.drawImage(videoElement.value, 0, 0)
  
  // Convertir a blob
  canvasElement.value.toBlob((blob) => {
    const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' })
    processImage(file)
  }, 'image/jpeg', 0.95)
}
```

---

## 🎯 Casos de Uso

### **Caso 1: Usuario en Casa**
```
1. Abre Casa Abierta
2. Clic en "📸 Usar cámara"
3. Aprueba permiso
4. Toma una selfie clara
5. Clic en "📸 Capturar"
6. Envía al análisis
7. Obtiene recomendación
```

### **Caso 2: Usuario en Barbería**
```
1. Barbería tiene iPad con Casa Abierta
2. Cliente abre la app
3. Toma foto con cámara frontal
4. Ve recomendación inmediatamente
5. Barbero compara estilos
```

### **Caso 3: Foto de Baja Calidad**
```
1. Usuario toma primera foto
2. No le gusta la calidad
3. Clic en "↻ Capturar otra foto"
4. Vuelve a intentar
5. Obtiene mejor resultado
```

---

## ⚙️ Configuración

### **Resolución Ideal**
```javascript
width: { ideal: 1280 }
height: { ideal: 720 }
```
- 720p es suficiente para análisis de rostros
- Se adapta a cámaras de menor resolución

### **Espejo (Flip)**
```javascript
context.scale(-1, 1)  // Invierte horizontalmente
```
- Simula comportamiento de selfie
- Más intuitivo para usuarios

### **Calidad JPEG**
```javascript
'image/jpeg', 0.95  // 95% de calidad
```
- Buena relación tamaño/calidad
- Suficiente para análisis

---

## 🚨 Manejo de Errores

### **Errores Comunes**

| Error | Causa | Solución |
|-------|-------|----------|
| "NotAllowedError" | Usuario rechazó | Pedir de nuevo |
| "NotFoundError" | Sin cámara | Seleccionar archivo |
| "NotReadableError" | Cámara en uso | Cerrar otra app |
| "OverconstrainedError" | Config no soportada | Valores genéricos |

### **Manejo Automático**
```javascript
catch (err) {
  cameraError.value = `Error: ${err.message}`
  showCamera.value = false
}
```

Se muestra mensaje claro al usuario y cierra la interfaz de cámara.

---

## 📊 Flujo de Datos

```
[Video Stream]
      ↓
[Canvas Element] ← Captura frame
      ↓
[Canvas toBlob()] ← Convierte a JPEG
      ↓
[Blob → File] ← Crea archivo
      ↓
[processImage()] ← Procesa
      ↓
[emit('image-selected')] ← Emite evento
      ↓
[HomeView] ← Recibe en padre
      ↓
[POST /analizar] ← Envía al backend
```

---

## 🎬 Animaciones

### **Face Circle (Pulse)**
```css
@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
  }
}
```
- Efecto de onda pulsante
- Guía visual para usuario

### **Botones**
- Cambio de color en hover
- Sombra elevada
- Transición suave 0.3s

---

## 📱 Responsive Design

### **Desktop (> 768px)**
- Video stream max-width: 500px
- Botones lado a lado
- Circle 200px

### **Móvil (< 768px)**
- Video stream fullwidth
- Botones apilados (fullwidth)
- Circle 150px
- Mejor para landscape

---

## ✅ Compatibilidad

### **Navegadores Soportados**
| Navegador | Soporte |
|-----------|---------|
| Chrome | ✅ Completo |
| Firefox | ✅ Completo |
| Safari | ✅ iOS 11+ |
| Edge | ✅ Completo |

### **Requisitos**
- ✅ HTTPS (en producción)
- ✅ Cámara disponible
- ✅ Permiso del usuario
- ✅ Navegador moderno (2019+)

---

## 🔧 Debugging

### **Ver Permisos Otorgados**
```javascript
navigator.permissions.query({ name: 'camera' })
  .then(result => console.log(result.state))
```

### **Listar Dispositivos**
```javascript
navigator.mediaDevices.enumerateDevices()
  .then(devices => {
    devices.forEach(device => {
      console.log(device.kind, device.label)
    })
  })
```

### **Test en Consola**
```javascript
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    console.log('Cámara accesible')
    stream.getTracks().forEach(track => track.stop())
  })
  .catch(err => console.error('Error:', err))
```

---

## 🎓 Alternativa: Archivo Local

Si los usuarios no desean usar la cámara:

1. Clic en "📁 Seleccionar archivo"
2. Eligen foto del equipo
3. Mismo flujo de análisis

---

## 🚀 Mejoras Futuras

- [ ] Filtros en vivo
- [ ] Efectos de belleza
- [ ] Múltiples ángulos
- [ ] Historial de capturas
- [ ] Descarga de foto
- [ ] Compartir directamente

---

**Versión**: 1.0.0
**Fecha**: 31 de enero de 2026
**Estado**: ✅ Completamente Funcional

Casa Abierta ahora permite capturar fotos reales desde la cámara del equipo. ¡Disfruta! 📸✨
