# Setup — Sesión 10: Streamlit Dashboard
### Python para Ingeniería de Datos · BSG Institute

---

## Archivos de esta sesión

```
sesion_10/
├── requirements_s10.txt      ← dependencias
├── api.py                    ← la misma API de la sesión 9 (copia o mueve)
├── dashboard.py              ← app Streamlit
├── .env                      ← credenciales (la misma del sesión 9)
└── Sesion_10_Streamlit.ipynb ← notebook para seguir la clase
```

---

## Paso 1 — Crear carpeta y copiar archivos

```bash
mkdir sesion_10
cd sesion_10
# Copia aquí: api.py y .env de la sesión 9
# Agrega: dashboard.py, requirements_s10.txt, Sesion_10_Streamlit.ipynb
```

---

## Paso 2 — Activar venv e instalar dependencias

Si usas el mismo venv de la sesión 9, solo agrega lo nuevo:

```bash
source venv/bin/activate          # Mac/Linux
# venv\Scripts\activate           # Windows

pip install -r requirements_s10.txt
```

Verifica:

```bash
python -c "import streamlit, plotly; print('✅ Todo instalado')"
```

---

## Paso 3 — Levantar la API (Terminal 1)

```bash
uvicorn api:app --reload --port 8000
```

---

## Paso 4 — Levantar el dashboard (Terminal 2)

```bash
streamlit run dashboard.py
```

Streamlit abre automáticamente el browser en **http://localhost:8501**

---

## Paso 5 — Abrir el notebook (Terminal 3)

```bash
jupyter notebook Sesion_10_Streamlit.ipynb
```

---

## Layout de terminales para la clase

```
Terminal 1 (venv) → uvicorn api:app --reload --port 8000
Terminal 2 (venv) → streamlit run dashboard.py
Terminal 3 (venv) → jupyter notebook

Browser pestaña 1 → http://localhost:8501   (Dashboard)
Browser pestaña 2 → http://localhost:8000/docs  (Swagger UI)
Browser pestaña 3 → Jupyter notebook
```
