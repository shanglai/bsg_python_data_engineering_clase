# -*- coding: utf-8 -*-
# Capítulo 6: Integración, despliegue y proyecto final
# Sección 11: CI/CD y monitoreo
# Bloque 3: Monitoreo (logs, health checks)

"""
Script demostrativo para implementar monitoreo basico,
logs estructurados y un endpoint de health check usando FastAPI.
"""

import json
import logging
import random
import time
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configurar semilla aleatoria para consistencia en simulaciones
random.seed(987654)

# =============================================================================
# Parte 1: Configurar Logging Estructurado
# =============================================================================
# Generar un formateador personalizado para que los logs salgan en formato JSON
# Esto facilita su ingesta y analisis en herramientas de monitoreo (observabilidad).

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def configurar_logger():
    """
    Configurar y retornar un logger con formato JSON para logs estructurados.
    """
    logger = logging.getLogger("DataPipelineLogger")
    logger.setLevel(logging.DEBUG)
    
    # Evitar duplicar handlers si se ejecuta multiples veces
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        
    return logger

logger = configurar_logger()

# =============================================================================
# Parte 2: Implementar Logging en Scripts (Pipeline Simulado)
# =============================================================================

def procesar_datos_pipeline():
    """
    Simular un proceso de ingenieria de datos que registra eventos clave,
    advertencias y errores.
    """
    logger.info("Iniciando la ejecucion del pipeline de datos")
    
    # Simular la lectura de datos
    logger.info("Leyendo datos desde la fuente (API/CSV)")
    time.sleep(0.5)
    
    # Simular una advertencia (WARNING)
    registros_leidos = random.randint(50, 150)
    if registros_leidos < 100:
        logger.warning(f"Se leyeron menos registros de los esperados: {registros_leidos}")
    else:
        logger.info(f"Se leyeron {registros_leidos} registros correctamente")
        
    # Simular la transformacion y un posible error (ERROR)
    logger.info("Iniciando la transformacion de datos")
    time.sleep(0.5)
    
    try:
        # Forzar un error aleatorio para demostrar el logging de excepciones
        probabilidad_error = random.random()
        if probabilidad_error > 0.8:
            raise ValueError("Inconsistencia detectada en los tipos de datos")
            
        logger.info("Transformacion de datos completada exitosamente")
        
    except Exception as e:
        logger.error(f"Fallo en la transformacion de datos: {str(e)}")
        # En un pipeline real, podriamos decidir detener la ejecucion aqui
        return False
        
    # Simular el almacenamiento
    logger.info("Almacenando los datos procesados en la base de datos")
    time.sleep(0.5)
    logger.info("Pipeline de datos finalizado correctamente")
    return True

# =============================================================================
# Parte 3: Implementar FastAPI con Endpoint de Salud (Health Check)
# =============================================================================
# Definir la aplicacion FastAPI
app = FastAPI(
    title="API de Datos con Monitoreo",
    description="Ejemplo de API con endpoints de salud y logging estructurado."
)

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: dict

@app.on_event("startup")
def evento_inicio():
    """
    Registrar el inicio de la aplicacion en el log estructurado.
    """
    logger.info("Iniciando la aplicacion FastAPI")

@app.get("/health", response_model=HealthResponse)
def endpoint_salud():
    """
    Definir el endpoint /health para monitoreo del sistema.
    Retorna el estado de la API y de los servicios de los que depende (simulado).
    """
    logger.info("Health check solicitado")
    
    # Simular la comprobacion de conexion a la base de datos
    conexion_db_ok = True
    # Simular la comprobacion de conexion al almacenamiento en la nube
    conexion_storage_ok = True
    
    estado_general = "ok" if conexion_db_ok and conexion_storage_ok else "degraded"
    
    if estado_general != "ok":
        logger.error(f"Health check reporta estado degradado. DB: {conexion_db_ok}, Storage: {conexion_storage_ok}")
        # Retornar un codigo HTTP 503 (Service Unavailable) si hay fallos criticos
        raise HTTPException(
            status_code=503, 
            detail="Servicio no disponible temporalmente debido a fallos internos"
        )
        
    return HealthResponse(
        status=estado_general,
        timestamp=datetime.utcnow().isoformat(),
        services={
            "database": "online" if conexion_db_ok else "offline",
            "cloud_storage": "online" if conexion_storage_ok else "offline"
        }
    )

@app.post("/ejecutar-pipeline")
def ejecutar_pipeline():
    """
    Definir un endpoint para disparar el pipeline desde la API.
    """
    logger.info("Solicitud recibida para ejecutar el pipeline")
    resultado = procesar_datos_pipeline()
    
    if resultado:
        return {"status": "success", "message": "Pipeline ejecutado correctamente"}
    else:
        raise HTTPException(status_code=500, detail="Error en la ejecucion del pipeline")

# =============================================================================
# Ejecucion local de prueba (solo como demostracion del script)
# =============================================================================
if __name__ == "__main__":
    # Importante: para ejecutar la API real, usar `uvicorn nombre_archivo:app --reload`
    logger.info("=== Demostracion de Pipeline con Logging Estructurado ===")
    procesar_datos_pipeline()
