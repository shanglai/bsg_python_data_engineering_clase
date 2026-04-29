# -*- coding: utf-8 -*-

# ==============================================================================
# Capítulo 1: Fundamentos de Python aplicado a datos
# Sección 2: Pandas y mini ETL
# Bloque 3: Transformaciones y generación de variables
# ==============================================================================

import pandas as pd
import numpy as np

# Configurar semilla para reproducibilidad
np.random.seed(987654)

# ==============================================================================
# ST8, ST11: Contexto de negocio y preparación de datos iniciales
# Generar un dataset simulado de transacciones
# ==============================================================================
def generar_datos_transacciones():
    """
    Generar un DataFrame con datos de transacciones simuladas
    para aplicar transformaciones.
    """
    n_registros = 100
    
    # Generar fechas aleatorias en el último mes
    fechas = pd.date_range(start='2026-04-01', periods=n_registros, freq='6H')
    
    datos = {
        'id_transaccion': range(1001, 1001 + n_registros),
        'id_cliente': np.random.randint(10, 20, size=n_registros), # 10 clientes distintos
        'monto_bruto': np.round(np.random.uniform(50.0, 1500.0, size=n_registros), 2),
        'categoria': np.random.choice(['Electrónica', 'Ropa', 'Hogar', 'Alimentos'], size=n_registros),
        'estado': np.random.choice(['Completado', 'Pendiente', 'Rechazado'], p=[0.7, 0.2, 0.1], size=n_registros),
        'fecha_transaccion': fechas
    }
    return pd.DataFrame(datos)

df = generar_datos_transacciones()
print("--- Dataset Original ---")
print(df.head())
print("\n")

# ==============================================================================
# ST1: Selección de columnas
# Seleccionar un subconjunto de columnas relevantes para el análisis
# ==============================================================================
print("--- ST1: Seleccionar columnas ---")
columnas_relevantes = ['id_transaccion', 'id_cliente', 'monto_bruto', 'estado', 'fecha_transaccion']
df_reducido = df[columnas_relevantes].copy()
print(df_reducido.head(3))
print("\n")

# ==============================================================================
# ST2: Filtrado de registros
# Filtrar únicamente las transacciones que fueron completadas
# ==============================================================================
print("--- ST2: Filtrar registros ---")
df_completados = df[df['estado'] == 'Completado'].copy()
print(f"Total registros originales: {len(df)}")
print(f"Total registros completados: {len(df_completados)}")
print("\n")

# ==============================================================================
# ST3: Operaciones vectorizadas
# ST4: Creación de columnas derivadas
# Calcular impuestos y monto neto usando operaciones vectorizadas (rápidas)
# ==============================================================================
print("--- ST3 y ST4: Operaciones vectorizadas y Columnas derivadas ---")
tasa_impuesto = 0.16

# Calcular el impuesto multiplicando directamente la serie completa
df_completados['impuesto'] = df_completados['monto_bruto'] * tasa_impuesto

# Crear la variable derivada del monto neto
df_completados['monto_neto'] = df_completados['monto_bruto'] - df_completados['impuesto']

print(df_completados[['monto_bruto', 'impuesto', 'monto_neto']].head())
print("\n")

# ==============================================================================
# ST5: Uso de apply
# Crear una lógica personalizada que no es fácilmente vectorizable
# ==============================================================================
print("--- ST5: Aplicar funciones custom con apply ---")

def categorizar_monto(monto):
    """
    Clasificar el monto en categorías de ticket.
    """
    if monto < 200:
        return 'Ticket Bajo'
    elif monto <= 800:
        return 'Ticket Medio'
    else:
        return 'Ticket Alto'

# Generar una nueva columna aplicando la función fila por fila
df_completados['tipo_ticket'] = df_completados['monto_neto'].apply(categorizar_monto)
print(df_completados[['monto_neto', 'tipo_ticket']].head())
print("\n")

# ==============================================================================
# ST9: Feature engineering básico
# Extraer componentes de fechas para enriquecer los datos
# ==============================================================================
print("--- ST9: Realizar Feature Engineering básico ---")
# Extraer el día de la semana y la hora de la transacción
df_completados['dia_semana'] = df_completados['fecha_transaccion'].dt.day_name()
df_completados['hora'] = df_completados['fecha_transaccion'].dt.hour
print(df_completados[['fecha_transaccion', 'dia_semana', 'hora']].head())
print("\n")

# ==============================================================================
# ST6: Cálculo de métricas
# ST7: Agrupaciones simples (groupby conceptual)
# ST8: Transformaciones basadas en lógica de negocio
# Generar un resumen por cliente para conocer su valor
# ==============================================================================
print("--- ST6, ST7 y ST8: Agrupar y Calcular métricas de negocio ---")

# Agrupar por id_cliente y calcular la suma del monto neto y el conteo de transacciones
metricas_cliente = df_completados.groupby('id_cliente').agg(
    ingresos_totales=('monto_neto', 'sum'),
    numero_transacciones=('id_transaccion', 'count')
).reset_index()

# Calcular el ticket promedio como métrica derivada del groupby
metricas_cliente['ticket_promedio'] = (
    metricas_cliente['ingresos_totales'] / metricas_cliente['numero_transacciones']
).round(2)

# Ordenar los clientes por ingresos totales (lógica de negocio para ver los mejores)
metricas_cliente = metricas_cliente.sort_values(by='ingresos_totales', ascending=False)

print(metricas_cliente.head())
print("\n")

# ==============================================================================
# ST10: Validación de resultados transformados
# Hacer chequeos de cordura (sanity checks) para asegurar la calidad de datos
# ==============================================================================
print("--- ST10: Validar resultados transformados ---")

# Verificar que no hay montos netos negativos
montos_invalidos = df_completados[df_completados['monto_neto'] < 0]
if montos_invalidos.empty:
    print("Validación exitosa: Todos los montos netos son mayores o iguales a cero.")
else:
    print("Alerta: Existen montos netos negativos.")

# Verificar que el estado de los registros analizados sea 'Completado'
estados_unicos = df_completados['estado'].unique()
print(f"Estados presentes en el dataset final: {estados_unicos}")

# Comprobar si la agrupación generó la misma cantidad de dinero que el total
ingresos_agrupados = metricas_cliente['ingresos_totales'].sum()
ingresos_totales = df_completados['monto_neto'].sum()

# Usar math.isclose o round para evitar problemas de precisión de coma flotante
if round(ingresos_agrupados, 2) == round(ingresos_totales, 2):
    print(f"Validación exitosa: Total ingresos ({ingresos_totales:.2f}) coincide con agrupación.")
else:
    print("Error: Descuadre en las métricas agrupadas.")
print("\nFin del script.")
