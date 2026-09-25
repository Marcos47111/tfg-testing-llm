# TFG: Metodología para testing de IA Generativa de texto en educación

**Autor:** Marcos Tomás Jiménez Meléndez  
**Tutor:** Xavier Alamán Roldán  
**Titulación:** Grado en Ingeniería Informática  
**Centro:** Escuela Politécnica Superior -- Universidad Autónoma de Madrid  
**Fecha de entrega:** Octubre de 2026  
**Licencia:** MIT (Código abierto)  
**Versión experimental de referencia:** `v1.0.12-tfg`

---

## 🎯 Objetivo del Proyecto
Diseñar, formalizar y evaluar una metodología sistemática y reproducible de **testing de calidad, fiabilidad, seguridad y utilidad pedagógica** para chatbots y asistentes conversacionales basados en Modelos de Lenguaje de Gran Tamaño (LLMs) aplicados a entornos educativos.

El marco se fundamenta en los atributos de calidad de producto de la norma **ISO/IEC 25010:2023**, la teoría de la **Zona de Desarrollo Próximo y Andamiaje** de Vygotsky, Wood, Bruner & Ross, y los modelos de retroalimentación formativa de Hattie & Timperley.

---

## 🚀 Guía Rápida de Uso y Reproducibilidad

### 1. Entorno Python e Instalación de Dependencias
Se recomienda utilizar Python 3.10 o superior:
```bash
pip install -r requirements.txt
```

### 2. Compilación de la Memoria (PDF)
Para compilar la memoria completa en formato LaTeX (plantilla oficial UAM/EPS) con resolución de bibliografía cruzada (`BibTeX` + `pdflatex`):
```bash
./compilar_memoria.sh
```
El documento generado se ubica en `docs/memoria/main.pdf` (68 páginas).

### 3. Ejecución de Tests Unitarios
Para validar la suite completa de pruebas unitarias de métricas dimensionales, agregación $IQE$, detección de fallos críticos, consistencia inter-evaluador ($\kappa$) y validación del LLM Judge:
```bash
python3 -m unittest discover -s src/analisis -p "test_*.py" && python3 -m unittest discover -s src/utils -p "test_*.py"
```

### 4. Pipeline de Ingestión, Validación, Análisis y Concordancia Humana
```bash
# 1. (Opcional) Importar y normalizar anotaciones humanas originales (raw CSV -> JSON):
python3 src/analisis/importar_evaluaciones_humanas.py

# 2. Validar integridad y esquemas de los datasets de evaluación (Evaluador 1 y 2):
python3 src/analisis/validar_datos_evaluacion.py

# 3. Ejecutar análisis comparativo global de los 3 perfiles de chatbot:
python3 src/analisis/analizador_experimentos.py

# 4. Calcular la concordancia inter-evaluador independiente (Kappa de Cohen global y dimensional):
python3 src/analisis/calcular_concordancia_evaluadores.py

# 5. Generar gráficos vectoriales de resultados (radar y barras):
python3 src/visualizacion/generar_graficos.py
```

### 5. Extensión Experimental: Evaluación Automática (LLM-as-a-Judge)
```bash
# 1. Ejecutar el evaluador automático a ciegas (modo calibrado offline o vía API Ollama/OpenAI):
python3 src/evaluador/evaluador_llm_judge.py --mode calibrado

# 2. Validar integridad de los datasets incluyendo el juez automático:
python3 src/analisis/validar_datos_evaluacion.py --incluir-judge

# 3. Ejecutar análisis estadístico de concordancia Humano-IA (Kappa, MAE, Deltas, Fallos Críticos):
python3 src/analisis/analizar_concordancia_llm_judge.py

# 4. Generar gráficos vectoriales específicos del juez automático:
python3 src/visualizacion/generar_graficos_llm_judge.py
```

### 6. Ejecución del Motor de Testing Conversacional (Ollama)
```bash
# Ejecución en tiempo real con servidor Ollama local o remoto:
python3 src/evaluador/ejecutor_pruebas.py --mode ollama --model llama3:8b --endpoint http://localhost:11434/api/chat
```

---

## 📁 Estructura del Repositorio

