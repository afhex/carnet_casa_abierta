# 🚀 INICIO RÁPIDO - Casa Abierta

## 📋 Requisitos

- **Node.js** 20.19.0+
- **Python** 3.10+
- **npm** o **yarn**

---

## ⚡ Instalación (5 minutos)

### 1️⃣ Frontend

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

✅ Frontend disponible en: `http://localhost:5173`

### 2️⃣ Backend

```bash
# Instalar dependencias
pip install -r backend/requirements.txt

# Ejecutar servidor
cd backend
python main.py
```

✅ Backend disponible en: `http://localhost:8000`

---

## 🎯 Uso Básico

1. **Abre** `http://localhost:5173` en tu navegador
2. **Sube** una foto o captura desde la cámara
3. **Espera** el análisis (2-3 segundos)
4. **Visualiza** resultados y recomendaciones

---

## 🔧 Configuración (Opcional)

Si deseas usar Replicate API para generación de imágenes:

```bash
# Crear archivo .env en la raíz del proyecto
export REPLICATE_API_TOKEN="tu-token-aqui"

# Obtener token en: https://replicate.com/account/api-tokens
```

---

## 📁 Archivos Importantes

| Archivo | Descripción |
|---------|------------|
| `README.md` | Guía completa del proyecto |
| `REPORTE_BACKEND.md` | Detalles técnicos del servidor |
| `REPORTE_FRONTEND.md` | Detalles de la interfaz |
| `CAMBIOS.md` | Registro de optimizaciones |
| `.env.example` | Plantilla de variables de entorno |

---

## 🐛 Troubleshooting

### Error: "Cannot find module 'vue'"
```bash
# Reinstalar dependencias
rm -rf node_modules
npm install
```

### Error: "Address already in use" (Puerto 5173)
```bash
# El servidor ya está corriendo en otro terminal.
# Cambia el puerto:
npm run dev -- --port 5174
```

### Error: "Connection refused" Backend
```bash
# Verifica que backend esté corriendo:
curl http://localhost:8000/

# Si no está:
cd backend
python main.py
```

### Error: Python dependencies
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar requerimientos
pip install -r backend/requirements.txt --force-reinstall
```

---

## 📊 API Endpoints

```bash
# Health check
curl http://localhost:8000/

# Analizar imagen (FormData)
curl -X POST http://localhost:8000/analizar \
  -F "file=@/ruta/a/imagen.jpg"

# Ver historial
curl http://localhost:8000/historial

# Ver análisis específico
curl http://localhost:8000/analisis/1
```

---

## 🏗️ Build para Producción

```bash
# Frontend
npm run build      # Genera carpeta 'dist'
npm run preview    # Previsualiza el build

# Backend (recomendado con Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 backend.main:app
```

---

## 🧹 Comandos Útiles

```bash
# Linting
npm run lint

# Ver estructura del proyecto
tree -I 'node_modules|__pycache__'

# Limpiar cachés
rm -rf .vite
rm -rf backend/__pycache__

# Ver logs del backend
tail -f backend/uploads/  # Verificar imágenes guardadas
```

---

## 📞 Contacto / Soporte

- **Autor:** Alejandro Vaca
- **Email:** [tu-email]
- **Institución:** Instituto Técnico Superior
- **Carrera:** Inteligencia Artificial - 4to Semestre

---

## 📚 Documentación Completa

Para más detalles, consulta:
- [README.md](./README.md) - Descripción general
- [REPORTE_BACKEND.md](./REPORTE_BACKEND.md) - API y arquitectura
- [REPORTE_FRONTEND.md](./REPORTE_FRONTEND.md) - Componentes e interfaz
- [CAMBIOS.md](./CAMBIOS.md) - Historial de optimizaciones

---

**¡Listo! El sistema ya está funcionando.** 🎉
