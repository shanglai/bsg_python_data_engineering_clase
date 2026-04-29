# =============================================================================
# Capítulo 1: Fundamentos de Python aplicado a datos
# Sección 1: Python para procesamiento de datos
# Bloque 3: Lectura de archivos (CSV) y primeros scripts
# =============================================================================

# Importar librerías estándar necesarias
import csv
import random
import os

# Fijar semilla para reproducibilidad según lineamientos
random.seed(987654)

# Definir el nombre del archivo con el que vamos a trabajar
ARCHIVO_CSV = "transacciones_pipeline.csv"

# =============================================================================
# 1. Generar un archivo CSV de prueba (Preparación del entorno)
# =============================================================================
# Vamos a crear un archivo con datos simulados que incluye errores intencionales
# para demostrar problemas comunes en la lectura de datos (ST7, ST9).

def generar_datos_prueba():
    """Generar un archivo CSV con datos de transacciones simulados."""
    datos = [
        ["id_transaccion", "fecha", "producto", "cantidad", "precio_unitario"],
        ["1001", "2026-04-01", "Laptop", "2", "1200.50"],
        ["1002", "2026-04-01", "Mouse", "5", "25.00"],
        ["1003", "2026-04-02", "Teclado", "1", "45.99"],
        # Datos corruptos para forzar errores (ST9)
        ["1004", "2026-04-02", "Monitor", "TRES", "299.99"], # Cantidad en texto
        ["1005", "2026-04-03", "Cable HDMI", "3", "N/A"],     # Precio no numérico
        ["1006", "2026-04-03", "Escritorio", "", "150.00"],   # Cantidad vacía
        ["1007", "2026-04-04", "Silla Ergonomica", "2", "199.90"]
    ]
    
    # Escribir el archivo CSV. Nota: Especificamos encoding="utf-8" (ST7)
    with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo, delimiter=",")
        escritor.writerows(datos)
    
    print(f"--- Archivo '{ARCHIVO_CSV}' generado exitosamente ---")

# =============================================================================
# 2. Leer archivos CSV y estructurar el Pipeline (ST1, ST2, ST3)
# =============================================================================
# Demostrar la lectura secuencial iterando sobre las filas del archivo.

def leer_y_procesar_csv():
    """Leer el archivo CSV, parsear datos y manejar errores."""
    
    # Inicializar variables para acumulaciones y métricas (ST8)
    total_ventas = 0.0
    transacciones_validas = 0
    transacciones_invalidas = 0
    
    print("\n--- Iniciando lectura y procesamiento de datos ---")
    
    # Verificar que el archivo exista
    if not os.path.exists(ARCHIVO_CSV):
        print("Error: El archivo no existe.")
        return

    # Abrir el archivo utilizando el gestor de contexto 'with'
    # Se maneja explícitamente el encoding para evitar problemas con caracteres especiales (ST7)
    with open(ARCHIVO_CSV, mode="r", encoding="utf-8") as archivo:
        
        # Utilizar csv.DictReader para leer cada fila como un diccionario (ST3)
        # Esto asume que la primera fila contiene los encabezados (ST2)
        lector_csv = csv.DictReader(archivo, delimiter=",")
        
        # Iterar sobre las filas leídas (ST4)
        for fila in lector_csv:
            id_tx = fila["id_transaccion"]
            producto = fila["producto"]
            cantidad_str = fila["cantidad"]
            precio_str = fila["precio_unitario"]
            
            # =================================================================
            # 3. Parsing de datos y Manejo de Errores (ST5, ST6)
            # =================================================================
            # Los datos leídos de un CSV siempre son strings.
            # Debemos convertirlos a tipos numéricos para operar con ellos.
            
            try:
                # Intentar castear (parsear) los valores string a int y float
                cantidad = int(cantidad_str)
                precio = float(precio_str)
                
                # Procesamiento básico: calcular el total de la transacción (ST8)
                subtotal = cantidad * precio
                total_ventas += subtotal
                transacciones_validas += 1
                
                print(f"Procesado OK: Transacción {id_tx} | {producto} | Subtotal: ${subtotal:.2f}")
                
            except ValueError as e:
                # Si ocurre un error al intentar convertir a int o float, entra aquí.
                # Esto evita que el script se detenga abruptamente.
                transacciones_invalidas += 1
                print(f"Error en Transacción {id_tx}: Datos inválidos. "
                      f"(Cantidad: '{cantidad_str}', Precio: '{precio_str}')")
                # En un entorno real, estos registros podrían enviarse a un archivo de auditoría.

    # =========================================================================
    # 4. Resultados del procesamiento básico
    # =========================================================================
    print("\n--- Resumen del Pipeline de Lectura ---")
    print(f"Transacciones válidas procesadas : {transacciones_validas}")
    print(f"Transacciones inválidas omitidas : {transacciones_invalidas}")
    print(f"Total de ventas calculadas       : ${total_ventas:.2f}")


# =============================================================================
# Ejecución del Script (ST9, ST10)
# =============================================================================
# Este bloque simula cómo se ejecuta de manera reproducible nuestro código
# estructurado como un pequeño flujo o "Pipeline thinking".

if __name__ == "__main__":
    # 1. Ingesta / Preparación
    generar_datos_prueba()
    
    # 2. Procesamiento / Limpieza básica
    leer_y_procesar_csv()
