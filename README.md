# TFG: Metodología para testing de IA Generativa de texto en educación

**Autor:** Marcos Tomás Jiménez Meléndez  
**Tutor:** Xavier Alamán Roldán  
**Titulación:** Grado en Ingeniería Informática  
**Centro:** Escuela Politécnica Superior -- Universidad Autónoma de Madrid  
**Fecha de entrega:** Octubre de 2026  
**Licencia:** MIT (Código abierto)  
**Versión experimental de referencia:** `v1.3.1-tfg`

---

## Objetivo del Proyecto
Diseñar, formalizar y evaluar una metodología sistemática y reproducible de **testing de calidad, fiabilidad, seguridad y utilidad pedagógica** para chatbots y asistentes conversacionales basados en Modelos de Lenguaje de Gran Tamaño (LLMs) aplicados a entornos educativos.

El marco se fundamenta en los atributos de calidad de producto de la norma **ISO/IEC 25010:2023**, la teoría de la **Zona de Desarrollo Próximo y Andamiaje** de Vygotsky, Wood, Bruner & Ross, y los modelos de retroalimentación formativa de Hattie & Timperley.

---

## Guía Rápida de Uso y Reproducibilidad

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
El documento generado se ubica en `docs/memoria/main.pdf` (70 páginas).

### 3. Ejecución de Tests Unitarios
Para validar la suite completa de pruebas unitarias de métricas dimensionales, agregación $IQE$, detección de fallos críticos, consistencia inter-evaluador ($\kappa$) y validación del LLM Judge:
```bash
python3 -m unittest discover -s src/analisis -p "test_*.py" && python3 -m unittest discover -s src/utils -p "test_*.py"
```

### 4. Pipeline de Ingestión, Validación, Análisis y Concordancia Humana
```bash
# 1. Importar y normalizar anotaciones humanas y consolidar Gold Standard adjudicado (raw CSV -> JSON):
python3 src/analisis/importar_evaluaciones_humanas.py

# 2. Validar integridad y esquemas de los datasets de evaluación (Gold Standard, E1 y E2):
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
# 1. Ejecutar el evaluador automático a ciegas (vía Ollama con Qwen2.5-14B-Instruct o endpoint compatible):
python3 src/evaluador/evaluador_llm_judge.py --mode ollama --model qwen2.5:14b-instruct --temperature 0

# (Opcional: modo mock para desarrollo local sin GPU / CI, aislado en results/demo_simulada/):
python3 src/evaluador/evaluador_llm_judge.py --mode mock

# 2. Validar integridad de los datasets incluyendo el juez automático:
python3 src/analisis/validar_datos_evaluacion.py --incluir-judge

# 3. Ejecutar análisis estadístico de concordancia Humano-IA (Kappa, MAE, Deltas, Fallos Críticos vs Gold Standard):
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

## Estructura del Repositorio

```text
TFG/
├── LICENSE                                 # Licencia de código abierto MIT
├── README.md                               # Documentación principal del repositorio
├── compilar_memoria.sh                     # Script para compilar la memoria en PDF (estricto)
│
├── docs/                                   # Documentación académica
│   └── memoria/                            # Memoria en LaTeX (Plantilla oficial UAM / EPS)
│       ├── main.tex                        # Documento principal
│       ├── main.pdf                        # Documento final compilado (70 págs.)
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
│       ├── raw_independientes/             # Anotaciones independientes Fase 1 (reconstruidas con SHA de commit)
│       ├── raw/                            # Hojas de anotaciones consolidadas Fase 2 (CSV)
│       ├── adjudicaciones_gold_standard.csv # Registro formal de adjudicación de discrepancias del Gold Standard
│       ├── evaluacion_gold_standard.json   # Dataset canónico Gold Standard unificado (126 registros)
│       ├── llm_judge/                      # Extensión experimental LLM-as-a-Judge
│       │   ├── raw/                        # Trazas de inferencia raw del juez automático (JSON)
│       │   └── ...                         # Datasets normalizados del juez pareados (JSON)
│       └── ...                             # Evaluaciones estructuradas pareadas en JSON (E1, E2 y particiones)
│
├── src/                                    # Código fuente y herramientas en Python
│   ├── evaluador/                          # Motores de ejecución de pruebas y LLM-as-a-Judge
│   │   ├── ejecutor_pruebas.py             # Ejecutor experimental con Ollama
│   │   └── evaluador_llm_judge.py          # Motor de evaluación automática a ciegas (LLM Judge)
│   ├── analisis/                           # Módulos de cálculo métrico, agregación, Kappa y validación
│   │   ├── metricas_tfg.py                 # Fórmulas de IQE, CFR, HR y Cohen's Kappa
│   │   ├── analizador_experimentos.py      # Agregación global comparativa
│   │   ├── calcular_concordancia_evaluadores.py # Concordancia humana E1 vs E2 (Fase 1: κ = 0.974, κ_w = 0.981)
│   │   ├── analizar_concordancia_llm_judge.py  # Concordancia Humano-IA (Judge vs Gold Standard y E1/E2)
│   │   └── validar_datos_evaluacion.py     # Validador exhaustivo de integridad y esquemas (5 fases)
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

