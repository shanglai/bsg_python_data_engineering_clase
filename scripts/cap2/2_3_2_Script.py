# -*- coding: utf-8 -*-

"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 3: SQL y MySQL
Bloque 2: JOINs y agregaciones

Descripción:
Este script ilustra los conceptos de combinación de tablas (JOINs) y funciones 
de agregación (GROUP BY, SUM, COUNT, AVG). Se utiliza SQLite como motor en memoria 
para demostrar la sintaxis estándar de SQL, preparando el terreno para la conexión 
a MySQL del siguiente bloque.

Subtemas cubiertos:
- ST1 a ST4: Concepto, tipos (INNER, LEFT) y ejemplo de JOINs.
- ST5 a ST7: Funciones de agregación y agrupaciones para métricas.
- ST8 a ST11: Errores comunes, problemas de agregación y validación de negocio.
"""

import sqlite3
import pandas as pd
import random

# Fijar semilla para reproducibilidad según requerimientos
random.seed(987654)

def configurar_base_datos_prueba(cursor):
    """
    Generar las tablas de prueba para simular el dataset de transacciones.
    """
    # Crear tabla de Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY,
            nombre TEXT,
            pais TEXT
        )
    ''')

    # Crear tabla de Transacciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacciones (
            id_transaccion INTEGER PRIMARY KEY,
            id_cliente INTEGER,
            monto REAL,
            estado TEXT,
            FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
        )
    ''')

    # Insertar datos de prueba en clientes
    clientes_data = [
        (1, 'Ana', 'Mexico'),
        (2, 'Luis', 'Colombia'),
        (3, 'Carlos', 'Chile'),
        (4, 'Marta', 'Peru') # Cliente sin transacciones para demostrar LEFT JOIN
    ]
    cursor.executemany('INSERT INTO clientes VALUES (?, ?, ?)', clientes_data)

    # Insertar datos de prueba en transacciones
    transacciones_data = [
        (101, 1, 150.50, 'Completada'),
        (102, 1, 200.00, 'Completada'),
        (103, 2, 50.00, 'Cancelada'),
        (104, 2, 300.25, 'Completada'),
        (105, 3, 120.00, 'Completada'),
        (106, 99, 500.00, 'Completada') # Transacción huérfana (cliente no existe) para demostrar INNER JOIN
    ]
    cursor.executemany('INSERT INTO transacciones VALUES (?, ?, ?, ?)', transacciones_data)

def ejecutar_inner_join(conexion):
    """
    Hacer una consulta utilizando INNER JOIN para combinar ambas tablas.
    Solo traerá los registros donde haya coincidencia en ambas tablas.
    (ST1, ST2, ST3, ST4)
    """
    query = '''
        SELECT 
            t.id_transaccion, 
            c.nombre AS nombre_cliente, 
            t.monto, 
            t.estado
        FROM transacciones t
        INNER JOIN clientes c 
            ON t.id_cliente = c.id_cliente;
    '''
    print("\n--- Resultado de INNER JOIN ---")
    df = pd.read_sql_query(query, conexion)
    print(df)
    # Nota de negocio: La transacción 106 desaparece porque el id_cliente 99 no está en la tabla clientes.

def ejecutar_left_join(conexion):
    """
    Hacer una consulta utilizando LEFT JOIN tomando a los clientes como tabla principal.
    Traerá todos los clientes, incluso si no tienen transacciones.
    (ST2)
    """
    query = '''
        SELECT 
            c.id_cliente,
            c.nombre, 
            t.id_transaccion, 
            t.monto
        FROM clientes c
        LEFT JOIN transacciones t 
            ON c.id_cliente = t.id_cliente;
    '''
    print("\n--- Resultado de LEFT JOIN ---")
    df = pd.read_sql_query(query, conexion)
    print(df)
    # Nota de negocio: Marta aparecerá con id_transaccion y monto nulos (NaN/None)

def generar_metricas_agregacion(conexion):
    """
    Generar métricas utilizando funciones de agregación (SUM, COUNT, AVG) y GROUP BY.
    (ST5, ST6, ST7, ST11)
    """
    query = '''
        SELECT 
            c.nombre,
            c.pais,
            COUNT(t.id_transaccion) AS numero_transacciones,
            SUM(t.monto) AS ingresos_totales,
            AVG(t.monto) AS ticket_promedio
        FROM clientes c
        INNER JOIN transacciones t 
            ON c.id_cliente = t.id_cliente
        WHERE t.estado = 'Completada'
        GROUP BY c.id_cliente, c.nombre, c.pais
        ORDER BY ingresos_totales DESC;
    '''
    print("\n--- Métricas por Cliente (Agregación y GROUP BY) ---")
    df = pd.read_sql_query(query, conexion)
    print(df)

def demostrar_error_duplicados_join(cursor):
    """
    Demostrar un error común: generar duplicados al hacer JOIN con relaciones 1 a N
    si no se usa la agregación adecuada (ST8, ST9, ST10).
    """
    # Insertar un registro duplicado en clientes (mala práctica de negocio)
    cursor.execute("INSERT INTO clientes VALUES (5, 'Ana', 'Mexico')")
    # Actualizar la transacción 101 para que apunte al nombre en lugar del id (simulando un mal diseño)
    
    query_mala = '''
        SELECT c.nombre, SUM(t.monto) AS suma_incorrecta
        FROM clientes c
        JOIN transacciones t ON c.id_cliente = t.id_cliente
        GROUP BY c.nombre;
    '''
    print("\n--- Validar resultados: Prevención de errores ---")
    print("El uso de agrupaciones por campos no únicos (como 'nombre' en vez de 'id') puede causar sobreescritura o sumas erróneas.")
    # Explicación: En un entorno real, las métricas deben validarse contra una suma total para evitar datos inflados por JOINs cartesianos.

def main():
    # 1. Crear conexión temporal a base de datos
    conexion = sqlite3.connect(':memory:')
    cursor = conexion.cursor()

    try:
        # 2. Configurar entorno y datos simulados
        configurar_base_datos_prueba(cursor)

        # 3. Ejecutar consultas de combinación (JOINs)
        ejecutar_inner_join(conexion)
        ejecutar_left_join(conexion)

        # 4. Ejecutar consultas de agregación (GROUP BY)
        generar_metricas_agregacion(conexion)

        # 5. Demostrar errores de agregación
        demostrar_error_duplicados_join(cursor)

    except sqlite3.Error as e:
        print(f"Error procesando la base de datos: {e}")
    finally:
        # 6. Cerrar la conexión para liberar recursos
        conexion.close()

if __name__ == "__main__":
    main()
