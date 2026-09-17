# TFG: Metodología de Testing para Sistemas Conversacionales basados en LLMs en Contextos Educativos

**Autor:** Marcos Tomás Jiménez Meléndez  
**Fecha de inicio:** Agosto 2026  
**Fecha de entrega objetivo:** 20 de octubre de 2026  

---

## 🎯 Objetivo del Proyecto
Diseñar, formalizar y validar experimentalmente una metodología sistemática y reproducible de **testing de calidad, fiabilidad, seguridad y utilidad pedagógica** para chatbots y asistentes conversacionales basados en Modelos de Lenguaje de Gran Tamaño (LLMs) aplicados a entornos educativos.

---

## 📁 Estructura del Repositorio

```text
TFG/
├── docs/                                # Documentación de soporte y redacción de la memoria
│   ├── memoria/                         # Fuente de la memoria académica del TFG (LaTeX/Markdown)
│   │   ├── capitulos/                   # Capítulos individuales de la memoria
│   │   ├── bibliografia/                # Archivos de referencias bibliográficas (.bib)
│   │   └── figuras/                     # Gráficos, esquemas y diagramas
│   ├── documentacion_inicial/           # Informes y propuestas iniciales de definición
│   └── planificacion/                   # Cronogramas y seguimiento temporal de hitos
│
├── metodologia/                         # Definición formal de la propuesta metodológica
│   ├── dimensiones/                     # Dimensiones de calidad evaluadas (factualidad, pedagogía, etc.)
│   ├── rubricas/                        # Rúbricas de evaluación cualitativas y escalas
│   └── metricas/                        # Fórmulas y criterios de agregación cuantitativa
│
├── data/                                # Conjuntos de datos y trazas de ejecución
│   ├── prompts/                         # Batería de casos de prueba organizados por categorías
│   │   ├── 01_correccion_factual/       # Pruebas de exactitud de conceptos y materias
│   │   ├── 02_deteccion_alucinaciones/  # Pruebas con preguntas trampa, premisas falsas y no existentes
│   │   ├── 03_claridad_y_pedagogia/     # Pruebas de explicación didáctica, ejemplos y feedback
│   │   ├── 04_robustez_y_seguridad/     # Pruebas de jailbreaks, inyecciones de prompt y límites éticos
│   │   ├── 05_adaptacion_nivel/         # Pruebas de adecuación según nivel educativo (primaria, ESO, universidad)
│   │   └── 06_seguimiento_instrucciones/# Pruebas de restricciones de formato, longitud y rol
│   ├── configuraciones_chatbot/         # System prompts y parámetros de los modelos evaluados
│   ├── respuestas_obtenidas/            # Respuestas brutas generadas por los modelos
│   └── evaluaciones/                    # Calificaciones y resultados de las rúbricas
│
├── src/                                 # Código fuente y scripts de soporte
│   ├── evaluador/                       # Scripts para automatizar la ejecución de pruebas (Ollama/APIs)
│   ├── analisis/                        # Scripts de procesado de datos y cálculo de métricas
│   ├── visualizacion/                   # Generación automática de gráficas y figuras
│   └── utils/                           # Funciones auxiliares de carga y formateo
│
└── results/                             # Resultados consolidados listos para la memoria
    ├── tablas/                          # Tablas resumen en formato LaTeX / CSV / Markdown
    ├── graficos/                        # Gráficas generadas para el documento
    └── informes/                        # Reportes de síntesis de resultados
```

---

## 📅 Cronograma y Fases Clave

| Periodo | Fase | Entregable principal |
| :--- | :--- | :--- |
| **8–16 ago** | Fundamentos LLM y arquitecturas | Base técnica consolidada |
| **17–23 ago** | Entorno experimental (Ollama/Open WebUI) | Chatbot local configurado |
| **24–31 ago** | Fundamentos de testing y contexto educativo | Marco teórico inicial |
| **1–7 sep** | Estado del arte y alcance definitivo | Índice y objetivos cerrados |
| **8–14 sep** | Diseño de la metodología | Dimensiones, métricas y rúbricas |
| **15–21 sep** | Batería de pruebas | Banco de casos de prueba completado |
| **22–28 sep** | Ejecución experimental | Recogida de respuestas de los LLMs |
| **29 sep–5 oct** | Análisis de resultados y marco teórico | Procesamiento de datos y gráficos |
| **6–12 oct** | Redacción integral | **Primer borrador completo** |
| **13–16 oct** | Revisión sustantiva | Ajustes y revisión con tutor |
| **17–20 oct** | Revisión final y entrega | **Documento final compilado** |
