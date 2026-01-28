from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import random

app = FastAPI()

# --- CONFIGURACIÓN ---
# ¡Peguen aquí sus credenciales de Supabase!
SUPABASE_URL = "https://tjzryawsqbhhwvkfquzb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRqenJ5YXdzcWJoaHd2a2ZxdXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk0MzUyODgsImV4cCI6MjA4NTAxMTI4OH0.Ota6MKcgHmdAVAiCCXZ0zjVqb7Qz5IS5Vddal3V8I4s"

# Conectamos con la base de datos
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de seguridad (CORS) para que Vue pueda hablar con Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción esto se restringe, para la casa abierta déjalo así
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "El cerebro de IA está activo 🧠"}

@app.post("/analizar")
async def analizar_rostro(file: UploadFile = File(...)):
    """
    1. Recibe la foto desde Vue.
    2. (Próximamente) Analiza con IA real.
    3. Guarda en Supabase.
    4. Devuelve recomendación.
    """
    print(f"📸 Recibida imagen: {file.filename}")

    # --- ZONA DE SIMULACIÓN DE IA (Semana 1) ---
    # Aquí irá MediaPipe después. Por ahora, inventamos datos para probar el flujo.
    opciones_rostro = ["Ovalado", "Cuadrado", "Redondo", "Diamante"]
    opciones_corte = ["Fade Bajo", "Pompadour", "Buzz Cut", "Mullet Moderno"]
    
    rostro_detectado = random.choice(opciones_rostro)
    corte_sugerido = random.choice(opciones_corte)
    emocion = "Sorprendido" # Esto también lo detectará la IA luego
    
    # URL falsa por ahora (luego vendrá de Replicate)
    url_fake = "https://placehold.co/600x400?text=Corte+Generado+por+IA"

    # --- GUARDAR EN SUPABASE (Gestión de Data) ---
    datos_para_guardar = {
        "tipo_rostro": rostro_detectado,
        "corte_recomendado": corte_sugerido,
        "emocion_detectada": emocion,
        "genero_detectado": "Masculino", # Placeholder
        "imagen_generada_url": url_fake
    }

    try:
        # Insertamos en la tabla que creaste
        data = supabase.table("historial_biometrico").insert(datos_para_guardar).execute()
        print("✅ Datos guardados en Supabase con éxito")
    except Exception as e:
        print(f"❌ Error guardando en Supabase: {e}")

    # --- RESPONDER A VUE ---
    return {
        "mensaje": "Análisis completado",
        "datos": datos_para_guardar
    }