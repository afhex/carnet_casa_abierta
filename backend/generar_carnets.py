"""
Módulo para generar carnets con imágenes IA.
Extrae rostros, superpone en plantilla y genera PDFs.
Reutiliza face_analysis.py para detección de rostros.
"""

import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Rutas
TEMPLATES_DIR = "templates"
GENERATED_CARNETS_DIR = "generated_carnets"

# Asegurar que existan carpetas
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(GENERATED_CARNETS_DIR, exist_ok=True)



def extraer_rostro_para_carnet(imagen_path: str) -> Image.Image:
    """
    Carga la imagen completa para el carnet.
    No recorta, solo carga la imagen tal cual para que se redimensione correctamente.
    
    Args:
        imagen_path: Ruta a la imagen
    
    Returns:
        PIL Image de la imagen completa
    """
    try:
        print(f"📸 Cargando imagen: {imagen_path}")
        
        # Verificar que la imagen existe
        if not os.path.exists(imagen_path):
            raise Exception(f"Archivo no encontrado: {imagen_path}")
        
        # Simplemente cargar la imagen completae
        img = Image.open(imagen_path).convert('RGB')
        print(f"✅ Imagen cargada: {img.size}")
        return img
        
    except Exception as e:
        print(f"❌ Error cargando imagen: {e}")
        import traceback
        traceback.print_exc()
        # Crear imagen blanca como fallback
        return Image.new('RGB', (550, 450), color='white')


def redimensionar_para_area(imagen: Image.Image, ancho_objetivo: int, alto_objetivo: int) -> Image.Image:
    """
    Redimensiona una imagen manteniendo aspecto y centrándola.
    
    Args:
        imagen: Imagen PIL
        ancho_objetivo: Ancho deseado
        alto_objetivo: Alto deseado
    
    Returns:
        Imagen redimensionada al tamaño deseado
    """
    # Calcular factor de escala
    escala_x = ancho_objetivo / imagen.width
    escala_y = alto_objetivo / imagen.height
    escala = min(escala_x, escala_y)  # Mantener aspecto
    
    nuevo_ancho = int(imagen.width * escala)
    nuevo_alto = int(imagen.height * escala)
    
    # Redimensionar
    imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    
    # Crear lienzo del tamaño objetivo
    lienzo = Image.new('RGB', (ancho_objetivo, alto_objetivo), color='white')
    
    # Centrar imagen
    offset_x = (ancho_objetivo - nuevo_ancho) // 2
    offset_y = (alto_objetivo - nuevo_alto) // 2
    
    lienzo.paste(imagen_redimensionada, (offset_x, offset_y))
    
    return lienzo


def superponer_rostro_en_carnet(
    carnet_path: str,
    rostro: Image.Image,
    pos_x: int,
    pos_y: int,
    ancho: int,
    alto: int
) -> Image.Image:
    """
    Superpone el rostro recortado en la plantilla del carnet.
    
    Args:
        carnet_path: Ruta a la plantilla del carnet
        rostro: PIL Image del rostro
        pos_x: Posición X donde pegar
        pos_y: Posición Y donde pegar
        ancho: Ancho del área
        alto: Alto del área
    
    Returns:
        PIL Image del carnet con rostro superpuesto
    """
    try:
        print("🎨 Superponiendo rostro en carnet...")
        
        # Validar que rostro no sea None
        if rostro is None:
            print("⚠️ Rostro es None, cargando imagen placeholder blanca")
            rostro = Image.new('RGB', (ancho, alto), color='white')
        
        # Validar que rostro es una imagen válida
        if not isinstance(rostro, Image.Image):
            print(f"⚠️ Rostro no es una imagen PIL válida, crear placeholder")
            rostro = Image.new('RGB', (ancho, alto), color='white')
        
        # Cargar carnet
        if not os.path.exists(carnet_path):
            print(f"❌ Plantilla no encontrada: {carnet_path}")
            raise Exception(f"Plantilla no encontrada: {carnet_path}")
        
        carnet = Image.open(carnet_path).convert('RGB')
        
        # Redimensionar rostro al área exacta
        rostro_redimensionado = redimensionar_para_area(rostro, ancho, alto)
        
        # Superponer
        carnet.paste(rostro_redimensionado, (pos_x, pos_y))
        
        print("✅ Rostro superpuesto correctamente")
        return carnet
        
    except Exception as e:
        print(f"❌ Error superponiendo rostro: {e}")
        import traceback
        traceback.print_exc()
        raise


