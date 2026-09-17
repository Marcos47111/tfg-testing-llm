# TFG: Metodología para testing de IA Generativa de texto

**Autor:** Marcos Tomás Jiménez Meléndez  
**Tutor:** Xavier Alamán Roldán  
**Titulación:** Grado en Ingeniería Informática  
**Centro:** Escuela Politécnica Superior -- Universidad Autónoma de Madrid  
**Fecha de entrega objetivo:** 20 de octubre de 2026  

---

## 🎯 Objetivo del Proyecto
Diseñar, formalizar y validar experimentalmente una metodología sistemática y reproducible de **testing de calidad, fiabilidad, seguridad y utilidad pedagógica** para chatbots y asistentes conversacionales basados en Modelos de Lenguaje de Gran Tamaño (LLMs) aplicados a entornos educativos.

El marco se fundamenta en los atributos de calidad de la norma **ISO/IEC 25010:2023**, la teoría de la **Zona de Desarrollo Próximo y Andamiaje** de Vygotsky, y los modelos de feedback formativo de Hattie & Timperley.

---

## 🚀 Guía Rápida de Uso

### 1. Compilación de la Memoria (PDF)
Para compilar la memoria completa en formato LaTeX (plantilla oficial UAM/EPS) con resolución de bibliografía e índices:
```bash
./compilar_memoria.sh
```
El documento generado se ubica en `docs/memoria/main.pdf` (48 páginas).

### 2. Ejecución de Tests Unitarios
Para validar la suite completa de pruebas unitarias de métricas, acuerdos $\kappa$ psicométricos y utilidades:
```bash
python3 -m unittest discover -s src/analisis -p "test_*.py" && python3 -m unittest discover -s src/utils -p "test_*.py"
```

### 3. Ejecución Experimental de Pruebas Conversacionales
```bash
# Modo simulado calibrado (offline reproducible):
python3 src/evaluador/ejecutor_pruebas.py --mode simulado

# Modo inferencia en tiempo real con servidor local de Ollama:
python3 src/evaluador/ejecutor_pruebas.py --mode ollama --model llama3:8b --endpoint http://localhost:11434/api/chat
```

---

## 📁 Estructura del Repositorio

```text
TFG/
├── .gitignore                              # Exclusiones de Git (temporales LaTeX, Python)
├── README.md                               # Documentación principal del repositorio
├── compilar_memoria.sh                     # Script para compilar la memoria en PDF
│
├── docs/                                   # Documentación académica
│   ├── documentacion_inicial/              # Informes previos, objetivos e índices provisionales
│   ├── planificacion/                      # Cronogramas temporales
│   └── memoria/                            # Memoria en LaTeX (Plantilla UAM / EPS)
│       ├── main.tex                        # Documento principal
│       ├── main.pdf                        # Documento final compilado (48 págs.)
│       ├── compilar_pdf.sh                 # Script de compilación interna
│       ├── tfgtfmthesisuam.cls             # Clase oficial UAM
│       ├── referencias.bib                 # Bibliografía en formato BibTeX
│       ├── inicio/                         # Resumen, abstract, agradecimientos, prefacio
│       ├── capitulos/                      # Capítulos del 01 al 08 (Anexos)
│       ├── figuras/                        # Gráficos vectoriales en PDF/PNG
│       └── img/                            # Logos institucionales EPS-UAM y figuras
│
├── metodologia/                            # Formalización teórica del testing
│   ├── justificacion_y_fundamentos.md      # Justificación científica y pedagógica
│   ├── dimensiones/                        # Fichas descriptivas de D1 a D7
│   ├── rubricas/                           # Rúbrica general y guía del evaluador
│   └── metricas/                           # Definición de fórmulas matemáticas (IQE, CFR, HR, κ)
│
├── data/                                   # Conjuntos de datos y trazas de ejecución
│   ├── prompts/                            # 42 casos de prueba organizados por dimensión
│   ├── configuraciones_chatbot/            # System prompts y parámetros de los perfiles
│   ├── respuestas_obtenidas/raw/           # 126 respuestas generadas en formato JSON
│   └── evaluaciones/                       # Calificaciones con la rúbrica multidimensional
│
├── src/                                    # Código fuente y herramientas
│   ├── evaluador/                          # Ejecutor de pruebas (simulado y Ollama live)
│   ├── analisis/                           # Módulos de métricas y tests unitarios
│   ├── utils/                              # Carga de datos y exportación
│   └── visualizacion/                      # Generación de gráficos vectoriales
│
└── results/                                # Resultados consolidados para la memoria
    ├── tablas/                             # Tablas comparativas en CSV, Markdown y LaTeX
    ├── graficos/                           # Gráficos de radar y barras
    └── informes/                           # Resumen comparativo global JSON
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
