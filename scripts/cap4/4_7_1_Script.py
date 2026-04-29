# -*- coding: utf-8 -*-

"""
Capítulo 4: Manejo de datos y despliegue local
Sección 7: Almacenamiento local y en la nube
Bloque 1: Importancia del almacenamiento y comparación de formatos (CSV vs Parquet)

Descripción: Este script demuestra empíricamente las diferencias entre los formatos
CSV (row-based, texto plano) y Parquet (columnar, comprimido) en términos de 
tamaño en disco, tiempos de escritura y tiempos de lectura. 
Entender estas diferencias es clave para preparar pipelines escalables.
"""

import pandas as pd
import numpy as np
import time
import os

# Establecer semilla para garantizar la reproducibilidad de los datos
np.random.seed(987654)

def generar_datos_prueba(num_registros=1000000):
    """
    Generar un DataFrame simulado de transacciones para evaluar rendimiento.
    Se utiliza un millón de registros para evidenciar las diferencias de formato.
    """
    print(f"Generando dataset de {num_registros} registros...")
    
    fechas = pd.date_range(start="2023-01-01", periods=num_registros, freq="S")
    clientes_id = np.random.randint(1000, 5000, size=num_registros)
    montos = np.random.uniform(10.0, 5000.0, size=num_registros)
    categorias = np.random.choice(["Electrónica", "Ropa", "Alimentos", "Hogar", "Juguetes"], size=num_registros)
    estados = np.random.choice(["Completado", "Pendiente", "Cancelado"], size=num_registros)
    
    df = pd.DataFrame({
        "fecha": fechas,
        "cliente_id": clientes_id,
        "monto": montos,
        "categoria": categorias,
        "estado": estados
    })
    
    print("Generación completada.\n")
    return df

def medir_escritura(df, ruta_archivo, formato):
    """
    Escribir el DataFrame en disco utilizando el formato especificado 
    y medir el tiempo de ejecución.
    """
    inicio = time.time()
    
    if formato == "csv":
        # CSV es legible por humanos pero ineficiente en grandes volúmenes
        df.to_csv(ruta_archivo, index=False)
    elif formato == "parquet":
        # Parquet comprime por defecto y guarda metadata columnar
        # Requiere la librería 'pyarrow' o 'fastparquet'
        df.to_parquet(ruta_archivo, index=False)
        
    fin = time.time()
    tiempo_transcurrido = fin - inicio
    
    print(f"Tiempo de escritura ({formato.upper()}): {tiempo_transcurrido:.4f} segundos")
    return tiempo_transcurrido

def medir_lectura(ruta_archivo, formato):
    """
    Leer el archivo desde disco utilizando el formato especificado 
    y medir el tiempo de ejecución.
    """
    inicio = time.time()
    
    if formato == "csv":
        df = pd.read_csv(ruta_archivo)
    elif formato == "parquet":
        df = pd.read_parquet(ruta_archivo)
        
    fin = time.time()
    tiempo_transcurrido = fin - inicio
    
    print(f"Tiempo de lectura ({formato.upper()}): {tiempo_transcurrido:.4f} segundos")
    return df, tiempo_transcurrido

def comparar_tamanos(ruta_csv, ruta_parquet):
    """
    Obtener y comparar el tamaño en disco de ambos archivos para evaluar eficiencia.
    """
    tamano_csv_mb = os.path.getsize(ruta_csv) / (1024 * 1024)
    tamano_parquet_mb = os.path.getsize(ruta_parquet) / (1024 * 1024)
    
    print(f"Tamaño en disco (CSV): {tamano_csv_mb:.2f} MB")
    print(f"Tamaño en disco (PARQUET): {tamano_parquet_mb:.2f} MB")
    
    reduccion = ((tamano_csv_mb - tamano_parquet_mb) / tamano_csv_mb) * 100
    print(f"Reducción de tamaño usando Parquet: {reduccion:.2f}%\n")

def ejecutar_comparacion():
    """
    Ejecutar el flujo completo de comparación entre CSV y Parquet,
    emulando la evaluación de formatos para un pipeline de datos.
    """
    # Definir rutas de archivo temporales para la prueba
    ruta_csv = "transacciones_temp.csv"
    ruta_parquet = "transacciones_temp.parquet"
    
    # 1. Generar los datos
    df = generar_datos_prueba(num_registros=1000000)
    
    # 2. Medir escritura (Load/Storage)
    print("--- PRUEBA DE ESCRITURA ---")
    medir_escritura(df, ruta_csv, "csv")
    medir_escritura(df, ruta_parquet, "parquet")
    print("-" * 30 + "\n")
    
    # 3. Comparar tamaños (Eficiencia de almacenamiento)
    print("--- COMPARACIÓN DE TAMAÑO EN DISCO ---")
    comparar_tamanos(ruta_csv, ruta_parquet)
    print("-" * 30 + "\n")
    
    # 4. Medir lectura (Extract/Consumo)
    print("--- PRUEBA DE LECTURA ---")
    _, _ = medir_lectura(ruta_csv, "csv")
    _, _ = medir_lectura(ruta_parquet, "parquet")
    print("-" * 30 + "\n")
    
    # 5. Limpiar el entorno eliminando archivos temporales
    print("Limpiando archivos temporales...")
    if os.path.exists(ruta_csv):
        os.remove(ruta_csv)
    if os.path.exists(ruta_parquet):
        os.remove(ruta_parquet)
    print("Proceso finalizado. El impacto del formato en performance es evidente.")

if __name__ == "__main__":
    # Nota: Para ejecutar este script y generar archivos parquet, 
    # es necesario instalar: pip install pandas numpy pyarrow
    ejecutar_comparacion()
