import random

# Intentar importar DeepFace, pero NO quebrar si no está disponible
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
    print("✅ DeepFace cargado correctamente")
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("⚠️  DeepFace no disponible. Usando fallback por nombre de archivo.")

# LISTA MASCULINA (Estilos cortos, degradados y texturizados)
CORTES_HOMBRE = [
    ("Buzz Cut", "buzz cut hairstyle, extremely short military style, clean fade on sides, masculine look"),
    ("Pompadour", "classic pompadour hairstyle, high volume slicked back hair on top, short faded sides"),
    ("Modern Mullet", "modern mullet hairstyle, short hair on sides, long hair on the back, messy texture"),
    ("Textured Crop", "textured crop hairstyle, short messy hair on top, straight fringe, high skin fade"),
    ("Undercut", "undercut hairstyle, long hair on top slicked back, shaved sides, disconnection"),
    ("Surfer Waves", "medium length wavy hair, surfer style, natural messy look, sun-kissed texture"),
    ("Afro Fade", "short afro hairstyle, defined curls with skin fade on temples"),
    ("Slick Back", "classic slick back hairstyle, gentleman look, shiny finish, combed back")
]

# LISTA FEMENINA (Estilos largos, capas y cortes estilizados)
CORTES_MUJER = [
    ("Long Layers", "long layered hairstyle, wavy texture, face framing layers, voluminous"),
    ("Classic Bob", "classic chin-length bob hairstyle, straight sleek hair, sharp edges, modern chic"),
    ("Pixie Cut", "short pixie cut hairstyle, feminine short hair, textured layers"),
    ("Beach Waves", "long messy beach waves hairstyle, natural bohemian look, middle part"),
    ("Messy Bun", "hair tied in a casual messy bun with loose strands and bangs"),
    ("Straight & Sleek", "long straight silk hair, extremely shiny, middle part, ironed look"),
    ("Curly Shag", "shag haircut with curly texture, volume, layers and fringe, retro style")
]

def detectar_caracteristicas(ruta_imagen):
    """
    Detecta género y emoción. 
    Si DeepFace está disponible, lo usa.
    Si no, usa heurística simple basada en nombre de archivo.
    """
    
    # OPCIÓN 1: Si DeepFace está disponible, usarlo
    if DEEPFACE_AVAILABLE:
        try:
            objs = DeepFace.analyze(img_path=ruta_imagen, 
                                    actions=['gender', 'emotion'],
                                    enforce_detection=False)
            
            resultado = objs[0]
            genero_detectado = resultado['gender'].get('dominant_gender', 'Man')
            emocion_detectada = resultado['emotion'].get('dominant_emotion', 'neutral')
            
            genero_final = "Hombre" if genero_detectado == "Man" else "Mujer"
            
            print(f"✅ DeepFace: Género detectado = {genero_final}")
            
            return {
                "genero": genero_final,
                "emocion": emocion_detectada,
                "status": "success"
            }
        except Exception as e:
            print(f"⚠️  Error en DeepFace: {e}. Cayendo a fallback...")
    
    # OPCIÓN 2: Fallback - Usar nombre del archivo para adivinar
    print("🔍 Usando heurística de nombre de archivo...")
    filename_lower = ruta_imagen.lower()
    
    if "mujer" in filename_lower or "woman" in filename_lower or "chica" in filename_lower or "girl" in filename_lower:
        genero_final = "Mujer"
        print(f"🎯 Fallback: Nombre sugiere MUJER")
    else:
        genero_final = "Hombre"
        print(f"🎯 Fallback: Asignando por defecto HOMBRE")
    
    return {
        "genero": genero_final,
        "emocion": "neutral",
        "status": "fallback"
    }

def seleccionar_corte(genero):
    """
    Selecciona un corte aleatorio basado en el género.
    Retorna: (prompt_visual, nombre_corte)
    """
    try:
        genero_lower = str(genero).lower()
        
        if 'mujer' in genero_lower or 'femenino' in genero_lower or 'woman' in genero_lower:
            lista = CORTES_MUJER
        else:
            lista = CORTES_HOMBRE
            
        nombre_corte, prompt_base = random.choice(lista)
        
        prompt_visual = f"professional portrait, 8k, realistic texture, {prompt_base}"
        
        return prompt_visual, nombre_corte
    except Exception as e:
        print(f"Error seleccionando corte: {e}")
        # Fallback seguro
        return "professional portrait, 8k, realistic texture, classic hairstyle", "Classic Cut"
