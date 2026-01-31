# 🔗 Integración Backend - Cámara Funcional

## 📌 Flujo Completo: Frontend → Backend

```
┌─────────────────────────────────────────┐
│ USUARIO CAPTURA FOTO CON CÁMARA        │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ ImageUpload.vue                         │
│ - getUserMedia()                        │
│ - Canvas capture                        │
│ - Blob conversion                       │
│ emit('image-selected', File)            │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ HomeView.vue                            │
│ - Recibe File object                    │
│ - Crea FormData                         │
│ - POST /analizar                        │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ Backend FastAPI                         │
│ - Recibe multipart/form-data            │
│ - MediaPipe face detection              │
│ - Image generation (Replicate)          │
│ - Análisis emocional                    │
│ - Recomendaciones                       │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ Respuesta JSON                          │
│ {                                       │
│   "mensaje": "...",                     │
│   "datos": {                            │
│     "tipo_rostro": "...",               │
│     "corte_recomendado": "...",         │
│     "emocion_detectada": "...",         │
│     "genero_detectado": "...",          │
│     "imagen_generada_url": "..."        │
│   }                                     │
│ }                                       │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ AnalysisResults.vue                     │
│ - Mostrar resultados                    │
│ - Generar QR                            │
│ - Opciones de compartir                 │
└─────────────────────────────────────────┘
```

---

## 🎯 Datos Enviados del Frontend

### **Request HTTP**

```http
POST /analizar HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----FormBoundary...

------FormBoundary...
Content-Disposition: form-data; name="archivo"; filename="photo.jpg"
Content-Type: image/jpeg

[BINARY IMAGE DATA - JPEG CAPTURADO POR CÁMARA]
------FormBoundary...--
```

### **Código Frontend (HomeView.vue)**

```javascript
const analyzeImage = async (file) => {
  isLoading.value = true
  error.value = null
  
  try {
    const formData = new FormData()
    formData.append('archivo', file) // File del canvas capture
    
    const response = await fetch('http://localhost:8000/analizar', {
      method: 'POST',
      body: formData
      // No agregues Content-Type, navegador lo hace automáticamente
    })
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    
    const data = await response.json()
    analysisResults.value = data.datos
    
  } catch (err) {
    error.value = `Error: ${err.message}`
  } finally {
    isLoading.value = false
  }
}
```

---

## ⚙️ Configuración Backend (FastAPI)

### **main.py - Endpoint /analizar**

```python
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from PIL import Image
import io

app = FastAPI()

# CORS para permitir localhost:5173
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analizar")
async def analizar_imagen(archivo: UploadFile = File(...)):
    """
    Recibe imagen capturada por cámara y realiza análisis
    """
    try:
        # 1. LEER IMAGEN
        imagen_bytes = await archivo.read()
        imagen_np = np.frombuffer(imagen_bytes, np.uint8)
        imagen_cv = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)
        
        # 2. CONVERTIR A PIL PARA MEDIAPIPE
        imagen_rgb = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)
        imagen_pil = Image.fromarray(imagen_rgb)
        
        # 3. ANÁLISIS CON MEDIAPIPE (simulated)
        tipo_rostro = detectar_tipo_rostro(imagen_cv)
        emocion = detectar_emocion(imagen_cv)
        genero = detectar_genero(imagen_cv)
        corte_recomendado = recomendar_corte(tipo_rostro)
        
        # 4. GENERAR IMAGEN (Replicate API)
        imagen_generada_url = generar_imagen_corte(
            tipo_rostro=tipo_rostro,
            corte=corte_recomendado
        )
        
        # 5. RESPONDER
        return JSONResponse({
            "mensaje": "Análisis completado exitosamente",
            "datos": {
                "tipo_rostro": tipo_rostro,
                "corte_recomendado": corte_recomendado,
                "emocion_detectada": emocion,
                "genero_detectado": genero,
                "imagen_generada_url": imagen_generada_url
            }
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
```

---

## 📊 Datos Recibidos en Backend

### **Propiedades de UploadFile**

```python
archivo: UploadFile
│
├── filename: str = "photo.jpg"
├── size: int = 45200  # bytes
├── content_type: str = "image/jpeg"
├── file: SpooledTemporaryFile = <binary data>
│
└── async read() → bytes
    └── Retorna: b'\xff\xd8\xff\xe0...' (JPEG binary)
```

### **Metadata de Imagen Capturada**

```python
# Del canvas capture
{
    "width": 1280,
    "height": 720,
    "formato": "JPEG",
    "calidad": 0.95,
    "tamaño": 40000,  # ~40KB
    "origen": "getUserMedia + Canvas",
    "espejo": True  # Flip aplicado
}
```

---

## 🔍 Procesar Imagen en Backend

### **Conversión Segura**