```text
TFG/
├── LICENSE                                 # Licencia de código abierto MIT
├── README.md                               # Documentación principal del repositorio
├── compilar_memoria.sh                     # Script para compilar la memoria en PDF
│
├── docs/                                   # Documentación académica
│   └── memoria/                            # Memoria en LaTeX (Plantilla oficial UAM / EPS)
│       ├── main.tex                        # Documento principal
│       ├── main.pdf                        # Documento final compilado (68 págs.)
│       ├── tfgtfmthesisuam.cls             # Clase oficial UAM (EPS)
│       ├── referencias.bib                 # Bibliografía en formato BibTeX
│       ├── inicio/                         # Resumen, abstract, agradecimientos, prefacio
│       ├── capitulos/                      # Capítulos del 01 al 08 (Anexos)
│       └── img/                            # Figuras vectoriales y logos institucionales
│
├── metodologia/                            # Formalización teórica del testing
│   ├── justificacion_y_fundamentos.md      # Justificación científica y pedagógica
│   ├── dimensiones/                        # Fichas descriptivas de D1 a D7
│   ├── rubricas/                           # Rúbrica general y guía del evaluador
│   └── metricas/                           # Definición de fórmulas matemáticas (IQE, CFR, HR, κ)
│
├── data/                                   # Conjuntos de datos experimentales
│   ├── prompts/                            # 42 casos de prueba organizados por dimensión y tipo
│   ├── configuraciones_chatbot/            # System prompts y parámetros de inferencia de los perfiles
│   ├── respuestas_obtenidas/raw/           # 126 trazas de respuesta conversacional completas
│   └── evaluaciones/                       # Datasets de evaluación normalizados y anotaciones raw
│       ├── raw/                            # Hojas originales de anotación de Evaluador 1 y 2 (CSV)
│       ├── llm_judge/                      # Extensión experimental LLM-as-a-Judge
│       │   ├── raw/                        # Trazas de inferencia raw del juez automático (JSON)
│       │   └── ...                         # Datasets normalizados del juez pareados (JSON)
│       └── ...                             # Evaluaciones estructuradas pareadas en JSON (E1 y E2)
│
├── src/                                    # Código fuente y herramientas en Python
│   ├── evaluador/                          # Motores de ejecución de pruebas y LLM-as-a-Judge
│   │   ├── ejecutor_pruebas.py             # Ejecutor experimental con Ollama
│   │   └── evaluador_llm_judge.py          # Motor de evaluación automática a ciegas (LLM Judge)
│   ├── analisis/                           # Módulos de cálculo métrico, agregación, Kappa y validación
│   │   ├── metricas_tfg.py                 # Fórmulas de IQE, CFR, HR y Cohen's Kappa
│   │   ├── analizador_experimentos.py      # Agregación global comparativa
│   │   ├── calcular_concordancia_evaluadores.py # Concordancia humana E1 vs E2 (κ = 0.982)
│   │   ├── analizar_concordancia_llm_judge.py  # Concordancia Humano-IA (Judge vs E1/E2)
│   │   └── validar_datos_evaluacion.py     # Validador exhaustivo de integridad y esquemas
│   ├── utils/                              # Loader de casos y exportadores de tablas
│   └── visualizacion/                      # Generadores de gráficos vectoriales (radar, barras, matrices)
│       ├── generar_graficos.py             # Gráficos del experimento principal
│       └── generar_graficos_llm_judge.py   # Gráficos de concordancia y matrices de confusión del juez
│
└── results/                                # Resultados consolidados para la memoria
    ├── tablas/                             # Tablas comparativas en CSV, Markdown y LaTeX
    ├── graficos/                           # Gráficos vectoriales en PDF y PNG
    └── informes/                           # Informes comparativos y de concordancia en JSON
```

---

## 📊 Resumen de Resultados Experimentales

### 1. Evaluación Principal (Evaluadores Humanos de Referencia $E_1$ y $E_2$)
Evaluación sistemática de 42 casos de prueba sobre el modelo **Meta-Llama-3-8B-Instruct** (`Q4_0`, `num_ctx=2048`, `seed=42`, $N_\kappa=882$, $\kappa_{\text{humano}} = 0{,}982$):

| Perfil de Chatbot | IQE (0--100) | CFR (%) | HR (%) | D1 (Factual) | D2 (Aluc.) | D3 (Claridad) | D4 (Feedback) | D5 (Seguridad) | D6 (Nivel) | D7 (Directriz) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Asistente Base** | **84.13** | 11.90% | 33.33% | 2.55 | 2.86 | 2.83 | 1.86 | 2.76 | 2.00 | 2.71 |
| **Tutor Directo** | **87.94** | 14.29% | 33.33% | 2.52 | 2.86 | 2.88 | 1.93 | 2.76 | 3.00 | 2.76 |
| **Tutor Socrático** | **92.98** | 11.90% | 16.67% | 2.48 | 2.88 | 2.93 | 2.81 | 2.93 | 3.00 | 2.81 |

* **Concordancia Inter-Evaluador Humana (Doble evaluación independiente):** $\kappa = 0{,}982$ ($P_o = 0{,}9932, P_e = 0{,}6260$).

### 2. Extensión Exploratoria LLM-as-a-Judge (Qwen2.5-14B-Instruct vs Humanos)
Evaluación a ciegas sobre las 126 respuestas ($N_\kappa=882$ juicios pareados, $T=0.0$):

- **Kappa Global Juez vs $E_1$:** $\kappa = 0{,}829$ (Acuerdo casi perfecto / Excelente), $\text{MAE} = 0{,}088$ puntos.
- **Kappa Global Juez vs $E_2$:** $\kappa = 0{,}849$.
- **Acuerdo Exacto ($|\Delta|=0$):** $94{,}1\,\%$ (830 / 882 pares).
- **Sensibilidad Safety-First:** $97{,}62\,\%$ coincidencia en fallos críticos ($0$ falsos negativos en Alucinaciones y Seguridad).
- **Nota sobre metadatos de inferencia:** Los campos `latencia_segundos` registrados en los ficheros JSON de `data/respuestas_obtenidas/raw/` se conservan únicamente a título de metadato operacional de contexto de la ejecución y no forman parte del cálculo de métricas de calidad ($IQE$, $CFR$, $HR$) ni constituyen un benchmark de rendimiento computacional del modelo.
