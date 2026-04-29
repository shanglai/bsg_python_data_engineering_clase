# -*- coding: utf-8 -*-

"""
===============================================================================
Capítulo 5: Automatización y orquestación
Sección 9: Automatización de procesos
Bloque 2: Cronjobs
===============================================================================

Este script representa una tarea automatizada (pipeline simple) preparada para
ser ejecutada mediante una herramienta de programación de tareas como cron. 
Aborda conceptos clave como el manejo de rutas absolutas, la generación de logs 
básicos y la consistencia en ejecuciones periódicas.

Al final del script se incluyen las instrucciones y ejemplos de sintaxis para 
programar este archivo en cron.
"""

import os
import sys
import datetime
import random

# Establecer semilla para reproducibilidad según requerimientos
random.seed(987654)

def obtener_rutas_absolutas():
    """
    Generar las rutas absolutas del proyecto.
    
    En la ejecución manual, las rutas relativas suelen funcionar porque 
    el directorio de trabajo es donde está el usuario. En cron, el entorno 
    de ejecución es distinto, por lo que usar rutas absolutas es obligatorio.
    """
    # Obtener el directorio donde reside este script
    directorio_base = os.path.dirname(os.path.abspath(__file__))
    
    # Definir carpetas de salida
    directorio_logs = os.path.join(directorio_base, "logs")
    directorio_datos = os.path.join(directorio_base, "datos_procesados")
    
    # Crear los directorios si no existen
    os.makedirs(directorio_logs, exist_ok=True)
    os.makedirs(directorio_datos, exist_ok=True)
    
    return directorio_base, directorio_logs, directorio_datos

def registrar_log(ruta_log, mensaje, nivel="INFO"):
    """
    Escribir un mensaje en el archivo de log con su marca de tiempo.
    
    El logging es fundamental cuando un script se ejecuta en segundo plano 
    (como con cron) para tener trazabilidad de procesos y errores.
    """
    marca_tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"[{marca_tiempo}] [{nivel}] {mensaje}\n"
    
    # Escribir en modo append para conservar el historial
    with open(ruta_log, "a", encoding="utf-8") as archivo:
        archivo.write(linea_log)
        
    # Imprimir en consola también (útil si cron envía la salida por correo o a otro log)
    print(linea_log.strip())

def simular_ingesta_y_transformacion():
    """
    Simular un proceso de extracción y transformación de datos.
    Retorna un valor numérico como resultado del proceso.
    """
    # Simular una métrica calculada, por ejemplo, transacciones procesadas
    registros_procesados = random.randint(100, 500)
    
    # Simular un posible error aleatorio (10% de probabilidad)
    if random.random() < 0.10:
        raise Exception("Error simulado de conexion a la fuente de datos")
        
    return registros_procesados

def guardar_resultados(ruta_salida, registros_procesados):
    """
    Guardar el resultado de la transformación en un archivo.
    """
    marca_tiempo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"resultado_batch_{marca_tiempo}.csv"
    ruta_completa = os.path.join(ruta_salida, nombre_archivo)
    
    with open(ruta_completa, "w", encoding="utf-8") as archivo:
        archivo.write("fecha_ejecucion,registros_procesados\n")
        archivo.write(f"{marca_tiempo},{registros_procesados}\n")
        
    return ruta_completa

def ejecutar_pipeline():
    """
    Ejecutar el flujo completo del script preparado para automatización.
    """
    directorio_base, directorio_logs, directorio_datos = obtener_rutas_absolutas()
    ruta_archivo_log = os.path.join(directorio_logs, "pipeline_cron.log")
    
    registrar_log(ruta_archivo_log, "Iniciando ejecucion programada del pipeline...")
    
    try:
        # Paso 1 y 2: Ingesta y Transformación
        registrar_log(ruta_archivo_log, "Ejecutando extraccion y transformacion de datos...")
        registros = simular_ingesta_y_transformacion()
        
        # Paso 3: Almacenamiento
        registrar_log(ruta_archivo_log, f"Transformacion exitosa. Registros obtenidos: {registros}")
        ruta_guardado = guardar_resultados(directorio_datos, registros)
        registrar_log(ruta_archivo_log, f"Datos guardados correctamente en: {ruta_guardado}")
        
        registrar_log(ruta_archivo_log, "Ejecucion del pipeline finalizada con exito.")
        
    except Exception as e:
        registrar_log(ruta_archivo_log, f"Fallo en la ejecucion del pipeline: {str(e)}", nivel="ERROR")
        sys.exit(1)

if __name__ == "__main__":
    ejecutar_pipeline()


"""
===============================================================================
INSTRUCCIONES DE CONFIGURACIÓN DE CRON (Comentarios formativos)
===============================================================================

Para automatizar este script en sistemas basados en Unix (Linux/macOS), se 
utiliza el comando `crontab -e` desde la terminal.

1. Estructura de un comando cron:
   * * * * * comando_a_ejecutar
   - - - - -
   | | | | |
   | | | | +----- Día de la semana (0 - 7) (Domingo es 0 y 7)
   | | | +------- Mes (1 - 12)
   | | +--------- Día del mes (1 - 31)
   | +----------- Hora (0 - 23)
   +------------- Minuto (0 - 59)

2. Ejemplos prácticos para programar este script:

   A) Ejecutar todos los días a las 02:00 AM:
      0 2 * * * /usr/bin/python3 /ruta/absoluta/a/este/script.py

   B) Ejecutar cada hora exacta (ej. 1:00, 2:00, 3:00):
      0 * * * * /usr/bin/python3 /ruta/absoluta/a/este/script.py

   C) Ejecutar cada 5 minutos:
      */5 * * * * /usr/bin/python3 /ruta/absoluta/a/este/script.py

3. Buenas prácticas en cron (Manejo de entorno y rutas):
   - Cron NO carga las variables de entorno de tu usuario por defecto (como PATH).
   - Siempre usar la ruta absoluta del intérprete de Python (ej. /usr/bin/python3 o la ruta de tu entorno virtual).
   - Siempre usar la ruta absoluta del script a ejecutar.
   - Es recomendable redirigir los errores estándar (stderr) a un archivo adicional:
     0 2 * * * /usr/bin/python3 /ruta/script.py >> /ruta/cron_salida.log 2>&1

4. Limitaciones de cron a considerar en pipelines complejos:
   - No tiene manejo nativo de dependencias (ejecutar script B solo si script A termina bien).
   - No proporciona una interfaz visual para ver el historial de ejecuciones.
   - El reintento en caso de fallo (retry) requiere lógica adicional dentro del código.
   (Estas limitaciones se resuelven posteriormente utilizando orquestadores como Airflow).
===============================================================================
"""
