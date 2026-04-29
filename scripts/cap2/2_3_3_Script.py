# -*- coding: utf-8 -*-
"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 3: SQL y MySQL
Bloque 3: Conexión Python -> MySQL

Descripción:
Script para demostrar la conexión entre Python y una base de datos MySQL. 
Se incluyen ejemplos utilizando las librerías `mysql-connector-python` y `SQLAlchemy`.
Se abordan buenas prácticas como el manejo de errores, prevención de inyección SQL 
(uso de parámetros) y la conversión directa de resultados a DataFrames de Pandas 
para su uso en un pipeline de datos.

Requisitos previos (ejecutar en terminal):
> pip install mysql-connector-python sqlalchemy pandas

Nota: Se asume que existe un servidor MySQL en ejecución con una base de datos 
llamada 'curso_data_engineering' y una tabla 'transacciones'.
"""

import random
import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

# Establecer semilla aleatoria para consistencia en caso de generar datos sintéticos
random.seed(987654)

# =============================================================================
# 1. Configuración de credenciales de la base de datos
# =============================================================================
# NOTA: En un entorno real, extraer estas credenciales desde variables de 
# entorno (.env) por seguridad. Nunca dejarlas en el código fuente.
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'password'  # Reemplazar con la contraseña real
DB_NAME = 'curso_data_engineering'

# =============================================================================
# 2. Conexión nativa y ejecución de queries (mysql-connector)
# =============================================================================

def conectar_mysql():
    """
    Generar y retornar una conexión a la base de datos MySQL.
    Incluye manejo de errores para evitar que el pipeline colapse (ST7).
    """
    conexion = None
    try:
        # Intentar establecer la conexión
        conexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if conexion.is_connected():
            print("[INFO] Conexión exitosa a la base de datos MySQL.")
    except Error as e:
        print(f"[ERROR] Fallo al conectar a MySQL: {e}")
        
    return conexion

def consultar_datos_basicos(conexion):
    """
    Hacer una consulta básica y leer los resultados en estructuras de Python (ST4, ST5).
    """
    if not conexion or not conexion.is_connected():
        print("[AVISO] No hay conexión activa. Omitiendo consulta básica.")
        return

    try:
        # dictionary=True retorna los registros como diccionarios en lugar de tuplas
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT id_transaccion, cliente_id, monto FROM transacciones LIMIT 5;"
        
        print(f"\n[INFO] Ejecutando query: {query}")
        cursor.execute(query)
        
        # Recuperar todos los registros resultantes
        resultados = cursor.fetchall()
        
        print("[INFO] Resultados obtenidos (Estructura nativa Python):")
        for fila in resultados:
            print(fila)
            
    except Error as e:
        print(f"[ERROR] Problema al ejecutar la consulta: {e}")
    finally:
        # Siempre cerrar el cursor para liberar recursos de memoria
        if 'cursor' in locals() and cursor:
            cursor.close()

# =============================================================================
# 3. Seguridad: Prevención de Inyección SQL (ST10, ST11)
# =============================================================================

def consultar_datos_con_parametros(conexion, limite_monto):
    """
    Hacer una consulta utilizando parámetros para evitar inyección SQL.
    Nunca concatenar variables de texto directamente en la instrucción SQL.
    """
    if not conexion or not conexion.is_connected():
        return

    try:
        cursor = conexion.cursor(dictionary=True)
        # Uso de '%s' como marcador de posición (placeholder) para los parámetros
        query = "SELECT cliente_id, monto FROM transacciones WHERE monto > %s LIMIT 3;"
        
        # Los parámetros siempre deben pasarse como una tupla
        parametros = (limite_monto,)
        
        print(f"\n[INFO] Ejecutando query parametrizada (monto > {limite_monto})...")
        cursor.execute(query, parametros)
        
        resultados = cursor.fetchall()
        for fila in resultados:
            print(fila)
            
    except Error as e:
        print(f"[ERROR] Problema en la consulta parametrizada: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

# =============================================================================
# 4. Integración con Pandas usando SQLAlchemy (ST2, ST6, ST8)
# =============================================================================

def extraer_datos_a_dataframe():
    """
    Generar una conexión mediante SQLAlchemy para cargar los datos 
    directamente en un DataFrame de Pandas. Esta es la práctica más común 
    en un pipeline de datos por su eficiencia y legibilidad.
    """
    print("\n[INFO] Extrayendo datos hacia un DataFrame de Pandas (SQLAlchemy)...")
    
    # Crear la cadena de conexión estándar (Connection String)
    cadena_conexion = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    try:
        # Crear el motor de conexión (engine)
        motor = create_engine(cadena_conexion)
        
        # Definir la consulta analítica
        query = """
            SELECT 
                cliente_id, 
                COUNT(id_transaccion) as total_transacciones,
                SUM(monto) as monto_total
            FROM transacciones
            GROUP BY cliente_id
            ORDER BY monto_total DESC
            LIMIT 5;
        """
        
        # pd.read_sql maneja la conexión, ejecución y conversión de resultados a DataFrame
        df_resultados = pd.read_sql(query, con=motor)
        
        print("[INFO] Datos cargados exitosamente en el DataFrame:")
        print(df_resultados)
        
        return df_resultados
        
    except Exception as e:
        print(f"[ERROR] Fallo al interactuar con SQLAlchemy/Pandas: {e}")
        return None

# =============================================================================
# 5. Capa de Acceso a Datos (Buenas Prácticas de Separación de Lógica) (ST9)
# =============================================================================

def ejecutar_pipeline_ingesta():
    """
    Hacer la orquestación de la capa de acceso a datos. 
    Mantener la lógica de la base de datos aislada del resto del sistema.
    """
    print("=== INICIANDO CAPA DE ACCESO A DATOS ===")
    
    # 1. Establecer conexión cruda (útil para validaciones previas o comandos de escritura ligeros)
    conexion = conectar_mysql()
    
    if conexion and conexion.is_connected():
        # 2. Ejecutar consultas aisladas de prueba
        consultar_datos_basicos(conexion)
        consultar_datos_con_parametros(conexion, 1000.0)
        
        # 3. Cerrar conexión nativa explícitamente
        conexion.close()
        print("\n[INFO] Conexión nativa cerrada correctamente.")
        
    # 4. Procesamiento masivo usando la integración Pandas + SQLAlchemy
    df_pipeline = extraer_datos_a_dataframe()
    
    if df_pipeline is not None:
        print("\n[INFO] Pipeline de ingesta finalizado. Datos listos para la etapa de transformación.")

# =============================================================================
# Punto de entrada del script
# =============================================================================
if __name__ == "__main__":
    ejecutar_pipeline_ingesta()