## Resumen de Resultados Experimentales

### 1. Evaluación Principal (Evaluadores Humanos y Gold Standard Canónico)
Evaluación sistemática de 42 casos de prueba sobre el modelo **Meta-Llama-3-8B-Instruct** (`Q4_0`, `num_ctx=2048`, `seed=42`, $N_\kappa=882$, $\kappa_{\text{humano}} = 0{,}974$):

| Perfil de Chatbot | IQE (0--100) | CFR (%) | HR (%) | D1 (Factual) | D2 (Aluc.) | D3 (Claridad) | D4 (Feedback) | D5 (Seguridad) | D6 (Nivel) | D7 (Directriz) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Asistente Base** | **83.49** | 14.29% | 33.33% | 2.43 | 2.86 | 2.83 | 1.88 | 2.76 | 2.07 | 2.71 |
| **Tutor Directo** | **87.30** | 14.29% | 33.33% | 2.48 | 2.86 | 2.88 | 1.93 | 2.76 | 2.93 | 2.76 |
| **Tutor Socrático** | **92.62** | 11.90% | 16.67% | 2.45 | 2.88 | 2.93 | 2.81 | 2.93 | 2.95 | 2.81 |

* **Protocolo de Evaluación Humana en Dos Fases:**
  * **Fase 1 (Doble evaluación independiente y a ciegas):** $\kappa_{\text{no-ponderado}} = 0{,}9742$, $\kappa_{\text{lineal}} = 0{,}9807$, $\kappa_{\text{cuadrático}} = 0{,}9884$ ($P_o = 99{,}55\%$, 878 / 882 coincidencias exactas, 4 discrepancias menores de un nivel, 0 severas).
  * **Fase 2 (Revisión, calibración y consolidación del Gold Standard):** Consolidación del conjunto canónico de referencia en `data/evaluaciones/evaluacion_gold_standard.json` tras la auditoría técnica y adjudicación explícita registrada en `adjudicaciones_gold_standard.csv`.
* **Análisis de Sensibilidad (Efecto Techo):** En Seguridad ($D_5$), la media transversal del Asistente Base es $2{,}76$ frente a $1{,}33$ en su subbatería primaria de tensión ($\Delta = +1{,}43$). En Feedback ($D_4$), el Tutor Socrático alcanza $2{,}81$ transversal frente a $1{,}67$ en casos de fallo discente ($\Delta = +1{,}14$).

### 2. Extensión Exploratoria LLM-as-a-Judge (Resultados Experimentales con Qwen2.5-14B-Instruct)
Evaluación automática a ciegas sobre las 126 respuestas reales ($N_\kappa=882$ juicios pareados, $T=0.0$, $\text{seed}=42$):

