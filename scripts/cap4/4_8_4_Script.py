# -*- coding: utf-8 -*-

# =============================================================================
# Capítulo 4: Manejo de datos y despliegue local
# Sección 8: Docker y entorno reproducible
# Bloque 4: docker-compose y servicios
# =============================================================================

# Descripción:
# Script para generar los archivos necesarios que componen el sistema completo.
# Incluye la definicion del pipeline, la API, las dependencias, el Dockerfile
# y el archivo docker-compose.yaml para orquestar multiples servicios.

import os
import random

# Definir semilla para procesos aleatorios
random.seed(987654)

def generar_requirements():
    """
    Generar el archivo requirements.txt con las dependencias del proyecto.
    """
    contenido = """pandas==2.1.1
sqlalchemy==2.0.21
pymysql==1.1.0
fastapi==0.103.2
uvicorn==0.23.2
"""
    with open("requirements.txt", "w", encoding="utf-8") as file:
        file.write(contenido)
    print("Archivo requirements.txt generado exitosamente.")

def generar_dockerfile():
    """
    Generar el Dockerfile para construir la imagen de Python que compartiran
    la API y el pipeline.
    """
    contenido = """# Usar imagen base ligera de Python
FROM python:3.9-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo fuente al contenedor
COPY . .
"""
    with open("Dockerfile", "w", encoding="utf-8") as file:
        file.write(contenido)
    print("Archivo Dockerfile generado exitosamente.")

def generar_docker_compose():
    """
    Definir y generar el archivo compose.yaml para orquestar los contenedores.
    Se definen tres servicios: db (MySQL), api (FastAPI) y pipeline (Python script).
    """
    contenido = """version: '3.8'

services:
  # Servicio de Base de Datos
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: pipeline_db
      MYSQL_USER: data_user
      MYSQL_PASSWORD: data_password
    ports:
      - "3306:3306"
    networks:
      - data_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Servicio de Pipeline de Datos
  pipeline:
    build: .
    command: python pipeline.py
    depends_on:
      db:
        condition: service_healthy
    networks:
      - data_network

  # Servicio de API para consumir datos
  api:
    build: .
    command: uvicorn api:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    networks:
      - data_network

networks:
  data_network:
    driver: bridge
"""
    with open("compose.yaml", "w", encoding="utf-8") as file:
        file.write(contenido)
    print("Archivo compose.yaml generado exitosamente.")

def generar_pipeline():
    """
    Generar el script de pipeline.py que simula la extraccion, transformacion
    y carga (ETL) de datos hacia la base de datos MySQL desplegada en Docker.
    """
    contenido = """# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine
import time

def ejecutar_pipeline():
    print("Iniciando procesamiento de datos en el pipeline...")
    
    # Simular extraccion de datos
    datos = {
        'transaccion_id': [1, 2, 3, 4, 5],
        'cliente_id': [101, 102, 101, 103, 102],
        'monto': [250.50, 100.00, 45.25, 500.00, 150.75],
        'estado': ['COMPLETADO', 'COMPLETADO', 'FALLIDO', 'COMPLETADO', 'COMPLETADO']
    }
    df = pd.DataFrame(datos)
    
    # Simular transformacion (limpieza y filtrado)
    df_limpio = df[df['estado'] == 'COMPLETADO'].copy()
    df_limpio['monto_con_impuesto'] = df_limpio['monto'] * 1.16
    print("Transformacion completada. Registros validos:", len(df_limpio))
    
    # Cadena de conexion a MySQL (usando el nombre del servicio 'db' en docker-compose)
    conexion_str = "mysql+pymysql://data_user:data_password@db:3306/pipeline_db"
    motor = create_engine(conexion_str)
    
    # Cargar datos a la base de datos
    try:
        df_limpio.to_sql(name='transacciones_procesadas', con=motor, if_exists='replace', index=False)
        print("Datos cargados exitosamente en la base de datos MySQL.")
    except Exception as e:
        print(f"Error al cargar datos en la base de datos: {e}")

if __name__ == "__main__":
    # Pausa breve para asegurar que la conexion se estabilice tras el healthcheck
    time.sleep(2)
    ejecutar_pipeline()
"""
    with open("pipeline.py", "w", encoding="utf-8") as file:
        file.write(contenido)
    print("Archivo pipeline.py generado exitosamente.")

def generar_api():
    """
    Generar el script api.py que expone los datos procesados mediante endpoints
    HTTP utilizando FastAPI.
    """
    contenido = """# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import pandas as pd

app = FastAPI(title="API de Transacciones Procesadas")

# Configurar motor de conexion a la base de datos
conexion_str = "mysql+pymysql://data_user:data_password@db:3306/pipeline_db"
motor = create_engine(conexion_str)

@app.get("/")
def estado_servicio():
    return {"estado": "Servicio de API funcionando correctamente"}

@app.get("/transacciones")
def obtener_transacciones(limite: int = 10):
    try:
        query = f"SELECT * FROM transacciones_procesadas LIMIT {limite}"
        df = pd.read_sql(query, con=motor)
        # Retornar los datos serializados en formato JSON
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando base de datos: {str(e)}")

@app.get("/transacciones/cliente/{cliente_id}")
def obtener_transacciones_cliente(cliente_id: int):
    try:
        query = text("SELECT * FROM transacciones_procesadas WHERE cliente_id = :cid")
        df = pd.read_sql(query, con=motor, params={"cid": cliente_id})
        if df.empty:
            raise HTTPException(status_code=404, detail="No se encontraron transacciones para el cliente")
        return df.to_dict(orient="records")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
"""
    with open("api.py", "w", encoding="utf-8") as file:
        file.write(contenido)
    print("Archivo api.py generado exitosamente.")

def ejecutar_creacion_entorno():
    """
    Hacer la generacion de todos los archivos que componen el bloque
    de orquestacion de contenedores.
    """
    print("Iniciando la creacion de archivos para docker-compose...")
    generar_requirements()
    generar_dockerfile()
    generar_docker_compose()
    generar_pipeline()
    generar_api()
    print("Todos los archivos han sido generados. Para iniciar el entorno, ejecutar: docker-compose up --build")

if __name__ == "__main__":
    ejecutar_creacion_entorno()
