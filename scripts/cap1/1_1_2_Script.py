# ==============================================================================
# Capítulo 1: Fundamentos de Python aplicado a datos
# Sección 1: Python para procesamiento de datos
# Bloque 2: Variables, tipos y estructuras básicas
# ==============================================================================

# ------------------------------------------------------------------------------
# ST1 & ST2: Concepto de variable y Tipos de datos en Python
# Definir variables que representan un registro de transacción simple
# ------------------------------------------------------------------------------
id_transaccion = 1001          # int: Identificador numérico único
monto_transaccion = 250.50     # float: Valor monetario (decimal)
cliente = "Juan Pérez"         # str: Cadena de texto
es_valida = True               # bool: Estado lógico (Verdadero/Falso)

# Mostrar los tipos de datos asignados en memoria
print("--- Tipos de Datos Básicos ---")
print("Valor:", id_transaccion, "| Tipo:", type(id_transaccion))
print("Valor:", monto_transaccion, "| Tipo:", type(monto_transaccion))
print("Valor:", cliente, "| Tipo:", type(cliente))
print("Valor:", es_valida, "| Tipo:", type(es_valida))
print()

# ------------------------------------------------------------------------------
# ST3, ST4 & ST10: Impacto de los tipos, Conversión (casting) y Tipado dinámico
# Convertir tipos de datos y observar el comportamiento del tipado dinámico
# ------------------------------------------------------------------------------
print("--- Conversión de Tipos (Casting) y Tipado Dinámico ---")

# Un monto extraído de un archivo de texto generalmente es un string
monto_texto = "1500.75"
print("Monto original (str):", monto_texto, type(monto_texto))

# Convertir la cadena de texto a un número decimal para operaciones matemáticas
monto_numerico = float(monto_texto)
print("Monto convertido (float):", monto_numerico, type(monto_numerico))

# Demostrar tipado dinámico: una variable puede cambiar de tipo en tiempo de ejecución
variable_dinamica = 100
print("Variable dinámica original (int):", variable_dinamica)
variable_dinamica = "Ahora soy un texto"
print("Variable dinámica reasignada (str):", variable_dinamica)
print()

# ------------------------------------------------------------------------------
# ST5 & ST6: Listas y Diccionarios
# Estructurar colecciones de datos y representar registros complejos
# ------------------------------------------------------------------------------
print("--- Estructuras de Datos Básicas ---")

# Lista: Útil para almacenar una secuencia o colección (ej. una columna)
montos_lista = [250.50, 1500.75, 89.99, 450.00]
print("Lista de montos:", montos_lista)

# Diccionario: Útil para representar un registro completo (pares clave-valor)
transaccion_registro = {
    "id": 1001,
    "cliente": "Juan Pérez",
    "monto": 250.50,
    "estado": "Completado"
}
print("Registro (Diccionario):", transaccion_registro)
print("Acceder al monto del registro:", transaccion_registro["monto"])
print()

# ------------------------------------------------------------------------------
# ST7 & ST8: Iteración con loops (for) y Operaciones básicas
# Iterar sobre una lista de diccionarios para calcular métricas simples
# ------------------------------------------------------------------------------
print("--- Iteración y Operaciones Básicas ---")

dataset_transacciones = [
    {"id": 1001, "cliente": "Juan", "monto": 250.50},
    {"id": 1002, "cliente": "María", "monto": 150.00},
    {"id": 1003, "cliente": "Carlos", "monto": 300.00}
]

total_ventas = 0.0  # Variable acumuladora

# Iterar registro por registro
for registro in dataset_transacciones:
    # Concatenación de strings
    mensaje = "Procesando transacción del cliente: " + registro["cliente"]
    print(mensaje)
    
    # Operación de suma iterativa
    total_ventas = total_ventas + registro["monto"]

print(f"Total de ventas calculadas: {total_ventas}")
print()

# ------------------------------------------------------------------------------
# ST9 & ST11: Problemas comunes (tipos incorrectos, nulos) y Procesamiento manual
# Crear un mini-pipeline lógico iterando sobre datos defectuosos
# ------------------------------------------------------------------------------
print("--- Procesamiento Manual de Datos (Primer Acercamiento a Pipeline) ---")

# Dataset con problemas reales: nulos (None), tipos incorrectos (str en lugar de float), y datos corruptos
dataset_sucio = [
    {"id": 1001, "cliente": "Ana", "monto": 100.00},
    {"id": 1002, "cliente": "Luis", "monto": "200.50"},   # Tipo incorrecto (str)
    {"id": 1003, "cliente": "Pedro", "monto": None},      # Valor nulo
    {"id": 1004, "cliente": "Marta", "monto": "error"}    # Dato corrupto, imposible castear
]

datos_limpios = []
ventas_validas = 0.0

# Iterar sobre los datos sucios para aplicar reglas de limpieza (Transformación)
for registro in dataset_sucio:
    monto_actual = registro["monto"]
    
    # Regla 1: Validar y descartar valores nulos
    if monto_actual is None:
        print(f"-> Registro {registro['id']} omitido: Monto nulo.")
        continue  # Saltar al siguiente registro
    
    # Regla 2: Intentar normalizar tipos de datos (Casting)
    try:
        monto_limpio = float(monto_actual)
        
        # Construir el registro limpio
        registro_limpio = {
            "id": registro["id"],
            "cliente": registro["cliente"],
            "monto": monto_limpio
        }
        
        # Almacenar en la estructura final (Carga)
        datos_limpios.append(registro_limpio)
        ventas_validas += monto_limpio
        
    except ValueError:
        # Regla 3: Manejar errores de datos corruptos
        print(f"-> Registro {registro['id']} omitido: No se puede convertir '{monto_actual}' a numérico.")

print("\nResultados del procesamiento manual:")
print("Registros limpios procesados:")
for r in datos_limpios:
    print("  ", r)
print(f"Métrica final - Total de ventas válidas: {ventas_validas}")
