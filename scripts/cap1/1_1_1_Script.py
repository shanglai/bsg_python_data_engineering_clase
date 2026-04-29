# =============================================================================
# Capítulo 1: Fundamentos de Python aplicado a datos
# Sección 1: Python para procesamiento de datos
# Bloque 1: Introducción al curso y caso del pipeline
# =============================================================================

# Contexto: Este script genera el dataset de transacciones (Caso práctico del curso).
# En Ingeniería de Datos, nos enfrentamos a problemas reales (nulos, duplicados, errores).
# Aquí vamos a "Generar" un archivo CSV con datos crudos y problemáticos que 
# servirá como punto de partida para construir nuestro pipeline en las siguientes sesiones.

# Importar las librerías necesarias para la generación de datos
import random
import csv
import os
from datetime import datetime, timedelta

# Establecer semilla aleatoria para reproducibilidad de los datos (Regla del curso)
random.seed(987654)

def generar_datos_transaccionales(num_registros=100):
    """
    Generar una lista de diccionarios simulando transacciones de una tienda.
    Se inyectan intencionalmente errores comunes en los datos (nulos, formatos, duplicados).
    """
    estados_posibles = ['COMPLETADA', 'PENDIENTE', 'FALLIDA', 'CANCELADA', '']
    tiendas = ['Tienda_Norte', 'Tienda_Sur', 'Tienda_Centro', 'Tienda_Este', None]
    
    datos = []
    fecha_base = datetime(2023, 1, 1)

    for i in range(1, num_registros + 1):
        # Generar identificador de transacción
        tx_id = f"TXN-{str(i).zfill(5)}"
        
        # Generar fecha con algunos formatos inconsistentes
        dias_aleatorios = random.randint(0, 365)
        fecha_tx = fecha_base + timedelta(days=dias_aleatorios)
        
        if random.random() < 0.1:
            # 10% de probabilidad de tener un formato de fecha incorrecto
            fecha_str = fecha_tx.strftime("%d-%m-%Y")
        else:
            fecha_str = fecha_tx.strftime("%Y-%m-%d")
            
        # Generar identificador de cliente (algunos nulos)
        cliente_id = random.randint(1000, 1050) if random.random() > 0.05 else None
        
        # Generar montos con errores tipográficos o valores negativos
        monto = round(random.uniform(10.0, 500.0), 2)
        if random.random() < 0.1:
            monto = f"${monto}" # Formato string con símbolo
        elif random.random() < 0.05:
            monto = -monto # Monto negativo (anomalía)
        elif random.random() < 0.05:
            monto = None # Monto nulo
            
        # Seleccionar estado y tienda con posibilidad de valores vacíos o nulos
        estado = random.choice(estados_posibles)
        tienda = random.choice(tiendas)
        
        # Crear el registro
        registro = {
            'transaction_id': tx_id,
            'date': fecha_str,
            'customer_id': cliente_id,
            'amount': monto,
            'status': estado,
            'store': tienda
        }
        
        datos.append(registro)
        
        # Inyectar duplicados intencionales (aprox 5% de las veces)
        if random.random() < 0.05:
            datos.append(registro.copy())
            
    return datos

def guardar_csv(datos, nombre_archivo):
    """
    Guardar la lista de transacciones en un archivo CSV.
    Representa la etapa de "Ingesta" de un pipeline de datos crudos.
    """
    # Definir los nombres de las columnas
    campos = ['transaction_id', 'date', 'customer_id', 'amount', 'status', 'store']
    
    # Crear directorio temporal si no existe
    if not os.path.exists("data"):
        os.makedirs("data")
        
    ruta_completa = os.path.join("data", nombre_archivo)
    
    # Escribir los datos en el archivo CSV
    with open(ruta_completa, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in datos:
            escritor.writerow(fila)
            
    print(f"Archivo guardado exitosamente en: {ruta_completa}")
    print(f"Total de registros generados (incluyendo duplicados): {len(datos)}")

def inspeccionar_datos(nombre_archivo, num_lineas=5):
    """
    Leer y mostrar las primeras líneas del archivo generado para evidenciar 
    los problemas reales de calidad de datos.
    """
    ruta_completa = os.path.join("data", nombre_archivo)
    print("\n--- Inspección inicial de datos crudos (Raw Data) ---")
    
    try:
        with open(ruta_completa, mode='r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for i, linea in enumerate(lector):
                if i > num_lineas:
                    break
                print(linea)
    except FileNotFoundError:
        print("El archivo no se encontró. Verificar la ruta de guardado.")

# =============================================================================
# Bloque de ejecución principal
# =============================================================================
if __name__ == "__main__":
    print("Iniciando simulación del caso práctico del curso de Data Engineering...\n")
    
    # 1. Generar los datos con problemas
    dataset_crudo = generar_datos_transaccionales(num_registros=100)
    
    # 2. Guardar los datos en un archivo CSV (nuestro "Raw Storage")
    archivo_salida = "transacciones_raw.csv"
    guardar_csv(dataset_crudo, archivo_salida)
    
    # 3. Inspeccionar el resultado para identificar inconsistencias
    inspeccionar_datos(archivo_salida, num_lineas=10)
    
    print("\nFin del script. Estos datos defectuosos justifican la necesidad de un Pipeline de Datos.")
