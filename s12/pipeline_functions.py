# ============================================================
# pipeline_functions.py — Funciones del pipeline para el DAG
# Python para Ingeniería de Datos · BSG Institute · Sesión 12
# ============================================================
# Este archivo contiene las funciones del pipeline de la
# sesión 8 adaptadas para ser llamadas desde Airflow.
# Coloca este archivo en ~/airflow/dags/ junto con el DAG.
# ============================================================

import random
import pymysql
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

random.seed(987654)

# ── Configuración de BD ──────────────────────────────────────
# ⚠️  TWIST DIDÁCTICO: DB_PORT empieza en 9999 (incorrecto)
# El DAG fallará en cargar_mysql con un error de conexión.
# Cuando vean el error en el log de Airflow, cambian a 10031.

DB_CONFIG = {
    'host':            os.getenv('DB_HOST', 'mysql-bsg-curso-d01.h.aivencloud.com'),
    'port':            int(os.getenv('DB_PORT_DAG', 9999)),   # ← CAMBIAR A 10031
    'user':            os.getenv('DB_USER', 'avnadmin'),
    'password':        os.getenv('DB_PASSWORD', ''),
    'db':              os.getenv('DB_NAME', 'defaultdb'),
    'charset':         'utf8mb4',
    'cursorclass':     pymysql.cursors.DictCursor,
    'connect_timeout': 10,
    'read_timeout':    10,
    'write_timeout':   10,
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)


# ── Módulo 1: Extracción ─────────────────────────────────────

def extraer(n=60):
    """Genera registros simulados de transacciones."""
    estados    = ['COMPLETADA', 'PENDIENTE', 'FALLIDA', 'CANCELADA']
    sucursales = ['CDMX-Norte', 'CDMX-Sur', 'MTY-Centro', 'GDL-Este', None]
    fecha_base = datetime(2024, 1, 1)
    datos = []

    for i in range(1, n + 1):
        fecha = fecha_base + timedelta(days=random.randint(0, 180))
        fecha_str = (fecha.strftime('%d-%m-%Y') if random.random() < 0.1
                     else fecha.strftime('%Y-%m-%d'))
        customer_id = str(random.randint(1000, 1050)) if random.random() > 0.05 else None
        monto = round(random.uniform(10.0, 500.0), 2)
        if   random.random() < 0.08: monto = f'${monto}'
        elif random.random() < 0.05: monto = -monto
        elif random.random() < 0.05: monto = None

        datos.append({
            'id_transaccion': f'TXN-S12-{str(i).zfill(5)}',
            'fecha':          fecha_str,
            'customer_id':    customer_id,
            'amount':         str(monto) if monto is not None else None,
            'status':         random.choice(estados),
            'store':          random.choice(sucursales),
        })

    print(f'[extraer] {len(datos)} registros generados')
    return datos


# ── Módulo 2: Transformación ─────────────────────────────────

def _limpiar_fecha(valor):
    for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
        try:
            return datetime.strptime(str(valor), fmt).date()
        except (ValueError, TypeError):
            continue
    return None


def _limpiar_monto(valor):
    if valor is None:
        return None
    try:
        m = float(str(valor).replace('$', '').strip())
        return round(m, 2) if m > 0 else None
    except ValueError:
        return None


def transformar(registros):
    """Limpia y valida los registros. Retorna (limpios, reporte)."""
    limpios = []
    reporte = {'total': len(registros), 'validos': 0, 'descartados': 0, 'razones': {}}

    def descartar(razon):
        reporte['descartados'] += 1
        reporte['razones'][razon] = reporte['razones'].get(razon, 0) + 1

    for r in registros:
        fecha  = _limpiar_fecha(r.get('fecha'))
        monto  = _limpiar_monto(r.get('amount'))
        status = (r.get('status') or '').strip()

        if not fecha:                   descartar('fecha_invalida');  continue
        if monto is None:               descartar('monto_invalido');  continue
        if not status:                  descartar('sin_status');      continue
        if not r.get('id_transaccion'): descartar('sin_id');          continue

        limpios.append({
            'id_transaccion': r['id_transaccion'],
            'fecha':          fecha,
            'customer_id':    int(r['customer_id']) if r.get('customer_id') else None,
            'amount':         monto,
            'status':         status,
            'store':          r.get('store'),
        })
        reporte['validos'] += 1

    print(f'[transformar] {reporte["validos"]} válidos / {reporte["descartados"]} descartados')
    print(f'[transformar] razones: {reporte["razones"]}')
    return limpios, reporte


