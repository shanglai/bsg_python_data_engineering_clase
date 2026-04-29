# -*- coding: utf-8 -*-
"""
Capítulo 5: Automatización y orquestación
Sección 10: Orquestación e infraestructura
Bloque 2: DAG simple

Descripción:
Script de ejemplo para definir un DAG (Directed Acyclic Graph) en Apache Airflow.
Cubre la estructura del DAG, definición de tareas, establecimiento de dependencias, 
configuración de reintentos (manejo de errores) y buenas prácticas de logging.
"""

from datetime import datetime, timedelta
import logging
import random

# Bloque de importación seguro para evitar fallos si se ejecuta fuera de Airflow
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except ImportError:
    logging.warning("Apache Airflow no está instalado en este entorno local.")
    logging.warning("Este script debe colocarse en la carpeta 'dags/' de tu entorno Airflow.")

# Configurar semilla para reproducibilidad de las simulaciones
random.seed(987654)

# =============================================================================
# 1. INTEGRACIÓN CON SCRIPTS DEL PIPELINE (Funciones a ejecutar)
# =============================================================================

def extraer_datos(**kwargs):
    """
    Extraer datos simulados de un CSV o API.
    En un entorno real, aquí se llamaría a las funciones de ingesta.
    """
    logging.info("Iniciando la tarea de extracción de datos...")
    
    # Simular la lectura de registros
    registros_extraidos = random.randint(1000, 5000)
    logging.info(f"Extracción completada. Se leyeron {registros_extraidos} registros.")
    
    # Enviar metadato a la siguiente tarea usando XCom de Airflow
    return registros_extraidos


def transformar_datos(**kwargs):
    """
    Limpiar y transformar datos.
    Demuestra la recuperación de información de la tarea previa.
    """
    logging.info("Iniciando la tarea de transformación de datos...")
    
    # Obtener la instancia de la tarea (Task Instance - ti)
    ti = kwargs['ti']
    
    # Recuperar el número de registros extraídos de la tarea anterior
    registros_recibidos = ti.xcom_pull(task_ids='extraccion_de_datos')
    
    if not registros_recibidos:
        # Simular manejo de errores en DAGs
        raise ValueError("No se recibieron registros para transformar. Abortando.")
        
    logging.info(f"Procesando {registros_recibidos} registros recibidos...")
    
    # Simular limpieza (eliminar nulos o duplicados)
    registros_limpios = registros_recibidos - random.randint(50, 200)
    logging.info(f"Transformación completada. Quedan {registros_limpios} registros válidos.")
    
    return registros_limpios


def cargar_datos(**kwargs):
    """
    Guardar los datos transformados en base de datos o almacenamiento final.
    """
    logging.info("Iniciando la tarea de carga de datos...")
    
    ti = kwargs['ti']
    registros_a_cargar = ti.xcom_pull(task_ids='transformacion_de_datos')
    
    if not registros_a_cargar:
        raise ValueError("No hay datos limpios para cargar.")
        
    logging.info(f"Cargando {registros_a_cargar} registros en MySQL y Parquet...")
    logging.info("Pipeline finalizado exitosamente. Datos persistidos.")


# =============================================================================
# 2. DEFINICIÓN DE ESTRUCTURA Y BUENAS PRÁCTICAS DEL DAG
# =============================================================================

# Definir argumentos por defecto para las tareas
# Esto centraliza la configuración y el manejo de errores (ej. reintentos)
default_args = {
    'owner': 'equipo_ingenieria_datos',
    'depends_on_past': False, # Las tareas no dependen de ejecuciones de días anteriores
    'start_date': datetime(2023, 10, 1), # Fecha de inicio teórica
    'email_on_failure': False, # Desactivar correos en este ejemplo
    'email_on_retry': False,
    'retries': 2, # Manejo de errores: intentar 2 veces adicionales si la tarea falla
    'retry_delay': timedelta(minutes=5), # Esperar 5 minutos entre intentos
}

# Crear la estructura principal del DAG
# Aquí se configura la ejecución programada vs manual
with DAG(
    dag_id='pipeline_transacciones_diario',
    default_args=default_args,
    description='DAG simple para orquestar ingesta, limpieza y almacenamiento',
    schedule_interval=timedelta(days=1), # Frecuencia diaria
    catchup=False, # No ejecutar días pasados acumulados al encender el DAG
    tags=['curso_python', 'pipeline', 'etl'], # Etiquetas para fácil visualización en la UI
) as dag:

    # =========================================================================
    # 3. DEFINICIÓN DE TAREAS
    # =========================================================================
    
    # Cada tarea es un nodo en el DAG (Directed Acyclic Graph)
    tarea_extraccion = PythonOperator(
        task_id='extraccion_de_datos',
        python_callable=extraer_datos,
        provide_context=True # Permite pasar el contexto (kwargs) a la función
    )

    tarea_transformacion = PythonOperator(
        task_id='transformacion_de_datos',
        python_callable=transformar_datos,
        provide_context=True
    )

    tarea_carga = PythonOperator(
        task_id='carga_de_datos',
        python_callable=cargar_datos,
        provide_context=True
    )

    # =========================================================================
    # 4. DEPENDENCIAS ENTRE TAREAS
    # =========================================================================
    
    # Definir el orden estricto de ejecución usando el operador >> (Bitshift right)
    # Flujo: Extracción -> Transformación -> Carga
    tarea_extraccion >> tarea_transformacion >> tarea_carga

"""
Nota sobre logs y UI:
- Visualización: Una vez guardado en la carpeta de dags, aparecerá en la interfaz web (UI) de Airflow.
- Ejecución: Puede ser activado mediante el botón "Trigger DAG" (manual) o esperar a su 'schedule_interval' (programada).
- Logs: Al hacer clic en cada cuadrado de tarea dentro de la vista 'Graph' o 'Grid', se pueden acceder a los logs 
  generados por la librería de logging.
"""
