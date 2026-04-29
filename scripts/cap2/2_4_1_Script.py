# -*- coding: utf-8 -*-
"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 4: Pipeline de datos v1
Bloque 1: Integración CSV/API -> transformación

Descripción:
Se construye el primer flujo completo de datos integrando fuentes externas (CSV, API) 
con el procesamiento en Python. Se establece la ingesta con control de errores, 
validación y conexión hacia la etapa de transformación, demostrando un pipeline 
como un flujo continuo integrado.
"""

import pandas as pd
import requests
import numpy as np
import logging
import os

# Configurar logging para trazar la ejecución continua del pipeline
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def generar_datos_prueba_csv(ruta_archivo: str) -> None:
    """
    Generar un archivo CSV con transacciones simuladas para probar la ingesta.
    """
    np.random.seed(987654)
    
    # Crear un dataset con problemas reales introducidos a propósito
    datos = {
        'id_transaccion': range(1, 101),
        'id_cliente': np.random.randint(1000, 1050, 100),
        'monto': np.random.uniform(10.0, 500.0, 100),
        'Fecha Transaccion': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'estado': np.random.choice(['completada', 'fallida', 'pendiente', None], 100)
    }
    
    df = pd.DataFrame(datos)
    
    # Introducir nulos para simular datos inconsistentes
    df.loc[10:15, 'monto'] = np.nan
    
    df.to_csv(ruta_archivo, index=False)
    logging.info(f"Archivo de prueba generado exitosamente en: {ruta_archivo}")


def extraer_datos_csv(ruta_archivo: str) -> pd.DataFrame:
    """
    Extraer datos de un archivo CSV implementando manejo de errores y buenas prácticas.
    """
    logging.info("Iniciando extracción de datos desde CSV...")
    try:
        df = pd.read_csv(ruta_archivo)
        logging.info(f"Extracción CSV exitosa. Registros leídos: {len(df)}")
        return df
    except FileNotFoundError:
        logging.error(f"Error de Ingesta: No se encontró el archivo '{ruta_archivo}'")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        logging.error("Error de Ingesta: El archivo CSV está vacío.")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error inesperado durante la extracción CSV: {e}")
        return pd.DataFrame()


def extraer_datos_api(url: str) -> pd.DataFrame:
    """
    Extraer datos simulando el consumo de una API REST con requests.
    """
    logging.info(f"Iniciando extracción de datos desde API: {url}")
    try:
        # Se establece un timeout como buena práctica de ingesta
        respuesta = requests.get(url, timeout=10)
        
        # Lanzar excepción si la respuesta es un error HTTP (ej. 404, 500)
        respuesta.raise_for_status() 
        
        datos_json = respuesta.json()
        df = pd.DataFrame(datos_json)
        
        logging.info(f"Extracción API exitosa. Registros obtenidos: {len(df)}")
        return df
    except requests.exceptions.Timeout:
        logging.error("Error de Ingesta: Tiempo de espera agotado al conectar con la API.")
        return pd.DataFrame()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error de Ingesta: Error HTTP al consumir la API -> {e}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error inesperado al consumir la API: {e}")
        return pd.DataFrame()


def validar_datos_ingestados(df: pd.DataFrame, fuente: str) -> pd.DataFrame:
    """
    Hacer validación inicial de los datos para preparar la transformación.
    """
    logging.info(f"Validando datos provenientes de {fuente}...")
    
    if df.empty:
        logging.warning(f"Validación detenida: El DataFrame de {fuente} está vacío.")
        return df
    
    # 1. Normalizar nombres de columnas (espacios por guiones bajos, minúsculas)
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    
    # 2. Detección de nulos
    nulos = df.isnull().sum().sum()
    if nulos > 0:
        logging.warning(f"Alerta de Calidad: Se encontraron {nulos} valores nulos en {fuente}.")
    
    # 3. Validar duplicados básicos
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        logging.warning(f"Alerta de Calidad: Se encontraron {duplicados} filas duplicadas.")
        
    logging.info(f"Validación completada para {fuente}. Columnas resultantes: {list(df.columns)}")
    return df


def transformar_datos_transacciones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Hacer transformaciones sobre los datos previamente validados.
    """
    logging.info("Iniciando fase de transformación de transacciones...")
    
    if df.empty:
        logging.warning("No hay datos para transformar.")
        return df
        
    df_transformado = df.copy()
    
    # Rellenar valores nulos en columnas críticas
    if 'monto' in df_transformado.columns:
        df_transformado['monto'] = df_transformado['monto'].fillna(0.0)
        df_transformado['monto'] = df_transformado['monto'].astype(float)
        
    if 'estado' in df_transformado.columns:
        df_transformado['estado'] = df_transformado['estado'].fillna('desconocido')
        df_transformado['estado'] = df_transformado['estado'].str.upper()
        
    # Crear columna derivada básica
    if 'fecha_transaccion' in df_transformado.columns:
        df_transformado['fecha_transaccion'] = pd.to_datetime(df_transformado['fecha_transaccion'])
        df_transformado['anio_mes'] = df_transformado['fecha_transaccion'].dt.strftime('%Y-%m')
        
    logging.info("Fase de transformación completada de manera exitosa.")
    return df_transformado


def ejecutar_pipeline_integrado():
    """
    Ejecutar el pipeline de datos v1 como un flujo continuo: 
    Ingesta -> Validación -> Transformación -> (Preparación para almacenamiento)
    """
    logging.info("=== INICIANDO PIPELINE DE DATOS V1 ===")
    
    # 0. Configuración y preparación de ambiente
    ruta_archivo_csv = 'transacciones_raw.csv'
    # Utilizando una API pública para propósitos demostrativos
    url_api_usuarios = 'https://jsonplaceholder.typicode.com/users' 
    
    generar_datos_prueba_csv(ruta_archivo_csv)
    
    # 1. ETAPA DE INGESTA
    logging.info("--- Fase 1: Ingesta de Datos ---")
    df_csv_raw = extraer_datos_csv(ruta_archivo_csv)
    df_api_raw = extraer_datos_api(url_api_usuarios)
    
    # 2. ETAPA DE VALIDACIÓN (Sanity Check)
    logging.info("--- Fase 2: Validación Inicial ---")
    df_csv_validado = validar_datos_ingestados(df_csv_raw, "Transacciones CSV")
    df_api_validado = validar_datos_ingestados(df_api_raw, "Usuarios API")
    
    # 3. ETAPA DE TRANSFORMACIÓN
    logging.info("--- Fase 3: Transformación ---")
    df_transacciones_procesado = transformar_datos_transacciones(df_csv_validado)
    
    # 4. PREPARACIÓN PARA PERSISTENCIA
    logging.info("--- Fase 4: Preparación para Persistencia ---")
    if not df_transacciones_procesado.empty:
        logging.info(f"Muestra final procesada (head 2):\n{df_transacciones_procesado.head(2)}")
        logging.info("Los datos están estructurados y listos para ser cargados en MySQL o Parquet.")
    else:
        logging.error("Pipeline falló: No hay datos resultantes para la persistencia.")
        
    logging.info("=== PIPELINE FINALIZADO ===")
    
    # Limpieza final del archivo temporal
    if os.path.exists(ruta_archivo_csv):
        os.remove(ruta_archivo_csv)
        logging.info(f"Archivo temporal '{ruta_archivo_csv}' eliminado.")

if __name__ == '__main__':
    ejecutar_pipeline_integrado()
