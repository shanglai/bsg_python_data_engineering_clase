# -*- coding: utf-8 -*-
# =============================================================================
# Capítulo 5: Automatización y orquestación
# Sección 9: Automatización de procesos
# Bloque 1: Scripts automatizados
# =============================================================================

"""
Este script demuestra la estructuración de un pipeline de datos para su
automatización. Se resalta la diferencia entre ejecución manual (hardcoded)
y una ejecución automatizada, parametrizada y reproducible (procesos batch).

Subtemas cubiertos:
- ST1: Concepto de automatización en ingeniería de datos.
- ST2: Diferencia entre ejecución manual y automática.
- ST3: Pipelines batch (procesos por lotes).
- ST4: Frecuencia de actualización de datos.
- ST5: Estructuración de scripts ejecutables.
- ST6: Parametrización básica de scripts.
- ST7: Reproducibilidad en ejecuciones.
- ST8: Importancia de consistencia en pipelines.
- ST9: Preparación de scripts para automatización.
- ST10: Casos de uso reales (actualización diaria).
- ST11: Automatización como primer paso hacia producción.
"""

import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime

# Establecer semilla para asegurar la reproducibilidad de los resultados generados (ST7)
np.random.seed(987654)

# =============================================================================
# 1. Funciones Modulares del Pipeline (ST5, ST9)
# =============================================================================

def extraer_datos_diarios(fecha_str):
    """
    Simular la ingesta de un lote de transacciones correspondiente a un dia especifico.
    En un entorno real, esto ejecutaria una consulta SQL o leeria un CSV de un bucket.
    """
    print(f"[INFO] Extrayendo datos de transacciones para el lote (batch): {fecha_str}")
    
    # Generar un numero aleatorio de transacciones para simular volumen variable
    num_transacciones = np.random.randint(500, 1500)
    
    datos = {
        "id_transaccion": range(1, num_transacciones + 1),
        "id_cliente": np.random.randint(1000, 1999, num_transacciones),
        "monto": np.random.uniform(5.0, 1000.0, num_transacciones),
        "fecha_transaccion": [fecha_str] * num_transacciones,
        "estado": np.random.choice(
            ["completada", "fallida", "pendiente"], 
            num_transacciones, 
            p=[0.85, 0.10, 0.05]
        )
    }
    
    df_raw = pd.DataFrame(datos)
    return df_raw


def transformar_datos(df):
    """
    Limpiar y transformar los datos extraidos para asegurar la consistencia (ST8).
    """
    print("[INFO] Iniciando limpieza y transformacion de datos...")
    
    # Filtrar unicamente transacciones completadas
    df_procesado = df[df["estado"] == "completada"].copy()
    
    # Formatear montos
    df_procesado["monto"] = df_procesado["monto"].round(2)
    
    # Generar nuevas variables de negocio
    df_procesado["rango_operacion"] = pd.cut(
        df_procesado["monto"], 
        bins=[0, 100, 500, float("inf")], 
        labels=["Bajo", "Medio", "Alto"]
    )
    
    # Eliminar columnas innecesarias tras el filtrado
    df_procesado = df_procesado.drop(columns=["estado"])
    
    print(f"[INFO] Transformacion completada. Total registros validos: {len(df_procesado)}")
    return df_procesado


def cargar_datos(df, fecha_str, directorio_salida="datos_procesados"):
    """
    Guardar el lote de datos procesados en un almacenamiento persistente.
    Se utiliza el particionamiento basado en la fecha (ST3, ST10).
    """
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        print(f"[INFO] Se genero el directorio de salida: {directorio_salida}")
        
    nombre_archivo = f"transacciones_limpias_{fecha_str}.csv"
    ruta_completa = os.path.join(directorio_salida, nombre_archivo)
    
    # Guardar en formato CSV
    df.to_csv(ruta_completa, index=False, encoding="utf-8")
    print(f"[INFO] Carga exitosa. Lote guardado en: {ruta_completa}")


# =============================================================================
# 2. Orquestacion del Pipeline (ST1, ST4)
# =============================================================================

def ejecutar_pipeline_batch(fecha_ejecucion):
    """
    Ejecutar el flujo completo. Encapsular esta logica permite que el proceso
    sea invocado por herramientas externas como Cron o Airflow en el futuro.
    """
    print(f"\n{'='*50}")
    print(f" INICIANDO PIPELINE BATCH | FECHA: {fecha_ejecucion}")
    print(f"{'='*50}")
    
    try:
        # 1. Ingesta
        df_crudo = extraer_datos_diarios(fecha_ejecucion)
        
        # 2. Transformacion
        df_limpio = transformar_datos(df_crudo)
        
        # 3. Almacenamiento
        cargar_datos(df_limpio, fecha_ejecucion)
        
        print("\n[EXITO] Ejecucion del pipeline finalizada correctamente.")
        
    except Exception as e:
        print(f"\n[ERROR] El pipeline fallo durante su ejecucion: {str(e)}")


# =============================================================================
# 3. Punto de Entrada Automatizable (ST6, ST11)
# =============================================================================

if __name__ == "__main__":
    # La parametrizacion del script sustituye las variables estaticas (hardcoding).
    # Esto facilita que un sistema automatizado cambie los argumentos dinamicamente.
    
    parser = argparse.ArgumentParser(
        description="Pipeline batch de transacciones preparado para ejecucion automatizada."
    )
    
    # Parametro de entrada: Fecha del lote a procesar
    parser.add_argument(
        "--fecha", 
        type=str, 
        help="Fecha del lote a procesar (Formato YYYY-MM-DD). Default: Fecha actual del sistema.",
        default=datetime.now().strftime("%Y-%m-%d")
    )
    
    args = parser.parse_args()
    
    # Extraer el argumento ingresado (ya sea por terminal o el valor por defecto)
    fecha_proceso = args.fecha
    
    # Llamar a la funcion principal
    ejecutar_pipeline_batch(fecha_proceso)