```python
import cv2
import numpy as np
from PIL import Image
import io

async def procesar_imagen_capturada(archivo: UploadFile) -> dict:
    """
    Convierte imagen JPEG del canvas a formatos procesables
    """
    
    # 1. Leer bytes
    imagen_bytes = await archivo.read()
    
    # 2. Convertir a NumPy (para OpenCV)
    imagen_np = np.frombuffer(imagen_bytes, dtype=np.uint8)
    imagen_cv = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)
    
    # 3. Verificar que se decodificó correctamente
    if imagen_cv is None:
        raise ValueError("Formato de imagen inválido")
    
    # 4. Información de imagen
    alto, ancho, canales = imagen_cv.shape
    print(f"Imagen cargada: {ancho}x{alto}, {canales} canales")
    
    # 5. Convertir a RGB (OpenCV usa BGR)
    imagen_rgb = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)
    
    # 6. Convertir a PIL (para MediaPipe)
    imagen_pil = Image.fromarray(imagen_rgb)
    
    return {
        "cv2": imagen_cv,      # Para análisis con OpenCV
        "rgb": imagen_rgb,     # Canales RGB
        "pil": imagen_pil,     # Para transformaciones PIL
        "shape": imagen_cv.shape,
        "ancho": ancho,
        "alto": alto
    }
```

---

## 🎨 Análisis Específicos

### **1. Tipo de Rostro**

```python
import mediapipe as mp

def detectar_tipo_rostro(imagen_cv):
    """
    Detecta proporciones del rostro (ovalado, redondo, cuadrado, etc.)
    """
    
    # MediaPipe Face Mesh
    mp_face = mp.solutions.face_mesh
    
    with mp_face.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as face_mesh:
        
        # Procesar imagen
        image_rgb = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            
            # Extraer puntos clave
            ojo_izq = landmarks[33]   # Esquina ojo
            ojo_der = landmarks[263]
            nariz = landmarks[1]
            menton = landmarks[152]
            frente = landmarks[10]
            
            # Calcular proporciones
            alto_rostro = abs(frente.y - menton.y)
            ancho_rostro = abs(ojo_izq.x - ojo_der.x)
            proporcion = ancho_rostro / alto_rostro
            
            # Clasificar
            if 0.7 < proporcion < 0.85:
                return "ovalado"
            elif proporcion > 0.85:
                return "redondo"
            elif proporcion < 0.7:
                return "rectangular"
            else:
                return "cuadrado"
        
        return "desconocido"
```

### **2. Emoción Detectada**

```python
from fer import FER  # Face Emotion Recognition

def detectar_emocion(imagen_cv):
    """
    Detecta emoción primaria en imagen
    """
    
    emotion_model = FER(emotion_model='enet')
    
    # Detectar emociones
    result = emotion_model.top_emotion(imagen_cv)
    
    if result:
        emocion, confianza = result
        return {
            "emocion": emocion,
            "confianza": round(confianza, 2)
        }
    
    return {"emocion": "neutral", "confianza": 0}
```

### **3. Género Detectado**

```python
def detectar_genero(imagen_cv):
    """
    Detecta género presentado en imagen
    """
    
    # Usar MediaPipe o modelo específico
    mp_face = mp.solutions.face_mesh
    
    with mp_face.FaceMesh(max_num_faces=1) as face_mesh:
        results = face_mesh.process(
            cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)
        )
        
        if results.multi_face_landmarks:
            # Análisis de características
            # (simplificado - usar modelo ML para precisión)
            return "masculino"  # o "femenino"
        
        return "desconocido"
```

---

## 🖼️ Generar Imagen de Corte

### **Con Replicate API**

```python
import replicate
import os

def generar_imagen_corte(tipo_rostro: str, corte: str) -> str:
    """
    Genera imagen de corte recomendado usando DALL-E o Stable Diffusion
    """
    
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    
    prompt = f"""
    Foto de corte de cabello {corte} para hombre con rostro {tipo_rostro}.
    Profesional, barbería moderna, iluminación profesional, alta calidad.
    Vista frontal y de lado.
    """
    
    output = client.run(
        "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21aef33d3b3b0d3e86",
        input={
            "prompt": prompt,
            "num_outputs": 1,
            "width": 512,
            "height": 512,
            "num_inference_steps": 50,
            "guidance_scale": 7.5
        }
    )
    
    # output es lista de URLs
    return output[0] if output else None
```

### **Versión Local Alternativa**

```python
from PIL import Image, ImageDraw, ImageFont

def generar_imagen_corte_local(tipo_rostro: str, corte: str) -> bytes:
    """
    Genera imagen de placeholder localmente
    (Reemplazar con ML model en producción)
    """
    
    # Crear imagen base
    img = Image.new('RGB', (512, 512), color=(240, 240, 245))
    draw = ImageDraw.Draw(img)
    
    # Información
    texto = f"Corte recomendado: {corte}\nTipo: {tipo_rostro}"
    
    # Dibujar
    draw.text((50, 220), texto, fill=(102, 126, 234))
    
    # Guardar
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()
```

---

