# ⚠️ Nota Técnica: Modo Simulación y Compatibilidad

**Fecha:** 1 de Febrero, 2026
**Autor:** Equipo de Desarrollo (Alejandro Vaca)

---

## 🛑 Situación Actual

Debido a **restricciones de compatibilidad de hardware** específicas encontradas durante el desarrollo en arquitectura macOS (Apple Silicon M1/M2/M3), las librerías de Inteligencia Artificial `tensorflow` y `mediapipe` presentaron conflictos críticos que impedían el arranque estable del servidor backend.

Para garantizar que **todo el equipo** pueda ejecutar el proyecto y visualizar el flujo completo (Frontend <-> Backend) sin errores de instalación, se ha tomado la siguiente decisión técnica:

### ✅ Solución Implementada: "Modo Simulación"

El backend (`main.py`) se ha configurado en un modo de **alta compatibilidad** que:

1.  **Mantiene la arquitectura real:** Los endpoints API, la recepción de imágenes y el flujo de datos son definitivos.
2.  **Simula el procesamiento pesado:** En lugar de cargar los modelos neuronales (que fallan en ciertos entornos), el sistema devuelve resultados aleatorios controlados (Ej: "Rostro Ovalado", "Corte Pompadour").
3.  **Genera evidencias visuales:** Utiliza la librería ligera `Pillow` para dibujar una respuesta visual, demostrando que el sistema es capaz de procesar y devolver archivos.

---

## 🔄 Cómo Activar la "IA Real" (Para Compiladores)

Si un miembro del equipo dispone de un entorno Windows/Linux con soporte nativo para las librerías requeridas, puede activar el modo real siguiendo estos pasos:

1.  **Instalar dependencias completas:**
    Asegúrate de que `backend/requirements.txt` incluya:
    ```txt
    mediapipe
    tensorflow
    fer
    ```

2.  **Modificar `backend/main.py`:**
    Descomentar las líneas de importación e inicialización:
    ```python
    # IMPORTANTE: Descomentar solo si tienes las librerías instaladas
    # import mediapipe as mp
    # from fer import FER
    
    # mp_face_mesh = mp.solutions.face_mesh ...
    ```

3.  **Reemplazar funciones Mock:**
    Cambiar las llamadas a `detectar_tipo_rostro_mock()` por la lógica real de MediaPipe implementada originalmente.

---

## 🎯 Conclusión

Esta versión garantiza que la **demo funcional** pueda ser presentada y ejecutada en **cualquier computadora** del equipo inmediatamente, sin pasar horas resolviendo conflictos de dependencias de Python (Dependency Hell).
