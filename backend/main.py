from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
import shutil
import base64
import random
import asyncio
from datetime import datetime
from PIL import Image
from io import BytesIO
import httpx
from fastapi.staticfiles import StaticFiles

# Agregar directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import face_analysis
import database

# Configuración
UPLOAD_DIR = "uploads"
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "") 

# Crear directorio de uploads si no existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Casa Abierta - API", version="1.0.0")

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Inicializar base de datos
database.init_db()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend API - Casa Abierta operativo"}

# ==================== Utilidades ====================

def image_to_base64(image_path):
    """Convierte una imagen a base64 para transmisión."""
    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            if img.width > 800:
                ratio = 800 / img.width
                img = img.resize((800, int(img.height * ratio)), Image.Resampling.LANCZOS)
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=90)
            buffer.seek(0)
            return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Error al procesar imagen: {e}")
        return None

async def generar_imagen(prompt, image_path, tipo_generacion, identity_strength=0.65):
    """Genera una imagen usando Replicate API."""
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        image_base64 = image_to_base64(image_path)
        if not image_base64:
            raise Exception("Error al convertir imagen a base64")
    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return None

    payload = {
        "version": "03914a0c3326bf44383d0cd84b06822618af879229ce5d1d53bef38d93b68279",
        "input": {
            "image": f"data:image/jpeg;base64,{image_base64}",
            "prompt": prompt,
            "negative_prompt": "smooth skin, plastic skin, airbrushed, photoshop, low quality, blurry",
            "num_inference_steps": 30,
            "guidance_scale": 3.5,
            "ip_adapter_scale": identity_strength,
            "controlnet_conditioning_scale": identity_strength
        }
    }

    async with httpx.AsyncClient(timeout=300) as client:
        print(f"Generando imagen: {tipo_generacion}...")
        r = await client.post(url, json=payload, headers=headers)

        if r.status_code != 201:
            print(f"Error de Replicate: {r.text}")
            return None

        get_url = r.json()["urls"]["get"]

        for _ in range(120):
            poll = await client.get(get_url, headers=headers)
            data = poll.json()

            if data["status"] == "succeeded":
                output = data.get("output")
                if isinstance(output, list) and len(output) > 0:
                    return output[0]
                return output if isinstance(output, str) else None

            if data["status"] == "failed":
                print(f"Fallo en generación: {data.get('error')}")
                return None

            await asyncio.sleep(2)
        return None


# ==================== Endpoints ====================

@app.post("/analizar")
async def analizar(file: UploadFile = File(...)):
    """
    Endpoint principal de análisis biométrico.
    Recibe una imagen, analiza el tipo de rostro y retorna recomendaciones de cortes.
    """
    try:
        # Guardar imagen
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ts}_{file.filename}"
        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"Imagen procesada: {filename}")

        # Analizar propiedades del rostro
        analysis_results = face_analysis.analyze_image_properties(path)
        rostro_detectado = analysis_results["face_shape"]
        genero_detectado = analysis_results["gender"]

        # Obtener recomendación de corte
        corte_recomendado = face_analysis.get_haircut_recommendation(rostro_detectado)

        # Seleccionar corte alternativo/gracioso
        cortes_alternativos = [
            "Completely Bald Head",
            "Crazy Einstein Hair",
            "Bright Neon Green Mohawk",
            "Clown Wig with red nose",
            "Historical Powdered Wig"
        ]
        corte_alternativo = random.choice(cortes_alternativos)

        # Generar prompts
        prompt_realista = (
            f"Raw candid photo of a person with a {corte_recomendado} hairstyle, "
            f"fitting a {rostro_detectado} face shape, professional portrait"
        )

        prompt_alternativo = (
            f"Hilarious and funny photo of a person with a {corte_alternativo}, "
            f"exaggerated and ridiculous style, comedic expression"
        )

        # Generar imágenes
        print("Generando imágenes...")
        url_realista = await generar_imagen(prompt_realista, path, "Corte Realista")
        url_alternativo = await generar_imagen(prompt_alternativo, path, "Corte Gracioso")

        # Guardar análisis en base de datos
        analysis_id = database.save_analysis(
            image_path=path,
            face_shape=rostro_detectado,
            biometrics=analysis_results.get("biometrics", {}),
            gender=genero_detectado
        )

        return {
            "mensaje": "Análisis completado exitosamente",
            "datos": {
                "analysis_id": analysis_id,
                "tipo_rostro": rostro_detectado,
                "corte_recomendado": corte_recomendado,
                "imagen_generada_url": url_realista,
                "corte_gracioso_nombre": corte_alternativo,
                "imagen_graciosa_url": url_alternativo,
                "genero_detectado": genero_detectado,
                "biometrics": analysis_results.get("biometrics", {}),
                "telemetria": analysis_results.get("biometrics", {})
            }
        }

    except Exception as e:
        print(f"Error en análisis: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/historial")
def get_historial(limit: int = 100, offset: int = 0):
    """Retorna el historial de análisis biométricos guardados."""
    try:
        analyses = database.get_all_analyses(limit=limit, offset=offset)
        total = database.get_total_count()

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "analyses": analyses
        }
    except Exception as e:
        print(f"Error obteniendo historial: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/analisis/{analysis_id}")
def get_analisis(analysis_id: int):
    """Retorna un análisis específico por ID."""
    try:
        analysis = database.get_analysis_by_id(analysis_id)

        if analysis is None:
            return JSONResponse(
                status_code=404,
                content={"error": f"Análisis {analysis_id} no encontrado"}
            )

        return analysis
    except Exception as e:
        print(f"Error obteniendo análisis: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)