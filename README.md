# 💇‍♂️ Casa Abierta - Manual del Programador (v1.0)

Bienvenido al Manual del Programador de **Casa Abierta**, una plataforma fullstack de análisis biométrico que utiliza Inteligencia Artificial para recomendar cortes de cabello personalizados.

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una arquitectura **Client-Server** desacoplada:

- **Frontend:** SPA construida con Vue 3, Vite y Tailwind CSS. Se encarga de la captura de imágenes (cámara/upload) y visualización de resultados dinámicos.
- **Backend:** API RESTful con FastAPI (Python). Gestiona la lógica pesada de IA, generación de imágenes con Replicate API, persistencia en SQLite y generación de carnets PDF.

---

## 🧠 Lógica del Backend (Deep Dive)

### 1. Punto de Entrada (`main.py`)

Centraliza los endpoints y coordina los servicios.

- `POST /analizar`: El flujo principal. Recibe la imagen, invoca `detectar_caracteristicas`, llama a Replicate para la imagen recomendada y guarda todo en la DB.
- `POST /generar-carnet`: Toma un `analysis_id` y genera un PDF usando `generar_carnets.py`.
- `GET /historial`: Retorna los análisis previos paginados.

### 2. Análisis Facil (`analisis_facial.py`)

Utiliza la librería **DeepFace** para extraer:

- **Género**: Identificación automática (con override manual mediante el nombre de archivo).
- **Emoción**: Detección de estado de ánimo actual.
- **Geometría**: Medidas de ratios faciales para recomendaciones.

### 3. Generación de Imágenes (IA)

Integración con **Replicate API** usando el modelo `ip-adapter` para mantener la identidad del usuario mientras se aplica el nuevo estilo de cabello.

- **Prompt Engineering**: Se construyen prompts dinámicos basados en el género y el corte seleccionado.

---

## 💾 Persistencia de Datos

Sistema basado en **SQLite** para simplicidad y portabilidad.

### Tabla: `biometric_analyses`

| Columna                  | Tipo     | Descripción                             |
| ------------------------ | -------- | --------------------------------------- |
| `id`                     | INT      | Clave primaria autoincremental          |
| `image_path`             | TEXT     | Ruta a la foto original capturada       |
| `face_shape`             | TEXT     | Forma del rostro detectada              |
| `gender`                 | TEXT     | Género detectado o forzado              |
| `haircut_recommendation` | TEXT     | Nombre del corte sugerido               |
| `generated_image_path`   | TEXT     | Ruta local a la imagen procesada por IA |
| `timestamp`              | DATETIME | Fecha y hora del análisis               |

---

## 🎨 Arquitectura del Frontend

### Componentes Clave (`src/components/`)

1. **`ImageUpload.vue`**: Gestiona el flujo de entrada (File API y acceso a cámara).
2. **`AnalysisResults.vue`**: Orquestador visual que muestra telemetría, imagen IA, QR de descarga y botón para carnet.

### Flujo de Datos

- **Vue Refs**: Se utiliza estado reactivo local en `HomeView.vue` para manejar el ciclo de vida del análisis (Loading -> Success -> Error).
- **Modo Mujer (Emergency Override)**: Si se activa, se renombra el archivo enviado al backend para forzar la detección femenina.

---

## 🛠️ Configuración y Despliegue

### Requisitos

- Node.js 20+
- Python 3.10+

### Variables de Env (`backend/.env`)

```bash
REPLICATE_API_TOKEN=tu_token_aqui
```

### Ejecución

```bash
# Frontend
npm install && npm run dev

# Backend
cd backend && python main.py
```

---

## 🤝 Extensibilidad

Para agregar nuevos cortes:

1. Modificar `analisis_facial.py` -> función `seleccionar_corte`.
2. Añadir el nuevo estilo al diccionario de prompts.

Para modificar el carnet:

1. Editar `backend/templates/carnet_template.png`.
2. Ajustar coordenadas en `backend/generar_carnets.py`.

---

## 👤 Equipo de Desarrollo

**Carrera:** Inteligencia Artificial  
**Semestre:** 4to  
**Proyecto:** Casa Abierta 2026

**Última actualización:** 23 de Febrero, 2026
