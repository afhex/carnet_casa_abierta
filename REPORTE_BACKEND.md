# ⚙️ REPORTE TÉCNICO: BACKEND

**Proyecto:** Casa Abierta - Análisis Biométrico de Cortes de Cabello  
**Última Actualización:** 6 de Febrero, 2026  
**Versión:** 1.1.0 (Optimizado)

---

## 1. 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.x | Lenguaje base |
| **FastAPI** | 0.115.x | Framework API de alto rendimiento |
| **Uvicorn** | 0.34.x | Servidor ASGI |
| **Pillow (PIL)** | 11.1.x | Procesamiento de imágenes |

---

## 2. 🏛️ Arquitectura del Servidor

API RESTful ligera para análisis biométrico de rostros y recomendación de cortes.

### Estructura de Archivos
```
backend/
├── main.py             # Lógica principal (Optimizado)
├── face_analysis.py    # Análisis biométrico
├── database.py         # Persistencia de datos
├── requirements.txt    # Dependencias
├── uploads/            # Almacenamiento de imágenes
└── history.json        # Log de análisis
```

---

## 3. 🌐 API Endpoints

### `POST /analizar`
**Análisis completo de imagen**

- **Entrada:** `multipart/form-data` (campo: `file`)
- **Proceso:**
  1. Guarda imagen con timestamp
  2. Analiza propiedades faciales
  3. Genera recomendaciones de cortes
  4. Persiste resultados en BD
  5. Retorna JSON con análisis

- **Respuesta Exitosa:**
```json
{
  "mensaje": "Análisis completado exitosamente",
  "datos": {
    "analysis_id": 1,
    "tipo_rostro": "ovalado",
    "corte_recomendado": "Pompadour Clásico",
    "corte_alternativo": "Mohawk Neon",
    "genero_detectado": "masculino",
    "imagen_generada_url": "https://...",
    "imagen_alternativa_url": "https://...",
    "biometrics": {}
  }
}
```

### `GET /`
**Health Check** - Verifica operatividad del backend
- **Respuesta:** `{"status": "Backend API - Casa Abierta operativo"}`

### `GET /historial?limit=100&offset=0`
**Historial paginado de análisis**
- **Parámetros:** `limit`, `offset`
- **Respuesta:** Listado de análisis guardados

### `GET /analisis/{analysis_id}`
**Recupera análisis específico por ID**
- **Respuesta:** Detalles completos del análisis

---

## 4. 🧠 Lógica de Análisis

### Modo de Operación: Simulación Robusta

Para asegurar compatibilidad en todos los entornos de desarrollo (especialmente macOS with Apple Silicon):

1. **Detección de Rostro:** Clasificación de tipos (Ovalado, Redondo, Cuadrado, etc.)
2. **Recomendación Inteligente:** Cortes basados en forma de rostro
3. **Alternativa Lúdica:** Opción decorativa/graciosa como valor agregado
4. **Persistencia Local:** Todos los datos guardados en `uploads/` para auditoría

### Parámetros de Identidad
- `identity_strength`: 0.65-0.85 (controla similitud con imagen original)
- `guidance_scale`: 3.5 (fidelidad de prompt)

---

## 5. 🔒 Seguridad

| Aspecto | Implementación |
|--------|----------------|
| **Privacidad** | Datos locales, sin cloud |
| **Git Ignore** | `uploads/` e `history.json` excluidas |
| **CORS** | Restringido a `localhost:5173`, `localhost:3000` |
| **API Tokens** | Cargados desde variables de entorno |
| **Validación** | Verificación de tipo de archivo |

---

## 6. 📝 Cambios Recientes (6 de Febrero, 2026)

### ✅ Optimizaciones Implementadas

**Código:**
- ✅ Eliminación de imports duplicados
- ✅ Consolidación de comentarios innecesarios
- ✅ Funciones documentadas con docstrings
- ✅ Eliminación de código comentado
- ✅ Refactorización de endpoints

**Seguridad:**
- ✅ Token de Replicate en variables de entorno
- ✅ CORS restringido a puertos conocidos
- ✅ Mejora en manejo de errores

**API:**
- ✅ Respuestas consistentes y documentadas
- ✅ Mejor estructura de datos de retorno
- ✅ Flujo de análisis consolidado
- ✅ Endpoints auxiliares (historial, análisis por ID)

---

## 7. 🚀 Instalación

```bash
# Instalar dependencias
pip install -r backend/requirements.txt

# Configurar variables de entorno (opcional)
export REPLICATE_API_TOKEN="tu-token"

# Ejecutar servidor
cd backend
python main.py

# Disponible en http://localhost:8000
```

---

## 8. 📊 Flujo de Datos

```
Frontend (Vue 3)
    ↓
    └─→ POST /analizar
        ↓
    Backend (FastAPI)
        ├─→ Guardado de imagen
        ├─→ Face Analysis
        ├─→ Haircut Recommendation
        ├─→ Database Persist
        └─→ JSON Response
            ↓
        Frontend muestra resultados
```

---

## 9. 📦 Dependencias Principales

```
fastapi==0.115.x
uvicorn==0.34.x
python-multipart
pillow==11.1.x
httpx
```

---

**Nota:** Para modo de IA real (Replicate API), descomentar llamadas en `generar_imagen()` y proporcionar token válido.
