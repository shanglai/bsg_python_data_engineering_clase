# -*- coding: utf-8 -*-
"""
Capítulo 1: Fundamentos de Python aplicado a datos
Sección 2: Pandas y mini ETL
Bloque 2: Limpieza de datos (nulos, tipos, columnas)

Descripción:
Script enfocado en la limpieza de datos como etapa crítica en ingeniería de datos.
Se abordan valores nulos, conversión de tipos, normalización de columnas, manejo
de strings, duplicados e inconsistencias.

Subtemas (ST):
ST1: Importancia de la limpieza de datos en pipelines
ST2: Identificación de valores nulos (isnull)
ST3: Tratamiento de nulos (fillna, dropna)
ST4: Conversión de tipos de datos (astype)
ST5: Normalización de nombres de columnas
ST6: Manejo de strings en columnas
ST7: Detección de inconsistencias
ST8: Manejo de duplicados
ST9: Formatos incorrectos (fechas, números)
ST10: Impacto de datos sucios en análisis
ST11: Buenas prácticas de limpieza
"""

import pandas as pd
import numpy as np

# Configurar semilla para reproducibilidad
np.random.seed(987654)

def generar_datos_sucios() -> pd.DataFrame:
    """
    Generar un DataFrame simulado con datos sucios para practicar limpieza.
    Contiene nulos, duplicados, nombres de columnas incorrectos y tipos erróneos.
    """
    datos = {
        ' ID Transaccion ': ['T001', 'T002', 'T003', 'T003', 'T005', np.nan, 'T007', 'T008'],
        'Fecha_Tx': ['2023-01-01', '02/01/2023', '2023-01-03', '2023-01-03', '2023-01-05', '2023-01-06', 'invalid_date', '2023-01-08'],
        'Cliente NOMB': ['  Juan Perez', 'Maria Lopez  ', 'carlos diaz', 'carlos diaz', 'Ana', 'Luis', 'Pedro', '  '],
        ' Monto $ ': ['$1,500.50', '2000', '$-350.00', '$-350.00', 'NaN', '450.75', '1000', '800.00'],
        'Categoria': ['Electrónica', 'Ropa', 'Ropa', 'Ropa', 'Alimentos', np.nan, 'Electrónica', 'Alimentos']
    }
    return pd.DataFrame(datos)

# =============================================================================
# ST1 & ST10: Importancia de la limpieza y el impacto de los datos sucios
# Un pipeline que procesa datos sucios generará reportes financieros erróneos 
# (ej. montos negativos, duplicados que inflan las ventas, formatos que rompen modelos).
# =============================================================================

# 1. Generar e inspeccionar los datos iniciales
print("--- DATOS ORIGINALES (SUCIOS) ---")
df = generar_datos_sucios()
print(df)
print("\nTipos de datos originales:")
print(df.dtypes)
print("\n")

# =============================================================================
# ST5: Normalización de nombres de columnas
# =============================================================================
def normalizar_columnas(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Estandarizar nombres de columnas: minúsculas, sin espacios extra y con guiones bajos.
    """
    dataframe.columns = (
        dataframe.columns
        .str.strip()          # Eliminar espacios al inicio y final
        .str.lower()          # Convertir a minúsculas
        .str.replace(' ', '_')# Reemplazar espacios por guiones bajos
        .str.replace('$', '') # Eliminar caracteres especiales
    )
    return dataframe

print("--- 1. NORMALIZACIÓN DE COLUMNAS ---")
df = normalizar_columnas(df)
print("Nuevas columnas:", df.columns.tolist())
print("\n")

# =============================================================================
# ST8: Manejo de duplicados
# =============================================================================
print("--- 2. MANEJO DE DUPLICADOS ---")
# Identificar duplicados
duplicados = df.duplicated().sum()
print(f"Filas duplicadas encontradas: {duplicados}")

# Eliminar duplicados
df = df.drop_duplicates(keep='first').reset_index(drop=True)
print("DataFrame sin duplicados:")
print(df)
print("\n")

# =============================================================================
# ST2 & ST3: Identificación y tratamiento de valores nulos
# =============================================================================
print("--- 3. IDENTIFICACIÓN Y TRATAMIENTO DE NULOS ---")
# ST2: Identificación de nulos
nulos_por_columna = df.isnull().sum()
print("Valores nulos por columna:")
print(nulos_por_columna)

# ST3: Tratamiento de nulos
# Eliminar filas donde el identificador principal (id_transaccion) sea nulo
df = df.dropna(subset=['id_transaccion'])

# Rellenar valores nulos en columnas categóricas con un valor por defecto
df['categoria'] = df['categoria'].fillna('Desconocido')
print("\nDataFrame tras tratar nulos:")
print(df)
print("\n")

# =============================================================================
# ST6: Manejo de strings en columnas
# =============================================================================
print("--- 4. MANEJO DE STRINGS ---")
# Limpiar nombres de clientes: quitar espacios extra y aplicar Title Case (Mayúscula Inicial)
# Se reemplazan también strings vacíos o compuestos solo por espacios a NaN
df['cliente_nomb'] = df['cliente_nomb'].str.strip().str.title()
df['cliente_nomb'] = df['cliente_nomb'].replace('', np.nan)
df['cliente_nomb'] = df['cliente_nomb'].fillna('Cliente Anónimo')

print(df[['id_transaccion', 'cliente_nomb']])
print("\n")

# =============================================================================
# ST4 & ST9: Formatos incorrectos y Conversión de tipos de datos (astype)
# =============================================================================
print("--- 5. FORMATOS INCORRECTOS Y CONVERSIÓN DE TIPOS ---")

# Limpiar columna de montos (eliminar símbolos de moneda y comas)
df['monto_'] = (
    df['monto_']
    .astype(str)
    .str.replace('$', '', regex=False)
    .str.replace(',', '', regex=False)
    .str.replace('NaN', '0', regex=False) # Manejar el string 'NaN'
)

# ST4: Convertir a numérico (float)
df['monto_'] = df['monto_'].astype(float)
# Renombrar columna para que tenga más sentido tras la limpieza
df = df.rename(columns={'monto_': 'monto'})

# ST9: Manejo de fechas incorrectas
# errors='coerce' transformará los formatos de fecha inválidos en NaT (Not a Time, el null de fechas)
df['fecha_tx'] = pd.to_datetime(df['fecha_tx'], errors='coerce')

print(df[['monto', 'fecha_tx']])
print("Nuevos tipos de datos:")
print(df[['monto', 'fecha_tx']].dtypes)
print("\n")

# =============================================================================
# ST7: Detección de inconsistencias
# =============================================================================
print("--- 6. DETECCIÓN DE INCONSISTENCIAS ---")
# Identificar montos negativos (una regla de negocio podría dictar que no existen montos negativos)
inconsistencias_monto = df[df['monto'] < 0]
print(f"Registros con montos negativos encontrados:\n{inconsistencias_monto}\n")

# Corregir la inconsistencia tomando el valor absoluto (o filtrándolo, dependiendo del negocio)
df['monto'] = df['monto'].abs()

# Tratar los NaT generados en la columna de fechas (eliminando las transacciones sin fecha válida)
df = df.dropna(subset=['fecha_tx']).reset_index(drop=True)

# =============================================================================
# ST11: Buenas prácticas de limpieza (Resultados Finales)
# =============================================================================
print("--- DATOS FINALES (LIMPIOS) ---")
# Ordenar el dataframe por fecha
df = df.sort_values('fecha_tx').reset_index(drop=True)
print(df)
print("\nResumen final del DataFrame:")
print(df.info())
