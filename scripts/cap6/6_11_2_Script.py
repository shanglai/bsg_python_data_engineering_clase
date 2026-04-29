# =============================================================================
# Capítulo 6: Integración, despliegue y proyecto final
# Sección 11: CI/CD y monitoreo
# Bloque 2: CI/CD con GitHub Actions
# =============================================================================

import os
import random

# Configurar semilla aleatoria
random.seed(987654)

# -----------------------------------------------------------------------------
# ST1, ST2, ST3, ST4: Conceptos de CI/CD y Automatización de procesos de código
# En este script vamos a generar la estructura de archivos necesaria para 
# simular y configurar un flujo de Integración Continua (CI) básico localmente,
# preparándolo para su uso en un repositorio real.
# -----------------------------------------------------------------------------

def generar_estructura_directorios():
    """
    Generar la estructura de carpetas requerida para el flujo de GitHub Actions
    y los scripts del proyecto de datos.
    """
    # Crear directorio especial para workflows de GitHub (ST5)
    os.makedirs(".github/workflows", exist_ok=True)
    
    # Crear directorios para el código fuente del pipeline y sus pruebas
    os.makedirs("src", exist_ok=True)
    os.makedirs("tests", exist_ok=True)
    print("Directorios del proyecto y CI/CD generados correctamente.")

# -----------------------------------------------------------------------------
# ST10: Integración CI con pipelines de datos
# Generar un componente del pipeline que será sometido a pruebas automatizadas.
# -----------------------------------------------------------------------------
def generar_codigo_pipeline():
    """
    Generar un script de Python que simula una función de limpieza de datos
    dentro de un pipeline de ingeniería.
    """
    codigo_pipeline = """# src/transformacion.py

def limpiar_monto_transaccion(monto, moneda):
    '''
    Validar y limpiar el monto de una transacción del pipeline.
    '''
    if monto is None or monto < 0:
        return None
    
    moneda_limpia = str(moneda).strip().upper()
    return f"{moneda_limpia} {float(monto):.2f}"
"""
    with open("src/transformacion.py", "w", encoding="utf-8") as f:
        f.write(codigo_pipeline)
    print("Script de transformación generado (src/transformacion.py).")

# -----------------------------------------------------------------------------
# ST8, ST9: Ejecución de scripts en CI y Validación automática de código
# Generar el script de pruebas unitarias que GitHub Actions ejecutará.
# -----------------------------------------------------------------------------
def generar_pruebas_unitarias():
    """
    Generar pruebas automatizadas (tests) para validar el comportamiento 
    del código de transformación del pipeline.
    """
    codigo_test = """# tests/test_transformacion.py

import sys
import os

# Ajustar el path para poder importar el módulo src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.transformacion import limpiar_monto_transaccion

def test_transaccion_valida():
    resultado = limpiar_monto_transaccion(150.5, "usd")
    assert resultado == "USD 150.50", f"Error en validación: {resultado}"

def test_transaccion_invalida_negativa():
    resultado = limpiar_monto_transaccion(-20, "eur")
    assert resultado is None, "Error: Se esperaba None para montos negativos"

def test_transaccion_nula():
    resultado = limpiar_monto_transaccion(None, "mxn")
    assert resultado is None, "Error: Se esperaba None para montos nulos"

if __name__ == "__main__":
    test_transaccion_valida()
    test_transaccion_invalida_negativa()
    test_transaccion_nula()
    print("Todas las validaciones del pipeline pasaron exitosamente.")
"""
    with open("tests/test_transformacion.py", "w", encoding="utf-8") as f:
        f.write(codigo_test)
    print("Script de validación generado (tests/test_transformacion.py).")

# -----------------------------------------------------------------------------
# ST5, ST6, ST7, ST11: Introducción a GitHub Actions, Estructura de workflow, 
# Eventos y Beneficios de CI/CD.
# -----------------------------------------------------------------------------
def generar_workflow_github_actions():
    """
    Generar el archivo YAML que define el pipeline de Integración Continua
    en GitHub Actions. Configurar para reaccionar a eventos de push y pull request.
    """
    codigo_yaml = """name: Pipeline de Datos CI/CD

# ST7: Definición de eventos que disparan el flujo automatizado
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

# ST6: Estructura de un workflow (jobs y steps)
jobs:
  validacion_datos:
    runs-on: ubuntu-latest

    steps:
      # Paso 1: Clonar el código del repositorio en el entorno de GitHub
      - name: Checkout del código fuente
        uses: actions/checkout@v3

      # Paso 2: Preparar el entorno reproducible (similar a lo visto en Docker)
      - name: Configurar entorno Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      # Paso 3: ST8, ST9 - Ejecutar la validación automática del código
      - name: Ejecutar pruebas del pipeline de datos
        run: |
          python tests/test_transformacion.py
"""
    with open(".github/workflows/ci.yml", "w", encoding="utf-8") as f:
        f.write(codigo_yaml)
    print("Workflow de GitHub Actions generado (.github/workflows/ci.yml).")

# =============================================================================
# Ejecución principal
# =============================================================================
if __name__ == "__main__":
    print("Iniciando construcción del entorno CI/CD simulado...")
    generar_estructura_directorios()
    generar_codigo_pipeline()
    generar_pruebas_unitarias()
    generar_workflow_github_actions()
    print("Entorno CI/CD generado exitosamente.")
    print("Nota: Al subir esta estructura a GitHub, el archivo .github/workflows/ci.yml automatizará las pruebas.")
