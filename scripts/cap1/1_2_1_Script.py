# -*- coding: utf-8 -*-
"""
Capítulo 1: Fundamentos de Python aplicado a datos
Sección 2: Pandas y mini ETL
Bloque 1: Introducción a Pandas y DataFrames

Este script cubre los siguientes subtemas (ST):
ST1: Introducción a Pandas como herramienta de manipulación de datos.
ST2: Limitaciones de listas/diccionarios vs DataFrames.
ST3: Concepto de Series y DataFrame.
ST4: Creación de DataFrames desde estructuras nativas.
ST5: Lectura de datos con Pandas (read_csv).
ST6: Inspección inicial (head, shape, info).
ST7: Tipos de columnas en Pandas.
ST8: Exploración básica de datos.
ST9: Contexto de uso en pipelines.
ST10: Escalabilidad conceptual (limitaciones de Pandas vs Big Data).
"""

import pandas as pd
import random
import os

# Fijar semilla para operaciones aleatorias si se requieren
random.seed(987654)

# =============================================================================
# ST1, ST2, ST3, ST4: Creación de Series y DataFrames desde estructuras nativas
# =============================================================================
print("--- ST1 a ST4: Creación de Series y DataFrames ---")

# Mostrar limitación de listas nativas (operaciones matemáticas requieren bucles)
precios_lista = [10.5, 20.0, 15.75, 40.2]
# Intentar multiplicar precios_lista * 2 duplicaría la lista, no los valores.
# Con Pandas (Series), las operaciones son vectorizadas.

# Crear una Serie en Pandas (Unidimensional)
precios_serie = pd.Series(precios_lista, name="Precio")
print("Serie de Pandas:\n", precios_serie)
print("\nMultiplicar Serie por 2 (Vectorizado):\n", precios_serie * 2)

# Crear un DataFrame desde un diccionario (Bidimensional)
datos_diccionario = {
    "id_transaccion": [1, 2, 3, 4],
    "cliente": ["Ana", "Luis", "Marta", "Pedro"],
    "monto": [150.50, 20.00, 340.10, 99.99],
    "categoria": ["Electrónica", "Ropa", "Electrónica", "Hogar"]
}

df_nombres = pd.DataFrame(datos_diccionario)
print("\nDataFrame creado desde un diccionario:\n", df_nombres)

# =============================================================================
# Preparación: Generar un archivo CSV de transacciones para el caso práctico
# =============================================================================
archivo_csv = "transacciones_b1.csv"

# Generar datos simulados para el CSV
transacciones_csv = "id_trx,fecha,id_cliente,monto,estado,metodo_pago\n"
estados = ["Completada", "Pendiente", "Fallida"]
metodos = ["Tarjeta", "Transferencia", "Efectivo"]

for i in range(1, 101):
    fecha = f"2023-10-{random.randint(1, 31):02d}"
    id_cliente = random.randint(1000, 1050)
    monto = round(random.uniform(10.0, 500.0), 2)
    estado = random.choice(estados)
    metodo = random.choice(metodos)
    # Introducir algunos nulos aleatorios en monto para realismo
    monto_str = str(monto) if random.random() > 0.05 else ""
    transacciones_csv += f"{i},{fecha},{id_cliente},{monto_str},{estado},{metodo}\n"

with open(archivo_csv, "w", encoding="utf-8") as f:
    f.write(transacciones_csv)

print(f"\n[INFO] Archivo {archivo_csv} generado con éxito.")

# =============================================================================
# ST5: Lectura de datos con Pandas (read_csv)
# =============================================================================
print("\n--- ST5: Lectura de datos con Pandas ---")
# Leer el archivo CSV recién generado
# En un pipeline, este es el paso de "Ingesta" o "Extracción"
df_transacciones = pd.read_csv(archivo_csv)
print("Archivo CSV leído y cargado en el DataFrame 'df_transacciones'.")

# =============================================================================
# ST6: Inspección inicial (head, shape, info)
# =============================================================================
print("\n--- ST6: Inspección inicial del DataFrame ---")

# Mostrar las primeras 5 filas (head)
print("\nPrimeras 5 filas (df.head()):")
print(df_transacciones.head())

# Mostrar la dimensión del DataFrame (filas, columnas)
print("\nDimensiones del dataset (df.shape):", df_transacciones.shape)

# Mostrar información general del DataFrame (tipos de datos, nulos, memoria)
print("\nInformación del DataFrame (df.info()):")
df_transacciones.info()

# =============================================================================
# ST7: Tipos de columnas en Pandas
# =============================================================================
print("\n--- ST7: Tipos de columnas ---")
# Mostrar específicamente los tipos de datos de cada columna (dtypes)
print(df_transacciones.dtypes)
# Nota: La columna 'monto' puede ser float64 y 'estado' es object (string)

# =============================================================================
# ST8: Exploración básica de datos
# =============================================================================
print("\n--- ST8: Exploración básica de datos ---")

# Resumen estadístico de las columnas numéricas (describe)
print("\nResumen estadístico (df.describe()):")
print(df_transacciones.describe())

# Conteo de valores categóricos (value_counts)
print("\nConteo de transacciones por estado:")
print(df_transacciones['estado'].value_counts())

print("\nConteo de transacciones por método de pago:")
print(df_transacciones['metodo_pago'].value_counts())

# =============================================================================
# ST9 y ST10: Contexto en pipelines y Escalabilidad (Comentarios de diseño)
# =============================================================================
"""
ST9: Contexto de uso en pipelines
---------------------------------
En un pipeline de datos (ETL), Pandas se ubica principalmente en la fase de 
Transformación (T), aunque también facilita la Extracción (E) de fuentes 
simples como CSV o Excel. El DataFrame actuará como nuestra estructura de 
datos en memoria para limpiar, enriquecer y agregar datos antes de guardarlos.

ST10: Escalabilidad conceptual (Limitaciones de Pandas vs Big Data)
-------------------------------------------------------------------
- Pandas procesa los datos "en memoria" (RAM). Si un dataset es más grande 
  que la memoria RAM disponible, Pandas fallará (ej. un CSV de 50GB en una 
  máquina de 16GB de RAM).
- Pandas utiliza un solo hilo (single-core) por defecto para sus cálculos.
- Cuando los datos crecen masivamente (Big Data), se requiere pasar de Pandas 
  a tecnologías distribuidas como Apache Spark, Dask o Polars.
- Sin embargo, para pipelines de datos pequeños o medianos (hasta algunos GBs), 
  Pandas es el estándar de la industria.
"""

# Limpiar el archivo generado para no dejar residuos
if os.path.exists(archivo_csv):
    os.remove(archivo_csv)
    print(f"\n[INFO] Archivo {archivo_csv} eliminado tras la ejecución.")
