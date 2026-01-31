# 🚀 QUICK START - Casa Abierta

## ⚡ En 3 Minutos

### 1️⃣ Instalar
```bash
cd "c:\Users\LENOVO\Desktop\Casa Abierta\carnet_casa_abierta"
npm install
```

### 2️⃣ Ejecutar Frontend
```bash
npm run dev
```
✓ Abre: http://localhost:5173

### 3️⃣ Ejecutar Backend (otro terminal)
```bash
cd backend
pip install fastapi uvicorn python-multipart supabase
uvicorn main:app --reload
```
✓ Abre: http://localhost:8000/docs

---

## 🎬 Demo Inmediato

1. Carga una foto desde tu computadora
2. Espera análisis
3. ¡Ve los resultados! ✨

---

## 📁 Archivos Clave

```
src/
├── views/HomeView.vue              ← Interfaz principal
├── components/
│   ├── ImageUpload.vue             ← Cargar imagen
│   ├── AnalysisResults.vue         ← Mostrar resultados
│   └── QRCodeDisplay.vue           ← Código QR
└── assets/main.css                 ← Estilos
```

---

## 📖 Documentación

- `COMPLETADO.md` - Resumen ejecutivo
- `GUIA_INSTALACION.md` - Instalación completa
- `EJEMPLOS_USO.md` - Casos de uso
- `INDICE.md` - Índice completo

---

## 🎯 Flujo Principal

```
[Cargar Imagen] → [Analizar] → [Ver Resultados] → [Código QR] → [Compartir]
```

---

## 🎨 Vista Previa

### Página Principal
- Hero section con gradiente
- Botones para cargar imagen
- Opción de cámara en móvil

### Resultados
- 4 tarjetas con datos
- Imagen generada
- Código QR generado
- Botones de acción

---

## ✅ Todo Funcionando

✓ Frontend completo
✓ Componentes listos
✓ Estilos responsivos
✓ Animaciones incluidas
✓ Documentación completa

---

## 🔗 URLs Locales

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🚨 Si Algo No Funciona

1. **Puerto en uso**: `npx kill-port 5173` o `npx kill-port 8000`
2. **Módulos faltantes**: `npm install`
3. **Backend no responde**: Asegúrate de `uvicorn main:app --reload`
4. **CORS error**: Verifica que backend esté en `localhost:8000`

---

**¡Disfruta Casa Abierta!** ✂️✨

*Última actualización: 31 de enero de 2026*
