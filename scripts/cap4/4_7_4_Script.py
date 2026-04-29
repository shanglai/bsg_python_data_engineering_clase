# =============================================================================
# Capítulo 4: Manejo de datos y despliegue local
# Sección 7: Cloud storage (demo) / Almacenamiento
# Bloque 4: Integración con pipeline
# =============================================================================

import os
import pandas as pd
import numpy as np
from pathlib import Path

# Configurar semilla para reproducibilidad según lineamientos
np.random.seed(987654)

# 1. Configurar estructura de directorios para el almacenamiento
def configurar_directorios():
    """
    Crear la estructura de carpetas para datos crudos, intermedios y finales.
    Garantizar una organizacion estructurada de los archivos del pipeline.
    """
    directorios = [
        "data/raw",
        "data/intermediate",
        "data/final"
    ]
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
    print("Directorios configurados correctamente.")

# 2. Generar datos simulados de transacciones (Raw Data)
def generar_datos_crudos(ruta_salida):
    """
    Generar un dataset simulado de transacciones y guardarlo en formato CSV.
    Simula la ingesta desde un sistema origen.
    """
    fechas = pd.date_range(start="2023-01-01", periods=100, freq="D")
    clientes = ["C001", "C002", "C003", "C004", "C005"]
    
    datos = {
        "id_transaccion": range(1, 101),
        "fecha": fechas,
        "id_cliente": np.random.choice(clientes, 100),
        "monto": np.random.uniform(10.5, 500.75, 100),
        "estado": np.random.choice(["completada", "pendiente", "fallida", None], 100, p=[0.7, 0.1, 0.1, 0.1])
    }
    
    df_raw = pd.DataFrame(datos)
    
    # Introducir algunos nulos aleatorios en el monto para forzar la limpieza
    df_raw.loc[np.random.choice(df_raw.index, 5), "monto"] = np.nan
    
    # Escribir el dataset original
    df_raw.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Datos crudos generados y guardados en: {ruta_salida}")

# 3. Leer y limpiar datos (Ingesta y almacenamiento intermedio)
def procesar_datos_intermedios(ruta_entrada, ruta_salida_intermedia):
    """
    Leer datos crudos, limpiar valores nulos, estandarizar y guardar como dataset intermedio.
    Persistir resultados intermedios evita reprocesar desde cero si el pipeline falla.
    """
    print(f"Leyendo datos desde: {ruta_entrada}")
    df = pd.read_csv(ruta_entrada, encoding="utf-8")
    
    # Limpieza de datos
    df["monto"] = df["monto"].fillna(df["monto"].median())
    df["estado"] = df["estado"].fillna("desconocido")
    df["fecha"] = pd.to_datetime(df["fecha"])
    
    # Guardar resultados intermedios en formato CSV
    df.to_csv(ruta_salida_intermedia, index=False, encoding="utf-8")
    print(f"Datos intermedios limpios guardados en: {ruta_salida_intermedia}")
    
    return df

# 4. Transformar datos y persistir el resultado final
def transformar_y_guardar_final(df_intermedio, ruta_directorio_final):
    """
    Aplicar transformaciones de negocio y guardar en formato Parquet.
    Muestra el uso de multiples formatos en el pipeline (CSV >> Parquet).
    Incluye un concepto basico de preparacion para particionamiento.
    """
    # Transformacion: Agregar columnas derivadas
    df_intermedio["anio"] = df_intermedio["fecha"].dt.year
    df_intermedio["mes"] = df_intermedio["fecha"].dt.month
    df_intermedio["es_alto_valor"] = df_intermedio["monto"] > 300
    
    # Filtrar unicamente transacciones completadas para el modelo final
    df_final = df_intermedio[df_intermedio["estado"] == "completada"].copy()
    
    # Escribir en formato Parquet (eficiente, tipado, columnar)
    ruta_archivo_final = Path(ruta_directorio_final) / "transacciones_completadas.parquet"
    
    # Nota: En un entorno de Big Data se particionaria, por ejemplo:
    # df_final.to_parquet(ruta_directorio_final, partition_cols=["anio", "mes"])
    df_final.to_parquet(ruta_archivo_final, index=False)
    print(f"Datos finales procesados y guardados en formato Parquet en: {ruta_archivo_final}")
    
    return ruta_archivo_final

# 5. Validar datos almacenados
def validar_datos_finales(ruta_archivo_final):
    """
    Leer el archivo Parquet persistido y mostrar metricas para validar que 
    los datos esten listos para consumo externo (APIs o automatizacion).
    """
    print(f"Validando datos persistidos desde: {ruta_archivo_final}")
    df_validado = pd.read_parquet(ruta_archivo_final)
    
    print("\n| Resumen de Datos Finales |")
    print(f"Total de registros: {len(df_validado)}")
    print(f"Monto total procesado: ${df_validado['monto'].sum():.2f}")
    print("Muestra de los datos:")
    print(df_validado[["id_transaccion", "fecha", "monto", "estado", "es_alto_valor"]].head(3))
    print("|--------------------------|\n")

# Ejecucion completa del flujo
def ejecutar_pipeline_con_almacenamiento():
    """
    Orquestar el flujo completo integrando lectura y escritura 
    en multiples etapas y formatos.
    """
    print("Iniciando Pipeline de Datos (Integracion de Almacenamiento)...")
    
    # Definir rutas de almacenamiento
    ruta_raw = "data/raw/transacciones.csv"
    ruta_intermedia = "data/intermediate/transacciones_limpias.csv"
    dir_final = "data/final"
    
    # Paso 1: Preparar entorno
    configurar_directorios()
    
    # Paso 2: Generar/Ingestar (simulando extraccion de fuente externa)
    generar_datos_crudos(ruta_raw)
    
    # Paso 3: Limpiar y generar dataset intermedio
    df_limpio = procesar_datos_intermedios(ruta_raw, ruta_intermedia)
    
    # Paso 4: Transformar y persistir dataset final (preparado para APIs/BI)
    ruta_parquet = transformar_y_guardar_final(df_limpio, dir_final)
    
    # Paso 5: Validar almacenamiento
    validar_datos_finales(ruta_parquet)
    
    print("Pipeline finalizado con exito. Los datos persistidos estan listos para consumo.")

if __name__ == "__main__":
    ejecutar_pipeline_con_almacenamiento()
