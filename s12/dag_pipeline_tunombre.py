# ============================================================
# dag_pipeline_tunombre.py — Proyecto Final · Sesión 12
# Python para Ingeniería de Datos · BSG Institute
# ============================================================
# INSTRUCCIONES:
# 1. Renombra este archivo: dag_pipeline_TUNOMBRE.py
# 2. Cambia DAG_OWNER y ALUMNO abajo con tu nombre
# 3. Copia este archivo Y pipeline_functions.py a ~/airflow/dags/
# 4. Airflow lo detecta en ~30 segundos
# 5. En la UI: activa el DAG con el toggle y dale ▶ Trigger DAG
#
# FLUJO DEL PROYECTO:
#   health_check_api → extraer_datos → transformar_datos
#                                           ↓
#                                    cargar_mysql  ← truena primero (puerto 9999)
#                                           ↓
#                                    calcular_metricas
# ============================================================

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.http import HttpSensor
from datetime import datetime, timedelta

# ── PERSONALIZACIÓN — cambia esto con tu nombre ──────────────
ALUMNO    = 'tunombre'          # ← pon tu nombre sin espacios
DAG_OWNER = 'Tu Nombre Completo'
# ─────────────────────────────────────────────────────────────

# Importamos las funciones del pipeline que ya construiste
# Asegúrate de que pipeline_functions.py está en ~/airflow/dags/
import sys, os
sys.path.insert(0, os.path.expanduser('~/airflow/dags'))
from pipeline_functions import extraer, transformar, cargar_mysql, calcular_metricas, crear_tablas


# ── Configuración del DAG ─────────────────────────────────────
default_args = {
    'owner':            DAG_OWNER,
    'retries':          1,                        # reintenta 1 vez si falla
    'retry_delay':      timedelta(minutes=1),     # espera 1 min antes de reintentar
    'email_on_failure': False,                    # sin emails por ahora
}

with DAG(
    dag_id=f'pipeline_transacciones_{ALUMNO}',   # ID único con tu nombre
    description='Pipeline ETL completo — Proyecto Final BSG',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule='@daily',                           # corre una vez al día
    catchup=False,                               # no corre días pasados
    tags=['bsg', 'pipeline', 'proyecto-final'],
) as dag:

    # ── TAREA 1: Health check de la API ──────────────────────
    # HttpSensor espera hasta que el endpoint retorne 200.
    # Si la API (contenedor Docker) no está corriendo, el DAG
    # se queda esperando y no avanza a las siguientes tareas.
    # poke_interval: verifica cada 10 segundos
    # timeout: falla si no responde en 60 segundos
    health_check_api = HttpSensor(
        task_id='health_check_api',
        http_conn_id='api_local',               # conexión definida en Airflow UI
        endpoint='/health',
        method='GET',
        response_check=lambda r: r.json().get('status') == 'ok',
        poke_interval=10,
        timeout=60,
        mode='poke',
    )

    # ── TAREA 2: Extracción ───────────────────────────────────
    def _extraer(**context):
        datos = extraer(n=60)
        # XCom: mecanismo de Airflow para pasar datos entre tareas
        # Limitación: solo para datos pequeños (<48KB)
        context['ti'].xcom_push(key='datos_crudos', value=datos)
        print(f'[DAG] Extracción OK: {len(datos)} registros → XCom')

    extraer_datos = PythonOperator(
        task_id='extraer_datos',
        python_callable=_extraer,
    )

    # ── TAREA 3: Transformación ───────────────────────────────
    def _transformar(**context):
        datos_crudos = context['ti'].xcom_pull(
            task_ids='extraer_datos', key='datos_crudos'
        )
        limpios, reporte = transformar(datos_crudos)
        context['ti'].xcom_push(key='datos_limpios', value=limpios)
        print(f'[DAG] Transformación OK: {reporte["validos"]} válidos')

    transformar_datos = PythonOperator(
        task_id='transformar_datos',
        python_callable=_transformar,
    )

    # ── TAREA 4: Carga a MySQL ────────────────────────────────
    # ⚠️  ESTA TAREA FALLARÁ LA PRIMERA VEZ
    # pipeline_functions.py tiene DB_PORT_DAG=9999 (incorrecto).
    # El error en el log de Airflow dirá:
    #   "Can't connect to MySQL server ... (port 9999)"
    # Para corregir:
    #   1. Abre pipeline_functions.py
    #   2. Cambia DB_PORT_DAG de 9999 a 10031 en el .env o en el código
    #   3. En la UI de Airflow: clic en la tarea → Clear → Re-run
    #   4. La tarea pasa de rojo a verde
    def _cargar_mysql(**context):
        datos_limpios = context['ti'].xcom_pull(
            task_ids='transformar_datos', key='datos_limpios'
        )
        crear_tablas()
        n = cargar_mysql(datos_limpios)
        print(f'[DAG] Carga MySQL OK: {n} registros nuevos')

    cargar_mysql_task = PythonOperator(
        task_id='cargar_mysql',
        python_callable=_cargar_mysql,
    )

    # ── TAREA 5: Métricas ─────────────────────────────────────
    def _calcular_metricas(**context):
        calcular_metricas()
        print('[DAG] Métricas actualizadas en metricas_sucursal')

    calcular_metricas_task = PythonOperator(
        task_id='calcular_metricas',
        python_callable=_calcular_metricas,
    )

    # ── DEPENDENCIAS ──────────────────────────────────────────
    # Lee de izquierda a derecha:
    # "health_check primero, luego extracción, luego transformación,
    #  luego carga, luego métricas"
    (
        health_check_api
        >> extraer_datos
        >> transformar_datos
        >> cargar_mysql_task
        >> calcular_metricas_task
    )