* **Modelo evaluador:** Qwen2.5-14B-Instruct (`qwen2.5:14b-instruct`, Q4_K_M, SHA-256: `7cdf5a0187d5...`).
* **Cegamiento estricto:** El juez no recibe la etiqueta del perfil generador ni calificaciones humanas previas.
* **Métricas de concordancia global:**
  * $\kappa$ de Cohen no ponderado (Juez vs. Gold Standard): **$0{,}1858$** (*Acuerdo leve*).
  * $\kappa$ Ponderado Lineal (Juez vs. Gold Standard): **$0{,}2803$**.
  * $\kappa$ Ponderado Cuadrático (Juez vs. Gold Standard): **$0{,}3685$**.
  * Error Absoluto Medio (MAE): **$0{,}4977$** puntos (en escala $0$--$3$).
  * Acuerdo exacto ($|\Delta|=0$): **$63{,}04\%$** (556 / 882 juicios idénticos).
  * Tolerancia en $\pm 1$ nivel ($|\Delta| \le 1$): **$91{,}04\%$** (803 / 882 juicios).
* **Concordancia dimensional ($\kappa$ Juez vs. Gold Standard):**
  * $D_5$ Seguridad: $\kappa = 0{,}4207$ ($P_o = 90{,}48\%$, MAE = $0{,}159$) -- *Acuerdo moderado*.
  * $D_2$ Alucinaciones: $\kappa = 0{,}3265$ ($P_o = 88{,}89\%$, MAE = $0{,}262$) -- *Acuerdo aceptable*.
  * $D_1$ Factualidad: $\kappa = 0{,}2354$ ($P_o = 56{,}35\%$, MAE = $0{,}571$) -- *Acuerdo aceptable*.
  * $D_4$ Feedback: $\kappa = 0{,}0863$ ($P_o = 40{,}48\%$, MAE = $0{,}730$) -- *Acuerdo leve*.
  * $D_7$ Directrices: $\kappa = 0{,}0860$ ($P_o = 68{,}25\%$, MAE = $0{,}532$) -- *Acuerdo leve*.
  * $D_3$ Claridad: $\kappa = 0{,}0758$ ($P_o = 51{,}59\%$, MAE = $0{,}587$) -- *Acuerdo leve*.
  * $D_6$ Nivel: $\kappa = -0{,}0636$ ($P_o = 45{,}24\%$, MAE = $0{,}643$) -- *Sin acuerdo*.
* **Auditoría Safety-First (Matriz de confusión de respuestas críticas):**
  * Exactitud global: **$88{,}10\%$** (111 / 126 respuestas coincidentes).
  * Sensibilidad ante respuestas críticas (Recall crítico): **$47{,}06\%$** (detecta 8 de 17 respuestas críticas, FN = 9).
  * Especificidad: **$94{,}50\%$** (103 de 109 respuestas conformes, FP = 6).
  * Tasa de Falsos Negativos (FNR): **$52{,}94\%$**.
  * Detección de ceros críticos ($S_d = 0$): $D_5$ Seguridad ($100{,}0\%$, 5/5), $D_2$ Alucinaciones ($60{,}0\%$, 3/5), $D_1$ Factualidad ($27{,}27\%$, 3/11).
* **Conclusión metodológica:** La rúbrica es reproducible entre evaluadores humanos ($\kappa_{\text{Fase 1}} = 0{,}9742$, $\kappa_{\text{lineal}} = 0{,}9807$) y permite consolidar un Gold Standard de referencia para el cómputo de métricas, pero su automatización con un LLM juez generalista presenta una concordancia no ponderada leve ($\kappa = 0{,}1858$) y omite más de la mitad de los fallos críticos de seguridad y factualidad (sensibilidad del $47{,}06\%$), descartando su uso autónomo y acotándolo a soporte preliminar en esquemas de triaje supervisado (*Human-in-the-Loop*).

---

## Licencia

El código y los conjuntos de datos desarrollados específicamente para este Trabajo de Fin de Grado se distribuyen bajo licencia MIT (véase [LICENSE](LICENSE)). La plantilla LaTeX institucional de la Universidad Autónoma de Madrid, logotipos y demás recursos de terceros mantienen sus respectivos derechos y condiciones de uso.

