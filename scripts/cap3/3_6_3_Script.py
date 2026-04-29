# -*- coding: utf-8 -*-
"""
Capítulo 3: Exposición y consumo de datos
Sección 6: Visualización con Streamlit
Bloque 3: Conexión a API o datos procesados

Este script demuestra cómo conectar una aplicación web en Streamlit
tanto a datos directamente almacenados en archivos (CSV) como a una API.
"""

import streamlit as st
import pandas as pd
import requests
import numpy as np
import os

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard de Transacciones", layout="wide")

# =============================================================================
# Preparación de datos simulados (Setup para el ejercicio)
# =============================================================================
def generar_datos_procesados():
    """
    Generar un archivo CSV simulando los datos ya procesados por el pipeline.
    """
    np.random.seed(987654)
    file_path = "datos_procesados_simulados.csv"
    
    if not os.path.exists(file_path):
        fechas = pd.date_range(start="2026-01-01", periods=100, freq="D")
        datos = {
            "id_transaccion": range(1, 101),
            "fecha": fechas,
            "monto": np.random.uniform(50.0, 500.0, 100).round(2),
            "cliente_id": np.random.randint(1000, 1020, 100),
            "estado": np.random.choice(["Completada", "Pendiente", "Rechazada"], 100, p=[0.8, 0.15, 0.05])
        }
        df = pd.DataFrame(datos)
        df.to_csv(file_path, index=False)
        return file_path
    return file_path

# Generar archivo antes de cargar la app
ruta_archivo = generar_datos_procesados()

# =============================================================================
# Interfaz del Dashboard
# =============================================================================
st.title("Consumo de Datos en Streamlit")
st.write("Demostración de los enfoques para alimentar un dashboard: Lectura directa vs Consumo de API.")

# Seleccionar el método de conexión
metodo_conexion = st.radio(
    "Seleccionar método de obtención de datos:",
    ("Lectura de Archivo Directo (CSV)", "Consumo de API (Backend)")
)

# =============================================================================
# Enfoque 1: Lectura de datos procesados (CSV/Parquet)
# Subtemas aplicados: ST2, ST8
# =============================================================================
if metodo_conexion == "Lectura de Archivo Directo (CSV)":
    st.header("Enfoque: Lectura Directa de Archivos")
    st.write("Ventaja: Rápido de implementar. Limitación: Alto acoplamiento, la app necesita acceso al disco/storage.")
    
    try:
        # Leer datos procesados directamente desde el CSV
        df_local = pd.read_csv(ruta_archivo)
        
        st.subheader("Datos Cargados desde Disco")
        st.dataframe(df_local.head(10))
        
        # Calcular métricas simples para mostrar flujo de datos completo
        total_ingresos = df_local[df_local['estado'] == 'Completada']['monto'].sum()
        st.metric(label="Ingresos Totales (Archivos)", value=f"${total_ingresos:,.2f}")
        
    except Exception as e:
        st.error(f"Error al leer el archivo local: {e}")

# =============================================================================
# Enfoque 2: Consumo de APIs desde Streamlit
# Subtemas aplicados: ST1, ST4, ST5, ST6
# =============================================================================
elif metodo_conexion == "Consumo de API (Backend)":
    st.header("Enfoque: Integración Frontend-Backend (Consumo de API)")
    st.write("Ventaja: Sistemas desacoplados (ST7). El dashboard no necesita saber dónde viven los datos.")
    
    # URL simulada de nuestra API FastAPI de bloques anteriores
    API_URL = "http://localhost:8000/transacciones"
    
    st.info(f"Intentando realizar petición GET a: {API_URL}")
    
    try:
        # Manejo de requests en Python (ST5)
        # Nota: Usamos un timeout corto porque el servidor FastAPI podría no estar levantado en esta prueba.
        respuesta = requests.get(API_URL, timeout=2)
        
        # Verificar si la petición fue exitosa (HTTP 200)
        if respuesta.status_code == 200:
            # Procesamiento de respuestas JSON (ST6)
            datos_json = respuesta.json()
            
            # Convertir JSON a DataFrame para visualización
            df_api = pd.DataFrame(datos_json)
            
            st.subheader("Datos Obtenidos desde la API")
            st.dataframe(df_api.head(10))
            
            total_ingresos_api = df_api[df_api['estado'] == 'Completada']['monto'].sum()
            st.metric(label="Ingresos Totales (API)", value=f"${total_ingresos_api:,.2f}")
            
        else:
            st.warning(f"La API respondió con código: {respuesta.status_code}")
            
    except requests.exceptions.ConnectionError:
        # Fallback para el ejercicio en caso de que FastAPI no esté corriendo
        st.error("No se pudo conectar a la API. Asegurar que el servidor FastAPI esté corriendo en localhost:8000.")
        st.write("Como alternativa demostrativa, simularemos la respuesta JSON que enviaría la API...")
        
        # Simular respuesta JSON de la API
        df_simulado = pd.read_csv(ruta_archivo).head(10)
        respuesta_json_simulada = df_simulado.to_dict(orient="records")
        
        # Mostrar código JSON crudo
        st.write("Respuesta JSON (Simulada):")
        st.json(respuesta_json_simulada[:2]) # Mostrar solo los 2 primeros registros para no saturar
        
        # Reconstruir DataFrame a partir del JSON
        df_reconstruido = pd.DataFrame(respuesta_json_simulada)
        st.write("DataFrame reconstruido a partir del JSON:")
        st.dataframe(df_reconstruido)

# =============================================================================
# Comparativa y Arquitectura (ST3, ST7, ST9, ST10, ST11)
# =============================================================================
st.markdown("---")
st.header("Análisis de Arquitectura Simple de Sistema")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Lectura Directa")
    st.markdown("""
    * **Arquitectura:** Pipeline >> Archivo CSV/Parquet >> Streamlit.
    * **Ventajas:** Simplicidad absoluta, sin latencia de red.
    * **Limitaciones:** Streamlit compite por recursos de lectura, no escala fácilmente si múltiples aplicaciones necesitan los datos.
    """)

with col2:
    st.subheader("Consumo por API")
    st.markdown("""
    * **Arquitectura:** Pipeline >> Base de Datos >> FastAPI >> Streamlit.
    * **Ventajas:** Desacoplamiento total. Múltiples frontends pueden consumir la misma API. Se pueden añadir validaciones y seguridad centralizada.
    * **Limitaciones:** Requiere mantener un servicio backend adicional levantado (preparación para escalabilidad).
    """)

# Instrucciones para ejecutar:
# Ejecutar en terminal: streamlit run nombre_del_script.py
