# =============================================================================
# Capítulo 5: Automatización y orquestación
# Sección 10: Orquestación e infraestructura
# Bloque 3: Infraestructura como código (Terraform demo)
# =============================================================================

"""
Subtemas cubiertos en este script:
ST1: Introducción a Infraestructura como Código (IaC)
ST2: Problema de provisión manual de infraestructura
ST3: Concepto declarativo vs imperativo
ST4: Introducción a Terraform
ST5: Estructura básica de archivos Terraform
ST6: Conceptos de provider y resource
ST7: Flujo init >> plan >> apply
ST8: Ejemplo básico (bucket en cloud) (demo)
ST9: Reproducibilidad de infraestructura
ST10: Integración con pipelines
ST11: IaC como práctica moderna en ingeniería

Este script en Python actúa como un generador para nuestra configuración 
de infraestructura. En un entorno real, los archivos de Terraform (.tf) 
se escriben directamente, pero usaremos Python para crear el archivo 
de demostración y detallar las instrucciones de ejecución.
"""

import os

def generar_archivo_terraform():
    """
    Generar el archivo main.tf para la demostración de Infraestructura como Código (IaC).
    Este archivo define un proveedor y un recurso (bucket de almacenamiento)
    utilizando un enfoque declarativo (decimos "qué" queremos, no "cómo" crearlo).
    """
    
    # ST5, ST6: Estructura básica, provider y resource
    # ST8: Ejemplo básico de bucket en cloud
    contenido_tf = """# ==========================================
# Archivo: main.tf
# Descripción: Demostración de IaC
# ==========================================

# 1. Definición del proveedor (Provider)
# Indica a Terraform con qué API debe comunicarse (ej. AWS, GCP, Azure).
provider "aws" {
  region                      = "us-east-1"
  
  # Credenciales simuladas para evitar cobros en la demo
  # En un entorno real, usaríamos variables de entorno o roles IAM.
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true
}

# 2. Definición del recurso (Resource)
# ST3: Declaramos que queremos que exista un bucket S3.
# Terraform se encarga de determinar si debe crearlo, actualizarlo o dejarlo igual.
resource "aws_s3_bucket" "bucket_datos_pipeline" {
  # Usamos la semilla 987654 para asegurar un nombre único
  bucket = "mi-bucket-de-datos-pipeline-987654"

  tags = {
    Environment = "Dev"
    Course      = "Data Engineering"
    Purpose     = "Almacenamiento de datos crudos y procesados"
  }
}
"""
    
    archivo_tf = "main.tf"
    with open(archivo_tf, "w", encoding="utf-8") as f:
        f.write(contenido_tf)
    
    print(f"[*] Archivo '{archivo_tf}' generado exitosamente.")
    print("[*] Este archivo representa nuestra infraestructura de forma declarativa (ST3).")
    print("[*] Al usar código, evitamos el aprovisionamiento manual y errores humanos (ST1, ST2, ST9).\n")

def hacer_instrucciones_windows():
    """
    Hacer un resumen de los comandos necesarios para instalar y ejecutar 
    Terraform en un entorno de Windows.
    Cubriendo el ST7: Flujo init >> plan >> apply.
    """
    instrucciones = """
====================================================================
INSTRUCCIONES PARA EJECUTAR TERRAFORM EN WINDOWS (ST4)
====================================================================

PREPARACION:
1. Descargar Terraform para Windows desde: https://developer.hashicorp.com/terraform/downloads
2. Descomprimir el archivo .zip.
3. Copiar el archivo 'terraform.exe' a un directorio seguro (ej. C:\\Terraform).
4. Agregar esa ruta a las Variables de Entorno del sistema (PATH).
5. Abrir la terminal (CMD o PowerShell) en el mismo directorio donde 
   se generó el archivo 'main.tf'.

FLUJO DE TRABAJO IAC (ST7):
Paso 1: Inicializar el entorno
Comando: >> terraform init
Detalle: Descarga los plugins del proveedor (en este caso, AWS).

Paso 2: Planificar los cambios
Comando: >> terraform plan
Detalle: Muestra qué recursos se van a crear, modificar o eliminar.
Es un paso de validación crucial.

Paso 3: Aplicar los cambios
Comando: >> terraform apply
Detalle: Ejecuta la creación en la nube. Terraform pedirá confirmación, 
se debe escribir 'yes'.

Paso 4: Limpieza (Opcional)
Comando: >> terraform destroy
Detalle: Elimina toda la infraestructura definida en el archivo para no 
incurrir en costos.

INTEGRACION (ST10, ST11):
Este archivo 'main.tf' se versiona junto con nuestro código de Python (ETL).
Así, nuestro pipeline siempre tendrá la infraestructura exacta que necesita
para correr, logrando una práctica moderna de ingeniería de datos.
====================================================================
"""
    print(instrucciones)

def main():
    """
    Función principal que orquesta la generación de los recursos de la lección.
    """
    print("Iniciando demostración de Infraestructura como Código (IaC)...")
    
    # 1. Generar la configuración de infraestructura
    generar_archivo_terraform()
    
    # 2. Hacer y mostrar las instrucciones para correr la demo en Windows
    hacer_instrucciones_windows()

if __name__ == "__main__":
    # Fijamos la semilla de forma conceptual para consistencia
    random_seed = 987654
    main()
