# ============================================================
# dashboard.py — Sesión 10: Streamlit Dashboard
# Python para Ingeniería de Datos · BSG Institute
# ============================================================
# Levantar con:
#   streamlit run dashboard.py
# ============================================================

import streamlit as st
import httpx
import pandas as pd
import plotly.express as px

# ── Configuración de la página ───────────────────────────────
st.set_page_config(
    page_title='Pipeline de Transacciones',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ── Constantes ───────────────────────────────────────────────
API_BASE = 'http://localhost:8000'

ESTADOS_VALIDOS = ['Todos', 'COMPLETADA', 'PENDIENTE', 'FALLIDA', 'CANCELADA']
SUCURSALES      = ['Todas', 'CDMX-Norte', 'CDMX-Sur', 'MTY-Centro', 'GDL-Este']

# ── Helpers: consumir la API ─────────────────────────────────

@st.cache_data(ttl=30)
def fetch_resumen():
    """Obtiene el resumen general desde la API. Cache de 30 segundos."""
    try:
        r = httpx.get(f'{API_BASE}/resumen', timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f'Error al obtener resumen: {e}')
        return None


@st.cache_data(ttl=30)
def fetch_transacciones(status=None, sucursal=None, limite=100):
    """Obtiene transacciones con filtros opcionales desde la API."""
    params = {'limite': limite}
    if status and status != 'Todos':
        params['status'] = status
    if sucursal and sucursal != 'Todas':
        params['sucursal'] = sucursal
    try:
        r = httpx.get(f'{API_BASE}/transacciones', params=params, timeout=5)
        r.raise_for_status()
        return r.json().get('transacciones', [])
    except Exception as e:
        st.error(f'Error al obtener transacciones: {e}')
        return []


@st.cache_data(ttl=30)
def fetch_metricas_sucursales():
    """Obtiene KPIs por sucursal desde la API."""
    try:
        r = httpx.get(f'{API_BASE}/metricas/sucursales', timeout=5)
        r.raise_for_status()
        return r.json().get('sucursales', [])
    except Exception as e:
        st.error(f'Error al obtener métricas: {e}')
        return []


@st.cache_data(ttl=30)
def fetch_metricas_mensuales():
    """Obtiene KPIs por mes desde la API."""
    try:
        r = httpx.get(f'{API_BASE}/metricas/mensual', timeout=5)
        r.raise_for_status()
        return r.json().get('meses', [])
    except Exception as e:
        st.error(f'Error al obtener métricas mensuales: {e}')
        return []


def fetch_cliente(customer_id):
    """Busca transacciones de un cliente específico. Sin cache (búsqueda en vivo)."""
    try:
        r = httpx.get(f'{API_BASE}/clientes/{customer_id}', timeout=5)
        if r.status_code == 404:
            return None, 'no_encontrado'
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)


# ── Health check silencioso ──────────────────────────────────
def api_disponible():
    try:
        r = httpx.get(f'{API_BASE}/health', timeout=3)
        return r.status_code == 200
    except Exception:
        return False


# ════════════════════════════════════════════════════════════
# LAYOUT PRINCIPAL
# ════════════════════════════════════════════════════════════

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.image(
        'https://via.placeholder.com/200x60/002060/AFCA0A?text=BSG+Institute',
        use_column_width=True,
    )
    st.markdown('## Pipeline de Transacciones')
    st.markdown('*Python para Ingeniería de Datos · 2026*')
    st.divider()

    # Estado de la API
    if api_disponible():
        st.success('API conectada')
    else:
        st.error('API no disponible — verifica que `uvicorn` está corriendo')
        st.stop()

    st.divider()

    # Filtros globales
    st.markdown('### Filtros')
    filtro_status    = st.selectbox('Status', ESTADOS_VALIDOS)
    filtro_sucursal  = st.selectbox('Sucursal', SUCURSALES)
    filtro_limite    = st.slider('Máx. transacciones', 10, 100, 50, step=10)

    st.divider()
    if st.button('Actualizar datos'):
        st.cache_data.clear()
        st.rerun()

    st.caption('Los datos se actualizan cada 30 segundos automáticamente.')


# ── Header ───────────────────────────────────────────────────
st.title('Dashboard de Transacciones')
st.caption('Datos procesados por el pipeline ETL · Sesiones 7 y 8')
st.divider()


# ── Sección 1: KPIs ─────────────────────────────────────────
resumen = fetch_resumen()

