# -*- coding: utf-8 -*-
# =============================================================================
# Capítulo 3: Exposición y consumo de datos
# Sección 5: APIs con FastAPI
# Bloque 2: Endpoints básicos
# =============================================================================

# Contexto: Este script ilustra cómo construir una API básica utilizando FastAPI.
# Se abordan conceptos como la definición de endpoints, manejo de parámetros
# (path y query), retorno de respuestas en formato JSON (serialización automática) 
# y la estructura inicial de una aplicación FastAPI.
#
# Requisitos: 
# pip install fastapi uvicorn
#
# Ejecución desde la terminal:
# uvicorn nombre_del_archivo:app --reload

from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any

# 1. Generar la instancia principal de la aplicación FastAPI.
# Esta variable 'app' es el componente central que Uvicorn utilizará 
# para levantar el servidor y mapear las rutas.
app = FastAPI(
    title="API de Transacciones Básica",
    description="API inicial para exponer datos estructurados de un pipeline de datos.",
    version="1.0.0"
)

# =============================================================================
# Datos estáticos (Simulación de la salida del pipeline)
# =============================================================================
# Hacer una pequeña base de datos en memoria utilizando diccionarios.
# En bloques posteriores, esto será sustituido por la conexión a MySQL o archivos.

DATOS_TRANSACCIONES: List[Dict[str, Any]] = [
    {"id_transaccion": 1001, "cliente": "Juan Perez", "monto": 250.50, "categoria": "Electrónica"},
    {"id_transaccion": 1002, "cliente": "Maria Lopez", "monto": 45.00, "categoria": "Comida"},
    {"id_transaccion": 1003, "cliente": "Carlos Ruiz", "monto": 1200.00, "categoria": "Electrónica"},
    {"id_transaccion": 1004, "cliente": "Ana Gomez", "monto": 15.75, "categoria": "Transporte"},
    {"id_transaccion": 1005, "cliente": "Luis Diaz", "monto": 310.20, "categoria": "Ropa"}
]

# =============================================================================
# Definición de Endpoints Básicos
# =============================================================================

# ST1, ST2: Creación de rutas (path operations) y endpoint básico
@app.get("/", tags=["Inicio"])
def obtener_inicio() -> Dict[str, str]:
    """
    Endpoint raíz de la API.
    Retorna un mensaje de bienvenida.
    FastAPI serializa automáticamente el diccionario de Python a JSON.
    """
    return {"mensaje": "Bienvenido a la API de Datos", "estado": "Activo"}


# ST8: Uso de datos estáticos vs dinámicos
@app.get("/transacciones", tags=["Transacciones"])
def obtener_todas_las_transacciones() -> Dict[str, Any]:
    """
    Retorna la lista completa de transacciones simuladas.
    """
    return {
        "total_registros": len(DATOS_TRANSACCIONES), 
        "datos": DATOS_TRANSACCIONES
    }


# ST3: Parámetros de entrada simples (Path Parameters)
@app.get("/transacciones/id/{id_transaccion}", tags=["Transacciones"])
def obtener_transaccion_por_id(id_transaccion: int) -> Dict[str, Any]:
    """
    Endpoint con parámetro de ruta (path parameter).
    El ID proporcionado en la URL se transforma automáticamente en un entero.
    """
    # Filtrar la lista de transacciones buscando el ID proporcionado
    for transaccion in DATOS_TRANSACCIONES:
        if transaccion["id_transaccion"] == id_transaccion:
            return {"encontrado": True, "datos": transaccion}
            
    # ST9: Buenas prácticas (Manejo básico de errores si no existe el registro)
    raise HTTPException(status_code=404, detail="Transacción no encontrada.")


# ST3: Parámetros de consulta (Query Parameters)
@app.get("/transacciones/filtrar", tags=["Transacciones"])
def filtrar_transacciones_por_categoria(categoria: str) -> Dict[str, Any]:
    """
    Endpoint con parámetro de consulta (query parameter).
    Permite filtrar los resultados.
    Ejemplo de uso: /transacciones/filtrar?categoria=Electrónica
    """
    # Generar una lista comprensiva filtrando por la categoría recibida
    resultados = [t for t in DATOS_TRANSACCIONES if t["categoria"].lower() == categoria.lower()]
    
    # ST4, ST5: Retorno de datos estructurados para su serialización a JSON
    return {
        "categoria_buscada": categoria,
        "coincidencias": len(resultados),
        "datos": resultados
    }

# =============================================================================
# ST7, ST11: Pruebas y Documentación Automática
# =============================================================================
# Al levantar el servidor (ej. con uvicorn), FastAPI genera automáticamente 
# interfaces interactivas para probar los endpoints.
# 
# Visitar en el navegador:
# - Swagger UI: http://127.0.0.1:8000/docs
# - ReDoc:      http://127.0.0.1:8000/redoc

if __name__ == "__main__":
    # Este bloque permite levantar el servidor directamente desde Python 
    # para entornos de desarrollo.
    import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    print("Para ejecutar la API de forma correcta, utilice el comando en la terminal:")
    print("uvicorn <nombre_del_script>:app --reload")
