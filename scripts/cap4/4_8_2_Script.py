# -*- coding: utf-8 -*-

# =============================================================================
# Capítulo 4: Manejo de datos y despliegue local
# Sección 8: Docker y entorno reproducible
# Bloque 2: Creación de Dockerfile
# =============================================================================

import os

def generar_script_pipeline():
    """
    Generar un script de pipeline básico en Python.
    Este script será el que empaquetaremos dentro del contenedor Docker.
    (Cubre ST7: Inclusión del código del pipeline).
    """
    contenido_pipeline = """# -*- coding: utf-8 -*-
import pandas as pd
import os

def ejecutar_pipeline():
    print("Iniciando ejecución del pipeline dentro del contenedor...")
    
    # Crear datos simulados para el ejemplo
    datos = {
        'id_transaccion': [1, 2, 3],
        'monto': [150.5, 200.0, 50.75],
        'estado': ['completado', 'pendiente', 'completado']
    }
    
    df = pd.DataFrame(datos)
    print("Datos originales:")
    print(df)
    
    # Transformación básica
    df_filtrado = df[df['estado'] == 'completado']
    
    # Configurar entorno y guardado (Cubre ST8: Configuración del entorno)
    directorio_salida = 'output'
    os.makedirs(directorio_salida, exist_ok=True)
    
    ruta_salida = os.path.join(directorio_salida, 'datos_procesados.csv')
    df_filtrado.to_csv(ruta_salida, index=False)
    
    print(f"Pipeline finalizado. Datos guardados en {ruta_salida}")

if __name__ == '__main__':
    ejecutar_pipeline()
"""
    with open("pipeline.py", "w", encoding="utf-8") as f:
        f.write(contenido_pipeline)
    print(">> Archivo 'pipeline.py' generado exitosamente.")


def generar_requirements():
    """
    Generar un archivo requirements.txt simple para el contenedor.
    """
    contenido_req = "pandas==2.2.0\n"
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(contenido_req)
    print(">> Archivo 'requirements.txt' generado exitosamente.")


def generar_dockerfile():
    """
    Generar el archivo Dockerfile con las instrucciones básicas.
    (Cubre ST1: Concepto de Dockerfile, ST2: Instrucciones básicas,
    ST4: Orden de instrucciones, ST5: Capas en Docker, 
    ST6: Optimización básica, ST11: Buenas prácticas).
    """
    contenido_dockerfile = """# 1. Definir la imagen base (Instrucción FROM)
# Utilizamos una imagen oficial y ligera de Python (ST11: Buenas prácticas)
FROM python:3.10-slim

# 2. Establecer el directorio de trabajo dentro del contenedor (Configuración del entorno)
WORKDIR /app

# 3. Copiar solo el archivo de dependencias primero (Instrucción COPY)
# Esto aprovecha el sistema de caché de capas de Docker (ST4, ST5, ST6: Optimización básica).
# Si requirements.txt no cambia, Docker no reinstalará las dependencias en futuras construcciones.
COPY requirements.txt .

# 4. Instalar las dependencias (Instrucción RUN)
# Ejecuta comandos en el contenedor durante el proceso de construcción.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código del pipeline (Instrucción COPY)
# (ST7: Inclusión del código del pipeline)
COPY pipeline.py .

# 6. Definir el comando por defecto al iniciar el contenedor (Instrucción CMD)
# A diferencia de RUN (que ocurre en el build), CMD ocurre al ejecutar el contenedor.
CMD ["python", "pipeline.py"]
"""
    with open("Dockerfile", "w", encoding="utf-8") as f:
        f.write(contenido_dockerfile)
    print(">> Archivo 'Dockerfile' generado exitosamente.")


def mostrar_instrucciones_docker():
    """
    Imprimir en consola los comandos necesarios para construir, ejecutar 
    y debugear el contenedor.
    (Cubre ST3: Construcción de imagen, ST9: Ejecución de contenedor, ST10: Debugging básico).
    """
    instrucciones = """
=============================================================================
INSTRUCCIONES PARA CONSTRUIR Y EJECUTAR EL CONTENEDOR (ST3, ST9, ST10)
=============================================================================

1. Construir la imagen de Docker (ST3):
   Abre tu terminal en este directorio y ejecuta:
   >> docker build -t mi_pipeline_datos:v1 .
   
   (Nota: El punto '.' al final indica que el Dockerfile está en el directorio actual.
   Docker descargará la imagen base de Python, copiará los archivos, instalará pandas
   y guardará la imagen resultante).

2. Ejecutar el contenedor (ST9):
   Para correr el pipeline empaquetado de forma aislada, ejecuta:
   >> docker run --name ejecucion_pipeline mi_pipeline_datos:v1

3. Debugging básico (ST10):
   Si el pipeline falla o quieres inspeccionar el contenedor por dentro, 
   puedes sobreescribir el comando CMD e iniciar una sesión interactiva (bash):
   >> docker run -it mi_pipeline_datos:v1 /bin/bash
   
   Comandos útiles para limpiar:
   >> docker rm ejecucion_pipeline   (Elimina el contenedor finalizado)
   >> docker rmi mi_pipeline_datos:v1 (Elimina la imagen creada)
=============================================================================
"""
    print(instrucciones)


def main():
    """
    Función principal para orquestar la generación de los archivos del bloque.
    """
    print("Generando material para Capítulo 4, Sección 8, Bloque 2...\n")
    generar_script_pipeline()
    generar_requirements()
    generar_dockerfile()
    mostrar_instrucciones_docker()

if __name__ == '__main__':
    main()
