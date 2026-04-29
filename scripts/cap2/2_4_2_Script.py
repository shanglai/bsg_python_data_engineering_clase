# -*- coding: utf-8 -*-

"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 4: Pipeline de datos v1
Bloque 2: Persistencia en MySQL y archivos

Descripción: Script para implementar la persistencia dual del pipeline. 
Se aborda la escritura de datos procesados (resultados intermedios y finales) 
tanto en archivos estructurados (CSV, Parquet) como en bases de datos (MySQL),
comparando estrategias de 'append' vs 'overwrite'.
"""

# Importar librerías necesarias
import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Configurar semilla para reproducibilidad
np.random.seed(987654)

def generar_datos_procesados() -> pd.DataFrame:
    """
    Generar un DataFrame simulando datos transformados 
    que provienen de la etapa anterior del pipeline.
    """
    # Generar fechas, clientes y montos aleatorios
    fechas = pd.date_range(start="2023-01-01", periods=100, freq="D")
    clientes = [f"Cliente_{np.random.randint(1, 20)}" for _ in range(100)]
    montos = np.round(np.random.uniform(10.0, 500.0, 100), 2)
    
    # Crear DataFrame
    df = pd.DataFrame({
        "id_transaccion": range(1, 101),
        "fecha": fechas,
        "cliente": clientes,
        "monto": montos,
        "estado": ["Completado"] * 100
    })
    
    return df

def configurar_directorios(ruta_base: str):
    """
    Crear directorios para manejar resultados intermedios y finales.
    """
    rutas = [
        f"{ruta_base}/intermedios",
        f"{ruta_base}/finales"
    ]
    for ruta in rutas:
        os.makedirs(ruta, exist_ok=True)
        print(f"Directorio verificado/creado: {ruta}")

def guardar_en_archivos(df: pd.DataFrame, ruta_base: str):
    """
    Guardar el DataFrame en formatos estructurados (CSV y Parquet).
    Muestra casos de uso y trade-offs entre legibilidad y eficiencia.
    """
    ruta_csv = f"{ruta_base}/finales/transacciones_procesadas.csv"
    ruta_parquet = f"{ruta_base}/finales/transacciones_procesadas.parquet"
    
    # 1. Guardar en CSV (Ventaja: Alta legibilidad, fácil inspección humana)
    # Estrategia Overwrite (sobrescritura) usando mode='w'
    df.to_csv(ruta_csv, index=False, mode='w', encoding='utf-8')
    print(f"Datos guardados en formato CSV (Overwrite) en: {ruta_csv}")
    
    # 2. Guardar en Parquet (Ventaja: Menor tamaño, tipado fuerte, alta velocidad de lectura)
    # Requiere instalar pyarrow o fastparquet
    try:
        df.to_parquet(ruta_parquet, index=False)
        print(f"Datos guardados en formato Parquet en: {ruta_parquet}")
    except ImportError:
        print("Advertencia: No se pudo guardar en Parquet. Instalar 'pyarrow' (pip install pyarrow).")

def guardar_en_base_de_datos(df: pd.DataFrame):
    """
    Conectar a MySQL y guardar los datos.
    Muestra la persistencia en DB para habilitar consultas SQL complejas
    y consumo posterior mediante APIs.
    """
    # Configurar cadena de conexión a MySQL
    # Formato: mysql+pymysql://usuario:password@host:puerto/base_de_datos
    # Nota: Se debe instalar pymysql (pip install pymysql sqlalchemy)
    usuario = "root"
    password = "password_seguro"
    host = "localhost"
    puerto = "3306"
    base_datos = "pipeline_db"
    
    cadena_conexion = f"mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{base_datos}"
    engine = create_engine(cadena_conexion)
    
    nombre_tabla = "transacciones_finales"
    
    try:
        # Estrategia Append: Agrega nuevos registros a la tabla existente
        # Trade-off: Append mantiene la historia, Overwrite (replace) limpia y carga de cero
        df.to_sql(
            name=nombre_tabla, 
            con=engine, 
            if_exists="append", # Opciones: 'fail', 'replace', 'append'
            index=False
        )
        print(f"Datos insertados exitosamente en la tabla MySQL: '{nombre_tabla}' (Estrategia: Append)")
        
    except OperationalError as e:
        print("Error de conexión a MySQL. Verifique que el servicio esté activo y las credenciales sean correctas.")
        print(f"Detalle del error: {e}")
        
        # Fallback opcional a SQLite para asegurar la ejecución demostrativa del script
        print("\nEjecutando fallback a SQLite local para demostración de persistencia DB...")
        engine_sqlite = create_engine("sqlite:///pipeline_local.db")
        df.to_sql(name=nombre_tabla, con=engine_sqlite, if_exists="replace", index=False)
        print(f"Datos insertados en SQLite local (pipeline_local.db), tabla: '{nombre_tabla}' (Estrategia: Replace)")

def ejecutar_persistencia_dual():
    """
    Ejecutar el flujo completo de persistencia dual integrándolo al pipeline.
    """
    print("--- Iniciando etapa de Persistencia Dual ---")
    
    # Paso 1: Obtener datos transformados
    df_procesado = generar_datos_procesados()
    print(f"Datos transformados obtenidos. Total de registros: {len(df_procesado)}")
    
    # Paso 2: Configurar estructura de almacenamiento
    ruta_almacenamiento = "./data_output"
    configurar_directorios(ruta_almacenamiento)
    
    # Paso 3: Persistencia en archivos (Ideal para data lakes, respaldos y analítica pesada)
    print("\n[Iniciando almacenamiento en Archivos]")
    guardar_en_archivos(df_procesado, ruta_almacenamiento)
    
    # Paso 4: Persistencia en Base de Datos (Ideal para aplicaciones, APIs y consultas transaccionales)
    print("\n[Iniciando almacenamiento en Base de Datos]")
    guardar_en_base_de_datos(df_procesado)
    
    print("\n--- Etapa de Persistencia Dual Completada ---")
    print("El pipeline ahora tiene los datos preparados para consumo posterior.")

if __name__ == "__main__":
    ejecutar_persistencia_dual()
