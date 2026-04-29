# -*- coding: utf-8 -*-
# Capítulo 4: Manejo de datos y despliegue local
# Sección 7: Almacenamiento
# Bloque 3: Cloud storage (demo)

"""
Demostración de interacción con Cloud Storage (Object Storage).
En este script se utiliza Amazon S3 mediante la librería boto3 como ejemplo
de servicio común de almacenamiento en la nube. 
Se requiere instalar boto3 (pip install boto3) y configurar credenciales
para una ejecución exitosa en un entorno real.
"""

import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import pandas as pd
import numpy as np

# Configurar semilla para reproducibilidad
np.random.seed(987654)

# =============================================================================
# 1. Generar datos de prueba locales para la demostración
# =============================================================================
def generar_datos_prueba(ruta_archivo):
    """
    Generar un dataset de transacciones en formato CSV de manera local.
    Este archivo simula los datos generados por una etapa previa del pipeline.
    """
    print(">> Generando datos de prueba locales...")
    
    fechas = pd.date_range(start="2026-01-01", periods=100, freq="h")
    clientes = np.random.randint(1000, 1050, size=100)
    montos = np.round(np.random.uniform(10.0, 500.0, size=100), 2)
    
    df = pd.DataFrame({
        "fecha": fechas,
        "cliente_id": clientes,
        "monto": montos
    })
    
    df.to_csv(ruta_archivo, index=False, encoding='utf-8')
    print(f">> Archivo local generado exitosamente en: {ruta_archivo}")

# =============================================================================
# 2. Configurar cliente de almacenamiento en la nube (Conceptos y Seguridad)
# =============================================================================
def configurar_cliente_s3():
    """
    Configurar y retornar el cliente de AWS S3.
    En un entorno productivo, las credenciales no deben incluirse en el codigo.
    Se deben utilizar variables de entorno o roles de ejecucion (Seguridad basica).
    """
    print("\n>> Configurando cliente de Cloud Storage (S3)...")
    # boto3 automaticamente busca credenciales en ~/.aws/credentials o variables de entorno
    s3_client = boto3.client('s3')
    return s3_client

# =============================================================================
# 3. Subir archivos a la nube (Object Storage)
# =============================================================================
def subir_archivo_cloud(s3_client, ruta_local, nombre_bucket, nombre_objeto):
    """
    Subir un archivo local a un bucket en la nube.
    Demuestra la transicion de almacenamiento local a cloud.
    """
    print(f"\n>> Intentando subir '{ruta_local}' al bucket '{nombre_bucket}' como '{nombre_objeto}'...")
    try:
        s3_client.upload_file(ruta_local, nombre_bucket, nombre_objeto)
        print(">> Subida completada con exito.")
    except FileNotFoundError:
        print(">> Error: El archivo local no fue encontrado.")
    except NoCredentialsError:
        print(">> Error: No se encontraron credenciales de AWS.")
        print(">> (Demo: Simula que la subida fue exitosa para propositos del curso)")
    except ClientError as e:
        print(f">> Error del cliente S3: {e}")

# =============================================================================
# 4. Listar archivos en la nube
# =============================================================================
def listar_archivos_cloud(s3_client, nombre_bucket, prefijo=""):
    """
    Listar los objetos almacenados en un bucket.
    Demuestra la capacidad de organizar y buscar archivos (uso colaborativo).
    """
    print(f"\n>> Listando archivos en el bucket '{nombre_bucket}' con prefijo '{prefijo}'...")
    try:
        respuesta = s3_client.list_objects_v2(Bucket=nombre_bucket, Prefix=prefijo)
        if 'Contents' in respuesta:
            for obj in respuesta['Contents']:
                print(f"   - Archivo: {obj['Key']} | Tamano: {obj['Size']} bytes")
        else:
            print(">> El bucket esta vacio o no contiene objetos con ese prefijo.")
    except NoCredentialsError:
        print(">> Error: No se encontraron credenciales para listar objetos.")
        print(">> (Demo: Se espera ver una lista de archivos y sus tamanos)")
    except ClientError as e:
        print(f">> Error del cliente S3: {e}")

