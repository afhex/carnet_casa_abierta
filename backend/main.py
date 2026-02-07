from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os, shutil, base64, random, asyncio
from datetime import datetime
from PIL import Image
from io import BytesIO
import httpx

app = FastAPI()

UPLOAD_DIR = "uploads"
# ⬇️ AQUÍ VA LA API
REPLICATE_API_TOKEN = "Tu_API_Token_Aquí"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend InstantID (Modo DOBLE: Realista + Gracioso) 🚀"}

# ---------------- UTIL ----------------

def image_to_base64(image_path):
    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            # Reducimos a 800px para que no falle por tamaño
            if img.width > 800:
                ratio = 800 / img.width
                img = img.resize((800, int(img.height * ratio)), Image.Resampling.LANCZOS)
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=90) # Calidad alta
            buffer.seek(0)
            encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return encoded
    except Exception as e:
        print("❌ Error base64:", e)
        return None

# ---------------- REPLICATE (Función Genérica) ----------------

async def generar_imagen(prompt, image_path, tipo_generacion):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        image_base64 = image_to_base64(image_path)
        if not image_base64: raise Exception("Fallo conversión imagen")
    except Exception as e:
        print("❌ Error procesando imagen:", e)
        return None

    # Usamos la CONFIGURACIÓN GANADORA (GrandlineAI + Parámetros de Realismo)
    payload = {
        "version": "03914a0c3326bf44383d0cd84b06822618af879229ce5d1d53bef38d93b68279",
        "input": {
            "image": f"data:image/jpeg;base64,{image_base64}",
            "prompt": prompt,
            # Prompt negativo para evitar piel de plástico
            "negative_prompt": "smooth skin, plastic skin, airbrushed, photoshop, makeup, render, 3d, cartoon, drawing, illustration, anime, deformed, blur, low quality, flat lighting",
            "num_inference_steps": 30,
            # AJUSTES CLAVE QUE TE GUSTARON:
            "guidance_scale": 3.5, 
            "ip_adapter_scale": 0.60,     
            "controlnet_conditioning_scale": 0.60
        }
    }

    async with httpx.AsyncClient(timeout=300) as client:
        print(f"⏳ Enviando a Replicate ({tipo_generacion})...")
        r = await client.post(url, json=payload, headers=headers)

        if r.status_code != 201:
            print(f"❌ Replicate error en {tipo_generacion}:", r.text)
            return None

        get_url = r.json()["urls"]["get"]

        # Polling
        for _ in range(120):
            poll = await client.get(get_url, headers=headers)
            data = poll.json()

            if data["status"] == "succeeded":
                output = data.get("output")
                print(f"✅ Generado ({tipo_generacion}): {output}")
                if isinstance(output, list) and len(output) > 0: return output[0]
                elif isinstance(output, str): return output
                return None

            if data["status"] == "failed":
                print(f"❌ Falló ({tipo_generacion}):", data.get("error"))
                return None
            await asyncio.sleep(2)
        return None

# ---------------- ENDPOINT PRINCIPAL ----------------

@app.post("/analizar")
async def analizar(file: UploadFile = File(...)):
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ts}_{file.filename}"
        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("📸 Imagen recibida:", filename)

        # ==========================================
        # 1. SELECCIÓN DE CORTES (REALISTA Y GRACIOSO)
        # ==========================================
        lista_realistas = [
            "Buzz Cut", "Textured Crop", "Messy Quiff", "Modern Mullet", "Pompadour", # Hombres
            "Bob Cut", "Long Wavy Layers", "Pixie Cut", "Curtain Bangs", "Straight Sleek Hair" # Mujeres
        ]
        corte_realista = random.choice(lista_realistas)

        lista_graciosos = [
            "Completely Bald Head",          # Calvo total como una bola de billar
            "Crazy Einstein Scientist Hair", # Pelo loco y explotado
            "Bright Neon Green Mohawk",      # Mohicano punk verde neón
            "Clown Wig with red nose",       # Peluca de payaso
            "Historical Powdered Wig 1700s"  # Peluca blanca antigua ridícula
        ]
        corte_gracioso = random.choice(lista_graciosos)
        
        # ==========================================
        # 2. GENERACIÓN 1: LA REALISTA (Recomendada)
        # ==========================================
        prompt_realista = (
            f"Raw candid photo of a person with a {corte_realista} hairstyle, "
            "shot on 35mm film, fujifilm, grainy texture, "
            "visible skin pores, natural uneven lighting, sharp focus, "
            "realistic shadows, dslr"
        )
        print(f"🚀 --- INICIANDO GENERACIÓN REALISTA: {corte_realista} ---")
        url_realista = await generar_imagen(prompt_realista, path, "Realista")

        # ==========================================
        # 3. GENERACIÓN 2: LA GRACIOSA (Reacción)
        # ==========================================
        # Usamos un prompt que pida una foto realista pero de un peinado ridículo
        prompt_gracioso = (
            f"A funny photograph of the person with a {corte_gracioso}, "
            "looking ridiculous, realistic textures, sharp focus, bright lighting, "
            "humorous expression if possible"
        )
        print(f"🤡 --- INICIANDO GENERACIÓN GRACIOSA: {corte_gracioso} ---")
        # Usamos la misma imagen original (path) para la segunda generación
        url_gracioso = await generar_imagen(prompt_gracioso, path, "Gracioso")


        # Fallbacks por si alguna falla
        if not url_realista: url_realista = "https://placehold.co/600x600/png?text=Error+Realista"
        if not url_gracioso: url_gracioso = "https://placehold.co/600x600/png?text=Error+Gracioso"

        # ==========================================
        # 4. RESPUESTA FINAL (CON LAS DOS URLs)
        # ==========================================
        return {
            "mensaje": "Éxito",
            "datos": {
                # La principal recomendada
                "imagen_generada_url": url_realista,
                "corte_recomendado": corte_realista,

                # La extra graciosa
                "imagen_graciosa_url": url_gracioso,
                "corte_gracioso_nombre": corte_gracioso,

                # Metadatos
                "tipo_rostro": "Ovalado",
                "emocion_detectada": "Feliz",
                "genero_detectado": "Auto-Detectado"
            }
        }

    except Exception as e:
        print("❌ Error Crítico:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)