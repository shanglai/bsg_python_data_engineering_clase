# -*- coding: utf-8 -*-
"""
Capítulo 6: Integración, despliegue y proyecto final
Sección 12: Presentación de proyecto e IA aplicada
Bloque 2: Presentación de proyectos (parte 2)

Este script simula el proceso de consolidación de resultados, retroalimentación 
entre pares y evaluación crítica de los proyectos finales presentados por los alumnos.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def configurar_entorno():
    """
    Configurar los parámetros iniciales de visualización y la semilla aleatoria.
    """
    np.random.seed(987654)
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)

def generar_datos_evaluacion_pares():
    """
    Generar un dataset simulado de las evaluaciones realizadas entre pares.
    Incluye distintos enfoques de proyecto para permitir la comparación.
    """
    enfoques = ['Pipeline Batch', 'API REST', 'Dashboard Interactivo', 'Arquitectura Lambda']
    
    datos = {
        'ID_Proyecto': [f'PRJ-{str(i).zfill(3)}' for i in range(1, 21)],
        'Enfoque_Principal': np.random.choice(enfoques, 20),
        'Claridad_Problema': np.random.uniform(7.0, 10.0, 20),
        'Arquitectura_Datos': np.random.uniform(6.5, 10.0, 20),
        'Calidad_Codigo': np.random.uniform(6.0, 9.5, 20),
        'Funcionalidad': np.random.uniform(7.5, 10.0, 20),
        'Buenas_Practicas': np.random.uniform(6.5, 9.8, 20)
    }
    
    df_evaluaciones = pd.DataFrame(datos)
    
    # Calcular un puntaje global promedio por proyecto
    columnas_metricas = ['Claridad_Problema', 'Arquitectura_Datos', 'Calidad_Codigo', 'Funcionalidad', 'Buenas_Practicas']
    df_evaluaciones['Puntaje_Global'] = df_evaluaciones[columnas_metricas].mean(axis=1)
    
    return df_evaluaciones

def comparar_enfoques(df):
    """
    Agrupar los datos por enfoque para identificar patrones comunes y 
    comparar las fortalezas de cada arquitectura.
    """
    print(">> Comparacion de Enfoques entre Alumnos")
    print("-" * 50)
    
    resumen_enfoques = df.groupby('Enfoque_Principal').agg(
        Cantidad_Proyectos=('ID_Proyecto', 'count'),
        Promedio_Arquitectura=('Arquitectura_Datos', 'mean'),
        Promedio_Codigo=('Calidad_Codigo', 'mean'),
        Promedio_Global=('Puntaje_Global', 'mean')
    ).round(2).reset_index()
    
    print(resumen_enfoques.to_string(index=False))
    print("\n")
    return resumen_enfoques

def identificar_mejores_practicas(df):
    """
    Extraer los proyectos con los puntajes mas altos para discutir 
    mejores practicas y reflexionar sobre decisiones tecnicas.
    """
    print(">> Identificacion de Mejores Practicas (Top 3 Proyectos)")
    print("-" * 50)
    
    top_proyectos = df.sort_values(by='Puntaje_Global', ascending=False).head(3)
    
    for _, fila in top_proyectos.iterrows():
        print(f"Proyecto: {fila['ID_Proyecto']} | Enfoque: {fila['Enfoque_Principal']}")
        print(f"  - Puntaje Global: {fila['Puntaje_Global']:.2f}")
        print(f"  - Destacado en Arquitectura: {fila['Arquitectura_Datos']:.2f}")
        print(f"  - Destacado en Buenas Practicas: {fila['Buenas_Practicas']:.2f}\n")

def discutir_areas_mejora(df):
    """
    Identificar las areas con promedios mas bajos a nivel general para 
    fomentar el aprendizaje colaborativo y la discusion de mejoras posibles.
    """
    print(">> Evaluacion Critica y Disposicion de Mejoras")
    print("-" * 50)
    
    metricas = ['Claridad_Problema', 'Arquitectura_Datos', 'Calidad_Codigo', 'Funcionalidad', 'Buenas_Practicas']
    promedios_globales = df[metricas].mean()
    area_mas_baja = promedios_globales.idxmin()
    valor_mas_bajo = promedios_globales.min()
    
    print("Promedios por metrica a nivel grupo:")
    for metrica, valor in promedios_globales.items():
        print(f"  - {metrica}: {valor:.2f}")
        
    print(f"\nArea critica a reforzar: {area_mas_baja} ({valor_mas_bajo:.2f})")
    print("Reflexion: Es fundamental revisar los principios de modularidad y documentacion")
    print("para elevar el estandar en futuros desarrollos.\n")

def visualizar_patrones_comunes(df):
    """
    Generar visualizaciones para observar patrones en la evaluacion 
    y consolidar el conocimiento del grupo.
    """
    columnas_metricas = ['Claridad_Problema', 'Arquitectura_Datos', 'Calidad_Codigo', 'Funcionalidad', 'Buenas_Practicas']
    
    # Preparar datos para grafico de barras (Promedios por enfoque)
    df_melted = df.melt(id_vars=['Enfoque_Principal'], value_vars=columnas_metricas, 
                        var_name='Metrica', value_name='Puntaje')
    
    plt.figure(figsize=(12, 7))
    sns.barplot(data=df_melted, x='Metrica', y='Puntaje', hue='Enfoque_Principal', errorbar=None)
    
    plt.title('Consolidacion de Conocimiento: Desempeño por Metrica y Enfoque', fontsize=14)
    plt.xlabel('Criterios de Evaluacion', fontsize=12)
    plt.ylabel('Puntaje Promedio', fontsize=12)
    plt.xticks(rotation=15)
    plt.legend(title='Enfoque del Proyecto', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Guardar la figura generada
    plt.savefig('patrones_comunes_proyectos.png', dpi=300)
    print(">> Visualizacion generada y guardada como 'patrones_comunes_proyectos.png'\n")

def realizar_cierre_presentaciones():
    """
    Imprimir el mensaje final que consolida los aprendizajes y da cierre a la actividad.
    """
    print(">> Cierre de Presentaciones")
    print("-" * 50)
    print("Se han concluido las presentaciones de los proyectos finales.")
    print("La retroalimentacion entre pares ha permitido evidenciar multiples formas")
    print("de resolver problemas de ingenieria de datos.")
    print("Aprendizaje clave: La eleccion entre un pipeline puro, una API o un dashboard")
    print("depende estrictamente del caso de uso de negocio y los consumidores de los datos.")
    print("¡Felicidades a todos por el esfuerzo y el conocimiento consolidado!")

def main():
    """
    Funcion principal para ejecutar el flujo de consolidacion de proyectos.
    """
    configurar_entorno()
    
    # 1. Generar los datos de las presentaciones y retroalimentacion
    df_proyectos = generar_datos_evaluacion_pares()
    
    # 2. Comparar enfoques distintos implementados por los alumnos
    comparar_enfoques(df_proyectos)
    
    # 3. Identificar y discutir mejores practicas
    identificar_mejores_practicas(df_proyectos)
    
    # 4. Evaluacion critica y areas de mejora
    discutir_areas_mejora(df_proyectos)
    
    # 5. Observar patrones comunes mediante visualizacion
    visualizar_patrones_comunes(df_proyectos)
    
    # 6. Cierre
    realizar_cierre_presentaciones()

if __name__ == "__main__":
    main()
