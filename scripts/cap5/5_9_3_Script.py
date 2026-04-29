# -*- coding: utf-8 -*-
"""
Capítulo 5: Automatización y orquestación
Sección 9: Automatización de procesos
Bloque 3: Logs y ejecución programada

Descripción: 
Este script demuestra cómo implementar un sistema de logging en un pipeline 
de datos. Se abordan los niveles de log (INFO, WARNING, ERROR), la inclusión 
de timestamps, el registro de eventos clave y el manejo de errores para 
garantizar la trazabilidad y facilitar el debugging de ejecuciones programadas.
"""

import logging
import pandas as pd
import numpy as np
import os
import sys

# Fijar semilla para reproducibilidad
np.random.seed(987654)

# =============================================================================
# ST1 a ST4: Configuración inicial de Logging y Timestamps
# =============================================================================

def configurar_logging(log_file="pipeline.log"):
    """
    Configurar el sistema de logging para escribir en un archivo y en consola.
    Se define el formato para incluir timestamps, nivel de severidad y mensaje.
    """
    # Crear un formateador estandarizado (Timestamp - Nivel - Mensaje)
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    
    # Configurar logging básico
    logging.basicConfig(
        level=logging.INFO, # Capturar desde nivel INFO en adelante
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'), # Guardar en archivo
            logging.StreamHandler(sys.stdout)                # Mostrar en consola
        ]
    )
    logging.info("Sistema de logging configurado correctamente.")

# =============================================================================
# Generación de datos de prueba para el caso
# =============================================================================

def generar_datos_prueba(ruta_archivo="transacciones_raw.csv"):
    """
    Generar un archivo CSV simulado con algunas inconsistencias para 
    demostrar el registro de advertencias (WARNING) y errores (ERROR).
    """
    logging.info(f"Iniciando generación de datos de prueba en {ruta_archivo}")
    
    try:
        datos = {
            'id_transaccion': range(1, 101),
            'monto': np.random.uniform(10.0, 500.0, 100),
            'cliente_id': np.random.randint(1000, 1050, 100)
        }
        df = pd.DataFrame(datos)
        
        # Introducir valores nulos aleatorios para forzar warnings
        indices_nulos = np.random.choice(df.index, 5, replace=False)
        df.loc[indices_nulos, 'monto'] = np.nan
        
        df.to_csv(ruta_archivo, index=False)
        logging.info(f"Archivo {ruta_archivo} generado con éxito con {len(df)} registros.")
        
    except Exception as e:
        # ST6: Manejo de errores en ejecución
        logging.error(f"Error crítico al generar datos de prueba: {str(e)}")
        raise

# =============================================================================
# ST5 y ST7: Registro de eventos clave y Debugging
# =============================================================================

def ingestar_datos(ruta_archivo):
    """
    Leer los datos desde la fuente. Registra el inicio y fin del proceso,
    y reporta error si el archivo no existe.
    """
    logging.info(f"Iniciando ingesta de datos desde {ruta_archivo}")
    
    if not os.path.exists(ruta_archivo):
        # Reportar error si falta la fuente de datos
        logging.error(f"El archivo {ruta_archivo} no se encuentra en el sistema.")
        raise FileNotFoundError(f"No se pudo localizar {ruta_archivo}")
    
    try:
        df = pd.read_csv(ruta_archivo)
        logging.info(f"Ingesta finalizada. Filas leídas: {df.shape[0]}, Columnas: {df.shape[1]}")
        return df
    except Exception as e:
        logging.error(f"Fallo al leer el archivo CSV: {str(e)}")
        raise

def transformar_datos(df):
    """
    Aplicar reglas de negocio y limpieza. Registra advertencias (WARNING) 
    cuando encuentra anomalías no críticas, como valores nulos.
    """
    logging.info("Iniciando fase de transformación y limpieza de datos.")
    
    # Validar nulos
    nulos_encontrados = df['monto'].isnull().sum()
    if nulos_encontrados > 0:
        # ST3: Tipos de logs (WARNING para anomalías que no detienen el flujo)
        logging.warning(f"Se detectaron {nulos_encontrados} valores nulos en la columna 'monto'.")
        
        # Imputar nulos
        mediana_monto = df['monto'].median()
        df['monto'] = df['monto'].fillna(mediana_monto)
        logging.info(f"Valores nulos imputados con la mediana: {mediana_monto:.2f}")
    
    # Crear columna derivada
    df['monto_con_impuesto'] = df['monto'] * 1.16
    logging.info("Columna 'monto_con_impuesto' calculada correctamente.")
    
    # Simular un debugging (ST7) registrando una muestra de control
    monto_total = df['monto_con_impuesto'].sum()
    logging.info(f"Transformación finalizada. Monto total procesado: {monto_total:.2f}")
    
    return df

def almacenar_datos(df, ruta_salida="transacciones_procesadas.csv"):
    """
    Guardar los datos procesados. Reporta el evento de escritura exitosa.
    """
    logging.info(f"Iniciando almacenamiento de datos en {ruta_salida}")
    try:
        df.to_csv(ruta_salida, index=False)
        logging.info("Datos almacenados correctamente. Fin de la fase de carga.")
    except Exception as e:
        logging.error(f"Error al intentar guardar el archivo de salida: {str(e)}")
        raise

# =============================================================================
# ST8 a ST11: Trazabilidad, análisis y ejecución del Pipeline
# =============================================================================

def ejecutar_pipeline():
    """
    Función orquestadora. Demuestra cómo envolver todo el proceso en un
    bloque try/except general para asegurar que cualquier fallo no controlado
    quede registrado en el log antes de que el script termine.
    """
    archivo_entrada = "transacciones_raw.csv"
    archivo_salida = "transacciones_procesadas.csv"
    
    logging.info("=== INICIO DE EJECUCIÓN DEL PIPELINE ===")
    
    try:
        # 1. Preparación
        generar_datos_prueba(archivo_entrada)
        
        # 2. Extracción
        datos_crudos = ingestar_datos(archivo_entrada)
        
        # 3. Transformación
        datos_limpios = transformar_datos(datos_crudos)
        
        # 4. Carga
        almacenar_datos(datos_limpios, archivo_salida)
        
        logging.info("=== PIPELINE EJECUTADO EXITOSAMENTE ===")
        
    except Exception as e:
        # Registrar cualquier excepción no capturada en las capas inferiores
        # exc_info=True incluye el traceback completo en el archivo de log
        logging.critical("El pipeline falló de manera inesperada.", exc_info=True)
        logging.info("=== PIPELINE TERMINADO CON ERRORES ===")

if __name__ == "__main__":
    # Inicializar el registro de eventos
    configurar_logging()
    
    # Iniciar el proceso
    ejecutar_pipeline()
