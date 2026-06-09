# ⚙️ Setup & Guión — Sesión 12: Cronjobs + Airflow + Proyecto Final
### Python para Ingeniería de Datos · BSG Institute

---

## Archivos de esta sesión

```
sesion_12/
├── airflow_intro.html           ← slides de la clase
├── pipeline_functions.py        ← funciones del pipeline (va en ~/airflow/dags/)
├── dag_pipeline_tunombre.py     ← DAG del proyecto final (va en ~/airflow/dags/)
└── .env                         ← credenciales (la misma de sesiones anteriores)
```

---

## Paso 1 — Instalar Airflow (en el inicio de clase)

```bash
# Activar venv
source venv/bin/activate

# Instalar Airflow con restricciones de versión (evita conflictos)
AIRFLOW_VERSION=2.10.3
PYTHON_VERSION=$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

> ⚠️ Si el URL de constraints da error, usar simplemente:
> `pip install apache-airflow==2.10.3`

---

## Paso 2 — Inicializar y levantar Airflow

```bash
# Carpeta de Airflow (se crea automáticamente)
export AIRFLOW_HOME=~/airflow

# Inicializar la base de datos interna
airflow db init

# Levantar todo en un solo comando
airflow standalone
```

Busca en el output:
```
Login with username: admin  password: XXXXXXXX
```

O busca el password en:
```bash
cat ~/airflow/simple_auth_manager_passwords.json
```

Abre **http://localhost:8080** → login con admin + password.

---

## Paso 3 — Configurar la conexión HTTP para el HttpSensor

En la UI de Airflow:
1. **Admin → Connections → +**
2. Llena los campos:
   - Connection Id: `api_local`
   - Connection Type: `HTTP`
   - Host: `http://localhost`
   - Port: `8001`
3. **Save**

> Esto permite que el HttpSensor del DAG llame a `http://localhost:8001/health`

---

## Paso 4 — Copiar los archivos del DAG

```bash
mkdir -p ~/airflow/dags

# Copia los dos archivos
cp pipeline_functions.py ~/airflow/dags/
cp dag_pipeline_tunombre.py ~/airflow/dags/

# Renombrar con tu nombre
mv ~/airflow/dags/dag_pipeline_tunombre.py \
   ~/airflow/dags/dag_pipeline_TUNOMBRE.py
```

Airflow detecta los DAGs en ~30 segundos. Refresca la UI.

---

## Paso 5 — Modificar el DAG con tu nombre

Abre `dag_pipeline_TUNOMBRE.py` y cambia:

```python
ALUMNO    = 'tunombre'           # ← tu nombre sin espacios, minúsculas
DAG_OWNER = 'Tu Nombre Completo' # ← tu nombre completo
```

Guarda. Airflow recarga automáticamente.

---

## Paso 6 — El twist: puerto incorrecto

`pipeline_functions.py` tiene por defecto:
```python
'port': int(os.getenv('DB_PORT_DAG', 9999)),   # ← puerto malo intencional
```

Añade al `.env`:
```
DB_PORT_DAG=9999
```

Cuando corras el DAG, `cargar_mysql` fallará con:
```
Can't connect to MySQL server on 'mysql-bsg-curso-d01...' (9999)
```

**Para corregir:** cambia en `.env`:
```
DB_PORT_DAG=10031
```

Luego en la UI: clic en la tarea roja → **Clear** → **Confirm** → la tarea se reintenta.

---

## Paso 7 — Levantar el contenedor Docker (para el health check)

En otra terminal:
```bash
cd sesion_11
docker run -d --name mi-api -p 8001:8001 --env-file .env api-bsg
```

Si no tienes la imagen:
```bash
docker build -t api-bsg .
```

---

## Paso 8 — Correr el DAG

1. En la UI de Airflow, busca `pipeline_transacciones_TUNOMBRE`
2. Activa el toggle (debe pasar de gris a azul)
3. Clic en **▶ Trigger DAG**
4. Observa el Graph View — las tareas se colorean en tiempo real

**Primera corrida:** `cargar_mysql` falla (rojo) → screenshot del DAG rojo
**Después de corregir el puerto:** todas las tareas verde → screenshot del DAG verde

---

## Guión de la sesión (2.5 hr)

| Tiempo | Qué | Herramienta |
|---|---|---|
| 0:00–0:05 | Pides que hagan pip install airflow mientras abren las slides | Terminal |
| 0:05–0:15 | Slides 1-2: concepto de cronjobs | HTML slides |
| 0:15–0:20 | Demo de crontab desde Cloud Shell | Cloud Shell |
| 0:20–0:35 | Slides 3-4: Airflow vs Cron, qué es un DAG | HTML slides |
| 0:35–0:50 | Slide 5: setup Airflow en vivo, todos lo hacen contigo | Terminal |
| 0:50–1:00 | Slide 6: explicas el proyecto final y el twist del puerto | HTML slides |
| 1:00–1:10 | Configuras la conexión api_local en la UI juntos | Airflow UI |
| 1:10–1:25 | Todos copian los archivos, modifican su nombre, primer trigger | Terminal + UI |
| 1:25–1:35 | DAG falla en cargar_mysql — lees el log juntos | Airflow UI |
| 1:35–1:45 | Todos corrigen el puerto en .env, Clear + rerun | Terminal + UI |
| 1:45–2:05 | DAG verde — todos toman sus screenshots | Airflow UI |
| 2:05–2:20 | Slide 7: cierre del curso, stack completo | HTML slides |
| 2:20–2:30 | Preguntas, instrucciones de entrega | — |

---

## Entregables finales

Dos archivos por alumno, enviados por el canal de la clase:

| Archivo | Qué muestra |
|---|---|
| `dag_rojo_TuNombre.png` | Airflow UI con `cargar_mysql` en rojo y el log del error visible |
| `dag_verde_TuNombre.png` | Airflow UI con todas las tareas en verde |

---

## Troubleshooting común

| Problema | Causa | Solución |
|---|---|---|
| DAG no aparece en la UI | Error de sintaxis en el .py | `python dag_pipeline_TUNOMBRE.py` en terminal para ver el error |
| HttpSensor timeout | Contenedor no está corriendo | `docker ps` → si no está, `docker run ...` |
| XCom error | Datos muy grandes | Reducir `n=60` en `extraer()` |
| `ModuleNotFoundError: pipeline_functions` | Archivo no en dags/ | `cp pipeline_functions.py ~/airflow/dags/` |
| Puerto 8080 ocupado | Otro proceso | `lsof -i :8080` → matar el proceso |
