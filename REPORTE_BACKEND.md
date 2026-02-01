# ⚙️ REPORTE TÉCNICO: BACKEND
**Proyecto: Casa Abierta - Análisis Biométrico de Cortes de Cabello**
**Fecha:** 1 de Febrero, 2026
**Versión:** 1.0.0

---

## 1. 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.x | Lenguaje base |
| **FastAPI** | 0.115.x | Framework de API de alto rendimiento |
| **Uvicorn** | 0.34.x | Servidor ASGI para producción/dev |
| **Pillow (PIL)** | 11.1.x | Procesamiento de imágenes |
| **JSON/OS** | N/A | Manejo de persistencia local |

---

## 2. 🏛️ Arquitectura del Servidor

El backend es una API RESTful ligera diseñada para procesar imágenes rápidamente y devolver análisis estructurados.

### Estructura de Archivos
```bash
backend/
├── main.py             # Punto de entrada de la aplicación (Lógica principal)
├── requirements.txt    # Lista de dependencias
├── uploads/            # (Generado) Almacenamiento local de imágenes recibidas
├── history.json        # (Generado) Log persistente de todos los análisis
└── .venv/              # Entorno virtual de Python aislado
```

---

## 3. 🌐 API Endpoints

### `POST /analizar`
Endpoint principal que recibe la imagen y ejecuta el flujo de análisis.
- **Entrada:** `multipart/form-data` (campo: `file`).
- **Proceso:**
    1.  Lee los bytes de la imagen.
    2.  Guarda una copia física en `backend/uploads/` con timestamp.
    3.  Ejecuta la lógica de análisis (Detección de rostro/corte).
    4.  Genera una imagen de resultado visual usando `Pillow`.
    5.  Guarda el registro en `history.json`.
- **Salida (JSON):**
    ```json
    {
      "mensaje": "Análisis exitoso (Simulado)",
      "datos": {
        "tipo_rostro": "ovalado",
        "corte_recomendado": "Pompadour Clásico",
        "emocion_detectada": "feliz",
        "imagen_generada_url": "data:image/png;base64..."
      }
    }
    ```

### `GET /`
Endpoint de verificación (Health Check).
- **Salida:** `{"status": "Backend corriendo..."}`

---

## 4. 🧠 Lógica de Análisis (Modo Simulación)

Debido a restricciones de hardware y compatibilidad (problemas con TensorFlow/MediaPipe en macOS durante el desarrollo), se implementó una **estrategia de simulación robusta** para la presentación:

1.  **Detección de Rostro:** Simula la clasificación entre 5 tipos (Ovalado, Redondo, Cuadrado, etc.) usando algoritmos aleatorizados para demostración.
2.  **Generación de Imagen:** En lugar de llamar a una API externa costosa, el backend genera dinámicamente una imagen `.png` usando `Pillow`, dibujando las características detectadas y el corte recomendado en un canvas digital.
3.  **Persistencia:** A diferencia de una demo volátil, este sistema guarda **evidencia real** en disco (`uploads/`) para auditoría posterior.

---

## 5. 🔒 Seguridad y Datos

- **Privacidad Local:** No se utiliza base de datos en la nube (Supabase fue desactivado). Todos los datos residen estrictamente en la carpeta del proyecto.
- **Git Ignore:** Se configuró `.gitignore` para excluir las carpetas `uploads/` y `history.json`, garantizando que las fotos de los usuarios nunca se suban al repositorio de código compartido.
- **CORS:** Configurado para permitir peticiones exclusivamente desde el frontend local (`localhost:5173`).
