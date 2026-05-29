# ============================================================
# api.py — Sesión 9: FastAPI + MySQL
# Python para Ingeniería de Datos · BSG Institute
# ============================================================
# Levantar con:
#   uvicorn api:app --reload --port 8000
# ============================================================

from fastapi import FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ── Configuración de base de datos ──────────────────────────
DB_CONFIG = {
    'host':            os.getenv('DB_HOST'),
    'port':            int(os.getenv('DB_PORT', 10031)),
    'user':            os.getenv('DB_USER'),
    'password':        os.getenv('DB_PASSWORD'),
    'db':              os.getenv('DB_NAME'),
    'charset':         'utf8mb4',
    'cursorclass':     pymysql.cursors.DictCursor,
    'connect_timeout': 10,
    'read_timeout':    10,
    'write_timeout':   10,
}


def get_connection():
    """Crea y retorna una conexión a MySQL."""
    return pymysql.connect(**DB_CONFIG)


# ── Ciclo de vida de la app ──────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Verifica la conexión a MySQL al arrancar la API."""
    try:
        conn = get_connection()
        conn.close()
        print('✅ Conexión a MySQL verificada')
    except Exception as e:
        print(f'❌ No se pudo conectar a MySQL: {e}')
    yield
    print('👋 API apagada')


# ── Inicializar la app ───────────────────────────────────────
app = FastAPI(
    title='Pipeline de Transacciones — API',
    description="""
API REST del caso práctico del curso **Python para Ingeniería de Datos**.

Expone los datos procesados por el pipeline ETL de las sesiones anteriores.

**BSG Institute · 2026**
    """,
    version='1.0.0',
    lifespan=lifespan,
)


