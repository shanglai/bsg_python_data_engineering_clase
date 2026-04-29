# -*- coding: utf-8 -*-
"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 4: Pipeline de datos v1
Bloque 4: Ejecución completa del pipeline

Descripción: Script para ejecutar el pipeline de datos end-to-end.
Incluye ingesta, transformación, almacenamiento dual (MySQL y CSV/Parquet)
y validación de resultados (sanity checks).
"""

import os
import logging
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error

# ==========================================
# Configuración Inicial y Reproducibilidad
# ==========================================
# ST8: Documentación básica del flujo mediante logs estructurados
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Semilla para reproducibilidad de datos de prueba
np.random.seed(987654)

# Configuración de base de datos MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password', # Cambiar por el password real del entorno
    'database': 'curso_data_eng'
}

# Rutas de archivos
INPUT_FILE = 'datos_raw.csv'
OUTPUT_FILE = 'datos_procesados.csv'

# ==========================================
# Funciones Auxiliares (Preparación)
# ==========================================
def generar_datos_prueba(ruta_archivo: str):
    """Generar un dataset de prueba simulando datos de transacciones sucios."""
    if not os.path.exists(ruta_archivo):
        logging.info(f"Generando datos de prueba en {ruta_archivo}...")
        datos = {
            'id_transaccion': range(1, 101),
            'id_cliente': np.random.randint(1000, 1050, 100),
            'monto': np.random.uniform(10.0, 500.0, 100),
            'fecha': pd.date_range(start='2023-01-01', periods=100, freq='D'),
            'estado': np.random.choice(['completado', 'pendiente', 'fallido', None], 100)
        }
        df = pd.DataFrame(datos)
        # Introducir algunos valores nulos aleatorios para simular suciedad
        df.loc[df.sample(frac=0.05).index, 'monto'] = np.nan
        df.to_csv(ruta_archivo, index=False)
        logging.info("Datos de prueba generados exitosamente.")

# ==========================================
# Módulos del Pipeline
# ==========================================

def extraer_datos(ruta_archivo: str) -> pd.DataFrame:
    """
    Fase de Ingesta: Leer datos desde la fuente (CSV).
    """
    logging.info(f"Iniciando extracción de datos desde {ruta_archivo}")
    try:
        df = pd.read_csv(ruta_archivo)
        logging.info(f"Datos extraídos correctamente. Registros leídos: {len(df)}")
        return df
    except Exception as e:
        # ST5: Manejo de errores en ejecución completa
        logging.error(f"Error al extraer los datos: {e}")
        raise

def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fase de Transformación: Limpiar y enriquecer los datos.
    """
    logging.info("Iniciando transformación de datos.")
    try:
        # ST9: Análisis de resultados (estado inicial)
        registros_iniciales = len(df)
        
        # 1. Limpieza: Eliminar nulos en columnas críticas
        df_limpio = df.dropna(subset=['monto', 'estado']).copy()
        
        # 2. Transformación: Filtrar solo transacciones completadas
        df_limpio = df_limpio[df_limpio['estado'] == 'completado']
        
        # 3. Enriquecimiento: Crear variable derivada (categoría de monto)
        df_limpio['categoria_monto'] = np.where(df_limpio['monto'] > 250, 'Alto', 'Bajo')
        
        registros_finales = len(df_limpio)
        logging.info(f"Transformación exitosa. Registros retenidos: {registros_finales} de {registros_iniciales}")
        return df_limpio
    
    except Exception as e:
        # ST6: Identificación de fallos en transformación
        logging.error(f"Error en la transformación de datos: {e}")
        raise

def cargar_datos_archivo(df: pd.DataFrame, ruta_salida: str):
    """
    Fase de Almacenamiento (Archivos): Persistir resultados en CSV.
    """
    logging.info(f"Iniciando carga de datos en archivo {ruta_salida}")
    try:
        df.to_csv(ruta_salida, index=False)
        logging.info("Datos almacenados en archivo exitosamente.")
    except Exception as e:
        logging.error(f"Error al guardar en archivo: {e}")
        raise

