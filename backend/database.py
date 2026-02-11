"""
Base de datos SQLite para almacenar análisis biométricos faciales.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "biometrics.db")

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS biometric_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            face_shape TEXT NOT NULL,
            face_width REAL NOT NULL,
            face_height REAL NOT NULL,
            ratio_width_height REAL NOT NULL,
            ratio_jaw REAL NOT NULL,
            ratio_forehead REAL NOT NULL,
            gender TEXT DEFAULT 'Auto-Detectado',
            generated_image_path TEXT,
            haircut_recommendation TEXT,
            emotion TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ Base de datos inicializada: {DB_PATH}")

def save_analysis(
    image_path: str,
    face_shape: str,
    biometrics: Dict[str, float],
    gender: str = "Auto-Detectado",
    generated_image_path: str = None,
    haircut_recommendation: str = None,
    emotion: str = None
) -> int:
    """
    Guarda un análisis biométrico en la base de datos.
    
    Args:
        image_path: Ruta relativa a la imagen original
        face_shape: Forma del rostro detectada
        biometrics: Diccionario con medidas biométricas
        gender: Género (por defecto Auto-Detectado)
        generated_image_path: Ruta a la imagen generada con IA
        haircut_recommendation: Recomendación de corte
        emotion: Emoción detectada
    
    Returns:
        ID del análisis guardado
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO biometric_analyses 
        (image_path, face_shape, face_width, face_height, 
         ratio_width_height, ratio_jaw, ratio_forehead, gender,
         generated_image_path, haircut_recommendation, emotion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        image_path,
        face_shape,
        biometrics["face_width"],
        biometrics["face_height"],
        biometrics["ratio_width_height"],
        biometrics["ratio_jaw"],
        biometrics["ratio_forehead"],
        gender,
        generated_image_path,
        haircut_recommendation,
        emotion
    ))
    
    analysis_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"💾 Análisis guardado con ID: {analysis_id}")
    return analysis_id

def get_all_analyses(limit: int = 100, offset: int = 0) -> List[Dict]:
    """
    Obtiene todos los análisis guardados.
    
    Args:
        limit: Número máximo de resultados
        offset: Desplazamiento para paginación
    
    Returns:
        Lista de análisis como diccionarios
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM biometric_analyses 
        ORDER BY timestamp DESC 
        LIMIT ? OFFSET ?
    """, (limit, offset))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convertir a lista de diccionarios
    analyses = [dict(row) for row in rows]
    return analyses

def get_analysis_by_id(analysis_id: int) -> Optional[Dict]:
    """
    Obtiene un análisis específico por ID.
    
    Args:
        analysis_id: ID del análisis
    
    Returns:
        Diccionario con los datos del análisis o None si no existe
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM biometric_analyses WHERE id = ?
    """, (analysis_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None

def get_total_count() -> int:
    """Retorna el número total de análisis en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM biometric_analyses")
    count = cursor.fetchone()[0]
    
    conn.close()
    return count
