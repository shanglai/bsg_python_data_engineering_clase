# ⚙️ Setup — Sesión 9: FastAPI
### Python para Ingeniería de Datos · BSG Institute

---

## Archivos de esta sesión

```
sesion_09/
├── requirements_s09.txt   ← dependencias
├── api.py                 ← servidor FastAPI (lo levantas en terminal)
├── .env                   ← credenciales de BD (lo creas tú)
└── Sesion_09_FastAPI.ipynb ← notebook para seguir la clase
```

---

## Paso 1 — Crear la carpeta y copiar los archivos

```bash
mkdir sesion_09
cd sesion_09
# Copia aquí los archivos: api.py, requirements_s09.txt, Sesion_09_FastAPI.ipynb
```

---

## Paso 2 — Crear y activar el entorno virtual

```bash
# Crear el venv
python -m venv venv

# Activar — Mac/Linux:
source venv/bin/activate

# Activar — Windows:
venv\Scripts\activate

# Verificar que estás dentro del venv (debe aparecer (venv) en el prompt)
```

---

## Paso 3 — Instalar dependencias

```bash
pip install -r requirements_s09.txt
```

Tarda ~1 minuto. Al terminar verifica:

```bash
python -c "import fastapi, uvicorn, pymysql; print('✅ Todo instalado')"
```

---

## Paso 4 — Crear el archivo .env con las credenciales

Crea un archivo llamado `.env` en la carpeta `sesion_09/` con este contenido
(el instructor comparte el password en clase):

```
DB_HOST=mysql-bsg-curso-d01.h.aivencloud.com
DB_PORT=10031
DB_USER=avnadmin
DB_PASSWORD=PON_EL_PASSWORD_AQUI
DB_NAME=defaultdb
```

> ⚠️ El archivo `.env` NUNCA se sube a GitHub. Contiene credenciales privadas.

---

## Paso 5 — Levantar la API

Abre una terminal, activa el venv y ejecuta:

```bash
uvicorn api:app --reload --port 8000
```

Debes ver algo como:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Paso 6 — Verificar que funciona

Abre tu browser en:

- **Swagger UI** (documentación interactiva): http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

Si ves el Swagger UI, la API está lista. 🎉

---

## Paso 7 — Abrir el notebook

Con el venv activo, en otra terminal:

```bash
pip install jupyter  # solo si no lo tienes
jupyter notebook Sesion_09_FastAPI.ipynb
```

---

## Resumen de terminales que necesitas abiertas

```
Terminal 1 (venv activo) → uvicorn api:app --reload --port 8000
Terminal 2 (venv activo) → jupyter notebook Sesion_09_FastAPI.ipynb
Browser pestaña 1        → http://localhost:8000/docs   (Swagger UI)
Browser pestaña 2        → Jupyter notebook
```
