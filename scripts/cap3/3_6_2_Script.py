# -*- coding: utf-8 -*-

"""
Capitulo 3: Exposicion y consumo de datos
Seccion 6: Visualizacion con Streamlit
Bloque 2: Dashboard basico

Descripcion:
Script para generar un dashboard basico utilizando la libreria Streamlit.
Demuestra la creacion de un layout estructurado, seleccion de metricas relevantes (KPIs),
introduccion a graficos simples, uso de tablas y principios de UX basica orientados 
a la presentacion clara de informacion y apoyo a la toma de decisiones.
"""

import streamlit as st
import pandas as pd
import numpy as np

# 1. Configurar pagina principal del dashboard
# Esto debe ejecutarse antes de cualquier otra instruccion de Streamlit
st.set_page_config(
    page_title="Dashboard de Transacciones",
    layout="wide"
)

# 2. Generar datos simulados del pipeline
# Se utiliza la semilla 987654 para garantizar la reproducibilidad de los datos
@st.cache_data
def generar_datos_pipeline():
    np.random.seed(987654)
    fechas = pd.date_range(start="2023-01-01", periods=30, freq="D")
    categorias = ["Electronica", "Ropa", "Hogar", "Alimentos"]
    
    datos = {
        "fecha": np.random.choice(fechas, 500),
        "cliente_id": np.random.randint(100, 200, 500),
        "categoria": np.random.choice(categorias, 500),
        "monto": np.random.uniform(15.0, 600.0, 500).round(2)
    }
    
    df = pd.DataFrame(datos)
    # Ordenar cronologicamente para dar sentido a la serie de tiempo
    df = df.sort_values("fecha").reset_index(drop=True)
    return df

# Ejecutar la carga de datos
df_transacciones = generar_datos_pipeline()

# 3. Estructurar el layout y UX basica
# El titulo y la introduccion proporcionan contexto (Storytelling con datos)
st.title("Panel de Control: Analisis de Transacciones")
st.markdown("""
Este dashboard resume los resultados del pipeline de procesamiento de transacciones. 
El objetivo es proveer informacion clara y evitar la sobrecarga visual, enfocandose 
estrictamente en las metricas que guian las decisiones de negocio.
""")

st.markdown("---")

# 4. Seleccion de metricas relevantes y presentacion de informacion clara
# Calcular indicadores clave de rendimiento (KPIs)
ingreso_total = df_transacciones["monto"].sum()
total_transacciones = len(df_transacciones)
ticket_promedio = df_transacciones["monto"].mean()

st.header("Metricas Principales")
st.markdown("Vision general del rendimiento del negocio.")

# Crear un layout de columnas para distribuir las metricas horizontalmente
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Ingreso Total (USD)", value=f"${ingreso_total:,.2f}")
    
with col2:
    st.metric(label="Volumen de Transacciones", value=total_transacciones)
    
with col3:
    st.metric(label="Ticket Promedio (USD)", value=f"${ticket_promedio:,.2f}")

st.markdown("---")

# 5. Introduccion a graficos simples para interpretacion rapida
st.header("Comportamiento y Tendencias")
st.markdown("Visualizaciones basicas para facilitar la rapida interpretacion de los resultados.")

# Dividir la pantalla en dos columnas para comparar graficos
col_grafica1, col_grafica2 = st.columns(2)

with col_grafica1:
    st.subheader("Ingresos Diarios")
    st.markdown("Grafico de linea temporal para identificar picos de ventas.")
    
    # Transformar datos: Agrupar por fecha sumando el monto
    ingresos_por_fecha = df_transacciones.groupby("fecha")["monto"].sum().reset_index()
    # Para st.line_chart, es conveniente colocar la fecha como indice
    ingresos_por_fecha = ingresos_por_fecha.set_index("fecha")
    
    # Generar grafico de lineas
    st.line_chart(ingresos_por_fecha)

with col_grafica2:
    st.subheader("Ingresos por Categoria")
    st.markdown("Grafico de barras para comparar el desempeño de productos.")
    
    # Transformar datos: Agrupar por categoria sumando el monto
    ingresos_por_categoria = df_transacciones.groupby("categoria")["monto"].sum().reset_index()
    ingresos_por_categoria = ingresos_por_categoria.set_index("categoria")
    
    # Generar grafico de barras
    st.bar_chart(ingresos_por_categoria)

st.markdown("---")

# 6. Uso de tablas para detalle granular
st.header("Detalle de Registros")
st.markdown("Exploracion de los datos procesados en formato tabular.")

# st.dataframe permite desplazamiento (scroll) vertical y horizontal, 
# evitando que una tabla grande rompa el layout visual
st.dataframe(df_transacciones, use_container_width=True, height=250)

# 7. Conexion entre visualizacion y decisiones de negocio
st.markdown("---")
st.subheader("Interpretacion de Resultados")
st.info("""
>> Insight de Negocio: Observar la tabla y graficos simultaneamente permite detectar anomalias. 
Si el grafico de barras muestra una categoria con ingresos excepcionalmente bajos, el equipo 
comercial puede decidir aplicar promociones dirigidas. Por otro lado, la vista tabular ayuda 
a auditar transacciones especificas en los dias donde el grafico de lineas presenta picos inusuales.
""")

# Instrucciones de ejecucion local (como comentario al final del script):
# Para ejecutar este dashboard, abrir la terminal y correr el comando:
# >> streamlit run nombre_del_script.py
