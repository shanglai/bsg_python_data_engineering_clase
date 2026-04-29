# -*- coding: utf-8 -*-

"""
Capítulo 4: Manejo de datos y despliegue local
Sección 7: Storage local y nube
Bloque 2: Concepto de almacenamiento local

Descripción:
Este script aborda los fundamentos de la persistencia de datos a nivel local.
Cubre la creación de la estructura de directorios típica de un proyecto de datos (raw, processed, output),
el manejo robusto de rutas, convenciones de nombres, estrategias de guardado (append vs overwrite) y 
el versionado de archivos para garantizar la reproducibilidad y evitar la pérdida de datos históricos.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# ST10: Reproducibilidad del pipeline
# Establecer semilla para garantizar resultados reproducibles al generar datos
np.random.seed(987654)

def estructurar_proyecto_datos(ruta_base: Path):
    """
    ST1, ST2, ST3, ST11: Concepto de almacenamiento local, Organización de carpetas y Buenas prácticas.
    Generar la estructura de directorios (raw, processed, output).
    """
    print("--- Configurando Estructura de Directorios ---")
    
    # Definición de las capas de almacenamiento del proyecto
    capas_almacenamiento = ['raw', 'processed', 'output']
    
    for capa in capas_almacenamiento:
        ruta_capa = ruta_base / capa
        # Crear directorio si no existe (parents=True permite crear directorios anidados si fuera necesario)
        ruta_capa.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Directorio validado/creado: {ruta_capa}")

def generar_datos_ingesta(cantidad: int = 100) -> pd.DataFrame:
    """
    Generar un dataset simulado de transacciones para alimentar el pipeline.
    """
    df = pd.DataFrame({
        'id_transaccion': range(1, cantidad + 1),
        'monto_usd': np.random.uniform(5.0, 1000.0, cantidad).round(2),
        'tipo_operacion': np.random.choice(['Compra', 'Reembolso', 'Suscripcion'], cantidad),
        'estado': np.random.choice(['Aprobado', 'Rechazado', 'Pendiente'], cantidad)
    })
    return df

def almacenar_datos_raw(df: pd.DataFrame, ruta_base: Path):
    """
    ST4, ST5: Naming conventions y Manejo de rutas en Python.
    Guardar los datos tal como llegan en la capa 'raw' para preservar la fuente original.
    """
    print("\n--- Almacenando Datos Raw ---")
    
    # ST5: Manejo robusto de rutas usando la librería pathlib en lugar de concatenar strings
    ruta_raw = ruta_base / 'raw'
    
    # ST4: Naming conventions. Es vital usar marcas de tiempo para identificar la ingesta.
    fecha_hoy = datetime.now().strftime('%Y%m%d')
    nombre_archivo = f"ingesta_transacciones_{fecha_hoy}.csv"
    
    ruta_destino = ruta_raw / nombre_archivo
    
    # ST7: Aquí se utiliza sobrescritura, pero referenciada al archivo del día específico.
    df.to_csv(ruta_destino, index=False, encoding='utf-8')
    print(f"[OK] Datos raw guardados en: {ruta_destino}")

def almacenar_datos_procesados(df: pd.DataFrame, ruta_base: Path):
    """
    ST6, ST7, ST8, ST9: Versionado básico de archivos, Estrategias de sobrescritura vs append, 
    Manejo de datos históricos y Evitar pérdida de datos.
    """
    print("\n--- Almacenando Datos Procesados ---")
    ruta_processed = ruta_base / 'processed'
    
    # Simular un procesamiento: filtrar solo transacciones aprobadas
    df_aprobadas = df[df['estado'] == 'Aprobado'].copy()
    
    # -------------------------------------------------------------------------
    # Estrategia A: Sobrescritura (Overwrite) - "Snapshot actual"
    # ST7: Sobrescribir siempre el mismo archivo. Útil cuando sistemas externos
    # consumen un nombre de archivo fijo. Riesgo: pérdida de historial previo.
    # -------------------------------------------------------------------------
    ruta_overwrite = ruta_processed / "transacciones_aprobadas_actual.csv"
    df_aprobadas.to_csv(ruta_overwrite, index=False, encoding='utf-8')
    print(f"[Estrategia Overwrite] Archivo actualizado: {ruta_overwrite.name}")
    
    # -------------------------------------------------------------------------
    # Estrategia B: Añadir (Append) - "Acumulación en archivo único"
    # ST7, ST8: Acumular registros en un mismo archivo. 
    # Mantiene historia, pero el archivo puede volverse pesado e ineficiente.
    # -------------------------------------------------------------------------
    ruta_append = ruta_processed / "transacciones_aprobadas_historico.csv"
    
    if not ruta_append.exists():
        # Escribir con encabezado si es la primera vez
        df_aprobadas.to_csv(ruta_append, mode='w', index=False, encoding='utf-8')
        print(f"[Estrategia Append] Archivo creado: {ruta_append.name}")
    else:
        # Añadir (append) sin encabezado si el archivo ya existe
        df_aprobadas.to_csv(ruta_append, mode='a', header=False, index=False, encoding='utf-8')
        print(f"[Estrategia Append] Registros añadidos a: {ruta_append.name}")

    # -------------------------------------------------------------------------
    # Estrategia C: Versionado por Timestamp (Datos inmutables por lote)
    # ST6, ST8, ST9: Crear un archivo nuevo para cada ejecución. 
    # La mejor práctica para evitar pérdida de datos y permitir trazabilidad.
    # -------------------------------------------------------------------------
    timestamp_exacto = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_versionado = f"transacciones_aprobadas_v{timestamp_exacto}.parquet"
    ruta_versionada = ruta_processed / nombre_versionado
    
    # Guardamos en Parquet para optimizar espacio en históricos grandes
    df_aprobadas.to_parquet(ruta_versionada, index=False)
    print(f"[Estrategia Versionado] Nuevo lote histórico guardado: {ruta_versionada.name}")

def ejecutar_modulo_almacenamiento():
    """
    ST10, ST11: Reproducibilidad del pipeline y Buenas prácticas de organización.
    Orquestador principal del script.
    """
    print("INICIO: Módulo de Almacenamiento Local")
    print("="*45)
    
    # ST5: Definir ruta base relativa al directorio actual
    directorio_proyecto = Path('./data_pipeline')
    
    # 1. Asegurar la estructura física de carpetas
    estructurar_proyecto_datos(directorio_proyecto)
    
    # 2. Simular llegada de datos de una API o base de datos
    datos_nuevos = generar_datos_ingesta(cantidad=50)
    
    # 3. Persistir datos crudos para trazabilidad
    almacenar_datos_raw(datos_nuevos, directorio_proyecto)
    
    # 4. Procesar y almacenar utilizando distintas estrategias
    almacenar_datos_procesados(datos_nuevos, directorio_proyecto)
    
    print("="*45)
    print("FIN: Módulo de Almacenamiento Local ejecutado exitosamente.")

if __name__ == "__main__":
    ejecutar_modulo_almacenamiento()
