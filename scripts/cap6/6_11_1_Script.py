# -*- coding: utf-8 -*-
# Capítulo 6: Integración, despliegue y proyecto final
# Sección 11: CI/CD y monitoreo
# Bloque 1: Introducción a GitHub y repositorios
# Objetivo: Generar la estructura base de un repositorio de datos y preparar archivos para versionar.

import os

def generar_estructura_repositorio():
    """
    Crear la estructura de directorios estándar para un proyecto de ingeniería de datos.
    Esto permite mantener el código organizado antes de inicializar Git.
    """
    directorios = [
        "mi_proyecto_datos/data/raw",
        "mi_proyecto_datos/data/processed",
        "mi_proyecto_datos/src",
        "mi_proyecto_datos/tests",
        "mi_proyecto_datos/notebooks"
    ]
    
    print("Iniciando la creacion de la estructura del repositorio...")
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
        print(f"Directorio creado: {directorio}")

def generar_archivo_gitignore():
    """
    Generar el archivo .gitignore.
    Demuestra el concepto de versionado de código vs datos (ST10),
    asegurando que los datos locales y credenciales no se suban al repositorio.
    """
    ruta_gitignore = "mi_proyecto_datos/.gitignore"
    contenido_gitignore = """# Ignorar entornos virtuales
venv/
env/
.env

# Ignorar datos (ST10: Versionamos codigo, no datos)
data/
*.csv
*.parquet
*.db

# Ignorar archivos compilados de Python
__pycache__/
*.pyc

# Ignorar configuraciones locales
.vscode/
.idea/
"""
    with open(ruta_gitignore, "w", encoding="utf-8") as f:
        f.write(contenido_gitignore)
    print(f"Archivo creado: {ruta_gitignore}")

def generar_script_pipeline():
    """
    Generar un script de pipeline básico dentro de la carpeta src/
    para tener código fuente que versionar en el primer commit (ST4, ST5).
    """
    ruta_script = "mi_proyecto_datos/src/pipeline.py"
    contenido_script = """# -*- coding: utf-8 -*-
# Script basico de pipeline para demostrar versionado

def extraer_datos():
    print("Extrayendo datos...")
    return []

def transformar_datos(datos):
    print("Transformando datos...")
    return datos

def cargar_datos(datos):
    print("Cargando datos en destino...")

if __name__ == '__main__':
    datos_crudos = extraer_datos()
    datos_limpios = transformar_datos(datos_crudos)
    cargar_datos(datos_limpios)
    print("Pipeline ejecutado correctamente.")
"""
    with open(ruta_script, "w", encoding="utf-8") as f:
        f.write(contenido_script)
    print(f"Archivo creado: {ruta_script}")

def generar_archivo_readme():
    """
    Generar un archivo README.md basico para documentar el repositorio.
    """
    ruta_readme = "mi_proyecto_datos/README.md"
    contenido_readme = """# Mi Proyecto de Datos

Repositorio para el pipeline de ingenieria de datos.

## Estructura
* `src/`: Contiene el codigo fuente del pipeline.
* `data/`: Directorio ignorado por Git, usado para almacenamiento local temporal.
* `tests/`: Pruebas unitarias.

## Ejecucion
Ejecutar el pipeline principal mediante:
`python src/pipeline.py`
"""
    with open(ruta_readme, "w", encoding="utf-8") as f:
        f.write(contenido_readme)
    print(f"Archivo creado: {ruta_readme}")

if __name__ == "__main__":
    generar_estructura_repositorio()
    generar_archivo_gitignore()
    generar_script_pipeline()
    generar_archivo_readme()
    print("Estructura de repositorio generada con exito. Proceder con las instrucciones de Git.")
```

```markdown
# Capítulo 6: Integración, despliegue y proyecto final
# Sección 11: CI/CD y monitoreo
# Bloque 1: Introducción a GitHub y repositorios

## Instrucciones de Git y GitHub para Windows

Este documento detalla los pasos para instalar Git, configurar el entorno local y realizar el flujo básico de versionado utilizando la consola (Command Prompt o PowerShell) en Windows.

### 1. Instalar Git en Windows
1. Descargar el instalador desde la pagina oficial: `https://git-scm.com/download/win`
2. Ejecutar el archivo `.exe` descargado.
3. Seguir el asistente de instalacion dejando las opciones por defecto (asegurarse de que la opcion "Git from the command line and also from 3rd-party software" este marcada).
4. Abrir la terminal (PowerShell o CMD) y verificar la instalacion ejecutando:
   ```cmd
   git --version
   ```

### 2. Configurar Git por primera vez
Configurar el nombre de usuario y correo electronico. Esta informacion se adjuntara a cada commit (ST4).
```cmd
git config --global user.name "Tu Nombre o Apellido"
git config --global user.email "tu_correo@ejemplo.com"
```

### 3. Inicializar el repositorio local (ST3)
Navegar a la carpeta del proyecto generada por el script de Python e inicializar Git.
```cmd
cd mi_proyecto_datos
git init
```
*Nota: Esto creara una carpeta oculta llamada `.git` que rastreara todos los cambios del directorio.*

### 4. Verificar el estado del repositorio
Revisar que archivos detecta Git y verificar que la carpeta `data/` sea ignorada gracias al archivo `.gitignore` (ST10).
```cmd
git status
```

### 5. Flujo basico: Add y Commit (ST4, ST5)
Agregar los archivos al "Staging Area" (area de preparacion) y crear un commit con un mensaje descriptivo.
```cmd
git add .
git commit -m "feat: configuracion inicial del repositorio y pipeline basico"
```
*Nota: Un buen mensaje de commit debe explicar que se hizo y por que. Usar prefijos como 'feat:' (nueva caracteristica), 'fix:' (correccion), o 'docs:' (documentacion) es una excelente practica.*

### 6. Manejo de ramas (ST7)
Crear una nueva rama para desarrollar una nueva caracteristica sin afectar la rama principal (generalmente `main` o `master`).
```cmd
git branch feature-limpieza-datos
git checkout feature-limpieza-datos
```
*Opcionalmente, hacer un cambio en `src/pipeline.py`, luego hacer `git add .` y `git commit -m "feat: agregar funcion de limpieza"` en esta nueva rama.*

### 7. Conectar con GitHub y hacer Push (ST5, ST8)
1. Ir a `https://github.com` e iniciar sesion.
2. Crear un nuevo repositorio vacio (sin README, ni .gitignore, para no generar conflictos).
3. Copiar la URL del repositorio (ej. `https://github.com/usuario/mi_proyecto_datos.git`).
4. Enlazar el repositorio local con el remoto en GitHub:
   ```cmd
   git remote add origin https://github.com/usuario/mi_proyecto_datos.git
   ```
5. Renombrar la rama principal a `main` (si por defecto se llamo `master`):
   ```cmd
   git branch -M main
   ```
6. Subir los cambios a GitHub:
   ```cmd
   git push -u origin main
   ```

### 8. Buenas practicas de versionado (ST9)
* Hacer commits pequenos y frecuentes.
* Nunca versionar credenciales o contrasenas.
* Mantener el archivo `.gitignore` actualizado.
* Versionar el codigo, orquestacion e infraestructura, pero NO los archivos de datos (CSV, Parquet, etc.).
