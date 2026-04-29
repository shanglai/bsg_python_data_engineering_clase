# -*- coding: utf-8 -*-

"""
Capítulo 6: Integración, despliegue y proyecto final
Sección 12: Presentación de proyecto e IA aplicada
Bloque 3: IA como acelerador de ingeniería

Este script demuestra cómo utilizar Inteligencia Artificial (LLMs) como
un copiloto en la ingeniería de datos. Contiene ejemplos de prompts
bien estructurados y el código resultante aplicable a pipelines.
"""

import pandas as pd
import numpy as np

# Establecer semilla para reproducibilidad
np.random.seed(987654)

# =============================================================================
# Subtema 8: Buenas prácticas de prompting
# =============================================================================
# Un buen prompt debe contener:
# 1. Contexto: ¿Qué estamos haciendo y quiénes somos?
# 2. Instrucción clara: ¿Qué necesitamos exactamente?
# 3. Restricciones: ¿Qué librerías usar? ¿Qué formatos evitar?
# =============================================================================

# =============================================================================
# Ejemplo 1: Generación de funciones de limpieza de datos (ST5)
# =============================================================================

PROMPT_LIMPIEZA = """
Contexto: Soy un ingeniero de datos construyendo un pipeline en Python.
Instrucción: Escribe una función en Python usando Pandas que reciba un DataFrame de transacciones. 
La función debe:
1. Rellenar los valores nulos de la columna 'monto' con la mediana.
2. Eliminar filas donde la columna 'id_cliente' sea nula.
3. Convertir la columna 'fecha' a formato datetime.
Restricciones: Usa Pandas, incluye docstrings, type hints y maneja posibles errores si la columna no existe.
"""

# Código generado por IA (Validado por el ingeniero):
def limpiar_datos_transacciones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpiar el DataFrame de transacciones aplicando reglas de negocio.
    
    Parametros:
        df (pd.DataFrame): DataFrame original con datos crudos.
        
    Retorna:
        pd.DataFrame: DataFrame limpio.
    """
    df_limpio = df.copy()
    
    try:
        # 1. Rellenar nulos en 'monto' con la mediana
        if 'monto' in df_limpio.columns:
            mediana_monto = df_limpio['monto'].median()
            df_limpio['monto'] = df_limpio['monto'].fillna(mediana_monto)
            
        # 2. Eliminar filas con 'id_cliente' nulo
        if 'id_cliente' in df_limpio.columns:
            df_limpio = df_limpio.dropna(subset=['id_cliente'])
            
        # 3. Convertir 'fecha' a datetime
        if 'fecha' in df_limpio.columns:
            df_limpio['fecha'] = pd.to_datetime(df_limpio['fecha'], errors='coerce')
            
    except Exception as e:
        print(f"Error durante la limpieza de datos: {e}")
        
    return df_limpio

# Generar datos de prueba para validar la función generada por IA (ST10)
def probar_limpieza_ia():
    datos_crudos = pd.DataFrame({
        'id_cliente': [1, 2, np.nan, 4, 5],
        'monto': [100.5, np.nan, 200.0, 50.0, np.nan],
        'fecha': ['2023-01-01', '2023/01/02', 'invalid_date', '2023-01-04', '2023-01-05']
    })
    
    print("Datos antes de limpieza (generados):")
    print(datos_crudos)
    
    datos_limpios = limpiar_datos_transacciones(datos_crudos)
    
    print("\nDatos despues de limpieza (funcion IA):")
    print(datos_limpios)

# =============================================================================
# Ejemplo 2: Generación de consultas SQL (ST6)
# =============================================================================

PROMPT_SQL = """
Contexto: Tenemos dos tablas en MySQL: 'transacciones' (id, id_cliente, monto, fecha) y 'clientes' (id, nombre, pais).
Instrucción: Genera una consulta SQL que calcule el monto total de transacciones por pais durante el mes de enero de 2023.
Restricciones: Usa un INNER JOIN. Ordena los resultados de mayor a menor monto. Excluye paises con un monto total menor a 500.
"""

# Código generado por IA:
QUERY_SQL_GENERADA = """
SELECT 
    c.pais,
    SUM(t.monto) as monto_total
FROM transacciones t
INNER JOIN clientes c ON t.id_cliente = c.id
WHERE t.fecha >= '2023-01-01' AND t.fecha < '2023-02-01'
GROUP BY c.pais
HAVING monto_total >= 500
ORDER BY monto_total DESC;
"""

# =============================================================================
# Ejemplo 3: Refactorización de código con IA (ST7)
# =============================================================================

# Código original (Poco eficiente, sin modularizar, nombres poco claros)
def procesar(x):
    l = []
    for i in range(len(x)):
        if x[i] > 0:
            l.append(x[i] * 1.16) # agregar impuesto
    return l

PROMPT_REFACTORIZACION = """
Contexto: Revisa la siguiente funcion en Python usada en un pipeline de datos.
Codigo:
def procesar(x):
    l = []
    for i in range(len(x)):
        if x[i] > 0:
            l.append(x[i] * 1.16)
    return l

Instrucción: Refactoriza este codigo para que sea mas eficiente, "pythonic" (usando listas por comprension o vectorizacion si es aplicable), y añade docstrings. Cambia los nombres de variables para que sean descriptivos.
"""

# Código refactorizado generado por IA:
def aplicar_impuestos_a_valores_positivos(valores: list) -> list:
    """
    Aplica una tasa de impuesto del 16% a todos los valores positivos de una lista.
    
    Parametros:
        valores (list): Lista de montos numericos.
        
    Retorna:
        list: Nueva lista con los montos con impuesto incluido.
    """
    TASA_IMPUESTO = 1.16
    return [monto * TASA_IMPUESTO for monto in valores if monto > 0]


# =============================================================================
# Ejemplo 4: Generación de APIs y Dockerfiles (ST3, ST4)
# =============================================================================

PROMPT_API_DOCKER = """
Contexto: Necesito exponer un modelo o pipeline de datos sencillo.
Instrucción: Genera el codigo para una API basica con FastAPI que tenga un endpoint GET '/status' que retorne {"status": "ok"}.
Luego, genera el Dockerfile optimizado para contenerizar esta API usando Python 3.9 slim.
"""

# Código generado por IA - API (main.py):
CODIGO_FASTAPI = """
from fastapi import FastAPI

app = FastAPI(title="Pipeline API", description="API generada con ayuda de IA")

@app.get("/status")
def read_status():
    return {"status": "ok", "message": "El pipeline esta operativo"}
"""

# Código generado por IA - Dockerfile:
DOCKERFILE_GENERADO = """
# Usar una imagen base ligera
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias (se asume que existe)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo de la aplicacion
COPY main.py .

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# =============================================================================
# Bloque de Ejecución Principal (Validación humana - ST10, ST11)
# =============================================================================
def ejecutar_demostracion():
    print("--- Demostracion de uso de IA en Ingenieria de Datos ---")
    print("1. IA como acelerador: La IA genero rapidamente la funcion de limpieza.")
    probar_limpieza_ia()
    
    print("\n2. Ejemplo de refactorizacion de codigo:")
    montos_originales = [-50, 100, 0, 200, 300]
    montos_procesados = aplicar_impuestos_a_valores_positivos(montos_originales)
    print(f"Montos originales: {montos_originales}")
    print(f"Montos con impuesto (refactorizado): {montos_procesados}")
    
    print("\nNota: La IA es un copiloto, la validacion humana siempre es requerida.")
    print("El ingeniero de datos debe asegurar la logica del negocio y la seguridad.")

if __name__ == "__main__":
    ejecutar_demostracion()
