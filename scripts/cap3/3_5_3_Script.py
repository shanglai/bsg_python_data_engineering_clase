# -*- coding: utf-8 -*-
"""
Capítulo 3: Exposición y consumo de datos
Sección 5: APIs con FastAPI
Bloque 3: Conexión API -> base de datos

Descripción:
Script para integrar una API construida con FastAPI a una base de datos MySQL.
Se implementa la capa de acceso a datos, ejecución de consultas dinámicas,
separación de responsabilidades y el uso de Pandas para retornar JSON.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
import pandas as pd

# ==========================================
# ST5, ST6: Capa de acceso a datos y separación
# ==========================================
# Configurar la conexión a la base de datos (valores de ejemplo)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "pipeline_db",
    "port": 3306
}

def obtener_conexion_db():
    """
    Generar y retornar una conexión a la base de datos MySQL.
    Implementa el manejo de conexiones (ST8) y aísla la lógica de DB.
    """
    conexion = None
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        # Retornar un error HTTP si la capa de datos falla
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    return conexion

# ==========================================
# ST1, ST9: Inicialización de la API
# ==========================================
# Generar la instancia de la aplicación FastAPI
app = FastAPI(
    title="API de Transacciones (Pipeline de Datos)",
    description="API para consumir datos procesados y almacenados en MySQL.",
    version="1.0.0"
)

@app.get("/")
def endpoint_raiz():
    """
    Proveer un endpoint básico para comprobar que la API está funcionando.
    """
    return {"mensaje": "Bienvenido a la API del Pipeline de Datos. El sistema está en línea."}

# ==========================================
# ST2, ST3, ST4, ST10: Ejecución de queries y conversión a JSON con Pandas
# ==========================================
@app.get("/transacciones")
def obtener_transacciones(limite: int = 100):
    """
    Consultar las transacciones almacenadas en la base de datos y retornarlas dinámicamente.
    Se limita la cantidad de registros por defecto para cuidar la performance básica (ST7).
    """
    conexion = obtener_conexion_db()
    try:
        # ST7: Performance básica - Seleccionar sólo las columnas necesarias
        query = """
            SELECT id_transaccion, fecha, id_cliente, monto, categoria 
            FROM transacciones 
            ORDER BY fecha DESC
            LIMIT %s
        """
        
        # ST10: Uso de DataFrames en APIs
        # Leer los datos directamente a un DataFrame de Pandas pasando parámetros seguros
        df_transacciones = pd.read_sql(query, conexion, params=(limite,))
        
        if df_transacciones.empty:
            return {"mensaje": "No se encontraron transacciones", "datos": []}
        
        # ST4: Conversión de resultados a JSON (diccionarios) para enviar por HTTP
        datos_json = df_transacciones.to_dict(orient="records")
        
        return {
            "mensaje": "Transacciones recuperadas exitosamente",
            "total_registros": len(datos_json),
            "datos": datos_json
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar la consulta: {str(e)}")
    finally:
        # ST8: Manejo de conexiones (asegurar el cierre para evitar saturar la base de datos)
        if conexion and conexion.is_connected():
            conexion.close()

# ==========================================
# ST6, ST11: Separación de lógica de negocio y escalabilidad
# ==========================================
@app.get("/transacciones/resumen")
def obtener_resumen_categoria():
    """
    Ejecutar una consulta de agregación dinámica desde la API.
    Delega el cálculo pesado a la base de datos (SQL) en lugar de procesarlo en Python,
    mejorando la performance (ST7) y preparándose para escalabilidad (ST11).
    """
    conexion = obtener_conexion_db()
    try:
        # Query de agregación en SQL
        query = """
            SELECT categoria, COUNT(*) as cantidad, SUM(monto) as monto_total
            FROM transacciones
            GROUP BY categoria
            ORDER BY monto_total DESC
        """
        
        # Usar el cursor nativo devolviendo diccionarios directamente
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        return {
            "mensaje": "Resumen por categoría generado exitosamente",
            "datos": resultados
        }
        
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

# Bloque de ejecución principal
if __name__ == "__main__":
    # Ejecutar servidor uvicorn de forma local para pruebas
    print("Iniciando servidor de FastAPI...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