def agregar_nombre_al_carnet(
    carnet: Image.Image,
    nombre: str,
    pos_x: int,
    pos_y: int,
    ancho: int
) -> Image.Image:
    """
    Agrega el nombre del estudiante al carnet.
    
    Args:
        carnet: PIL Image del carnet
        nombre: Nombre a escribir
        pos_x: Posición X
        pos_y: Posición Y
        ancho: Ancho disponible para centrar
    
    Returns:
        PIL Image con nombre agregado
    """
    try:
        draw = ImageDraw.Draw(carnet)
        
        # Intentar usar Times New Roman (multi-plataforma)
        try:
            fuente = ImageFont.truetype("/System/Library/Fonts/Times New Roman.ttf", 48)
        except:
            try:
                fuente = ImageFont.truetype("C:\\Windows\\Fonts\\times.ttf", 48)
            except:
                try:
                    fuente = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 48)
                except:
                    fuente = ImageFont.load_default()
        
        # Obtener bounding box del texto
        bbox = draw.textbbox((0, 0), nombre, font=fuente)
        texto_ancho = bbox[2] - bbox[0]
        
        # Centrar horizontalmente
        offset_x = pos_x + (ancho - texto_ancho) // 2
        
        # Color blanco
        color_texto = (255, 255, 255)  # RGB blanco
        
        # Dibujar nombre
        draw.text((offset_x, pos_y), nombre, font=fuente, fill=color_texto)
        
        print(f"✅ Nombre '{nombre}' agregado al carnet")
        return carnet
        
    except Exception as e:
        print(f"❌ Error agregando nombre: {e}")
        raise


