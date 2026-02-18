from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
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
import urllib.request
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Agregar directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import face_analysis
import database
import generar_carnets

# Configuración
UPLOAD_DIR = "uploads"
GENERATED_DIR = "generated_images"
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not REPLICATE_API_TOKEN:
    print("⚠️  ADVERTENCIA: REPLICATE_API_TOKEN no está configurado.")
    print("   Por favor, crea un archivo .env en la carpeta backend/")
    print("   y agrega tu token de Replicate: REPLICATE_API_TOKEN=tu_token_aqui")
    print("   O configura la variable de entorno antes de iniciar.")

# Crear directorios si no existen
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)

app = FastAPI(title="Casa Abierta - API", version="1.0.0")

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

async def descargar_y_guardar_imagen(url: str, tipo_corte: str, ts: str) -> str:
    """
    Descarga una imagen desde una URL y la guarda localmente.
    
    Args:
        url: URL de la imagen a descargar
        tipo_corte: Tipo de corte (para nombre del archivo)
        ts: Timestamp para nombre único
    
    Returns:
        Ruta local del archivo guardado
    """
    try:
        # Crear nombre de archivo único
        sanitized_tipo = tipo_corte.replace(" ", "_").replace("/", "_")
        filename = f"{ts}_{sanitized_tipo}.jpg"
        filepath = os.path.join(GENERATED_DIR, filename)
        
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(url)
            if response.status_code == 200:
                # Guardar imagen
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"✅ Imagen generada guardada: {filename}")
                return filepath
            else:
                print(f"Error descargando imagen: {response.status_code}")
                return None
    except Exception as e:
        print(f"Error descargando y guardando imagen: {e}")
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
    Recibe una imagen, analiza el tipo de rostro y guarda automáticamente
    la imagen generada con IA en carpeta local.
    """
    try:
        # Guardar imagen original
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ts}_{file.filename}"
        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"📸 Imagen original guardada: {filename}")

        # Analizar propiedades del rostro
        analysis_results = face_analysis.analyze_image_properties(path)
        rostro_detectado = analysis_results["face_shape"]
        genero_detectado = analysis_results["gender"]
        emocion_detectada = analysis_results.get("emotion", "Desconocida")

        # Obtener recomendación de corte
        corte_recomendado = face_analysis.get_haircut_recommendation(rostro_detectado)

        # Generar prompt realista para el corte
        prompt_realista = (
            f"Raw candid photo of a person with a {corte_recomendado} hairstyle, "
            f"fitting a {rostro_detectado} face shape, professional portrait"
        )

        # Intentar generar imagen con Replicate
        url_generada = await generar_imagen(prompt_realista, path, "Corte Recomendado")
        
        # --- Lógica de Corte Gracioso ---
        cortes_alternativos = [
            "Completely Bald Head",
            "Crazy Einstein Hair",
            "Bright Neon Green Mohawk",
            "Clown Wig with red nose",
            "Historical Powdered Wig",
            "Spaghetti Hair",
            "Super Saiyan Hair"
        ]
        import random
        corte_alternativo = random.choice(cortes_alternativos)
        
        prompt_alternativo = (
            f"Hilarious and funny photo of a person with a {corte_alternativo}, "
            f"exaggerated and ridiculous style, comedic expression"
        )
        
        url_generada_graciosa = await generar_imagen(prompt_alternativo, path, "Corte Gracioso")
        # --------------------------------

        ruta_imagen_generada = None
        
        if url_generada:
            # Descargar y guardar la imagen generada localmente
            ruta_imagen_generada = await descargar_y_guardar_imagen(
                url_generada, 
                corte_recomendado, 
                ts
            )
            print(f"✅ Imagen IA generada y descargada: {ruta_imagen_generada}")
        else:
            # Si falla la generación, crear un placeholder para carnet
            print("⚠️ No se pudo generar imagen con Replicate")
            try:
                # Crear un placeholder visual para el carnet
                from PIL import Image
                placeholder = Image.new('RGB', (600, 600), color=(200, 180, 160))
                placeholder_path = os.path.join(
                    GENERATED_DIR,
                    f"{ts}_placeholder_{corte_recomendado.replace(' ', '_')}.jpg"
                )
                os.makedirs(GENERATED_DIR, exist_ok=True)
                placeholder.save(placeholder_path, 'JPEG', quality=90)
                ruta_imagen_generada = placeholder_path
                print(f"✅ Placeholder creado: {placeholder_path}")
            except Exception as e:
                print(f"❌ Error creando placeholder: {e}")
                ruta_imagen_generada = None

        # Preparar biometría por defecto si falla o viene vacía
        biometrics_data = analysis_results.get("biometrics")
        if not biometrics_data:
            # Valores por defecto para evitar KeyError en base de datos
            biometrics_data = {
                "face_width": 0.0,
                "face_height": 0.0,
                "ratio_width_height": 0.0,
                "ratio_jaw": 0.0,
                "ratio_forehead": 0.0
            }

        # Guardar análisis en base de datos (AUTOMÁTICAMENTE sin preguntar)
        analysis_id = database.save_analysis(
            image_path=path,
            face_shape=rostro_detectado,
            biometrics=biometrics_data,
            gender=genero_detectado,
            generated_image_path=ruta_imagen_generada,
            haircut_recommendation=corte_recomendado,
            emotion=emocion_detectada
        )

        # Preparar URLs para la respuesta
        response_data = {
            "mensaje": "✅ Análisis completado - Imágenes guardadas automáticamente",
            "datos": {
                "analysis_id": analysis_id,
                "tipo_rostro": rostro_detectado,
                "corte_recomendado": corte_recomendado,
                "emocion_detectada": emocion_detectada,
                "genero_detectado": genero_detectado,
                "imagen_original_path": path,
                "imagen_generada_path": ruta_imagen_generada,
                "imagen_graciosa_url": url_generada_graciosa,
                "corte_gracioso_nombre": corte_alternativo,
                "biometrics": biometrics_data,
                "telemetria": biometrics_data
            }
        }
        
        # Si hay imagen generada, agregar URL para acceso (URL absoluta)
        if ruta_imagen_generada:
            response_data["datos"]["imagen_generada_url"] = f"http://localhost:8000/generated/{analysis_id}"

        return response_data

    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/generar-carnet")
async def generar_carnet_endpoint(payload: dict):
    """
    Genera un carnet PDF con la imagen IA.
    
    Recibe JSON:
    {
        "analysis_id": 1,
        "nombre": "Juan García"  (opcional, puede ser null)
    }
    
    Retorna: PDF del carnet descargable
    """
    try:
        analysis_id = payload.get("analysis_id")
        nombre_estudiante = payload.get("nombre")
        
        print(f"\n📋 Solicitud de carnet para análisis {analysis_id}")
        if nombre_estudiante:
            print(f"   Nombre: {nombre_estudiante}")
        
        # Validar que exista el análisis
        analysis = database.get_analysis_by_id(analysis_id)
        if not analysis:
            return JSONResponse(
                status_code=404,
                content={"error": f"Análisis {analysis_id} no encontrado"}
            )
        
        # Validar que exista la imagen generada
        imagen_ia_path = analysis.get("generated_image_path")
        if not imagen_ia_path or not os.path.exists(imagen_ia_path):
            return JSONResponse(
                status_code=404,
                content={"error": "Imagen generada no encontrada"}
            )
        
        # Obtener ruta de plantilla
        plantilla_path = os.path.join("templates", "carnet_template.png")
        
        # Si no existe plantilla personalizada, crear demo
        if not os.path.exists(plantilla_path):
            print("⚠️ Plantilla personalizada no encontrada, usando demo...")
            plantilla_path = generar_carnets.crear_plantilla_demo()
        
        # Generar carnet PDF
        pdf_ruta = generar_carnets.generar_pdf_carnet(
            imagen_ia_path=imagen_ia_path,
            plantilla_path=plantilla_path,
            nombre=nombre_estudiante,
            analysis_id=analysis_id
        )
        
        print(f"✅ Carnet generado exitosamente")
        
        # Retornar PDF
        return FileResponse(
            pdf_ruta,
            media_type="application/pdf",
            filename=f"carnet_{analysis_id}.pdf"
        )
    
    except Exception as e:
        print(f"❌ Error generando carnet: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/generated/{analysis_id}")
def get_generated_image(analysis_id: int):
    """Retorna la imagen generada para un análisis específico."""
    try:
        analysis = database.get_analysis_by_id(analysis_id)
        
        if analysis is None or not analysis.get("generated_image_path"):
            return JSONResponse(
                status_code=404,
                content={"error": f"Imagen generada para análisis {analysis_id} no encontrada"}
            )
        
        image_path = analysis["generated_image_path"]
        if os.path.exists(image_path):
            return FileResponse(image_path, media_type="image/jpeg")
        else:
            return JSONResponse(
                status_code=404,
                content={"error": "Archivo de imagen no encontrado en el servidor"}
            )
    except Exception as e:
        print(f"Error obteniendo imagen generada: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/generated-images-list")
def get_generated_images_list(skip: int = 0, limit: int = 100):
    """
    Retorna la lista de todas las imágenes generadas disponibles.
    Ideal para que tus compañeros recopilen las imágenes para el carnet.
    """
    try:
        # Obtener todos los análisis con imágenes generadas
        conn = database.sqlite3.connect(database.DB_PATH)
        conn.row_factory = database.sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM biometric_analyses 
            WHERE generated_image_path IS NOT NULL 
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        """, (limit, skip))
        
        rows = cursor.fetchall()
        cursor.execute("""
            SELECT COUNT(*) as total FROM biometric_analyses 
            WHERE generated_image_path IS NOT NULL
        """)
        total = cursor.fetchone()["total"]
        conn.close()
        
        analyses = [dict(row) for row in rows]
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "generated_images": analyses,
            "mensaje": "Lista de imágenes generadas para carnets disponibles"
        }
    except Exception as e:
        print(f"Error obteniendo lista de imágenes generadas: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/archivos-generados")