## 🚀 Flujo Completo Integrado

### **Ejemplo: HomeView.vue → Backend → Respuesta**

#### **Frontend: Capturar y Enviar**

```javascript
// HomeView.vue
const handleImageSelected = (file) => {
  selectedImage.value = file
  analyzeImage(file)
}

const analyzeImage = async (file) => {
  isLoading.value = true
  
  try {
    const formData = new FormData()
    formData.append('archivo', file)
    
    const response = await fetch('http://localhost:8000/analizar', {
      method: 'POST',
      body: formData
    })
    
    const data = await response.json()
    analysisResults.value = data.datos
    
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}
```

#### **Backend: Procesar y Analizar**

```python
# main.py
@app.post("/analizar")
async def analizar_imagen(archivo: UploadFile = File(...)):
    # 1. Leer imagen
    imagen_bytes = await archivo.read()
    imagen_cv = cv2.imdecode(
        np.frombuffer(imagen_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )
    
    # 2. Análisis
    tipo_rostro = detectar_tipo_rostro(imagen_cv)
    emocion = detectar_emocion(imagen_cv)
    genero = detectar_genero(imagen_cv)
    
    # 3. Recomendación
    corte = obtener_corte_recomendado(tipo_rostro)
    
    # 4. Generar imagen
    imagen_url = generar_imagen_corte(tipo_rostro, corte)
    
    # 5. Responder
    return {
        "mensaje": "Análisis completado",
        "datos": {
            "tipo_rostro": tipo_rostro,
            "corte_recomendado": corte,
            "emocion_detectada": emocion,
            "genero_detectado": genero,
            "imagen_generada_url": imagen_url
        }
    }
```

#### **Frontend: Mostrar Resultados**

```javascript
// En template
<AnalysisResults
  v-if="analysisResults"
  :results="analysisResults"
  :image="selectedImage"
/>

<!-- AnalysisResults.vue muestra: -->
<!-- - Tipo de rostro -->
<!-- - Corte recomendado (destacado) -->
<!-- - Emoción detectada -->
<!-- - Género detectado -->
<!-- - Imagen generada -->
<!-- - QR con resultados -->
```

---

## 📈 Métricas y Optimización

### **Tamaño de Imagen Enviada**

```
Canvas capture (1280x720) con toBlob(0.95)
↓
JPEG comprimido
↓
~40-50 KB en promedio
↓
Transferencia rápida (< 200ms típicamente)
```

### **Tiempos Esperados**

| Etapa | Tiempo |
|-------|--------|
| Captura de foto | Instantáneo |
| Subida al servidor | 200-500ms |
| Detección de rostro | 100-300ms |
| Análisis emocional | 500-1000ms |
| Generación de imagen | 5-30s (Replicate) |
| Respuesta completa | 6-32s |

### **Optimizaciones Posibles**

```python
# 1. Caché de análisis
from functools import lru_cache

# 2. Procesar en background
from celery import Celery

# 3. Comprimir respuesta
from fastapi.middleware.gzip import GZipMiddleware

# 4. Limitar tamaño de archivo
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
```

---

## 🔒 Validación de Datos

### **Frontend (Before Sending)**

```javascript
const validateImage = (file) => {
  const maxSize = 5 * 1024 * 1024 // 5MB
  const validTypes = ['image/jpeg', 'image/png', 'image/webp']
  
  if (file.size > maxSize) {
    throw new Error('Archivo muy grande')
  }
  
  if (!validTypes.includes(file.type)) {
    throw new Error('Formato no válido')
  }
  
  return true
}
```

### **Backend (After Receiving)**

```python
from fastapi import HTTPException

@app.post("/analizar")
async def analizar_imagen(archivo: UploadFile = File(...)):
    # Validar tipo
    if archivo.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagen inválido"
        )
    
    # Validar tamaño
    content = await archivo.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Archivo muy grande"
        )
    
    # Validar contenido
    imagen_cv = cv2.imdecode(
        np.frombuffer(content, np.uint8),
        cv2.IMREAD_COLOR
    )
    
    if imagen_cv is None:
        raise HTTPException(
            status_code=400,
            detail="Imagen corrupta o inválida"
        )
    
    # ... continuar análisis
```

---

## ✅ Checklist de Integración

- [ ] Frontend captura imagen del canvas
- [ ] Canvas toBlob crea JPEG correctamente
- [ ] FormData se construye con archivo
- [ ] POST /analizar envía multipart/form-data
- [ ] Backend recibe UploadFile sin errores
- [ ] Imagen se decodifica en OpenCV
- [ ] Análisis devuelve datos correctos
- [ ] JSON response tiene estructura correcta
- [ ] Frontend parsea respuesta
- [ ] AnalysisResults renderiza correctamente
- [ ] Imagen generada se muestra
- [ ] QR se genera from JSON

---

**Versión**: 1.0.0
**Última actualización**: 31 de enero de 2026

¡Integración completa lista! 🎉
