# -*- coding: utf-8 -*-

"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 3: SQL y MySQL
Bloque 1: Fundamentos SQL (SELECT, WHERE)

Descripción: Script para demostrar los conceptos básicos de bases de datos
relacionales, creación de esquemas, y consultas fundamentales utilizando
SQL estándar. Para facilitar la ejecución sin configuración previa, 
utilizaremos SQLite (integrado en Python), cuyos conceptos son 
directamente aplicables a MySQL.
"""

import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

# Configurar semilla para reproducibilidad
random.seed(987654)

# =============================================================================
# ST1, ST2, ST3, ST4: Bases de datos relacionales, tablas, filas, columnas, 
# claves primarias y esquemas.
# =============================================================================

def crear_base_datos_y_esquema():
    """
    Crear una conexión a una base de datos en memoria y definir su esquema.
    Un esquema define la estructura de las tablas, sus columnas y tipos de datos.
    """
    print("--- Creando Base de Datos y Esquema ---")
    # Conexión a base de datos en memoria (se borra al cerrar el script)
    conexion = sqlite3.connect(":memory:")
    cursor = conexion.cursor()

    # Definir el esquema de la tabla 'transacciones'
    # id_transaccion: Clave primaria (ST3 - Unicidad)
    # Las columnas tienen tipos de datos definidos (INTEGER, REAL, TEXT)
    query_crear_tabla = """
    CREATE TABLE transacciones (
        id_transaccion INTEGER PRIMARY KEY,
        id_cliente INTEGER NOT NULL,
        monto REAL NOT NULL,
        fecha TEXT NOT NULL,
        categoria TEXT,
        estado TEXT
    );
    """
    cursor.execute(query_crear_tabla)
    conexion.commit()
    print("Tabla 'transacciones' creada exitosamente con su esquema.\n")
    
    return conexion, cursor

# =============================================================================
# Generar datos simulados para el caso práctico del curso
# =============================================================================

def generar_e_insertar_datos(conexion, cursor):
    """
    Generar un dataset de transacciones e insertarlo en la base de datos.
    """
    categorias = ["Alimentación", "Transporte", "Entretenimiento", "Servicios"]
    estados = ["Completada", "Pendiente", "Fallida"]
    
    datos_insertar = []
    fecha_base = datetime(2023, 1, 1)
    
    for i in range(1, 101): # Generar 100 transacciones
        id_cliente = random.randint(1000, 1010)
        monto = round(random.uniform(10.0, 500.0), 2)
        fecha = (fecha_base + timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        categoria = random.choice(categorias)
        estado = random.choice(estados)
        
        datos_insertar.append((i, id_cliente, monto, fecha, categoria, estado))
    
    # Insertar filas en la tabla
    query_insertar = """
    INSERT INTO transacciones (id_transaccion, id_cliente, monto, fecha, categoria, estado)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(query_insertar, datos_insertar)
    conexion.commit()
    print(f"Se insertaron {len(datos_insertar)} filas en la tabla 'transacciones'.\n")

# =============================================================================
# ST5, ST6: Introducción a SQL y Sintaxis básica de SELECT
# =============================================================================

def ejecutar_select_basico(cursor):
    """
    Ejecutar consultas SELECT para extraer datos de la tabla.
    """
    print("--- ST6: Sintaxis Básica de SELECT ---")
    
    # Consultar todas las columnas (*) de las primeras 3 filas
    query_todas_columnas = "SELECT * FROM transacciones LIMIT 3;"
    cursor.execute(query_todas_columnas)
    resultados = cursor.fetchall()
    
    print("Consulta: SELECT * FROM transacciones LIMIT 3;")
    for fila in resultados:
        print(fila)
        
    # Consultar columnas específicas
    query_columnas_especificas = "SELECT id_cliente, monto, categoria FROM transacciones LIMIT 3;"
    cursor.execute(query_columnas_especificas)
    resultados_especificos = cursor.fetchall()
    
    print("\nConsulta: SELECT id_cliente, monto, categoria FROM transacciones LIMIT 3;")
    for fila in resultados_especificos:
        print(fila)
    print("\n")

# =============================================================================
# ST7: Uso de WHERE para filtrado
# =============================================================================

