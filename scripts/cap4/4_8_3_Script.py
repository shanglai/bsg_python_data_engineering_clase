# -*- coding: utf-8 -*-

"""
Capítulo 4: Manejo de datos y despliegue local
Sección 8: Docker y entorno reproducible
Bloque 3: requirements.txt y dependencias

Este script demuestra cómo gestionar las dependencias de un proyecto en Python,
la generación de un archivo requirements.txt, la fijación de versiones y la
validación de librerías externas, conceptos clave para preparar el entorno
para un contenedor Docker.
"""

import os
import subprocess
import sys
import random

# Establecer semilla aleatoria por convención del curso
random.seed(987654)

def generar_requirements_manual():
    """
    ST1: Gestión de dependencias en Python
    ST2: Uso de requirements.txt
    ST4: Fijación de versiones
    ST10: Buenas prácticas de dependencias
    
    Generar un archivo requirements.txt definiendo explícitamente las versiones.
    Esto previene problemas de compatibilidad al asegurar que el entorno sea
    exactamente igual en desarrollo y en producción (Docker).
    """
    print(">> Generando archivo requirements.txt manual con versiones fijas...")
    
    # Lista de dependencias esenciales para nuestro pipeline de datos y API
    # Se utiliza la convención == para fijar la versión exacta.
    dependencias = [
        "pandas==2.1.1",
        "fastapi==0.103.1",
        "uvicorn==0.23.2",
        "mysql-connector-python==8.1.0",
        "streamlit==1.27.0"
    ]
    
    ruta_archivo = "requirements.txt"
    
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            for dep in dependencias:
                f.write(f"{dep}\n")
        print(f">> Archivo {ruta_archivo} generado exitosamente.")
    except Exception as e:
        print(f">> Error al generar {ruta_archivo}: {e}")

def generar_dependencias_freeze():
    """
    ST3: Generación de dependencias (pip freeze)
    ST8: Reproducibilidad del entorno
    
    Hacer uso de pip freeze mediante el módulo subprocess para capturar
    todas las dependencias actualmente instaladas en el entorno activo.
    """
    print(">> Ejecutando pip freeze para capturar el entorno actual...")
    ruta_freeze = "requirements_freeze.txt"
    
    try:
        # Ejecutar el comando pip freeze e interceptar la salida
        resultado = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        with open(ruta_freeze, "w", encoding="utf-8") as f:
            f.write(resultado.stdout)
            
        print(f">> Archivo {ruta_freeze} generado mediante pip freeze.")
    except subprocess.CalledProcessError as e:
        print(f">> Error al ejecutar pip freeze: {e}")
    except Exception as e:
        print(f">> Error inesperado: {e}")

def simular_integracion_dockerfile():
    """
    ST6: Integración con Dockerfile
    ST7: Instalación de dependencias en contenedor
    ST11: Preparación para despliegue
    
    Generar un Dockerfile de demostración que muestra cómo se integra
    el requirements.txt en el proceso de construcción de la imagen.
    """
    print(">> Generando Dockerfile de ejemplo para demostrar la integración...")
    
    contenido_dockerfile = """# Usar imagen base oficial de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar UNICAMENTE el archivo de dependencias primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instalar dependencias en el contenedor (ST7)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del pipeline
COPY . .

# Comando por defecto
CMD ["python", "pipeline.py"]
"""
    ruta_dockerfile = "Dockerfile_demo"
    
    try:
        with open(ruta_dockerfile, "w", encoding="utf-8") as f:
            f.write(contenido_dockerfile)
        print(">> Dockerfile generado. Nota cómo COPY requirements.txt precede a RUN pip install.")
    except Exception as e:
        print(f">> Error al generar el Dockerfile: {e}")

def validar_librerias_externas():
    """
    ST5: Problemas de compatibilidad
    ST9: Manejo de librerías externas
    
    Validar si las librerías críticas para el pipeline están disponibles
    en el entorno actual y capturar problemas si las versiones no coinciden
    o no están instaladas.
    """
    print(">> Validando librerías externas en el entorno actual...")
    
    librerias_a_revisar = ["pandas", "fastapi", "mysql.connector", "streamlit"]
    
    for lib en librerias_a_revisar:
        try:
            # Intento de importación dinámica
            modulo = __import__(lib)
            # Intentar obtener la versión si está disponible
            version = getattr(modulo, "__version__", "Version desconocida")
            print(f"   [OK] {lib} instalado (Version: {version})")
        except ImportError:
            print(f"   [ERROR] {lib} no esta instalado. Posible problema de compatibilidad o falta ejecutar 'pip install -r requirements.txt'.")

def main():
    """
    Función principal para orquestar la demostración de gestión de dependencias.
    """
    print("=== Inicio de Gestión de Dependencias (Bloque 4.8.3) ===")
    
    # 1. Crear un requirements.txt con versiones específicas
    generar_requirements_manual()
    print("-" * 50)
    
    # 2. Demostrar cómo se extraen dependencias del entorno real
    generar_dependencias_freeze()
    print("-" * 50)
    
    # 3. Mostrar cómo esto se conecta con el despliegue
    simular_integracion_dockerfile()
    print("-" * 50)
    
    # 4. Comprobar el entorno actual
    validar_librerias_externas()
    
    print("=== Fin de ejecución ===")

if __name__ == "__main__":
    main()
