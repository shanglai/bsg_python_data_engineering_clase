# -*- coding: utf-8 -*-

"""
Capítulo 5: Automatización y orquestación
Sección 9: Automatización de procesos
Bloque 4: Integración con pipeline

Este script consolida la ejecución de un pipeline completo (ingesta, transformación 
y almacenamiento) preparado para ser ejecutado periódicamente. Incluye mecanismos 
de reintentos, validaciones automáticas y monitoreo básico mediante logs, 
simulando un contexto operativo de producción.
"""

import pandas as pd
import sqlite3
import logging
import time
import random
import os
from datetime import datetime

# Fijar semilla para reproducibilidad
random.seed(987654)

# ==========================================
# 1. CONFIGURACIÓN DE MONITOREO BÁSICO (ST7)
# ==========================================
# Configurar logs para tener trazabilidad de cada ejecución del pipeline.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("pipeline_produccion.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==========================================
# 2. MECANISMO DE REINTENTOS (ST4, ST5)
# ==========================================
def ejecutar_con_reintentos(funcion, max_reintentos=3, delay=2, *args, **kwargs):
    """
    Concepto de reintentos (retry): Permite manejar fallos transitorios en ejecución.
    Intenta ejecutar una función y si falla, espera un tiempo y lo vuelve a intentar.
    """
    intentos = 0
    while intentos < max_reintentos:
        try:
            return funcion(*args, **kwargs)
        except Exception as e:
            intentos += 1
            logger.warning(f"Fallo en {funcion.__name__} (Intento {intentos}/{max_reintentos}). Error: {str(e)}")
            if intentos == max_reintentos:
                logger.error(f"Se agotaron los reintentos para {funcion.__name__}. Abortando.")
                raise e
            time.sleep(delay)

# ==========================================
# 3. COMPONENTES DEL PIPELINE (ST1)
# ==========================================

def extraer_datos():
    """
    Fase de Ingestión.
    Simula la lectura de una API o base de datos externa. 
    Se introduce una probabilidad de fallo simulado para probar los reintentos.
    """
    logger.info("Iniciando extracción de datos...")
    
    # Simulador de fallo aleatorio en red
    if random.random() < 0.3:
        raise ConnectionError("Fallo simulado de conexión a la fuente de datos.")
    
    # Generar datos simulados del periodo actual
    datos_crudos = {
        "id_transaccion": [random.randint(1000, 9999) for _ in range(5)],
        "cliente": ["Cliente A", "Cliente B", "Cliente C", "Cliente A", None],
        "monto": [150.5, 200.0, -50.0, 300.75, 100.0],
        "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(5)]
    }
    
    df = pd.DataFrame(datos_crudos)
    logger.info(f"Extracción completada. {len(df)} registros obtenidos.")
    return df

def transformar_datos(df):
    """
    Fase de Transformación.
    Limpia nulos, formatea valores y genera métricas derivadas.
    """
    logger.info("Iniciando transformación de datos...")
    
    # Copia para no modificar el original directamente
    df_clean = df.copy()
    
    # Limpieza: Tratamiento de nulos
    df_clean['cliente'] = df_clean['cliente'].fillna('Cliente Desconocido')
    
    # Limpieza: Filtrar montos negativos (inconsistencias)
    df_clean = df_clean[df_clean['monto'] > 0]
    
    # Generar variables derivadas
    df_clean['impuesto'] = df_clean['monto'] * 0.16
    df_clean['monto_total'] = df_clean['monto'] + df_clean['impuesto']
    
    logger.info(f"Transformación completada. {len(df_clean)} registros válidos.")
    return df_clean

def cargar_datos(df, db_path="produccion.db"):
    """
    Fase de Almacenamiento.
    Persiste los datos de manera consistente asegurando que múltiples ejecuciones
    mantengan la integridad.
    """
    logger.info("Iniciando carga de datos en base de datos...")
    
    # Consistencia de datos en ejecuciones múltiples (ST6): Usar 'append'
    # En un motor real se usarían transacciones o inserciones idempotentes.
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql("transacciones", conn, if_exists="append", index=False)
        conn.close()
        logger.info("Carga completada exitosamente.")
    except Exception as e:
        logger.error("Error crítico durante la escritura en base de datos.")
        raise e

# ==========================================
# 4. VALIDACIÓN AUTOMÁTICA (ST3, ST9)
# ==========================================
def validar_resultados(df, db_path="produccion.db"):
    """
    Evaluación de resultados automáticos para asegurar que el pipeline 
    operó correctamente.
    """
    logger.info("Validando resultados automáticos en base de datos...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM transacciones")
    total_registros = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(monto_total) FROM transacciones")
    suma_total = cursor.fetchone()[0] or 0.0
    
    conn.close()
    
    logger.info("=== REPORTE DE VALIDACIÓN ===")
    logger.info(f"Registros procesados en esta corrida: {len(df)}")
    logger.info(f"Total histórico en BD: {total_registros}")
    logger.info(f"Ingresos totales acumulados: ${suma_total:.2f}")
    logger.info("=============================")

# ==========================================
# 5. INTEGRACIÓN DEL PIPELINE (ST1, ST8, ST11)
# ==========================================
def ejecutar_pipeline_completo():
    """
    Ejecución del pipeline de extremo a extremo.
    Concepto de pipeline operativo (producción) frente a desarrollo.
    """
    logger.info(">>> INICIO DEL PIPELINE DE PRODUCCIÓN <<<")
    inicio = time.time()
    
    try:
        # 1. Ingesta (con reintentos)
        df_crudo = ejecutar_con_reintentos(extraer_datos, max_reintentos=3, delay=1)
        
        # 2. Transformación
        df_transformado = transformar_datos(df_crudo)
        
        if df_transformado.empty:
            logger.warning("El dataset transformado está vacío. Se omite la carga.")
            return
            
        # 3. Carga
        cargar_datos(df_transformado)
        
        # 4. Validación
        validar_resultados(df_transformado)
        
        duracion = time.time() - inicio
        logger.info(f">>> PIPELINE FINALIZADO CON ÉXITO EN {duracion:.2f} SEGUNDOS <<<\n")
        
    except Exception as e:
        logger.error(f">>> FALLO CRÍTICO EN EL PIPELINE: {str(e)} <<<\n")
        # En producción, aquí se enviaría una alerta (email, Slack, etc.)

# ==========================================
# 6. SIMULACIÓN DE EJECUCIÓN PERIÓDICA (ST2, ST10)
# ==========================================
def simular_ejecucion_programada(num_ejecuciones=3):
    """
    Simula lo que haría una herramienta de automatización (cron) 
    u orquestación (Airflow) llamando al script periódicamente.
    """
    logger.info("Preparando entorno de orquestación simulada...")
    
    # Limpiar BD de pruebas si existe, para iniciar fresco
    if os.path.exists("produccion.db"):
        os.remove("produccion.db")
        
    for i in range(1, num_ejecuciones + 1):
        logger.info(f"--- DISPARADOR AUTOMÁTICO: EJECUCIÓN {i} ---")
        ejecutar_pipeline_completo()
        
        if i < num_ejecuciones:
            logger.info("Esperando siguiente ciclo programado (simulado de 3 segundos)...\n")
            time.sleep(3)
            
    logger.info("Simulación de ejecuciones continuas finalizada.")
    logger.info("Nota (ST10): El siguiente paso natural es llevar este flujo a un orquestador como Apache Airflow.")

if __name__ == "__main__":
    # Ejecutar simulación de ejecución periódica
    simular_ejecucion_programada()
