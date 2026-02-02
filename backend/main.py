from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import json
from datetime import datetime
import random
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

# --- CONFIGURACIÓN ---
UPLOAD_DIR = "uploads"
HISTORY_FILE = "history.json"

# Asegurar directorios
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend Simulado Activo 🧠 (Modo Local)"}

def guardar_historial(datos):
    """Guarda el análisis en un JSON local."""
    historial = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                historial = json.load(f)
        except json.JSONDecodeError:
            pass
    
    # Inicia el historial si está vacío
    if not isinstance(historial, list):
        historial = []

    historial.insert(0, datos) # Agregar al inicio
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(historial, f, indent=2)

def generar_imagen_mock(ancho=400, alto=400):
    """Genera una imagen placeholder con Pillow para simular IA."""
    img = Image.new('RGB', (ancho, alto), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((10,10), "Simulacion AI", fill=(255,255,0))
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

@app.post("/analizar")
async def analizar_rostro(file: UploadFile = File(...)):
    try:
        # 1. Guardar Imagen Localmente
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"📸 Imagen guardada en: {file_path}")

        # 2. Análisis Simulado (Aquí iría MediaPipe)
        opciones_rostro = ["Ovalado", "Redondo", "Cuadrado", "Corazon"]
        opciones_corte = ["Fade Medio", "Pompadour", "Buzz Cut", "Crop Top"]
        opciones_emocion = ["Feliz", "Serio", "Sorprendido", "Neutro"]
        opciones_genero = ["Masculino", "Femenino"]
        
        datos_analisis = {
            "timestamp": timestamp,
            "filename": filename,
            "tipo_rostro": random.choice(opciones_rostro),
            "corte_recomendado": random.choice(opciones_corte),
            "emocion_detectada": random.choice(opciones_emocion),
            "genero_detectado": random.choice(opciones_genero),
            "imagen_generada_url": generar_imagen_mock() # Devuelve base64
        }
        
        # 3. Guardar en Historial
        guardar_historial(datos_analisis)
        print("✅ Análisis registrado en history.json")

        return {
            "mensaje": "Análisis completado (Modo Local)",
            "datos": datos_analisis
        }

    except Exception as e:
        print(f"❌ Error en backend: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})