def listar_archivos_generados():
    """
    Retorna la lista física de archivos guardados en generated_images/.
    Útil para acceso directo a los archivos.
    """
    try:
        archivos = []
        if os.path.exists(GENERATED_DIR):
            for archivo in os.listdir(GENERATED_DIR):
                ruta_completa = os.path.join(GENERATED_DIR, archivo)
                tamaño = os.path.getsize(ruta_completa)
                archivos.append({
                    "nombre": archivo,
                    "ruta": ruta_completa,
                    "tamaño_bytes": tamaño,
                    "url_descarga": f"/descargar-generada/{archivo}"
                })
        
        return {
            "total_archivos": len(archivos),
            "directorio": GENERATED_DIR,
            "archivos": archivos
        }
    except Exception as e:
        print(f"Error listando archivos generados: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/descargar-generada/{filename}")
def descargar_generada(filename: str):
    """Descarga una imagen generada específica por nombre de archivo."""
    try:
        # Validar que el filename no intente acceso a directorios superiores
        if ".." in filename or "/" in filename:
            return JSONResponse(
                status_code=400,
                content={"error": "Nombre de archivo inválido"}
            )
        
        filepath = os.path.join(GENERATED_DIR, filename)
        
        if not os.path.exists(filepath):
            return JSONResponse(
                status_code=404,
                content={"error": f"Archivo {filename} no encontrado"}
            )
        
        return FileResponse(filepath, media_type="image/jpeg", filename=filename)
    except Exception as e:
        print(f"Error descargando imagen: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/historial")
def get_historial(limit: int = 100, offset: int = 0):
    """
    Retorna el historial de análisis biométricos guardados.
    Incluye referencias a imágenes generadas.
    """
    try:
        analyses = database.get_all_analyses(limit=limit, offset=offset)
        total = database.get_total_count()

        # Agregar URLs para imágenes generadas
        for analysis in analyses:
            if analysis.get("generated_image_path"):
                analysis["imagen_generada_url"] = f"http://localhost:8000/generated/{analysis['id']}"

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
    """
    Retorna un análisis específico por ID.
    Incluye referencias a imagen original e imagen generada.
    """
    try:
        analysis = database.get_analysis_by_id(analysis_id)

        if analysis is None:
            return JSONResponse(
                status_code=404,
                content={"error": f"Análisis {analysis_id} no encontrado"}
            )

        # Agregar URL para imagen generada si existe
        if analysis.get("generated_image_path"):
            analysis["imagen_generada_url"] = f"http://localhost:8000/generated/{analysis_id}"

        return analysis
    except Exception as e:
        print(f"Error obteniendo análisis: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)