def ejecutar_select_con_where(cursor):
    """
    Ejecutar consultas utilizando WHERE para filtrar registros específicos.
    """
    print("--- ST7: Uso de WHERE para filtrado ---")
    
    # Filtrar transacciones por categoría
    query_where_categoria = "SELECT id_transaccion, monto, categoria FROM transacciones WHERE categoria = 'Alimentación' LIMIT 3;"
    cursor.execute(query_where_categoria)
    print("Consulta: ... WHERE categoria = 'Alimentación'")
    for fila in cursor.fetchall():
        print(fila)
        
    # Filtrar transacciones usando operadores lógicos y de comparación
    query_where_complejo = """
    SELECT id_transaccion, monto, estado 
    FROM transacciones 
    WHERE monto > 300 AND estado = 'Completada'
    LIMIT 3;
    """
    cursor.execute(query_where_complejo)
    print("\nConsulta: ... WHERE monto > 300 AND estado = 'Completada'")
    for fila in cursor.fetchall():
        print(fila)
    print("\n")

# =============================================================================
# ST8, ST9: Comparación entre procesamiento Python vs SQL y Casos de Uso
# =============================================================================

def comparar_python_vs_sql(conexion):
    """
    Demostrar la diferencia entre procesar en motor de base de datos (SQL)
    versus cargar todo en memoria y procesar con Pandas (Python).
    """
    print("--- ST8: Comparación Python vs SQL ---")
    
    # CASO 1: Usando SQL (El motor de la base de datos hace el trabajo y solo devuelve lo necesario)
    query_sql = "SELECT id_transaccion, monto FROM transacciones WHERE monto > 400;"
    df_sql = pd.read_sql_query(query_sql, conexion)
    print("1. Procesamiento en SQL (Retorna solo lo filtrado a Python):")
    print(df_sql.head(3))
    print(f"Total registros traídos a memoria: {len(df_sql)}\n")
    
    # CASO 2: Usando Python/Pandas (Se trae toda la tabla a memoria y luego se filtra)
    df_completo = pd.read_sql_query("SELECT * FROM transacciones;", conexion)
    df_python = df_completo[df_completo['monto'] > 400][['id_transaccion', 'monto']]
    print("2. Procesamiento en Python (Trae todo y filtra en memoria):")
    print(df_python.head(3))
    print("Nota: En Big Data o Ingeniería de Datos (ST9), traer millones de registros a Python colapsaría la memoria. SQL es clave para filtrar en origen.\n")

# =============================================================================
# ST10, ST11: Consultas eficientes y concepto de Índices
# =============================================================================

def demostrar_indices_basicos(conexion, cursor):
    """
    Explicar y crear un índice para mejorar el rendimiento de lectura.
    """
    print("--- ST10 & ST11: Importancia de performance e Índices ---")
    
    # Supongamos que consultamos frecuentemente por 'id_cliente'
    # Sin un índice, la base de datos debe escanear toda la tabla (Full Table Scan)
    
    # Crear un índice en la columna 'id_cliente'
    query_crear_indice = "CREATE INDEX idx_id_cliente ON transacciones(id_cliente);"
    cursor.execute(query_crear_indice)
    conexion.commit()
    
    print("Se ejecutó: CREATE INDEX idx_id_cliente ON transacciones(id_cliente);")
    print("Concepto: Un índice funciona como el índice de un libro. Permite a la base de datos")
    print("encontrar rápidamente los registros asociados a 'id_cliente' sin leer cada fila de la tabla.")
    print("Esto es fundamental para mantener pipelines de datos eficientes y consultas veloces.\n")

# =============================================================================
# Bloque Principal de Ejecución
# =============================================================================

if __name__ == "__main__":
    # 1. Crear entorno y esquema
    conexion_db, cursor_db = crear_base_datos_y_esquema()
    
    # 2. Población de datos
    generar_e_insertar_datos(conexion_db, cursor_db)
    
    # 3. Exploración de comandos SQL
    ejecutar_select_basico(cursor_db)
    ejecutar_select_con_where(cursor_db)
    
    # 4. Análisis comparativo e introducción a performance
    comparar_python_vs_sql(conexion_db)
    demostrar_indices_basicos(conexion_db, cursor_db)
    
    # Cerrar conexión
    conexion_db.close()
    print("Conexión a la base de datos cerrada. Fin del script.")
