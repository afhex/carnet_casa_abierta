# 🎬 QUICK START - Cámara Funcional

## ⚡ En 30 Segundos

### **Paso 1: Inicia Vite** (Terminal)
```bash
cd c:\Users\LENOVO\Desktop\Casa\ Abierta\carnet_casa_abierta
npm run dev
```

**Debería ver:**
```
➜  Local:   http://localhost:5173/
```

---

### **Paso 2: Abre el Navegador**
```
URL: http://localhost:5173
```

**Debería ver:**
- ✅ Página de Casa Abierta carga
- ✅ Botón "📸 Usar cámara" visible

---

### **Paso 3: Prueba Cámara**

1. Clic en **"📸 Usar cámara"**
2. Navegador muestra: *"¿Casa Abierta quiere acceder a tu cámara?"*
3. Clic en **"[Permitir]"**
4. ¡Ves tu rostro en la pantalla! 📷
5. Clic en **"📸 Capturar"**
6. ¡Foto tomada! ✨

---

## 🎯 Pantalla de Cámara

```
┌─────────────────────────────┐
│   📹 TU ROSTRO (EN VIVO)    │
│                             │
│  ╔═══════════════════════╗ │
│  ║                       ║ │
│  ║      CÁMARA VIDEO    ║ │
│  ║                       ║ │
│  ║   ◯ CENTRA AQUÍ       ║ │
│  ║   (círculo pulsante)  ║ │
│  ║                       ║ │
│  ╚═══════════════════════╝ │
│                             │
│  [📸 Capturar] [✕ Cancelar] │
└─────────────────────────────┘
```

---

## ✨ Botones

| Botón | Acción |
|-------|--------|
| **📸 Capturar** | Toma la foto |
| **✕ Cancelar** | Cierra cámara |
| **📸 Capturar otra foto** | Vuelve a intentar |
| **🔍 Analizar imagen** | Envía al backend |

---

## 🎨 Lo Que Verás

### **Fase 1: Pantalla Inicial**
```
CASA ABIERTA
━━━━━━━━━━━━━━━━
[📸 Seleccionar foto]    
           o            
[📸 Usar cámara]         
```

### **Fase 2: Cámara Activa**
```
TIENES ACCESO A LA CÁMARA
━━━━━━━━━━━━━━━━━━━━━━━━
[    Video en vivo      ]
[    Circle guide       ]
[Capturar] [Cancelar]
```

### **Fase 3: Foto Capturada**
```
FOTO LISTA
━━━━━━━━━━━━━━━━
[   Tu foto aquí   ]

[Otra foto] [Analizar]
```

---

## 🔐 Permiso de Cámara

**Primera vez:**
```
🔔 Casa Abierta quiere acceder a tu cámara

[Permitir]  [Denegar]
  ↑ Click aquí
```

**Después:**
- ✅ Se recuerda tu decisión
- ✅ Acceso automático
- ✅ Puedes revocar en ajustes

---

## 📱 En Móvil

### **iOS (iPhone)**
1. Abre Safari
2. URL: `http://192.168.1.X:5173`*
3. Clic en "📸 Usar cámara"
4. Permite acceso
5. ¡Captura! 📸

\* Reemplaza X con tu IP

### **Android**
1. Abre Chrome
2. URL: `http://192.168.1.X:5173`*
3. Clic en "📸 Usar cámara"
4. Permite acceso
5. ¡Captura! 📸

\* Reemplaza X con tu IP

---

## 🐛 Si Algo Va Mal

### **"Permiso Denegado"**
- Abre DevTools (F12)
- Settings → Privacy → Camera
- Cambia a "Ask"
- Recarga F5
- Intenta de nuevo

### **"Cámara No Encontrada"**
- Verifica que tu cámara funciona
- Intenta en otra app (ej: Zoom)
- Reinicia el navegador

### **"Video Negro"**
- Verifica iluminación
- Limpia lente cámara
- Prueba en otro lugar con luz

### **No Ves Nada"**
- Abre DevTools: F12
- Consola → busca errores
- Compara con GUIA_PRUEBA_CAMARA.md

