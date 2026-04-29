# -*- coding: utf-8 -*-

"""
Capítulo 5: Automatización y orquestación
Sección 10: Orquestación e infraestructura
Bloque 4: Definición del proyecto final

Descripción:
Este script genera automáticamente la estructura de directorios y los archivos 
base (scaffolding) recomendados para iniciar el Proyecto Final del curso. 
Permite a los alumnos aplicar las buenas prácticas de organización e 
integración de componentes vistos durante las sesiones.
"""

import os
from pathlib import Path

def crear_estructura_directorios(ruta_base):
    """
    Crear los directorios principales para el proyecto final.
    Refleja la separación de responsabilidades: ingesta, transformación, API y dashboard.
    """
    directorios = [
        "data/raw",               # Datos crudos originales
        "data/processed",         # Datos limpios y transformados
        "src/pipeline",           # Scripts de ingesta y transformación (ETL)
        "src/api",                # Código de la API (FastAPI)
        "src/dashboard",          # Código de visualización (Streamlit)
        "infrastructure/docker",  # Archivos de configuración de contenedores
        "infrastructure/airflow", # DAGs para orquestación
        "tests"                   # Pruebas unitarias y validaciones
    ]
    
    print("Iniciando la creacion de la estructura de directorios...")
    for directorio in directorios:
        ruta_completa = Path(ruta_base) / directorio
        ruta_completa.mkdir(parents=True, exist_ok=True)
        print(f"Directorio creado: {ruta_completa}")

def generar_archivo_readme(ruta_base):
    """
    Generar el archivo README.md con la definicion de los entregables,
    criterios de evaluacion y rutas del proyecto final (ST1 a ST7).
    """
    contenido_readme = """# Proyecto Final: Curso de Ingeniería de Datos con Python

## Objetivo del Proyecto
Aplicar los conocimientos adquiridos en el curso construyendo un sistema de datos funcional end-to-end. 

## Rutas Posibles (Seleccionar al menos una principal o combinarlas):
1. **Ruta Pipeline (Enfoque Backend/ETL):** Extraer datos de una API/CSV, limpiarlos exhaustivamente, transformarlos y almacenarlos en una base de datos MySQL de forma automatizada.
2. **Ruta API (Enfoque Exposición):** Tomar datos procesados y construir una API robusta con FastAPI, implementando filtros, validaciones y conexión directa a base de datos.
3. **Ruta Dashboard (Enfoque Frontend/Analítica):** Consumir datos de una API o archivos Parquet/CSV procesados y construir un dashboard interactivo con Streamlit mostrando KPIs relevantes.

## Entregables Mínimos
- Repositorio estructurado (como esta plantilla).
- Archivo `requirements.txt` o manejo de dependencias.
- Código modularizado y comentado.
- Instrucciones claras de ejecución.

## Criterios de Evaluación
- **Funcionalidad:** El código se ejecuta sin errores.
- **Limpieza:** Uso de buenas prácticas (nombres de variables claros, modularidad).
- **Integración:** Conexión correcta entre al menos dos componentes (ej. Pipeline >> Base de Datos, o Base de Datos >> API).
- **Reproducibilidad:** Facilidad para levantar el proyecto usando Docker o instrucciones precisas.

## Planificación del Desarrollo
1. Definir el problema y seleccionar el dataset.
2. Construir la ingesta y limpieza.
3. Almacenar los datos.
4. Exponer mediante API o visualizar en Dashboard.
5. Empaquetar y documentar.
"""
    ruta_archivo = Path(ruta_base) / "README.md"
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_readme)
    print("Archivo generado: README.md")

def generar_archivos_configuracion(ruta_base):
    """
    Generar archivos de configuracion base para preparar la implementacion (ST8, ST11).
    """
    # Archivo requirements.txt
    contenido_req = """pandas>=2.0.0
fastapi>=0.100.0
uvicorn>=0.22.0
streamlit>=1.25.0
mysql-connector-python>=8.0.0
sqlalchemy>=2.0.0
"""
    with open(Path(ruta_base) / "requirements.txt", "w", encoding="utf-8") as req:
        req.write(contenido_req)
    print("Archivo generado: requirements.txt")

    # Archivo .gitignore
    contenido_gitignore = """__pycache__/
*.pyc
.env
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep
"""
    with open(Path(ruta_base) / ".gitignore", "w", encoding="utf-8") as gitignore:
        gitignore.write(contenido_gitignore)
    print("Archivo generado: .gitignore")
    
    # Crear archivos .gitkeep para mantener carpetas vacías en control de versiones
    for carpeta in ["data/raw", "data/processed"]:
        with open(Path(ruta_base) / carpeta / ".gitkeep", "w", encoding="utf-8") as gitkeep:
            gitkeep.write("")

def generar_scripts_plantilla(ruta_base):
    """
    Generar scripts vacios o con esqueleto inicial para guiar el desarrollo.
    """
    # Plantilla pipeline ETL
    contenido_etl = """# -*- coding: utf-8 -*-
# Script de ingesta y transformacion principal

def extraer_datos():
    pass

def transformar_datos(df):
    pass

def cargar_datos(df):
    pass

if __name__ == '__main__':
    print('Iniciando pipeline...')
    # df_raw = extraer_datos()
    # df_clean = transformar_datos(df_raw)
    # cargar_datos(df_clean)
"""
    with open(Path(ruta_base) / "src" / "pipeline" / "main_etl.py", "w", encoding="utf-8") as etl:
        etl.write(contenido_etl)
    print("Archivo generado: src/pipeline/main_etl.py")

def ejecutar_setup_proyecto(nombre_proyecto="mi_proyecto_final"):
    """
    Funcion principal para orquestar la creacion del scaffolding del proyecto final.
    """
    ruta_base = Path.cwd() / nombre_proyecto
    
    print(f"--- Configurando Proyecto Final en: {ruta_base} ---")
    crear_estructura_directorios(ruta_base)
    generar_archivo_readme(ruta_base)
    generar_archivos_configuracion(ruta_base)
    generar_scripts_plantilla(ruta_base)
    print("--- Configuracion completada con exito ---")
    print("¡Mucho exito en el desarrollo de tu Proyecto Final!")

if __name__ == "__main__":
    # Ejecutar la creacion de la estructura para el alumno
    ejecutar_setup_proyecto("proyecto_ingenieria_datos")
