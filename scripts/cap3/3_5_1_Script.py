# -*- coding: utf-8 -*-
# =============================================================================
# Capítulo 3: Exposición y consumo de datos
# Sección 5: APIs con FastAPI
# Bloque 1: Introducción a APIs y FastAPI
# =============================================================================

# Importar las librerías necesarias
import random
from fastapi import FastAPI
from pydantic import BaseModel

# Fijar semilla aleatoria para garantizar reproducibilidad en datos simulados
random.seed(987654)

# =============================================================================
# ST1 a ST7: Conceptos de API, HTTP, Endpoints y JSON
# Una API (Application Programming Interface) actúa como un puente entre 
# sistemas. Utiliza el protocolo HTTP mediante un modelo de Petición/Respuesta.
# Los datos viajan comúnmente en formato JSON, el estándar en pipelines modernos.
# =============================================================================

# ST8 y ST9: Introducción a FastAPI y sus ventajas
# FastAPI es un framework moderno, rápido y basado en tipado estático.
# Generar la instancia principal de la aplicación:
app = FastAPI(
    title="API de Transacciones - Pipeline de Datos",
    description="Introducción a APIs como productos de datos para consumo externo",
    version="1.0.0"
)

# =============================================================================
# ST11: Concepto de contrato (entrada/salida)
# Utilizar Pydantic para definir cómo deben estructurarse los datos recibidos y
# enviados. Esto asegura un contrato claro entre consumidor y proveedor.
# =============================================================================
class Transaccion(BaseModel):
    id_transaccion: int
    cliente: str
    monto: float
    estado: str

# =============================================================================
# ST4 y ST5: Métodos HTTP y Conceptos de endpoint
# Definir rutas (endpoints) que responderán a diferentes métodos HTTP
# (GET para consultar datos, POST para enviar o crear datos).
# =============================================================================

@app.get("/")
def obtener_raiz():
    """
    Endpoint base usando el método GET.
    Retorna un mensaje simple en formato JSON.
    Demuestra la estructura básica de Petición/Respuesta (ST3).
    """
    # ST6: Formato JSON como estándar.
    # FastAPI convierte automáticamente los diccionarios de Python a JSON.
    return {"mensaje": "Bienvenido a la API del Pipeline de Datos"}


@app.get("/transacciones/{id_transaccion}")
def obtener_transaccion(id_transaccion: int):
    """
    Endpoint usando el método GET para consultar una transacción específica.
    Expone datos consolidados como producto de datos (ST10 y ST7).
    """
    # Simular la lectura de un dato ya procesado por el pipeline
    monto_simulado = round(random.uniform(10.0, 500.0), 2)
    
    transaccion_simulada = {
        "id_transaccion": id_transaccion,
        "cliente": "Cliente_Pipeline_01",
        "monto": monto_simulado,
        "estado": "Procesada"
    }
    
    return transaccion_simulada


@app.post("/transacciones/")
def crear_transaccion(transaccion: Transaccion):
    """
    Endpoint usando el método POST para recibir datos.
    Demuestra el uso de contratos: FastAPI validará automáticamente que
    el cuerpo de la petición cumpla con el modelo 'Transaccion'.
    """
    # Al recibir los datos, se asume que cumplen con el contrato validado
    return {
        "mensaje": "Transacción recibida y validada correctamente",
        # Convertir el modelo a diccionario (compatible con Pydantic v2)
        "datos_recibidos": transaccion.model_dump() 
    }

# =============================================================================
# Ejecución local del servidor
# =============================================================================
if __name__ == "__main__":
    # Imprimir instrucciones sobre cómo levantar el servidor localmente
    print("Para ejecutar esta API, hacer uso del siguiente comando en la terminal:")
    print("uvicorn nombre_de_este_archivo:app --reload")
    print("Posteriormente, acceder a http://127.0.0.1:8000/docs para visualizar la documentación automática (Swagger UI).")