def generar_pdf_carnet(
    imagen_ia_path: str,
    plantilla_path: str,
    nombre: str = None,
    analysis_id: int = None
) -> str:
    """
    Genera un PDF del carnet completo.
    
    Pasos:
    1. Extrae rostro de la imagen IA
    2. Superpone en plantilla
    3. Agrega nombre (si existe)
    4. Convierte a PDF
    
    Args:
        imagen_ia_path: Ruta a imagen generada con IA
        plantilla_path: Ruta a plantilla del carnet
        nombre: Nombre del estudiante (opcional)
        analysis_id: ID del análisis
    
    Returns:
        Ruta del PDF generado
    """
    try:
        print(f"\n🎫 Iniciando generación de carnet para análisis {analysis_id}...")
        
        # Validar que la imagen existe
        if not os.path.exists(imagen_ia_path):
            raise Exception(f"Imagen no encontrada: {imagen_ia_path}")
        
        print(f"📁 Imagen IA: {imagen_ia_path}")
        print(f"📋 Plantilla: {plantilla_path}")
        
        # 1. Extraer rostro
        print("Paso 1: Extrayendo rostro...")
        rostro = extraer_rostro_para_carnet(imagen_ia_path)
        
        if rostro is None:
            print("⚠️ No se pudo extraer rostro, creando placeholder")
            rostro = Image.new('RGB', (550, 450), color='lightgray')
        
        print(f"✅ Rostro obtenido: {rostro.size}")
        
        # 2. Superponer en carnet
        print("Paso 2: Superponiendo rostro en carnet...")
        # Coordenadas exactas según plantilla 663x1068
        # Área de foto: X=159 (165-6px más a la izquierda), Y=373, Ancho=315, Alto=391
        carnet = superponer_rostro_en_carnet(
            carnet_path=plantilla_path,
            rostro=rostro,
            pos_x=159,      # Posición X (6px más a la izquierda)
            pos_y=373,      # Posición Y
            ancho=315,      # Ancho del rectángulo
            alto=391        # Alto del rectángulo
        )
        
        print(f"✅ Carnet con rostro: {carnet.size}")
        
        # 3. Agregar nombre si existe
        if nombre and nombre.strip():
            print(f"Paso 3: Agregando nombre '{nombre}'...")
            # Área del nombre: justo debajo de la foto
            carnet = agregar_nombre_al_carnet(
                carnet=carnet,
                nombre=nombre.strip(),
                pos_x=10,       # Posición X (20px más a la izquierda)
                pos_y=840,      # Posición Y (50px más abajo)
                ancho=600       # Ancho disponible para centrar
            )
        
        # 4. Guardar como PDF
        print("Paso 4: Guardando como PDF...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = nombre.replace(" ", "_") if nombre else "sin_nombre"
        pdf_filename = f"carnet_{analysis_id}_{timestamp}_{nombre_archivo}.pdf"
        pdf_ruta = os.path.join(GENERATED_CARNETS_DIR, pdf_filename)
        
        # Asegurar que el directorio existe
        os.makedirs(GENERATED_CARNETS_DIR, exist_ok=True)
        
        # Guardar PDF
        try:
            carnet.save(pdf_ruta, "PDF")
            print(f"✅ Carnet PDF guardado: {pdf_filename}")
        except Exception as e:
            print(f"⚠️ Error guardando como PDF: {e}")
            print(f"   Intentando guardar como JPG...")
            pdf_ruta = pdf_ruta.replace('.pdf', '.jpg')
            carnet.save(pdf_ruta, "JPEG", quality=95)
            print(f"✅ Carnet guardado como JPEG: {os.path.basename(pdf_ruta)}")
        
        print(f"📁 Ubicación: {os.path.abspath(pdf_ruta)}")
        
        return pdf_ruta
        
    except Exception as e:
        print(f"❌ Error generando carnet: {e}")
        import traceback
        traceback.print_exc()
        raise


def crear_plantilla_demo() -> str:
    """
    Crea una plantilla de carnet de demostración.
    Retorna la ruta de la plantilla.
    """
    try:
        print("🎨 Creando plantilla de demostración...")
        
        # Tamaño carnet: 85x54mm @ 300dpi ≈ 1004x638 px
        carnet = Image.new('RGB', (1004, 638), color=(240, 240, 240))
        draw = ImageDraw.Draw(carnet)
        
        # Color azul del carnet
        azul_oscuro = (25, 51, 102)
        
        # Usar fuentes disponibles (PNG por defecto si no hay system fonts)
        try:
            # Intentar fuentes comunes del sistema
            fuente_grande = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            fuente_media = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
            fuente_pequeña = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except:
            try:
                # Windows
                fuente_grande = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 48)
                fuente_media = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 32)
                fuente_pequeña = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 24)
            except:
                # Linux
                try:
                    fuente_grande = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
                    fuente_media = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                    fuente_pequeña = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
                except:
                    # Por defecto
                    fuente_grande = fuente_media = fuente_pequeña = ImageFont.load_default()
        
        # Encabezado
        draw.text((100, 20), "CASA ABIERTA", font=fuente_grande, fill=azul_oscuro)
        draw.text((450, 20), "Febrero 2026", font=fuente_media, fill=azul_oscuro)
        
        # Institución
        draw.text((50, 80), "Instituto Tecnologico Universitario Ruminahui", font=fuente_pequeña, fill=azul_oscuro)
        
        # Carrera
        draw.text((150, 130), "Sistemas y Gestion de Data", font=fuente_media, fill=azul_oscuro)
        
        # Rectángulo para foto (blanco, sin fondo)
        draw.rectangle([227, 95, 777, 545], outline=azul_oscuro, width=3, fill=(255, 255, 255))
        
        # Etiqueta "NOMBRE:"
        draw.text((165, 550), "NOMBRE:", font=fuente_pequeña, fill=azul_oscuro)
        
        # Línea para nombre
        draw.line([(240, 580), (840, 580)], fill=azul_oscuro, width=2)
        
        # Pie de página
        draw.text((100, 600), "Experto en Inteligencia Artificial Aplicada", font=fuente_pequeña, fill=azul_oscuro)
        
        # Guardar plantilla
        plantilla_ruta = os.path.join(TEMPLATES_DIR, "carnet_template_demo.jpg")
        carnet.save(plantilla_ruta, "JPEG", quality=95)
        
        print(f"✅ Plantilla demo creada: {plantilla_ruta}")
        return plantilla_ruta
        
    except Exception as e:
        print(f"❌ Error creando plantilla demo: {e}")
        raise
