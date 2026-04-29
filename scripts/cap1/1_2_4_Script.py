# -*- coding: utf-8 -*-
# Capítulo 1: Fundamentos de Python aplicado a datos
# Sección 2: Pandas y mini ETL
# Bloque 4: Guardado de datos (CSV y Parquet)

"""
Este script demuestra el cierre de un flujo Mini ETL (Extract, Transform, Load).
Se aborda la persistencia de datos procesados, la exportación a formatos CSV y Parquet,
la comparación entre ambos y la organización básica de archivos.
"""

import pandas as pd
import numpy as np
import os

# Establecer semilla aleatoria solicitada
np.random.seed(987654)

# Crear directorios para organizar los datos procesados (ST8)
# Utilizar verbos neutros: Crear, Generar, Guardar
def crear_directorios():
    rutas = ['datos/crudos', 'datos/procesados']
    for ruta in rutas:
        os.makedirs(ruta, exist_ok=True)
    print("Directorios generados exitosamente.")

crear_directorios()

# ==========================================
# FASE 1: EXTRACT (Extracción) - ST1, ST9
# ==========================================
# Generar un dataset simulado de transacciones
def extraer_datos():
    print("\n--- Fase de Extracción ---")
    fechas = pd.date_range(start='2023-01-01', periods=10000, freq='h')
    datos = {
        'id_transaccion': range(1, 10001),
        'fecha': fechas,
        'id_cliente': np.random.randint(100, 500, size=10000),
        'monto': np.random.uniform(10.0, 500.0, size=10000),
        'categoria': np.random.choice(['Electrónica', 'Ropa', 'Hogar', 'Alimentos', np.nan], size=10000)
    }
    df_raw = pd.DataFrame(datos)
    print(f"Datos extraídos: {df_raw.shape[0]} filas.")
    return df_raw

df_crudo = extraer_datos()

# ==========================================
# FASE 2: TRANSFORM (Transformación) - ST1, ST9
# ==========================================
# Aplicar limpieza y transformaciones básicas
def transformar_datos(df):
    print("\n--- Fase de Transformación ---")
    df_transformado = df.copy()
    
    # Manejar nulos
    df_transformado['categoria'] = df_transformado['categoria'].fillna('Desconocido')
    
    # Crear columna derivada
    df_transformado['impuesto'] = df_transformado['monto'] * 0.16
    df_transformado['total_con_impuesto'] = df_transformado['monto'] + df_transformado['impuesto']
    
    # Redondear valores
    df_transformado['monto'] = df_transformado['monto'].round(2)
    df_transformado['impuesto'] = df_transformado['impuesto'].round(2)
    df_transformado['total_con_impuesto'] = df_transformado['total_con_impuesto'].round(2)
    
    print("Transformaciones aplicadas exitosamente.")
    return df_transformado

df_limpio = transformar_datos(df_crudo)

# ==========================================
# FASE 3: LOAD (Carga / Persistencia) - ST2, ST3, ST5, ST6, ST10, ST11
# ==========================================
print("\n--- Fase de Carga (Almacenamiento) ---")

# Ruta de los archivos de salida
ruta_csv = 'datos/procesados/transacciones_limpias.csv'
ruta_parquet = 'datos/procesados/transacciones_limpias.parquet'

# Guardar en formato CSV (ST2)
# Ventajas: Legible por humanos, universal. Desventajas: Más pesado, lento.
print("Exportando datos a CSV...")
df_limpio.to_csv(ruta_csv, index=False, encoding='utf-8')

# Guardar en formato Parquet (ST3)
# Nota: Requiere instalar la librería 'pyarrow' o 'fastparquet' (pip install pyarrow)
# Ventajas: Formato columnar, compresión eficiente, preserva tipos de datos, rápido.
print("Exportando datos a Parquet...")
try:
    df_limpio.to_parquet(ruta_parquet, engine='pyarrow', index=False)
except ImportError:
    print("Aviso: 'pyarrow' no está instalado. Ejecute 'pip install pyarrow' para guardar en Parquet.")

# ==========================================
# COMPARACIÓN CSV VS PARQUET - ST4
# ==========================================
def comparar_tamanos(archivo_csv, archivo_parquet):
    print("\n--- Comparación de Tamaño (CSV vs Parquet) ---")
    if os.path.exists(archivo_csv) and os.path.exists(archivo_parquet):
        tamano_csv = os.path.getsize(archivo_csv) / 1024 # en KB
        tamano_parquet = os.path.getsize(archivo_parquet) / 1024 # en KB
        
        print(f"Tamaño CSV: {tamano_csv:.2f} KB")
        print(f"Tamaño Parquet: {tamano_parquet:.2f} KB")
        print(f"Diferencia: Parquet es {tamano_csv / tamano_parquet:.2f} veces más pequeño en este caso.")
    else:
        print("Archivos no encontrados para comparar.")

comparar_tamanos(ruta_csv, ruta_parquet)

# ==========================================
# VERSIONADO BÁSICO: SOBRESCRITURA VS APPEND - ST7
# ==========================================
print("\n--- Versionado Básico (Append vs Sobrescritura) ---")

# Generar un pequeño lote nuevo de datos
nuevos_datos = pd.DataFrame({
    'id_transaccion': [10001, 10002],
    'fecha': [pd.Timestamp('2024-02-15 10:00:00'), pd.Timestamp('2024-02-15 11:00:00')],
    'id_cliente': [998, 999],
    'monto': [150.00, 200.00],
    'categoria': ['Hogar', 'Electrónica'],
    'impuesto': [24.00, 32.00],
    'total_con_impuesto': [174.00, 232.00]
})

# Modo Sobrescritura (por defecto, mode='w')
ruta_sobrescritura = 'datos/procesados/demo_sobrescritura.csv'
nuevos_datos.to_csv(ruta_sobrescritura, index=False, encoding='utf-8')
print("Archivo creado con modo sobrescritura.")

# Modo Append (Agregar datos al final, mode='a')
# Se usa header=False para no repetir los nombres de las columnas
nuevos_datos.to_csv(ruta_csv, mode='a', index=False, header=False, encoding='utf-8')
print("Nuevos registros agregados al archivo CSV existente (Append).")

print("\nFlujo ETL finalizado. Datos persistidos y organizados, listos para consumo en bases de datos o APIs.")
