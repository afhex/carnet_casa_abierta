# 💇‍♂️ Casa Abierta - Análisis Biométrico de Cortes de Cabello

Aplicación fullstack que utiliza análisis biométrico de IA para recomendar cortes de cabello personalizados basados en la forma del rostro del usuario.

---

## 🎯 Características

- ✅ **Análisis biométrico** en tiempo real del tipo de rostro
- ✅ **Recomendaciones inteligentes** de cortes basadas en geometría facial
- ✅ **Interfaz moderna** y responsiva con Vue 3
- ✅ **API RESTful** robusta con FastAPI
- ✅ **Persistencia local** segura de datos
- ✅ **Generación de QR** para compartir resultados

---

## 🛠️ Stack Tecnológico

### Frontend
- **Vue 3** - Framework reactivo
- **Vite** - Build tool rápido
- **Vue Router** - Navegación SPA
- **Tailwind CSS** - Estilos modernos

### Backend
- **Python 3.x** - Lenguaje base
- **FastAPI** - API de alto rendimiento
- **Pillow** - Procesamiento de imágenes

---

## 📋 Requisitos Previos

- **Node.js** 20.19.0 o superior
- **Python** 3.10+
- **npm** o **yarn**

---

## 🚀 Instalación Rápida

### Frontend

```bash
# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build
```

### Backend

```bash
# Instalar dependencias
pip install -r backend/requirements.txt

# Ejecutar servidor
cd backend
python main.py

# El backend estará disponible en http://localhost:8000
```

---

## 📱 Uso

1. **Abrir Frontend:** Navega a `http://localhost:5173`
2. **Cargar imagen:** Sube una foto del rostro o usa la cámara
3. **Esperar análisis:** El sistema analiza la forma del rostro
4. **Ver resultados:** Obtén recomendaciones de cortes personalizadas
5. **Compartir:** Genera un QR para compartir resultados

---

## 📁 Estructura del Proyecto

```
.
├── src/                    # Frontend (Vue 3)
│   ├── components/         # Componentes reutilizables
│   ├── views/              # Páginas principales
│   ├── assets/             # CSS y recursos
│   └── router/             # Configuración de rutas
├── backend/                # Backend (Python/FastAPI)
│   ├── main.py             # Lógica principal de API
│   ├── face_analysis.py    # Análisis biométrico
│   ├── database.py         # Persistencia de datos
│   └── requirements.txt    # Dependencias Python
├── public/                 # Archivos estáticos
└── package.json            # Configuración de dependencias
```

---

## 🔌 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/analizar` | Análisis de imagen |
| `GET` | `/historial` | Histórico paginado |
| `GET` | `/analisis/{id}` | Análisis específico |

---

## 🔒 Seguridad

- Datos almacenados **localmente** (sin servicio cloud)
- CORS configurado para **desarrollo local**
- Tokens sensibles en **variables de entorno**
- Carpetas de datos excluidas del repositorio

---

## 📊 Documentación Técnica

- [Backend Report](./REPORTE_BACKEND.md) - Detalles técnicos del servidor
- [Frontend Report](./REPORTE_FRONTEND.md) - Detalles de la interfaz

---

## 🤝 Contribuir

Este proyecto es parte del currículo académico. Para mejoras:

1. Crear rama feature (`git checkout -b feature/mejora`)
2. Commit cambios (`git commit -m 'Add feature'`)
3. Push (`git push origin feature/mejora`)
4. Abrir Pull Request

---

## 📄 Licencia

Proyecto académico 2026 - Instituto Técnico Superior

---

## 👤 Autores - Estudiantes de Sistemas y Gestión de Data

Carrera: Inteligencia Artificial  
Semestre: 4

---

## 📞 Soporte

Para reportar bugs o solicitar features, abre un issue en el repositorio.

---

**Última actualización:** 6 de Febrero, 2026
