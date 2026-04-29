# -*- coding: utf-8 -*-

"""
Capítulo 3: Exposición y consumo de datos
Sección 6: Visualización con Streamlit
Bloque 1: Introducción a Streamlit

Descripción: 
Script introductorio para Streamlit. Muestra cómo construir una aplicación web 
en Python, el uso de componentes básicos (texto, tablas) y la estructura general 
de una app para visualizar datos provenientes de un pipeline.

Instrucciones de ejecución:
1. Asegurar tener instalada la librería: pip install streamlit pandas numpy
2. Guardar este archivo como `app.py`
3. Ejecutar en la terminal: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np

# Establecer semilla para reproducibilidad según requerimientos
np.random.seed(987654)

def generar_datos_dummy():
    """
    Generar un conjunto de datos simulado que representa la salida 
    procesada de un pipeline de transacciones.
    """
    fechas = pd.date_range(start="2023-01-01", periods=10, freq="D")
    datos = {
        "fecha": fechas,
        "id_cliente": np.random.randint(100, 150, size=10),
        "monto": np.random.uniform(50.0, 500.0, size=10).round(2),
        "estado": np.random.choice(["Completada", "Pendiente", "Fallida"], size=10)
    }
    return pd.DataFrame(datos)

def main():
    # 1. Uso de componentes de texto básicos
    st.title("Introducción a Streamlit")
    st.header("Mi Primera Aplicación Web de Datos")
    
    st.write("""
    Streamlit permite convertir scripts de Python en aplicaciones web interactivas 
    de forma rápida. En el contexto de nuestro curso, cumple el rol de la **capa de visualización** 
    para consumir los datos procesados en el pipeline.
    """)

    # 2. Integración con Python y Pandas
    st.subheader("Visualización de Datos del Pipeline")
    st.text("A continuación, mostrar una tabla generada a partir de un DataFrame de Pandas:")

    # Obtener datos simulados
    df_transacciones = generar_datos_dummy()

    # 3. Componentes para mostrar tablas de datos
    # st.dataframe presenta los datos de forma interactiva (permite ordenamiento y scroll)
    st.dataframe(df_transacciones)

    # 4. Explicar el flujo de ejecución
    st.subheader("Flujo de Ejecución y Métricas")
    st.info("Nota: El flujo de ejecución de Streamlit es de arriba hacia abajo. Cualquier interacción recarga el script completo.")
    
    # Calcular métricas simples para demostrar procesamiento al vuelo
    monto_total = df_transacciones["monto"].sum()
    transacciones_completadas = df_transacciones[df_transacciones["estado"] == "Completada"].shape[0]

    # Mostrar métricas usando columnas para estructurar el layout básico
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Monto Total Procesado", value=f"${monto_total:,.2f}")
        
    with col2:
        st.metric(label="Transacciones Completadas", value=transacciones_completadas)

    # 5. Demostrar interactividad básica como ventaja para prototipos rápidos
    st.subheader("Interactividad Básica")
    mostrar_detalle = st.checkbox("Mostrar detalle técnico de los datos")
    
    if mostrar_detalle:
        st.write("Tipos de datos presentes en el DataFrame:")
        # st.write es lo suficientemente inteligente para renderizar diccionarios, series, etc.
        st.write(df_transacciones.dtypes)
        st.success("Esta interactividad demuestra las ventajas de Streamlit para construir prototipos sin saber HTML o JavaScript.")

if __name__ == "__main__":
    # Ejecutar la función principal
    main()
