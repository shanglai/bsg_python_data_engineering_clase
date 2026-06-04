# ============================================================
# Dockerfile — API de Transacciones
# Python para Ingeniería de Datos · BSG Institute
# ============================================================
#
# Construir la imagen:
#   docker build -t api-bsg .
#
# Correr el contenedor:
#   docker run -d --name mi-api -p 8001:8001 --env-file .env api-bsg
#
# Verificar que corre:
#   docker ps
#   curl http://localhost:8001/health
#
# Detener el contenedor:
#   docker stop mi-api
#   docker rm mi-api
# ============================================================

# ── Capa 1: imagen base ──────────────────────────────────────
# python:3.12-slim es una versión reducida de Python
# "slim" significa que no trae herramientas extras que no necesitamos
# Resultado: imagen más pequeña y más segura
FROM python:3.12-slim

# ── Capa 2: directorio de trabajo ────────────────────────────
# Todo lo que hagamos dentro del contenedor vivirá en /app
# Es como hacer "mkdir /app && cd /app"
WORKDIR /app

# ── Capa 3: dependencias ─────────────────────────────────────
# Copiamos PRIMERO solo el requirements para aprovechar el cache de Docker.
# Si el código cambia pero el requirements no, Docker no reinstala todo.
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

# ── Capa 4: código de la aplicación ──────────────────────────
# Copiamos el código DESPUÉS de las dependencias (por el cache)
COPY api.py .

# ── Capa 5: variables de entorno ─────────────────────────────
# .env se carga en tiempo de ejecución con --env-file
# NO lo copiamos dentro de la imagen — contiene credenciales
# (El .dockerignore lo excluye también como medida extra)

# ── Documentación: puerto expuesto ───────────────────────────
# EXPOSE es solo documentación — el puerto real se define con -p al correr
# Usamos 8001 para distinguirlo del proceso local (8000)
EXPOSE 8001

# ── Comando de inicio ────────────────────────────────────────
# CMD es lo que corre cuando el contenedor arranca
# --host 0.0.0.0 permite conexiones desde fuera del contenedor
# --port 8001 es el puerto interno del contenedor
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]
