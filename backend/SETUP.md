# Configuración de API Keys y Variables de Entorno

## 🔐 Replicate API Token

El proyecto usa [Replicate](https://replicate.com) para generar imágenes con IA. 

### Pasos para configurar:

1. **Obtén tu token de Replicate:**
   - Ve a https://replicate.com/account/api-tokens
   - Copia tu token personal

2. **Crea el archivo `.env` en la carpeta `backend/`:**
   ```bash
   cd backend
   cp .env.example .env
   ```

3. **Edita el archivo `.env` y agrega tu token:**
   ```
   REPLICATE_API_TOKEN=tu_token_real_aqui
   ```

4. **Reinicia el servidor backend:**
   ```bash
   # Desde la carpeta backend/
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### ⚠️ IMPORTANTE
- **No compartas tu `.env` en GitHub** - está en `.gitignore`
- Cada miembro del equipo debe tener su propio token
- El archivo `.env.example` es solo como referencia (sin token real)

### 🚀 Iniciar la aplicación

Desde la raíz del proyecto:

```bash
# Terminal 1: Backend (Python)
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (Node.js)
npm run dev
```

Accede a:
- Frontend: http://localhost:5173
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
