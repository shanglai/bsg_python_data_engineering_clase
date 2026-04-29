# -*- coding: utf-8 -*-

"""
Capítulo 6: Integración, despliegue y proyecto final
Sección 12: Presentación de proyecto e IA aplicada
Bloque 1: Presentación de proyectos (parte 1)

Este script simula la estructura de evaluación y la demostración funcional 
(demo) de los proyectos finales presentados por los alumnos.
"""

import random
import time
from typing import Dict, List

# Fjar semilla aleatoria para consistencia en la generación de puntajes
random.seed(987654)

class ProyectoFinal:
    """
    Clase que representa la estructura de un proyecto final de Data Engineering.
    Cubre la definición del problema, solución, arquitectura y flujo de datos.
    """
    def __init__(self, alumno: str, problema: str, solucion: str, arquitectura: List[str]):
        # ST1: Presentación de proyectos (estructura)
        self.alumno = alumno
        # ST2: Definición del problema
        self.problema = problema
        # ST3: Explicación de la solución
        self.solucion = solucion
        # ST4: Arquitectura del sistema
        self.arquitectura = arquitectura

    def ejecutar_demo_funcional(self) -> bool:
        """
        ST6: Demo funcional
        ST5: Flujo de datos
        Simula la ejecución end-to-end del pipeline del alumno.
        """
        print(f"\n[{self.alumno}] Iniciando Demo Funcional...")
        print(f"Problema abordado: {self.problema}")
        print(f"Solución propuesta: {self.solucion}")
        print("Arquitectura implementada:", " >> ".join(self.arquitectura))
        
        pasos_exitosos = 0
        for paso in self.arquitectura:
            print(f"  Ejecutando: {paso}...")
            time.sleep(0.5) # Simular tiempo de procesamiento
            
            # Simular una probabilidad de éxito del 90% por paso
            if random.random() < 0.90:
                print(f"  [OK] {paso} completado.")
                pasos_exitosos += 1
            else:
                print(f"  [ERROR] Fallo en el paso: {paso}.")
                break
                
        exito_total = pasos_exitosos == len(self.arquitectura)
        if exito_total:
            print(f"[{self.alumno}] Flujo de datos ejecutado correctamente.")
        else:
            print(f"[{self.alumno}] La demo funcional presentó errores.")
            
        return exito_total


class EvaluadorProyectos:
    """
    Clase para evaluar los proyectos presentados utilizando criterios predefinidos.
    """
    def __init__(self):
        # ST9: Evaluación por criterios
        self.criterios = [
            "Claridad del problema y solución",
            "Funcionalidad de la arquitectura",
            "Conexión entre componentes",
            "Justificación técnica",
            "Comunicación efectiva"
        ]

    def evaluar_proyecto(self, proyecto: ProyectoFinal, exito_demo: bool) -> Dict[str, any]:
        """
        Generar la evaluación de un proyecto.
        """
        print(f"\nGenerando evaluación para: {proyecto.alumno}")
        puntajes = {}
        
        # Evaluar cada criterio (escala 1 a 10)
        for criterio in self.criterios:
            base = 7 if exito_demo else 4
            puntaje = random.randint(base, 10)
            puntajes[criterio] = puntaje
            
        promedio = sum(puntajes.values()) / len(puntajes)
        
        # ST7: Justificación de decisiones técnicas
        # ST8: Comunicación efectiva
        print("Detalle de la evaluación:")
        for crit, punt in puntajes.items():
            print(f" - {crit}: {punt}/10")
            
        # ST10: Identificación de fortalezas
        # ST11: Aprendizajes obtenidos
        fortaleza = self._identificar_fortaleza(puntajes)
        print(f"Fortaleza principal identificada: {fortaleza}")
        print(f"Aprendizaje clave evidenciado: Capacidad para integrar {proyecto.arquitectura[0]} con {proyecto.arquitectura[-1]}")
        print(f"Puntaje Final: {promedio:.2f}/10\n" + "-"*40)
        
        return puntajes

    def _identificar_fortaleza(self, puntajes: Dict[str, int]) -> str:
        """Determinar la fortaleza principal basada en la puntuación más alta."""
        mejor_criterio = max(puntajes, key=puntajes.get)
        return mejor_criterio


def ejecutar_bloque_presentaciones():
    """
    Función principal para orquestar la presentación de proyectos (Parte 1).
    """
    # Generar proyectos de prueba
    proyectos = [
        ProyectoFinal(
            alumno="Alumno A",
            problema="Datos de transacciones inconsistentes y reportes manuales lentos.",
            solucion="Pipeline batch automatizado que limpia datos y expone métricas.",
            arquitectura=["Extracción CSV", "Limpieza con Pandas", "Carga en MySQL", "Visualización Streamlit"]
        ),
        ProyectoFinal(
            alumno="Alumno B",
            problema="Sistemas de terceros necesitan acceder a los datos procesados en tiempo real.",
            solucion="API REST para consumo de datos de transacciones normalizadas.",
            arquitectura=["Consumo API externa", "Transformación Python", "Almacenamiento GCS", "Exposición FastAPI"]
        )
    ]
    
    evaluador = EvaluadorProyectos()
    
    print("=== INICIO DE PRESENTACIONES DE PROYECTOS FINALES (PARTE 1) ===")
    
    for proyecto in proyectos:
        # Ejecutar ST6: Demo funcional
        exito = proyecto.ejecutar_demo_funcional()
        
        # Ejecutar ST9: Evaluación
        evaluador.evaluar_proyecto(proyecto, exito)

if __name__ == "__main__":
    ejecutar_bloque_presentaciones()
