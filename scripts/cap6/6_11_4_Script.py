# -*- coding: utf-8 -*-
# =============================================================================
# Capítulo 6: Integración, despliegue y proyecto final
# Sección 11: CI/CD y monitoreo
# Bloque 4: Seguimiento del proyecto
# =============================================================================

# Descripción: Script de validación para el proyecto final. 
# Este script permite a los alumnos realizar una revisión automática de su 
# arquitectura, comprobar la integración de los módulos, validar la funcionalidad 
# end-to-end e imprimir un checklist de entrega para la presentación.

import os
import requests
import sqlite3
import logging

# Configurar logging para el seguimiento técnico (ST1, ST4)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

def validar_arquitectura_proyecto(ruta_base: str) -> bool:
    """
    ST2: Revisión de arquitectura del proyecto.
    Valida que el proyecto contenga la estructura de directorios recomendada
    para separar ingesta, transformación, almacenamiento y API.
    """
    logging.info("Iniciando validación de arquitectura del proyecto...")
    
    carpetas_esperadas = [
        "data/raw",
        "data/processed",
        "src/pipeline",
        "src/api",
        "src/dashboard"
    ]
    
    todas_existen = True
    for carpeta in carpetas_esperadas:
        ruta_completa = os.path.join(ruta_base, carpeta)
        if not os.path.exists(ruta_completa):
            logging.warning(f"Falta el directorio recomendado: {carpeta}")
            todas_existen = False
        else:
            logging.info(f"Directorio encontrado: {carpeta}")
            
    if todas_existen:
        logging.info("La arquitectura del proyecto cumple con las mejores prácticas.")
    else:
        logging.warning("Se sugiere ajustar la arquitectura para mejorar la modularidad (ST5).")
        
    return todas_existen

def validar_componente_pipeline(ruta_archivo_procesado: str) -> bool:
    """
    ST3: Validación de componentes (pipeline).
    Verifica que el pipeline haya generado un archivo de salida válido.
    ST6: Validación de funcionalidad end-to-end.
    """
    logging.info("Validando el componente del Pipeline de Datos...")
    
    if os.path.exists(ruta_archivo_procesado):
        tamano = os.path.getsize(ruta_archivo_procesado)
        if tamano > 0:
            logging.info(f"Pipeline validado: Archivo procesado encontrado con {tamano} bytes.")
            return True
        else:
            logging.error("Pipeline fallido: El archivo procesado está vacío.")
            return False
    else:
        logging.error("Pipeline fallido: No se encontró el archivo procesado.")
        return False

def validar_componente_api(url_health_check: str) -> bool:
    """
    ST3: Validación de componentes (API).
    ST5: Integración de módulos.
    Realiza una petición al endpoint de salud para verificar si la API está viva.
    """
    logging.info(f"Validando el componente API en {url_health_check}...")
    
    try:
        respuesta = requests.get(url_health_check, timeout=5)
        if respuesta.status_code == 200:
            logging.info("API validada: El endpoint responde correctamente (Status 200).")
            return True
        else:
            logging.warning(f"API con problemas: Respondió con status {respuesta.status_code}.")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al conectar con la API: {e}")
        logging.info("Sugerencia (ST4): Verifica que el contenedor de la API esté en ejecución.")
        return False

def generar_checklist_entrega():
    """
    ST7: Mejores prácticas de presentación.
    ST8: Ajustes finales.
    ST9: Checklist de entrega.
    ST10: Preparación para demo.
    ST11: Enfoque en claridad y funcionalidad.
    """
    checklist = """
    ==================================================
              CHECKLIST DE ENTREGA FINAL
    ==================================================
    Preparación para Demo (ST10) y Ajustes Finales (ST8):
    
    [ ] 1. Repositorio de GitHub actualizado (commits descriptivos).
    [ ] 2. Archivo README.md claro con instrucciones de ejecución.
    [ ] 3. Dockerfile y docker-compose.yaml funcionales (reproducibilidad).
    [ ] 4. Pipeline de datos se ejecuta sin errores (End-to-End validado).
    [ ] 5. API o Dashboard consume los datos procesados correctamente.
    [ ] 6. Código modularizado y comentado.
    [ ] 7. Diapositivas preparadas (Enfoque en claridad y funcionalidad - ST11).
    [ ] 8. Presentación ensayada (Justificación de arquitectura - ST7).
    
    ==================================================
    ¡Éxito en la presentación de tu proyecto de Data Engineering!
    """
    print(checklist)

def ejecutar_seguimiento_integral():
    """
    Función principal que orquesta la revisión completa del proyecto.
    """
    print("\n" + "="*50)
    print("INICIO DE VALIDACIÓN DE PROYECTO FINAL (6.11.4)")
    print("="*50 + "\n")
    
    # Directorio actual simulado
    ruta_base_proyecto = "."
    
    # 1. Revisar Arquitectura
    validar_arquitectura_proyecto(ruta_base_proyecto)
    print("-" * 50)
    
    # 2. Validar Pipeline (simulando que buscamos un archivo output.parquet)
    # Nota: Crea un archivo vacío local para que pase la prueba si lo deseas
    archivo_prueba = "./data/processed/output.parquet"
    if not os.path.exists("./data/processed"):
        os.makedirs("./data/processed", exist_ok=True)
    with open(archivo_prueba, 'w') as f:
        f.write("mock_data")
        
    validar_componente_pipeline(archivo_prueba)
    print("-" * 50)
    
    # 3. Validar API (simulando localhost:8000/health)
    validar_componente_api("http://localhost:8000/health")
    print("-" * 50)
    
    # 4. Imprimir Checklist para el alumno
    generar_checklist_entrega()

if __name__ == "__main__":
    ejecutar_seguimiento_integral()
