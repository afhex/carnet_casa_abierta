# 🔧 Solución de Problemas - Windows

## ❌ Problema: "pip no se reconoce"

### Solución 1: Usar python -m pip (RECOMENDADO)

En PowerShell:
```powershell
python -m pip install fastapi uvicorn python-multipart supabase
```

O más específicamente:
```powershell
python.exe -m pip install -r requirements.txt
```

---

## ❌ Problema: "python no se encuentra"

### Solución A: Verificar que Python está instalado

```powershell
# En PowerShell:
Get-Command python
# Debería mostrar: Application     python.exe
```

### Solución B: Usar el script automático

En la carpeta `backend/`, ejecuta:
```powershell
.\instalar.bat
```

Este script automáticamente:
- Actualiza pip
- Instala todos los requisitos

### Solución C: Instalación manual

1. Descarga Python desde https://www.python.org/downloads/
2. Durante la instalación, **marca**: "Add Python to PATH"
3. Reinicia PowerShell
4. Intenta de nuevo

---

## ❌ Problema: "npm run dev" no funciona

### Solución:

```powershell
# Verifica que estás en la carpeta correcta
cd "c:\Users\LENOVO\Desktop\Casa Abierta\carnet_casa_abierta"

# Instala dependencias
npm install

# Ejecuta
npm run dev
```

---

## ❌ Problema: Error "Invalid end tag" en App.vue

### Solución:

Ya está reparado. El archivo fue reconstruido. Si aún hay problemas:

```powershell
# Limpiar y reinstalar
rm -r node_modules
npm install

# Ejecutar de nuevo
npm run dev
```

---

## ✅ Pasos Correctos para Windows

### 1. Frontend Setup
```powershell
cd "c:\Users\LENOVO\Desktop\Casa Abierta\carnet_casa_abierta"
npm install
npm run dev
```

### 2. Backend Setup (en otro terminal)
```powershell
cd "c:\Users\LENOVO\Desktop\Casa Abierta\carnet_casa_abierta\backend"

# Opción A: Script automático
.\instalar.bat

# Opción B: Manual
python.exe -m pip install -r requirements.txt

# Ejecutar servidor
python.exe -m uvicorn main:app --reload
```

---

## 🔍 Verificación

Después de instalar, verifica:

### Frontend
```powershell
npm --version
node --version
```

Debería mostrar versiones (ej: npm 10.x, node 20.x)

### Backend
```powershell
python.exe -m pip list
```

Debería mostrar:
- fastapi
- uvicorn
- python-multipart
- supabase

---

## 🚀 Comandos Rápidos

```powershell
# Frontend - Terminal 1
cd "c:\Users\LENOVO\Desktop\Casa Abierta\carnet_casa_abierta"
npm run dev

# Backend - Terminal 2
cd "c:\Users\LENOVO\Desktop\Casa Abierta\carnet_casa_abierta\backend"
python.exe -m uvicorn main:app --reload
```

---

## 📝 Alternativa: Usar Conda

Si tienes Anaconda instalado:

```powershell
# Crear entorno
conda create -n casa_abierta python=3.11

# Activar
conda activate casa_abierta

# Instalar dependencias
pip install -r requirements.txt

# O manual
pip install fastapi uvicorn python-multipart supabase

# Ejecutar
python -m uvicorn main:app --reload
```

---

## 💾 requirements.txt

```
fastapi==0.109.0
uvicorn==0.27.0
python-multipart==0.0.6
supabase==2.4.0
```

Archivo ubicado en: `backend/requirements.txt`

---

## 🆘 Si Nada Funciona

1. **Reinstala Python**
   - Descarga desde https://www.python.org/downloads/
   - Marca "Add Python to PATH"
   - Reinicia Windows

2. **Verifica Rutas**
   ```powershell
   $env:Path -split ';' | Select-String python
   ```
   Debería mostrar rutas de Python

3. **Usa Path Completo**
   ```powershell
   C:\Python311\Scripts\pip install fastapi
   ```
   (Ajusta la versión según tengas)

---

**Última actualización**: 31 de enero de 2026
