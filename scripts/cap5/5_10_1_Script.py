# -*- coding: utf-8 -*-
# Capítulo 5: Automatización y orquestación
# Sección 10: Orquestación e infraestructura
# Bloque 1: Introducción a Airflow

# Descripción: Script ilustrativo para definir un DAG (Directed Acyclic Graph)
# en Apache Airflow. Demuestra conceptualmente las ventajas de la orquestación
# sobre cron, el manejo de dependencias, reintentos y control de fallos.

import random
from datetime import datetime, timedelta

# Nota: Para ejecutar este script de forma funcional se requiere Apache Airflow.
# Instalar mediante: pip install apache-airflow
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except ImportError:
    print("Advertencia: Apache Airflow no esta instalado. El script se ejecutara en modo mock.")
    # Generar clases mock para permitir la ejecucion estructural del script sin errores
    class DAG:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
    class PythonOperator:
        def __init__(self, *args, **kwargs): pass

# Establecer semilla para reproducibilidad en la simulacion de eventos
random.seed(987654)

# -------------------------------------------------------------------
# ST1, ST2, ST6: Limitaciones de cron e Introduccion a la Orquestacion
# -------------------------------------------------------------------
# Explicacion: A diferencia de cron, donde los scripts se ejecutan en 
# horarios fijos (asumiendo que los procesos anteriores terminaron), 
# la orquestacion permite crear flujos de trabajo orientados a eventos. 
# Si el paso A falla o se retrasa, el orquestador pausa el paso B.

# -------------------------------------------------------------------
# Funciones base del pipeline (Simulacion de procesos de datos)
# -------------------------------------------------------------------

def extraer_datos(**kwargs):
    """
    Ejecutar la extraccion de datos desde una API externa o base de datos.
    """
    print("Iniciando extraccion de datos...")
    
    # ST9: Control de fallos. Simular una falla aleatoria para demostrar reintentos.
    # En un entorno real, esto puede ser una caida de red o un timeout.
    probabilidad_falla = random.random()
    if probabilidad_falla < 0.2:
        raise ValueError("Error simulado de conexion durante la extraccion.")
        
    print("Datos extraidos correctamente.")
    return {"registros": 1500, "estado": "completado"}

def transformar_datos(**kwargs):
    """
    Aplicar reglas de limpieza y transformacion a los datos ingeridos.
    """
    print("Iniciando transformacion de datos...")
    print("Limpieza y generacion de variables derivadas completadas.")
    return {"registros_procesados": 1450, "estado": "completado"}

def cargar_datos(**kwargs):
    """
    Insertar datos finales en la base de datos de consumo o data warehouse.
    """
    print("Iniciando persistencia de datos procesados...")
    print("Carga exitosa. Fin del flujo.")
    return {"estado": "completado"}

# -------------------------------------------------------------------
# ST8, ST9: Control de ejecucion y reintentos
# -------------------------------------------------------------------
# Definir los argumentos base del DAG. Centraliza la configuracion
# operativa, delegando el manejo de reintentos (retries) al orquestador.
default_args = {
    'owner': 'equipo_ingenieria',
    'depends_on_past': False, # Si es True, requiere que la ejecucion anterior haya sido exitosa
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,             # Configurar 3 intentos en caso de falla de cualquier tarea
    'retry_delay': timedelta(minutes=5), # Establecer tiempo de espera entre intentos
}

# -------------------------------------------------------------------
# ST3, ST5, ST7, ST10, ST11: Definicion del DAG (Directed Acyclic Graph)
# -------------------------------------------------------------------
# Instanciar el objeto DAG.
# Este bloque representa el concepto central de Airflow. En la interfaz web,
# esto genera la representacion visual del flujo (ST7), facilitando la 
# escalabilidad del monitoreo en entornos de produccion (ST10, ST11).
with DAG(
    dag_id='pipeline_transacciones_diario',
    default_args=default_args,
    description='DAG basico demostrativo del pipeline de transacciones',
    schedule_interval=timedelta(days=1), # Declarar la frecuencia, superando la sintaxis crontab
    start_date=datetime(2023, 1, 1),
    catchup=False,                       # Evitar ejecuciones retroactivas automaticas
    tags=['ingenieria_datos', 'curso', 'pipeline_v1'],
) as dag:

    # Declarar Tareas (Nodos del Grafo Aciclico Dirigido)
    # Se utiliza PythonOperator para ejecutar funciones nativas de Python.
    
    tarea_extraccion = PythonOperator(
        task_id='extraer_datos',
        python_callable=extraer_datos,
    )

    tarea_transformacion = PythonOperator(
        task_id='transformar_datos',
        python_callable=transformar_datos,
    )

    tarea_carga = PythonOperator(
        task_id='cargar_datos',
        python_callable=cargar_datos,
    )

    # -------------------------------------------------------------------
    # ST4: Concepto de dependencias entre tareas
    # -------------------------------------------------------------------
    # Establecer la topologia del DAG mediante operadores de desplazamiento (bitshift).
    # La transformacion requiere estrictamente la finalizacion exitosa de la extraccion.
    # La carga requiere estrictamente la finalizacion de la transformacion.
    
    tarea_extraccion >> tarea_transformacion >> tarea_carga

# Nota operativa:
# El script no ejecuta las funciones por si solo al hacer `python script.py`.
# El Scheduler de Airflow procesa el archivo, mapea el DAG y maneja la ejecucion
# segun el schedule_interval y el estado de cada tarea.