if resumen:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label='💰 Ventas Totales',
            value=f'${resumen["ventas_totales"]:,.2f}',
        )
    with col2:
        st.metric(
            label='🎫 Ticket Promedio',
            value=f'${resumen["ticket_promedio"]:,.2f}',
        )
    with col3:
        st.metric(
            label='📦 Total Transacciones',
            value=f'{resumen["total_transacciones"]:,}',
        )
    with col4:
        st.metric(
            label='📈 Venta Máxima',
            value=f'${resumen["venta_maxima"]:,.2f}',
        )

st.divider()


# ── Sección 2: Gráficas ──────────────────────────────────────
col_izq, col_der = st.columns(2)

# Gráfica 1: ventas por sucursal (barras)
with col_izq:
    st.subheader('Ventas por Sucursal')
    metricas_suc = fetch_metricas_sucursales()
    if metricas_suc:
        df_suc = pd.DataFrame(metricas_suc)
        fig = px.bar(
            df_suc,
            x='sucursal',
            y='ventas_totales',
            color='ventas_totales',
            color_continuous_scale=['#2C4290', '#AFCA0A'],
            labels={'sucursal': 'Sucursal', 'ventas_totales': 'Ventas ($)'},
            text_auto='.2s',
        )
        fig.update_layout(
            plot_bgcolor='white',
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=20, b=20),
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info('Sin datos de sucursales')

# Gráfica 2: ventas por mes (línea)
with col_der:
    st.subheader('Ventas Mensuales')
    metricas_mes = fetch_metricas_mensuales()
    if metricas_mes:
        df_mes = pd.DataFrame(metricas_mes)
        df_mes['periodo'] = df_mes['anio'].astype(str) + '-' + df_mes['mes'].astype(str).str.zfill(2)
        fig2 = px.line(
            df_mes,
            x='periodo',
            y='ventas_totales',
            markers=True,
            labels={'periodo': 'Período', 'ventas_totales': 'Ventas ($)'},
            color_discrete_sequence=['#002060'],
        )
        fig2.update_traces(line_width=2.5, marker_size=8, marker_color='#AFCA0A')
        fig2.update_layout(
            plot_bgcolor='white',
            margin=dict(t=20, b=20),
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info('Sin datos mensuales')

st.divider()


# ── Sección 3: Tabla de transacciones ───────────────────────
st.subheader('Transacciones')

transacciones = fetch_transacciones(
    status=filtro_status,
    sucursal=filtro_sucursal,
    limite=filtro_limite,
)

if transacciones:
    df_tx = pd.DataFrame(transacciones)

    # Formatear columnas para mostrar
    df_tx['amount'] = df_tx['amount'].apply(lambda x: f'${x:,.2f}')

    # Color por status
    def color_status(val):
        colores = {
            'COMPLETADA': 'background-color: #e8f5e9',
            'PENDIENTE':  'background-color: #fff8e1',
            'FALLIDA':    'background-color: #fce4ec',
            'CANCELADA':  'background-color: #f3e5f5',
        }
        return colores.get(val, '')

    st.dataframe(
        df_tx.style.applymap(color_status, subset=['status']),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f'{len(df_tx)} transacciones mostradas')
else:
    st.info('No hay transacciones con los filtros seleccionados.')

st.divider()


# ── Sección 4: Búsqueda por cliente ─────────────────────────
st.subheader('Buscar por Cliente')

col_input, col_btn = st.columns([3, 1])
with col_input:
    customer_id_input = st.text_input(
        'Customer ID',
        placeholder='Ej: 1001',
        label_visibility='collapsed',
    )
with col_btn:
    buscar = st.button('Buscar', use_container_width=True)

if buscar and customer_id_input:
    with st.spinner('Consultando API...'):
        resultado, error = fetch_cliente(customer_id_input.strip())

    if error == 'no_encontrado':
        st.warning(f'Cliente {customer_id_input} no encontrado.')
    elif error:
        st.error(f'Error: {error}')
    elif resultado:
        txs = resultado.get('transacciones', [])
        st.success(f'Cliente {customer_id_input} — {len(txs)} transacciones')
        if txs:
            df_cliente = pd.DataFrame(txs)
            df_cliente['amount'] = df_cliente['amount'].apply(lambda x: f'${float(x):,.2f}')
            st.dataframe(df_cliente, use_container_width=True, hide_index=True)

            total_cliente = sum(float(str(t['amount']).replace('$','').replace(',','')) for t in txs)
            st.metric('Total compras del cliente', f'${total_cliente:,.2f}')
