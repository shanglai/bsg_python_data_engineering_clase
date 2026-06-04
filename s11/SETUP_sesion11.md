# ⚙️ Setup — Sesión 11/12: Docker + Proyecto Final
### Python para Ingeniería de Datos · BSG Institute

---

## Tarea previa (hacer ANTES de llegar a clase)

Instala Docker Desktop en tu máquina:
- **Mac / Windows:** https://www.docker.com/products/docker-desktop
- **Linux:** https://docs.docker.com/engine/install/

Verifica que funciona abriendo una terminal y ejecutando:

```bash
docker --version
# Docker version 27.x.x, build ...

docker run hello-world
# Hello from Docker! ...
```

Si ves esos mensajes, estás listo. Si no, avisa al instructor antes de la sesión.

---

## Archivos de esta sesión

```
sesion_11/
├── requirements_s11.txt   ← venv local (clase + Jupyter)
├── requirements_api.txt   ← imagen Docker (solo la API)
├── Dockerfile             ← instrucciones para construir la imagen
├── .dockerignore          ← archivos excluidos de la imagen
├── api.py                 ← la misma API de la sesión 9 (modificada)
├── dashboard.py           ← el mismo dashboard de la sesión 10 (modificado)
├── .env                   ← credenciales (la misma de sesiones anteriores)
└── Sesion_11_Docker.ipynb ← notebook de la clase
```

---

## Paso 1 — Crear carpeta y copiar archivos

```bash
mkdir sesion_11
cd sesion_11

# Copia desde sesión 9/10:
#   api.py
#   dashboard.py
#   .env

# Agrega los nuevos:
#   Dockerfile
#   .dockerignore
#   requirements_api.txt
#   requirements_s11.txt
#   Sesion_11_Docker.ipynb
```

---

## Paso 2 — Modificar api.py (tu personalización)

Abre `api.py` y en el endpoint `/health` añade tu nombre:

```python
@app.get('/health')
def health_check():
    return {
        'status':  'ok',
        'alumno':  'TU NOMBRE AQUÍ',   # ← pon tu nombre
        'version': '1.0.0',
        'database': db_status,
    }
```

---

## Paso 3 — Modificar dashboard.py (tu personalización)

Abre `dashboard.py` y cambia el caption del título:

```python
st.title('📊 Dashboard de Transacciones')
st.caption('Desarrollado por: TU NOMBRE · BSG Institute 2026')
```

Y cambia la URL base de la API al puerto del contenedor:

```python
API_BASE = 'http://localhost:8001'   # ← puerto del contenedor Docker
```

---

## Paso 4 — Construir la imagen Docker

```bash
docker build -t api-bsg .
```

Tarda ~2 minutos la primera vez (descarga Python y dependencias).
Las siguientes veces es casi instantáneo gracias al cache de capas.

Verifica que la imagen existe:

```bash
docker images
# REPOSITORY   TAG       IMAGE ID       SIZE
# api-bsg      latest    abc123...      ~200MB
```

---

## Paso 5 — Correr el contenedor

```bash
docker run -d --name mi-api -p 8001:8001 --env-file .env api-bsg
```

Verifica que corre:

```bash
docker ps
# CONTAINER ID   IMAGE     STATUS         PORTS
# a3f2c1...      api-bsg   Up X seconds   0.0.0.0:8001->8001/tcp

curl http://localhost:8001/health
# {"status":"ok","alumno":"Tu Nombre","version":"1.0.0","database":"ok"}
```

---

## Paso 6 — Levantar el dashboard

```bash
# Terminal separada, venv activo
streamlit run dashboard.py
```

El dashboard ahora consume la API del contenedor (puerto 8001).

---

## Paso 7 — Tomar el screenshot del entregable

El screenshot debe mostrar **todo simultáneamente**:

```
┌─────────────────────────┬────────────────────────────────┐
│  Browser                │  Terminal                      │
│  localhost:8501         │                                │
│                         │  $ docker ps                   │
│  📊 Dashboard de        │  CONTAINER ID  IMAGE  STATUS   │
│     Transacciones       │  a3f2c1...  api-bsg  Up 2 min  │
│                         │                                │
│  Desarrollado por:      │  $ curl localhost:8001/health  │
│  [Tu Nombre]            │  {"alumno":"[Tu Nombre]",...}  │
│                         │                                │
│  [KPIs con datos]       │                                │
└─────────────────────────┴────────────────────────────────┘
```

Herramientas para dividir pantalla:
- **Mac:** Mission Control o arrastrar ventanas a los lados
- **Windows:** Win + ← / Win + →
- **Zoom:** compartir pantalla completa, no solo ventana

---

## Paso 8 — Detener el contenedor al terminar

```bash
docker stop mi-api
docker rm mi-api
```

---

## Entrega

Envía el screenshot al instructor por el canal de la clase.
Formato del nombre del archivo: `proyecto_final_TuNombre.png`
