# -*- coding: utf-8 -*-

"""
Capítulo 1: Fundamentos de Python aplicado a datos
Sección 1: Python para procesamiento de datos
Bloque 4: Funciones aplicadas a limpieza de datos

Este script demuestra cómo utilizar funciones en Python para encapsular lógica 
de limpieza de datos, manejar errores y estructurar un mini-pipeline modular.
"""

import random

# Establecer semilla aleatoria por requerimiento de buenas prácticas y reproducibilidad
random.seed(987654)


# =============================================================================
# ST1: Definición y propósito de funciones
# ST3: Encapsulación de lógica
# =============================================================================
# Definir una función básica para entender su estructura. 
# Las funciones encapsulan lógica que puede ser reutilizada para no repetir código.

def saludar_sistema(nombre_sistema):
    """
    Imprimir un mensaje de inicio del sistema.
    """
    print(f"--- Iniciando módulo de limpieza para el sistema: {nombre_sistema} ---")

# Invocar la función
saludar_sistema("Pipeline de Transacciones v1.0")


# =============================================================================
# ST2: Funciones aplicadas a limpieza de datos
# ST4: Manejo de errores en funciones (try/except)
# ST5: Valores por defecto y fallback
# =============================================================================

def limpiar_monto(monto_str, valor_defecto=0.0):
    """
    Convertir un monto de texto a número flotante.
    Manejar valores nulos, vacíos o textos no numéricos usando try/except.
    Asignar un valor por defecto en caso de error (fallback).
    """
    # Manejar caso de nulos o cadenas vacías
    if monto_str is None or str(monto_str).strip() == "":
        return valor_defecto
    
    try:
        # Intentar convertir a flotante
        monto_limpio = float(monto_str)
        
        # Lógica de negocio: los montos no deberían ser negativos en este caso
        if monto_limpio < 0:
            print(f"Advertencia: Monto negativo detectado ({monto_limpio}). Asignando {valor_defecto}.")
            return valor_defecto
            
        return monto_limpio
    
    except ValueError:
        # Capturar el error si el texto no es un número (ej. "N/A", "Desconocido")
        print(f"Error de conversión: '{monto_str}' no es un número válido. Asignando {valor_defecto}.")
        return valor_defecto


def estandarizar_estado(estado_str):
    """
    Limpiar textos de estados de transacción: eliminar espacios extra y convertir a mayúsculas.
    """
    if estado_str is None:
        return "DESCONOCIDO"
    # El método strip() elimina espacios al inicio y al final; upper() convierte a mayúsculas
    return str(estado_str).strip().upper()


def limpiar_fecha(fecha_str):
    """
    Estandarizar el formato de fecha reemplazando barras por guiones.
    """
    if fecha_str is None:
        return "1970-01-01"
    return str(fecha_str).replace("/", "-").strip()


# =============================================================================
# ST6: Aplicación masiva de funciones (listas por comprensión)
# =============================================================================

# Generar datos crudos simulados (como si vinieran de un archivo CSV mal formateado)
transacciones_crudas = [
    {"id_transaccion": "101", "monto": "150.50", "fecha": "2023-10-01", "estado": "COMPLETADA"},
    {"id_transaccion": "102", "monto": "N/A", "fecha": "2023-10-02", "estado": "pendiente "},
    {"id_transaccion": "103", "monto": "-20.00", "fecha": "2023/10/03", "estado": "COMPLETADA"},
    {"id_transaccion": "104", "monto": "1000", "fecha": "2023-10-04", "estado": "  Rechazada"},
    {"id_transaccion": "105", "monto": "", "fecha": "2023/10/05", "estado": None}
]

print("\n--- Procesando datos con Listas por Comprensión ---")

# Aplicar las funciones de limpieza de manera masiva utilizando una lista por comprensión.
# Esto evita escribir bucles 'for' extensos y mejora el rendimiento.
transacciones_limpias = [
    {
        "id_transaccion": int(t["id_transaccion"]),
        "monto": limpiar_monto(t["monto"]),
        "fecha": limpiar_fecha(t["fecha"]),
        "estado": estandarizar_estado(t["estado"])
    }
    for t in transacciones_crudas
]

# Mostrar los resultados limpios
for t in transacciones_limpias:
    print(t)


# =============================================================================
# ST7: Separación de responsabilidades (ingesta vs transformación)
# ST8: Buenas prácticas (modularidad, claridad, reutilización)
# ST9: Evitar duplicación de código
# ST10: Preparación para pipelines estructurados
# =============================================================================

# Para construir un pipeline real, es vital no mezclar la extracción de datos
# con la limpieza de los mismos. Definir módulos separados (funciones orquestadoras).

def extraer_datos():
    """
    Simular la extracción de datos desde una fuente (ej. lectura de CSV o API).
    Responsabilidad única: Obtener los datos, sin modificarlos.
    """
    print("\n[Fase 1] Extrayendo datos de la fuente...")
    # En un caso real, aquí iría código como: leer_archivo_csv("datos.csv")
    datos = [
        {"id": "201", "valor": "500", "status": " ok "},
        {"id": "202", "valor": "error", "status": "FAIL"}
    ]
    return datos

def transformar_datos(datos_crudos):
    """
    Aplicar reglas de negocio y limpieza a los datos extraídos.
    Responsabilidad única: Modificar y limpiar los datos.
    Reutiliza funciones previamente definidas, evitando la duplicación de código.
    """
    print("[Fase 2] Transformando y limpiando datos...")
    datos_transformados = []
    
    for registro in datos_crudos:
        registro_limpio = {
            "id": int(registro["id"]),
            "valor_limpio": limpiar_monto(registro["valor"]), # Reutilización de función
            "estado_estandar": estandarizar_estado(registro["status"]) # Reutilización de función
        }
        datos_transformados.append(registro_limpio)
        
    return datos_transformados

def cargar_datos(datos_procesados):
    """
    Simular la carga de datos limpios a un sistema destino (ej. Base de datos o archivo nuevo).
    """
    print("[Fase 3] Cargando datos procesados al destino final...")
    for d in datos_procesados:
        print(f"Guardando registro -> {d}")
    print("Carga completada con éxito.")

def ejecutar_pipeline():
    """
    Orquestar el flujo de datos completo: Extracción -> Transformación -> Carga (ETL).
    Demostrar la preparación para pipelines estructurados.
    """
    print("\n=== INICIO DE EJECUCIÓN DEL PIPELINE ===")
    
    # 1. Ingesta
    datos_extraidos = extraer_datos()
    
    # 2. Transformación
    datos_limpios = transformar_datos(datos_extraidos)
    
    # 3. Almacenamiento / Carga
    cargar_datos(datos_limpios)
    
    print("=== FIN DE EJECUCIÓN DEL PIPELINE ===")

# Ejecutar la función principal que orquesta el mini-pipeline
ejecutar_pipeline()
