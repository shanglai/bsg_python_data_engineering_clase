# -*- coding: utf-8 -*-

"""
Capítulo 4: Manejo de datos y despliegue local
Sección 8: Docker y entorno reproducible
Bloque 1: Introducción a Docker

Descripción:
Este script sirve como base teórica y práctica para introducir los conceptos
de Docker en el contexto de la ingeniería de datos. El código a continuación
representa un mini-pipeline que ejemplifica el problema "en mi máquina funciona",
preparando el terreno para su posterior contenedorización.

Subtemas abordados en la documentación del script:
ST1: Problema de entornos no reproducibles.
ST2: "Works on my machine" problem.
ST3: Introducción a Docker.
ST4: Concepto de imagen.
ST5: Concepto de contenedor.
ST6: Diferencia entre VM y contenedor.
ST7: Uso de Docker en ingeniería de datos.
ST8: Instalación y ejecución básica (Conceptos).
ST9: Ciclo de vida de contenedores.
ST10: Beneficios (portabilidad, consistencia).
ST11: Docker en pipelines reales.
"""

import sys
import os
import platform
import random

# =============================================================================
# NOTAS TEÓRICAS: INTRODUCCIÓN A DOCKER (ST1 - ST11)
# =============================================================================
#
# ST1 & ST2: El problema de entornos no reproducibles ("Works on my machine")
# Frecuentemente un script de datos funciona en la laptop del desarrollador
# pero falla en producción debido a versiones distintas de Python, librerías
# faltantes o diferencias en el sistema operativo (rutas de archivos, etc.).
#
# ST3: Introducción a Docker
# Docker es una plataforma que permite empaquetar aplicaciones y sus dependencias
# en unidades estandarizadas llamadas "contenedores", garantizando que el software
# se ejecute de la misma forma en cualquier entorno.
#
# ST4 & ST5: Imagen vs Contenedor
# - Imagen: Es una plantilla de solo lectura (como una receta o un plano). Contiene
#   el código, las librerías, las variables de entorno y los archivos de configuración.
# - Contenedor: Es una instancia en ejecución de una imagen.
#
# ST6: VM vs Contenedor
# A diferencia de una Máquina Virtual (VM) que emula un sistema operativo completo
# (consumiendo muchos recursos), un contenedor comparte el kernel del sistema 
# operativo host, haciéndolo mucho más ligero y rápido.
#
# ST7 & ST11: Docker en Ingeniería de Datos
# Se utiliza para garantizar que un pipeline de ingesta, transformación o 
# entrenamiento de modelos se ejecute idénticamente en desarrollo, testing y 
# producción (portabilidad y consistencia - ST10).
#
# ST8 & ST9: Ciclo de Vida
# Instalación local -> Crear código -> Construir Imagen (build) -> 
# Ejecutar Contenedor (run) -> Detener/Destruir (stop/rm).
# =============================================================================

def Validar_entorno():
    """
    Mostrar información del entorno actual.
    Esto ejemplifica las variables que causan el problema "en mi máquina funciona".
    """
    print("--- Verificación de Entorno de Ejecución ---")
    print(f"Sistema Operativo: {platform.system()} {platform.release()}")
    print(f"Versión de Python: {sys.version.split(' ')[0]}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    print("-" * 44)
    print("Nota: Si este script se ejecuta en otra máquina, estos valores cambiarán.")
    print("Docker nos ayudará a estandarizar este entorno.\n")

def Generar_datos_ficticios():
    """
    Generar un archivo temporal simulando un proceso de pipeline.
    Utilizar semilla aleatoria para reproducibilidad en la generación.
    """
    random.seed(987654)
    
    directorio_salida = "output_data"
    nombre_archivo = "transacciones_demo.csv"
    
    # Crear directorio si no existe
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        
    ruta_completa = os.path.join(directorio_salida, nombre_archivo)
    
    print("--- Ejecutando proceso de datos ---")
    print("Generando transacciones ficticias...")
    
    try:
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write("id_transaccion,monto,estado\n")
            for i in range(1, 6):
                monto = round(random.uniform(10.0, 500.0), 2)
                estado = random.choice(["Aprobado", "Rechazado", "Pendiente"])
                f.write(f"{i},{monto},{estado}\n")
                
        print(f"Exito: Archivo generado en la ruta {ruta_completa}")
        print("Lectura de validacion del archivo:")
        
        with open(ruta_completa, "r", encoding="utf-8") as f:
            contenido = f.read()
            print(contenido)
            
    except Exception as e:
        print(f"Error al generar los datos: {e}")

def Simular_falla_dependencia():
    """
    Hacer una llamada a una libreria que podria no estar instalada.
    Representa el clásico error de dependencias faltantes en pipelines.
    """
    print("--- Simulando carga de librerias externas ---")
    try:
        import pandas as pd
        print(f"Pandas cargado correctamente. Version: {pd.__version__}")
    except ImportError:
        print("ADVERTENCIA: 'pandas' no esta instalado en este entorno local.")
        print("En un contenedor Docker, asegurariamos su instalacion mediante un requirements.txt.")

def Ejecutar_pipeline_base():
    """
    Ejecutar el flujo completo del script introductorio.
    """
    Validar_entorno()
    Simular_falla_dependencia()
    print("\n")
    Generar_datos_ficticios()
    print("\nProceso finalizado. Preparado para contenedorizacion en el siguiente bloque.")

if __name__ == "__main__":
    Ejecutar_pipeline_base()
