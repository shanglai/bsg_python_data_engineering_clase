# -*- coding: utf-8 -*-
# ==============================================================================
# Capítulo 2: Almacenamiento y consultas de datos
# Sección 4: Pipeline de datos v1
# Bloque 3: Modularización del pipeline
# ==============================================================================
# Descripción: 
# Este script actúa como un "constructor". Al ejecutarlo, se va a generar 
# una estructura de carpetas profesional para proyectos de datos y se van
# a crear archivos modulares (.py) separando las responsabilidades de:
# 1. Ingesta (Lectura de datos)
# 2. Transformación (Limpieza y reglas de negocio)
# 3. Almacenamiento (Persistencia de datos)
# Finalmente, genera un script principal (main.py) que orquesta el pipeline.
# ==============================================================================

import os
import pandas as pd
import numpy as np

def generar_estructura_directorios(base_path="proyecto_pipeline"):
    """
    Generar la estructura de carpetas necesaria para un proyecto modular.
    Separa el código fuente (src) de los datos (data).
    """
    directorios = [
        f"{base_path}/data/raw",         # Datos crudos, inmutables
        f"{base_path}/data/processed",   # Datos limpios y procesados
        f"{base_path}/src"               # Código fuente modularizado
    ]
    
    print("-> Generando estructura de directorios...")
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
        print(f"   Creado: {directorio}")

def generar_datos_prueba(base_path="proyecto_pipeline"):
    """
    Generar un dataset CSV de prueba en la carpeta 'raw'.
    Usa la semilla 987654 para reproducibilidad.
    """
    np.random.seed(987654)
    print("-> Generando datos crudos de prueba...")
    
    n_filas = 20
    datos = {
        'id_transaccion': range(1, n_filas + 1),
        'nombre_cliente': np.random.choice(['Ana', 'Luis', 'Carlos', 'Maria', None], n_filas),
        'cantidad': np.random.randint(1, 10, n_filas),
        'precio_unitario': np.random.uniform(10.0, 100.0, n_filas).round(2),
        'fecha': pd.date_range(start='2023-01-01', periods=n_filas, freq='D')
    }
    
    df = pd.DataFrame(datos)
    # Introducir algunos errores intencionales para probar la transformación
    df.loc[3, 'cantidad'] = np.nan
    df.loc[7, 'precio_unitario'] = np.nan
    
    ruta_salida = os.path.join(base_path, "data", "raw", "transacciones.csv")
    df.to_csv(ruta_salida, index=False)
    print(f"   Archivo generado: {ruta_salida}")

def generar_modulo_ingesta(base_path="proyecto_pipeline"):
    """
    Generar el módulo de Python encargado única y exclusivamente de la lectura de datos.
    """
    ruta_archivo = os.path.join(base_path, "src", "ingesta.py")
    codigo = """# -*- coding: utf-8 -*-
import pandas as pd

def extraer_datos_csv(ruta_archivo):
    \"\"\"
    Extraer datos crudos desde un archivo CSV.
    Responsabilidad: Solo lectura y validación de existencia de archivo.
    \"\"\"
    print(f"[Ingesta] Leyendo datos desde: {ruta_archivo}")
    try:
        df = pd.read_csv(ruta_archivo)
        print(f"[Ingesta] Lectura exitosa. Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
        return df
    except FileNotFoundError:
        print(f"[Ingesta] Error: No se encontró el archivo {ruta_archivo}")
        return None
    except Exception as e:
        print(f"[Ingesta] Error inesperado durante la lectura: {e}")
        return None
"""
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(codigo)
    print(f"   Módulo generado: {ruta_archivo}")

def generar_modulo_transformacion(base_path="proyecto_pipeline"):
    """
    Generar el módulo encargado de las transformaciones y limpieza de datos.
    No sabe de dónde vienen ni a dónde van los datos.
    """
    ruta_archivo = os.path.join(base_path, "src", "transformacion.py")
    codigo = """# -*- coding: utf-8 -*-
import pandas as pd

def limpiar_y_transformar(df):
    \"\"\"
    Aplicar reglas de negocio, manejo de nulos y generación de nuevas variables.
    Responsabilidad: Solo transformación de la estructura DataFrame.
    \"\"\"
    print("[Transformación] Iniciando limpieza de datos...")
    
    # 1. Crear una copia para no mutar el original
    df_procesado = df.copy()
    
    # 2. Manejo de nulos (eliminar registros con nulos en columnas clave)
    filas_antes = df_procesado.shape[0]
    df_procesado = df_procesado.dropna(subset=['nombre_cliente', 'cantidad', 'precio_unitario'])
    filas_despues = df_procesado.shape[0]
    print(f"[Transformación] Registros nulos eliminados: {filas_antes - filas_despues}")
    
    # 3. Normalizar texto
    df_procesado['nombre_cliente'] = df_procesado['nombre_cliente'].str.upper().str.strip()
    
    # 4. Generación de variables derivadas (Lógica de negocio)
    df_procesado['ingreso_total'] = df_procesado['cantidad'] * df_procesado['precio_unitario']
    print("[Transformación] Nueva columna generada: 'ingreso_total'")
    
    return df_procesado
"""
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(codigo)
    print(f"   Módulo generado: {ruta_archivo}")