# ── Módulo 3: Carga a MySQL ───────────────────────────────────

def crear_tablas():
    """Crea las tablas si no existen."""
    ddl = [
        """
        CREATE TABLE IF NOT EXISTS transacciones_clean (
            id             INT AUTO_INCREMENT PRIMARY KEY,
            id_transaccion VARCHAR(20) UNIQUE NOT NULL,
            fecha          DATE NOT NULL,
            customer_id    INT,
            amount         DECIMAL(10,2) NOT NULL,
            status         VARCHAR(20) NOT NULL,
            store          VARCHAR(50),
            procesado_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS metricas_sucursal (
            id                  INT AUTO_INCREMENT PRIMARY KEY,
            sucursal            VARCHAR(50),
            total_transacciones INT,
            ventas_totales      DECIMAL(12,2),
            ticket_promedio     DECIMAL(10,2),
            calculado_en        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uq_sucursal (sucursal)
        )
        """
    ]
    conn = get_connection()
    try:
        cur = conn.cursor()
        for sql in ddl:
            cur.execute(sql)
        conn.commit()
        print('[crear_tablas] Tablas verificadas')
    finally:
        conn.close()


def cargar_mysql(registros):
    """Inserta registros limpios en transacciones_clean."""
    SQL = """
        INSERT IGNORE INTO transacciones_clean
            (id_transaccion, fecha, customer_id, amount, status, store)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    # ── AQUÍ ES DONDE FALLA CON PUERTO 9999 ──────────────────
    # Airflow mostrará: "Can't connect to MySQL server on '...' (111)"
    # El alumno ve el log, identifica el puerto, cambia DB_PORT_DAG y
    # vuelve a correr el DAG. Tarea cargar_mysql pasa de rojo a verde.
    conn = get_connection()
    insertados = 0
    try:
        cur = conn.cursor()
        for r in registros:
            cur.execute(SQL, (
                r['id_transaccion'], r['fecha'], r['customer_id'],
                r['amount'], r['status'], r['store']
            ))
            insertados += cur.rowcount
        conn.commit()
        print(f'[cargar_mysql] {insertados} registros nuevos insertados')
        return insertados
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Módulo 4: Métricas ───────────────────────────────────────

def calcular_metricas():
    """Calcula y guarda KPIs por sucursal."""
    SQL_READ = """
        SELECT
            COALESCE(store,'Sin sucursal') AS sucursal,
            COUNT(*)                       AS total_transacciones,
            SUM(amount)                    AS ventas_totales,
            AVG(amount)                    AS ticket_promedio
        FROM transacciones_clean
        WHERE status = 'COMPLETADA'
        GROUP BY store
    """
    SQL_WRITE = """
        REPLACE INTO metricas_sucursal
            (sucursal, total_transacciones, ventas_totales, ticket_promedio)
        VALUES (%s, %s, %s, %s)
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(SQL_READ)
        metricas = cur.fetchall()
        for m in metricas:
            cur.execute(SQL_WRITE, (
                m['sucursal'],
                m['total_transacciones'],
                float(m['ventas_totales']),
                float(m['ticket_promedio']),
            ))
        conn.commit()
        print(f'[calcular_metricas] {len(metricas)} sucursales actualizadas')
    finally:
        conn.close()