# =============================================================================
# 5. Descargar archivos de la nube
# =============================================================================
def descargar_archivo_cloud(s3_client, nombre_bucket, nombre_objeto, ruta_descarga):
    """
    Descargar un objeto desde la nube al almacenamiento local.
    """
    print(f"\n>> Intentando descargar '{nombre_objeto}' del bucket '{nombre_bucket}' a '{ruta_descarga}'...")
    try:
        s3_client.download_file(nombre_bucket, nombre_objeto, ruta_descarga)
        print(">> Descarga completada con exito.")
    except NoCredentialsError:
        print(">> Error: No se encontraron credenciales para descargar.")
        print(">> (Demo: Simula que la descarga se completo correctamente)")
    except ClientError as e:
        print(f">> Error del cliente S3: {e}")

# =============================================================================
# 6. Integracion directa con el Pipeline (Pandas + Cloud)
# =============================================================================
def integracion_pipeline_pandas(ruta_s3):
    """
    Demostrar como las herramientas modernas (como Pandas) se integran 
    directamente con Cloud Storage, evitando el paso de descarga manual.
    Requiere s3fs (pip install s3fs) para leer desde 's3://'.
    """
    print(f"\n>> Integracion de pipeline: Leyendo datos directamente desde {ruta_s3}...")
    try:
        # Pandas puede leer directamente de S3 si se tienen credenciales configuradas
        df_cloud = pd.read_csv(ruta_s3)
        print(">> Datos leidos desde la nube exitosamente:")
        print(df_cloud.head(3))
        
        # Transformacion de ejemplo en pipeline
        df_cloud['monto_con_impuesto'] = df_cloud['monto'] * 1.16
        print(">> Transformacion aplicada en memoria.")
        
    except Exception as e:
        print(">> No se pudo leer directamente de la nube (falta de credenciales o s3fs).")
        print(f">> Detalle del error: {e}")
        print(">> (Demo: En produccion, Pandas leera el archivo como si fuera local)")

# =============================================================================
# Bloque Principal de Ejecucion
# =============================================================================
if __name__ == "__main__":
    # Nombres de prueba
    ARCHIVO_LOCAL = "transacciones_pipeline.csv"
    ARCHIVO_DESCARGA = "transacciones_descargadas.csv"
    NOMBRE_BUCKET = "mi-bucket-ingenieria-datos-curso"
    LLAVE_OBJETO = "procesado/transacciones_pipeline.csv"
    RUTA_S3_PANDAS = f"s3://{NOMBRE_BUCKET}/{LLAVE_OBJETO}"
    
    # 1. Preparar datos
    generar_datos_prueba(ARCHIVO_LOCAL)
    
    # 2. Inicializar cliente
    s3_cliente = configurar_cliente_s3()
    
    # 3. Demostrar subida
    subir_archivo_cloud(s3_cliente, ARCHIVO_LOCAL, NOMBRE_BUCKET, LLAVE_OBJETO)
    
    # 4. Demostrar listado
    listar_archivos_cloud(s3_cliente, NOMBRE_BUCKET, prefijo="procesado/")
    
    # 5. Demostrar descarga
    descargar_archivo_cloud(s3_cliente, NOMBRE_BUCKET, LLAVE_OBJETO, ARCHIVO_DESCARGA)
    
    # 6. Demostrar integracion
    integracion_pipeline_pandas(RUTA_S3_PANDAS)
    
    # Limpieza local
    if os.path.exists(ARCHIVO_LOCAL):
        os.remove(ARCHIVO_LOCAL)
    if os.path.exists(ARCHIVO_DESCARGA):
        os.remove(ARCHIVO_DESCARGA)
        
    print("\n>> Fin de la demostracion de Cloud Storage.")