def generar_modulo_almacenamiento(base_path="proyecto_pipeline"):
    """
    Generar el módulo encargado de guardar los datos en su destino final.
    """
    ruta_archivo = os.path.join(base_path, "src", "almacenamiento.py")
    codigo = """# -*- coding: utf-8 -*-
import pandas as pd
import os

def guardar_datos_csv(df, ruta_salida):
    \"\"\"
    Persistir el dataframe procesado en formato CSV.
    Responsabilidad: Solo escritura de datos.
    \"\"\"
    print(f"[Almacenamiento] Guardando datos en: {ruta_salida}")
    try:
        # Asegurar que el directorio destino existe
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        df.to_csv(ruta_salida, index=False)
        print("[Almacenamiento] Guardado completado con éxito.")
    except Exception as e:
        print(f"[Almacenamiento] Error al intentar guardar los datos: {e}")
"""
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(codigo)
    print(f"   Módulo generado: {ruta_archivo}")

def generar_script_orquestador(base_path="proyecto_pipeline"):
    """
    Generar el script principal (main.py) que importa los módulos 
    y define el flujo (pipeline) paso a paso.
    """
    # Archivo init necesario para que python reconozca 'src' como paquete
    open(os.path.join(base_path, "src", "__init__.py"), "w").close()
    
    ruta_archivo = os.path.join(base_path, "main.py")
    codigo = """# -*- coding: utf-8 -*-
import os

# Importar funciones modulares desde nuestro paquete 'src'
# Esto evita la duplicación de lógica y facilita la mantenibilidad
from src.ingesta import extraer_datos_csv
from src.transformacion import limpiar_y_transformar
from src.almacenamiento import guardar_datos_csv

def ejecutar_pipeline():
    \"\"\"
    Orquestador principal del pipeline de datos.
    Define claramente los pasos: Ingesta -> Transformación -> Almacenamiento.
    \"\"\"
    print("="*50)
    print(" INICIANDO PIPELINE DE DATOS V1 (MODULAR)")
    print("="*50)
    
    # Definición de rutas relativas
    ruta_entrada = os.path.join("data", "raw", "transacciones.csv")
    ruta_salida = os.path.join("data", "processed", "transacciones_limpias.csv")
    
    # Paso 1: Ingesta
    df_crudo = extraer_datos_csv(ruta_entrada)
    
    # Validación de continuidad
    if df_crudo is not None and not df_crudo.empty:
        
        # Paso 2: Transformación
        df_procesado = limpiar_y_transformar(df_crudo)
        
        # Paso 3: Almacenamiento
        guardar_datos_csv(df_procesado, ruta_salida)
        
    else:
        print("Pipeline detenido: No hay datos para procesar.")
        
    print("="*50)
    print(" PIPELINE FINALIZADO")
    print("="*50)

if __name__ == "__main__":
    ejecutar_pipeline()
"""
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(codigo)
    print(f"   Módulo generado: {ruta_archivo}")

def hacer_setup_completo():
    """Ejecutar todas las funciones generadoras."""
    carpeta_base = "proyecto_pipeline"
    print(f"\n--- Iniciando creación del proyecto en la carpeta '{carpeta_base}' ---\n")
    
    generar_estructura_directorios(carpeta_base)
    generar_datos_prueba(carpeta_base)
    generar_modulo_ingesta(carpeta_base)
    generar_modulo_transformacion(carpeta_base)
    generar_modulo_almacenamiento(carpeta_base)
    generar_script_orquestador(carpeta_base)
    
    print("\n--- Configuración completa ---")
    print("Para probar la modularidad, abre una terminal, navega a la carpeta generada y ejecuta el orquestador:")
    print(f"   cd {carpeta_base}")
    print("   python main.py\n")

if __name__ == "__main__":
    hacer_setup_completo()