---

## 📚 Documentación

Si quieres saber más, lee:

1. **RESUMEN_CAMARA_FUNCIONAL.md** - Resumen ejecutivo
2. **CAMARA_DOCUMENTACION.md** - Guía técnica
3. **GUIA_PRUEBA_CAMARA.md** - Checklist validación
4. **INTEGRACION_BACKEND_CAMARA.md** - Backend

---

## 🎬 Ejemplo Visual Paso a Paso

### **1. Abre Casa Abierta**
```
http://localhost:5173
     ↓
[Página carga]
```

### **2. Clic "Usar cámara"**
```
[📸 Usar cámara]
     ↓
[Navegador pide permiso]
```

### **3. Permite Acceso**
```
"¿Permitir acceso a cámara?"
[Permitir] ← Clic aquí
     ↓
[Cámara inicia]
```

### **4. Ves Tu Rostro**
```
Tu cara en la pantalla
Espejada (como selfie)
     ↓
[Clic Capturar]
```

### **5. Foto Tomada**
```
Canvas dibuja frame
Conversión JPEG
     ↓
[Preview visible]
```

---

## ⚙️ Configuración Técnica

### **Lo que sucede internamente**

```javascript
// 1. Solicitar acceso
navigator.mediaDevices.getUserMedia({
  video: { facingMode: 'user' }
})

// 2. Mostrar video
videoElement.srcObject = stream

// 3. Capturar frame
canvas.drawImage(video, 0, 0)

// 4. Convertir a archivo
canvas.toBlob(blob => {
  // Enviar al padre (HomeView)
})
```

---

## 📊 Compatibilidad Rápida

| Dispositivo | Navegador | ✅ Funciona |
|-------------|-----------|------------|
| PC/Laptop | Chrome | ✅ |
| PC/Laptop | Firefox | ✅ |
| Mac | Safari | ✅ |
| iPhone | Safari | ✅ |
| Android | Chrome | ✅ |

---

## 🎓 Tips Pro

### **Mejor Calidad**
- ✅ Buena iluminación frontal
- ✅ Centra tu rostro en el círculo
- ✅ Mantén la cámara estable

### **Rápido y Fácil**
- ✅ Clic directo en "📸 Capturar"
- ✅ No es necesario esperar
- ✅ Foto instantánea

### **Múltiples Intentos**
- ✅ Si no gusta → "📸 Capturar otra foto"
- ✅ Sin límite de intentos
- ✅ Mismo dispositivo

---

## 🚀 Próximo Paso

Cuando termines de probar:

```bash
# Terminal nuevo
python -m uvicorn main:app --reload

# Debería mostrar:
# INFO:     Application startup complete
# Uvicorn running on http://127.0.0.1:8000
```

Luego prueba:
1. Captura foto
2. Clic "Analizar"
3. ¡Obtén recomendación! 🎉

---

## 💡 Atajos

### **Navegador**
- `F5` - Recargar página
- `F12` - DevTools (para debugging)
- `Ctrl+Shift+Del` - Limpiar caché

### **Terminal**
- `Ctrl+C` - Detener servidor
- `npm run dev` - Iniciar Vite

---

## 🎯 El Flujo Completo

```
CASA ABIERTA
      ↓
[📸 Usar cámara]
      ↓
[Cámara funciona]
      ↓
[Captura foto]
      ↓
[Preview visible]
      ↓
[Analizar]
      ↓
[Backend procesa]
      ↓
[Resultados mostrados]
      ↓
🎉 ¡COMPLETADO!
```

---

## ✅ Checklist

- [ ] Terminal abierta
- [ ] `npm run dev` ejecutado
- [ ] Navegador en http://localhost:5173
- [ ] Clic en "📸 Usar cámara"
- [ ] Permiso otorgado
- [ ] Video visible
- [ ] Clic en "📸 Capturar"
- [ ] Preview aparece
- [ ] ¡Funciona! 🎉

---

**¡Eso es todo! 🚀**

Casa Abierta tiene cámara funcional lista para usar.

📸 ¡Diviértete capturando fotos! ✨