def cargar_datos_mysql(df: pd.DataFrame, config: dict):
    """
    Fase de Almacenamiento (Base de Datos): Persistir en MySQL.
    ST2: Integración completa de almacenamiento.
    """
    logging.info("Iniciando carga de datos en MySQL...")
    conexion = None
    try:
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        
        # Crear tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacciones_procesadas (
                id_transaccion INT PRIMARY KEY,
                id_cliente INT,
                monto FLOAT,
                fecha DATE,
                estado VARCHAR(20),
                categoria_monto VARCHAR(10)
            )
        """)
        
        # Limpiar tabla para evitar duplicados en la reejecución (idempotencia)
        # ST7: Pipeline reproducible
        cursor.execute("TRUNCATE TABLE transacciones_procesadas")
        
        # Preparar datos para inserción
        insert_query = """
            INSERT INTO transacciones_procesadas 
            (id_transaccion, id_cliente, monto, fecha, estado, categoria_monto) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        datos_insertar = [tuple(x) for x in df.to_numpy()]
        
        # Inserción masiva
        cursor.executemany(insert_query, datos_insertar)
        conexion.commit()
        logging.info(f"Se insertaron {cursor.rowcount} registros en MySQL.")
        
    except Error as e:
        logging.error(f"Error conectando o insertando en MySQL: {e}")
        logging.warning("El pipeline continuará, pero la persistencia en DB falló.")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
            logging.info("Conexión a MySQL cerrada.")

def realizar_sanity_checks(df: pd.DataFrame):
    """
    ST3, ST4: Validación de resultados y sanity checks (conteo, métricas).
    Asegurar que los datos cumplen las reglas de negocio antes de darlos por buenos.
    """
    logging.info("Ejecutando Sanity Checks...")
    errores = []
    
    # Check 1: No debe haber montos nulos
    if df['monto'].isnull().sum() > 0:
        errores.append("Check Fallido: Existen montos nulos en los datos procesados.")
        
    # Check 2: Todos los estados deben ser 'completado'
    if not (df['estado'] == 'completado').all():
        errores.append("Check Fallido: Existen transacciones no completadas en la salida.")
        
    # Check 3: Conteo mínimo (ej. asegurar que el pipeline no borró todo)
    if len(df) == 0:
        errores.append("Check Fallido: El dataset procesado está vacío.")
        
    if errores:
        for error in errores:
            logging.error(error)
        raise ValueError("Los datos procesados no pasaron los Sanity Checks.")
    else:
        logging.info("Sanity Checks aprobados con éxito. Los datos son consistentes.")

# ==========================================
# Orquestación del Pipeline (Main)
# ==========================================

def ejecutar_pipeline():
    """
    ST1, ST10: Ejecución end-to-end del pipeline de datos funcional.
    Integra de forma secuencial la ingesta, transformación, validación y almacenamiento.
    """
    logging.info("=== INICIANDO EJECUCIÓN DEL PIPELINE V1 ===")
    
    try:
        # ST11: Preparación para automatización (estructurado de forma procedural y limpia)
        
        # 0. Preparar entorno
        generar_datos_prueba(INPUT_FILE)
        
        # 1. Ingesta
        df_raw = extraer_datos(INPUT_FILE)
        
        # 2. Transformación
        df_procesado = transformar_datos(df_raw)
        
        # 3. Validación (Sanity Checks)
        realizar_sanity_checks(df_procesado)
        
        # 4. Almacenamiento Dual
        cargar_datos_archivo(df_procesado, OUTPUT_FILE)
        cargar_datos_mysql(df_procesado, DB_CONFIG)
        
        logging.info("=== PIPELINE EJECUTADO EXITOSAMENTE ===")
        
    except Exception as e:
        # ST5, ST6: Manejo de errores global y reporte de fallos
        logging.error(f"=== FALLO CRÍTICO EN EL PIPELINE: {e} ===")
        logging.info("Revisar los logs anteriores para identificar el punto de fallo.")

if __name__ == "__main__":
    ejecutar_pipeline()
