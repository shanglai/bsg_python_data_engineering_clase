# -*- coding: utf-8 -*-
# =============================================================================
# Capítulo 3: Exposición y consumo de datos
# Sección 5: APIs con FastAPI
# Bloque 4: Filtros y validaciones
# =============================================================================

# Importar las librerías necesarias
import random
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Path, status
from pydantic import BaseModel, Field

# Configurar semilla aleatoria estandarizada para el curso
random.seed(987654)

# =============================================================================
# ST8, ST11: Evitar errores comunes en APIs y creación de APIs robustas
# Inicializar la aplicación con metadatos descriptivos
# =============================================================================
app = FastAPI(
    title="API de Transacciones (Pipeline V1)",
    description="API robusta demostrando filtros, validaciones, Pydantic y manejo de errores HTTP.",
    version="1.0.0"
)

# Generar datos simulados (mock) que representan la salida del pipeline de datos
# En un escenario real (Bloque 3), esto provendría de MySQL.
CATEGORIAS = ["Alimentacion", "Transporte", "Entretenimiento", "Servicios", "Tecnologia"]
mock_db = [
    {
        "transaction_id": i,
        "customer_id": random.randint(100, 500),
        "amount": round(random.uniform(10.0, 500.0), 2),
        "category": random.choice(CATEGORIAS)
    }
    for i in range(1, 101)
]

# =============================================================================
# ST3, ST4: Validación de datos con Pydantic y Tipado en FastAPI
# ST7, ST9: Validación de entradas del usuario y seguridad (inputs controlados)
# =============================================================================

# Definir el modelo de salida (lo que la API devuelve)
class Transaction(BaseModel):
    transaction_id: int
    customer_id: int
    amount: float
    category: str

# Definir el modelo de entrada (lo que el usuario envía por POST)
# Field permite agregar validaciones restrictivas (min_length, gt, etc.)
class TransactionCreate(BaseModel):
    transaction_id: int = Field(..., gt=0, description="ID único de la transacción (mayor a 0)")
    customer_id: int = Field(..., gt=0, description="ID del cliente (mayor a 0)")
    amount: float = Field(..., gt=0, description="Monto de la transacción (estrictamente positivo)")
    category: str = Field(..., min_length=2, max_length=50, description="Categoría (entre 2 y 50 caracteres)")

# =============================================================================
# ST1, ST2, ST10: Implementación de filtros, query params y mejora de flexibilidad
# =============================================================================
@app.get("/transactions/", response_model=List[Transaction], status_code=status.HTTP_200_OK)
def get_transactions(
    # Parámetros de consulta (Query params) opcionales con validaciones
    category: Optional[str] = Query(None, description="Filtrar exactamente por categoría"),
    min_amount: Optional[float] = Query(None, ge=0, description="Monto mínimo (mayor o igual a 0)"),
    max_amount: Optional[float] = Query(None, ge=0, description="Monto máximo (mayor o igual a 0)")
):
    """
    Obtener transacciones aplicando filtros opcionales.
    """
    # Hacer una copia de los datos para filtrar
    resultados = mock_db.copy()

    # Aplicar filtro de categoría si el usuario lo provee
    if category:
        resultados = [t for t in resultados if t["category"].lower() == category.lower()]
    
    # Aplicar filtro de monto mínimo
    if min_amount is not None:
        resultados = [t for t in resultados if t["amount"] >= min_amount]
        
    # Aplicar filtro de monto máximo
    if max_amount is not None:
        resultados = [t for t in resultados if t["amount"] <= max_amount]
        
    # ST5: Manejo de escenarios donde no hay resultados (opcional pero buena práctica)
    if not resultados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron transacciones con los filtros proporcionados."
        )

    return resultados

# =============================================================================
# ST5, ST6: Manejo de errores en APIs y códigos de estado HTTP (404)
# =============================================================================
@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction_by_id(
    # Path es usado para validar parámetros en la URL
    transaction_id: int = Path(..., gt=0, description="ID de la transacción a buscar")
):
    """
    Obtener una única transacción por su ID.
    """
    # Buscar la transacción en la base de datos simulada
    for transaction in mock_db:
        if transaction["transaction_id"] == transaction_id:
            return transaction
            
    # Lanzar error 404 si el ID no existe
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Transacción con ID {transaction_id} no encontrada."
    )

# =============================================================================
# ST6, ST7, ST9: Códigos de estado HTTP (201, 400), validación de inputs y seguridad
# =============================================================================
@app.post("/transactions/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate):
    """
    Crear una nueva transacción validando los datos de entrada.
    """
    # Validar si el ID ya existe (Evitar duplicados - error 400 Bad Request)
    for t in mock_db:
        if t["transaction_id"] == transaction.transaction_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La transacción con ID {transaction.transaction_id} ya existe."
            )
            
    # ST8: Evitar errores comunes procesando el payload de forma segura
    nueva_transaccion = transaction.dict()
    mock_db.append(nueva_transaccion)
    
    return nueva_transaccion

# =============================================================================
# Instrucciones de ejecución (Para el entorno local)
# Guardar este archivo como `api_filtros.py`
# Ejecutar en consola: uvicorn api_filtros:app --reload
# Visitar http://127.0.0.1:8000/docs para ver la interfaz interactiva de Swagger
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    # Iniciar servidor localmente para pruebas
    uvicorn.run(app, host="0.0.0.0", port=8000)
