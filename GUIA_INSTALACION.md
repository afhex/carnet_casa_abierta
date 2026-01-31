# 🚀 Guía de Instalación y Despliegue

## 📦 Requisitos Previos

```bash
Node.js: v20.19.0 o superior
npm: v10.0.0 o superior
Python: 3.9+ (para backend)
pip: últimas versiones
```

Verifica tus versiones:
```bash
node --version
npm --version
python --version
pip --version
```

---

## 🏃 Instalación Rápida (Local)

### 1. **Navegar al Proyecto**
```bash
cd "c:\Users\LENOVO\Desktop\Casa Abierta\carnet_casa_abierta"
```

### 2. **Instalar Dependencias Frontend**
```bash
npm install
```

Esto instalará:
- `vue@3.5.26`
- `vue-router@4.6.4`
- `qrcode.vue@3.6.0`
- `vite@7.3.1`
- `@supabase/supabase-js`
- ESLint y dev tools

### 3. **Instalar Dependencias Backend (en otro terminal)**
```bash
cd backend
pip install fastapi uvicorn python-multipart supabase python-dotenv
```

### 4. **Configurar Variables de Entorno**

#### Backend (.env)
```bash
# backend/.env
SUPABASE_URL=https://tjzryawsqbhhwvkfquzb.supabase.co
SUPABASE_KEY=tu_clave_api_aqui
```

**⚠️ IMPORTANTE**: Nunca commits las credenciales. Usa `.env` local.

### 5. **Ejecutar el Proyecto**

#### Terminal 1 - Frontend
```bash
npm run dev
```
Abre: `http://localhost:5173`

#### Terminal 2 - Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```
Abre: `http://localhost:8000/docs` (Swagger UI)

---

## 📋 Scripts Disponibles

### Frontend
```bash
npm run dev          # Inicia servidor de desarrollo
npm run build        # Compila para producción
npm run preview      # Previsualiza la compilación
npm run lint         # Ejecuta ESLint con --fix
```

### Backend
```bash
# En carpeta backend/
uvicorn main:app --reload          # Desarrollo
uvicorn main:app --port 8000       # Producción (requiere PM2)
```

---

## 🛠️ Configuración Detallada

### Vite Config (vite.config.js)
```javascript
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
```

### ESLint Config (eslint.config.js)
Ya está configurado. Para limpiar código:
```bash
npm run lint
```

---

## 🔌 Configuración de Backend

### FastAPI (backend/main.py)

El servidor debe estar en `http://localhost:8000` con:

#### Endpoints Esperados
```
GET  /                    # Health check
POST /analizar           # Análisis de imagen
```

#### Ejemplo de Petición
```bash
curl -X POST "http://localhost:8000/analizar" \
  -F "file=@imagen.jpg" \
  -H "Accept: application/json"
```

#### Ejemplo de Respuesta
```json
{
  "mensaje": "Análisis completado",
  "datos": {
    "tipo_rostro": "Ovalado",
    "corte_recomendado": "Fade Bajo",
    "emocion_detectada": "Neutral",
    "genero_detectado": "Masculino",
    "imagen_generada_url": "https://..."
  }
}
```

---

## 🌐 Despliegue en Producción

### Opción 1: Vercel (Frontend)

```bash
# 1. Instalar CLI de Vercel
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel --prod
```

### Opción 2: Netlify (Frontend)

```bash
# 1. Build
npm run build

# 2. Deploy carpeta "dist" a Netlify
# O usa drag & drop en netlify.com
```

### Opción 3: Heroku (Backend)

```bash
# 1. Login
heroku login

# 2. Crear app
heroku create nombre-app

# 3. Configurar variables
heroku config:set SUPABASE_URL=xxx
heroku config:set SUPABASE_KEY=xxx

# 4. Deploy
git push heroku main
```

### Opción 4: Railway (Backend)

1. Conectar repo GitHub
2. Railway detecta `requirements.txt`
3. Configurar variables
4. Deploy automático

---

## 📱 Variables de Entorno

### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Casa Abierta
```

En componente:
```javascript
const apiUrl = import.meta.env.VITE_API_URL
```

### Backend (.env)
```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
CORS_ORIGINS=http://localhost:5173,https://tudominio.com
```

---

## 🐳 Docker (Opcional)

### Dockerfile Frontend
```dockerfile
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### Dockerfile Backend
```dockerfile
FROM python:3.11
WORKDIR /app
COPY backend .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Docker Compose
```yaml
version: '3'
services:
  frontend:
    build: .
    ports:
      - "3000:3000"
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      SUPABASE_URL: ${SUPABASE_URL}
      SUPABASE_KEY: ${SUPABASE_KEY}
```

---

## 🧪 Testing

### Frontend
```bash
# Linting
npm run lint

# Pruebas manuales
npm run dev
# Abre en navegador y prueba manualmente
```

### Backend
```bash
# Swagger UI (automático)
http://localhost:8000/docs

# Try it out
# Sube una imagen desde la interfaz
```

---

## 🔒 Seguridad en Producción

### Checklist
- [ ] Mover credenciales a variables de entorno
- [ ] Usar HTTPS (certificado SSL)
- [ ] Configurar CORS específico (no `["*"]`)
- [ ] Implementar rate limiting
- [ ] Validar tipos de archivo en backend
- [ ] Comprimir imágenes antes de procesar
- [ ] Usar headers de seguridad (HSTS, CSP)
- [ ] Implementar autenticación
- [ ] Usar base de datos en producción
- [ ] Backup automático de datos

### CORS Seguro
```python
# backend/main.py
ALLOWED_ORIGINS = [
    "https://tudominio.com",
    "https://www.tudominio.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## 📊 Monitoreo

### Frontend (Vercel)
- Dashboard automático en vercel.com
- Logs en tiempo real
- Métricas de performance

### Backend (Heroku/Railway)
```bash
# Ver logs
heroku logs --tail

# Métricas
heroku metrics -d
```

---

## 🐛 Troubleshooting

### Problema: "Port 8000 already in use"
```bash
# Encontrar proceso
netstat -ano | findstr :8000

# Matar proceso (Windows)
taskkill /PID <PID> /F

# O usar otro puerto
uvicorn main:app --port 8001
```

### Problema: "CORS error in browser"
- Verifica que backend esté corriendo en `http://localhost:8000`
- Comprueba que CORS esté habilitado
- Limpia caché del navegador

### Problema: "Image upload fails"
- Verifica tamaño máximo de archivo
- Confirma que el formato es JPG/PNG/WebP
- Revisa permisos de carpeta temporal

### Problema: "Module not found"
```bash
# Borra node_modules y reinstala
rm -r node_modules
npm install
```

---

## 📞 Contacto y Soporte

**Desarrollador**: Tu Nombre
**Email**: tu@email.com
**GitHub**: github.com/tuuser

---

## 📝 Changelog

### v1.0.0 (31 de enero, 2026)
- ✅ Interfaz frontend completa
- ✅ Componentes de análisis
- ✅ Generador de QR
- ✅ Diseño responsivo
- ✅ Documentación

### v0.1.0 (Inicial)
- Backend básico con FastAPI
- Integración Supabase

---

**Última actualización**: 31 de enero de 2026
**Versión**: 1.0.0