# ============================================================
# ENDPOINT 1: Health check
# Siempre es el primer endpoint de cualquier API profesional.
# Permite verificar que el servidor está vivo.
# ============================================================
@app.get(
    '/health',
    tags=['Sistema'],
    summary='Verifica que la API está funcionando',
)
def health_check():
    """
    Retorna el estado de la API y la conexión a la base de datos.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        db_status = 'ok'
    except Exception as e:
        db_status = f'error: {str(e)}'

    return {
        'status':   'ok',
        'api':      'Pipeline de Transacciones',
        'version':  '1.0.0',
        'database': db_status,
    }


# ============================================================
# ENDPOINT 2: Resumen general
# Retorna métricas globales del pipeline.
# ============================================================
@app.get(
    '/resumen',
    tags=['Métricas'],
    summary='Resumen general de transacciones',
)
def get_resumen():
    """
    Retorna métricas agregadas de todas las transacciones limpias:
    - Total de transacciones
    - Ventas totales
    - Ticket promedio
    - Venta máxima y mínima
    """
    SQL = """
        SELECT
            COUNT(*)       AS total_transacciones,
            SUM(amount)    AS ventas_totales,
            AVG(amount)    AS ticket_promedio,
            MAX(amount)    AS venta_maxima,
            MIN(amount)    AS venta_minima
        FROM transacciones_clean
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(SQL)
        row = cursor.fetchone()
        return {
            'total_transacciones': row['total_transacciones'],
            'ventas_totales':      float(row['ventas_totales'] or 0),
            'ticket_promedio':     round(float(row['ticket_promedio'] or 0), 2),
            'venta_maxima':        float(row['venta_maxima'] or 0),
            'venta_minima':        float(row['venta_minima'] or 0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# ============================================================
# ENDPOINT 3: Listar transacciones con filtros
# Introduce query parameters — el concepto central de este bloque.
# ============================================================
@app.get(
    '/transacciones',
    tags=['Transacciones'],
    summary='Lista transacciones con filtros opcionales',
)
def get_transacciones(
    status: str = Query(
        default=None,
        description='Filtrar por status: COMPLETADA, PENDIENTE, FALLIDA, CANCELADA'
    ),
    sucursal: str = Query(
        default=None,
        description='Filtrar por nombre de sucursal'
    ),
    limite: int = Query(
        default=20,
        ge=1,
        le=100,
        description='Máximo de registros a retornar (1-100)'
    ),
):
    """
    Retorna una lista de transacciones limpias.

    Puedes combinar los filtros:
    - `/transacciones` → todas (máx 20)
    - `/transacciones?status=COMPLETADA` → solo completadas
    - `/transacciones?sucursal=CDMX-Norte&limite=5` → 5 de esa sucursal
    """
    # Construcción dinámica del WHERE según los filtros recibidos
    condiciones = []
    valores     = []

    if status:
        condiciones.append('status = %s')
        valores.append(status.upper())

    if sucursal:
        condiciones.append('store = %s')
        valores.append(sucursal)

    where = ('WHERE ' + ' AND '.join(condiciones)) if condiciones else ''

    SQL = f"""
        SELECT id_transaccion, fecha, customer_id, amount, status, store
        FROM transacciones_clean
        {where}
        ORDER BY fecha DESC
        LIMIT %s
    """
    valores.append(limite)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(SQL, valores)
        filas = cursor.fetchall()

        # Serializar tipos no-JSON (Decimal, date)
        for f in filas:
            f['amount'] = float(f['amount'])
            f['fecha']  = str(f['fecha'])

        return {
            'total':          len(filas),
            'filtros':        {'status': status, 'sucursal': sucursal, 'limite': limite},
            'transacciones':  filas,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# ============================================================
# ENDPOINT 4: Detalle de una transacción por ID
# Introduce path parameters.
# ============================================================
@app.get(
    '/transacciones/{id_transaccion}',
    tags=['Transacciones'],
    summary='Detalle de una transacción específica',
)
def get_transaccion(id_transaccion: str):
    """
    Retorna el detalle completo de una transacción dado su ID.

    Ejemplo: `/transacciones/TXN-00001`

    Retorna 404 si el ID no existe.
    """
    SQL = """
        SELECT id_transaccion, fecha, customer_id, amount, status, store, procesado_en
        FROM transacciones_clean
        WHERE id_transaccion = %s
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(SQL, (id_transaccion,))
        fila = cursor.fetchone()

        if not fila:
            raise HTTPException(
                status_code=404,
                detail=f"Transacción '{id_transaccion}' no encontrada"
            )

        fila['amount']       = float(fila['amount'])
        fila['fecha']        = str(fila['fecha'])
        fila['procesado_en'] = str(fila['procesado_en'])
        return fila

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# ============================================================
# ENDPOINT 5: Métricas por sucursal
# ============================================================
@app.get(
    '/metricas/sucursales',
    tags=['Métricas'],
    summary='KPIs agrupados por sucursal',
)
def get_metricas_sucursales():
    """
    Retorna ventas totales, número de transacciones y ticket promedio
    por sucursal. Solo incluye transacciones COMPLETADAS.
    """
    SQL = """
        SELECT
            COALESCE(store, 'Sin sucursal') AS sucursal,
            COUNT(*)                        AS total_transacciones,
            SUM(amount)                     AS ventas_totales,
            AVG(amount)                     AS ticket_promedio
        FROM transacciones_clean
        WHERE status = 'COMPLETADA'
        GROUP BY store
        ORDER BY ventas_totales DESC
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(SQL)
        filas = cursor.fetchall()
        for f in filas:
            f['ventas_totales']  = float(f['ventas_totales'])
            f['ticket_promedio'] = round(float(f['ticket_promedio']), 2)
        return {'sucursales': filas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# ============================================================
# ENDPOINT 6: Métricas por mes
# Introducido como tarea de la sesión 8 — quien la hizo ya tiene los datos
# ============================================================
@app.get(
    '/metricas/mensual',
    tags=['Métricas'],
    summary='KPIs agrupados por mes',
)
def get_metricas_mensuales():
    """
    Retorna ventas totales y conteo de transacciones agrupadas por mes.
    """
    SQL = """
        SELECT
            YEAR(fecha)  AS anio,
            MONTH(fecha) AS mes,
            COUNT(*)     AS total_transacciones,
            SUM(amount)  AS ventas_totales
        FROM transacciones_clean
        WHERE status = 'COMPLETADA'
        GROUP BY YEAR(fecha), MONTH(fecha)
        ORDER BY anio, mes
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(SQL)
        filas = cursor.fetchall()
        for f in filas:
            f['ventas_totales'] = float(f['ventas_totales'])
        return {'meses': filas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
