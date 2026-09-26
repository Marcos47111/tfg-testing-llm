# TFG: Metodología para testing de IA Generativa de texto en educación

**Autor:** Marcos Tomás Jiménez Meléndez  
**Tutor:** Xavier Alamán Roldán  
**Titulación:** Grado en Ingeniería Informática  
**Centro:** Escuela Politécnica Superior -- Universidad Autónoma de Madrid  
**Fecha de entrega:** Octubre de 2026  
**Licencia:** MIT (Código abierto)  
**Versión experimental de referencia:** `v1.2.0-tfg`

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

### 4. Pipeline de Ingestión, Validación, Análisis y Evaluación Humana de Referencia
```bash
# 1. Validar integridad criptográfica (SHA-256) y esquemas de los datasets de evaluación:
python3 src/analisis/validar_datos_evaluacion.py --incluir-judge

# 2. Ejecutar análisis comparativo global de los 3 perfiles de chatbot (Gold Standard):
python3 src/analisis/analizador_experimentos.py

# 3. Generar gráficos vectoriales de resultados principales (radar y barras):
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

# 3. Ejecutar análisis estadístico de concordancia Humano-IA (Kappa simple/ponderado, MAE, Deltas, Fallos Críticos con Wilson 95%):
python3 src/analisis/analizar_concordancia_llm_judge.py

# 4. Generar gráficos vectoriales específicos del juez automático (dimensional, confusión y deltas):
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
│   └── metricas/                           # Definición de fórmulas matemáticas (IQE, CFR, HR, κ, Wilson)
│
├── data/                                   # Conjuntos de datos experimentales
│   ├── prompts/                            # 42 casos de prueba organizados por dimensión y tipo
│   ├── configuraciones_chatbot/            # System prompts y parámetros de inferencia de los perfiles
│   ├── respuestas_obtenidas/raw/           # 126 trazas de respuesta conversacional completas
│   └── evaluaciones/                       # Datasets de evaluación normalizados y anotaciones de referencia
│       ├── llm_judge/                      # Extensión experimental LLM-as-a-Judge (Qwen 14B)
│       │   ├── raw/                        # Trazas de inferencia raw del juez automático (JSON)
│       │   └── ...                         # Datasets normalizados del juez pareados (JSON)
│       └── ...                             # Evaluaciones estructuradas del Gold Standard Humano en JSON
│
├── src/                                    # Código fuente y herramientas en Python
│   ├── evaluador/                          # Motores de ejecución de pruebas y LLM-as-a-Judge
│   │   ├── ejecutor_pruebas.py             # Ejecutor experimental con Ollama
│   │   └── evaluador_llm_judge.py          # Motor de evaluación automática a ciegas (LLM Judge)
│   ├── analisis/                           # Módulos de cálculo métrico, agregación, Kappa y validación
│   │   ├── metricas_tfg.py                 # Fórmulas de IQE, CFR, HR, Cohen's Kappa (simple/ponderado) y Wilson
│   │   ├── analizador_experimentos.py      # Agregación global comparativa
│   │   ├── analizar_concordancia_llm_judge.py # Pipeline de concordancia Humano-IA (Gold Standard vs Qwen 14B)
│   │   └── validar_datos_evaluacion.py     # Validador exhaustivo de integridad y esquemas con SHA-256
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

### 1. Evaluación Principal (Estándar Humano Experto de Referencia -- *Gold Standard*)
Evaluación sistemática de 42 casos de prueba sobre el modelo **Meta-Llama-3-8B-Instruct** (`Q4_0`, `num_ctx=2048`, `seed=42`, $N=126$ respuestas, 882 juicios multidimensionales):

| Perfil de Chatbot | IQE (0--100) | CFR (%) | HR (%) | D1 (Factual) | D2 (Aluc.) | D3 (Claridad) | D4 (Feedback) | D5 (Seguridad) | D6 (Nivel) | D7 (Directriz) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Asistente Base** | **84,13** | 11,90% | 33,33% | 2,55 | 2,86 | 2,83 | 1,86 | 2,76 | 2,00 | 2,71 |
| **Tutor Directo** | **87,94** | 14,29% | 33,33% | 2,52 | 2,86 | 2,88 | 1,93 | 2,76 | 3,00 | 2,76 |
| **Tutor Socrático** | **92,98** | 11,90% | 16,67% | 2,48 | 2,88 | 2,93 | 2,81 | 2,93 | 3,00 | 2,81 |

* **Criterio Safety-First:** Ningún perfil supera el filtro de seguridad prioritaria ($CFR > 0$ en todos los casos).

### 2. Extensión Exploratoria LLM-as-a-Judge (Resultados Experimentales con Qwen2.5-14B-Instruct)
Evaluación automática a ciegas sobre las 126 respuestas reales ($N_\kappa=882$ juicios pareados frente al Gold Standard, $T=0.0$, $\text{seed}=42$):

* **Modelo evaluador:** Qwen2.5-14B-Instruct (`qwen2.5:14b-instruct`, Q4_K_M).
* **Cegamiento estricto:** El juez no recibe la etiqueta del perfil generador ni calificaciones humanas previas.
* **Métricas de concordancia global:**
  * $\kappa$ de Cohen simple (no ponderado): **$0{,}1900$** (*Acuerdo leve*).
  * $\kappa_{\text{lin}}$ (ponderación lineal ordinal): **$0{,}2800$** (*Acuerdo aceptable*).
  * $\kappa_{\text{quad}}$ (ponderación cuadrática ordinal): **$0{,}3642$** (*Acuerdo aceptable*).
  * Error Absoluto Medio (MAE): **$0{,}4943$** puntos (en escala $0$--$3$).
  * Acuerdo exacto ($|\Delta|=0$): **$63{,}49\%$** (560 / 882 juicios idénticos).
  * Tolerancia en $\pm 1$ nivel ($|\Delta| \le 1$): **$90{,}93\%$** (802 / 882 juicios).
* **Concordancia dimensional ($\kappa$ simple / $\kappa_{\text{lin}}$ / $\kappa_{\text{quad}}$ Juez vs. Gold Standard):**
  * $D_5$ Seguridad: $\kappa = 0{,}421$ / $\kappa_{\text{lin}} = 0{,}572$ / $\kappa_{\text{quad}} = 0{,}646$ ($P_o = 90{,}48\%$, MAE = $0{,}159$) -- *Acuerdo moderado*.
  * $D_1$ Factualidad: $\kappa = 0{,}261$ / $\kappa_{\text{lin}} = 0{,}429$ / $\kappa_{\text{quad}} = 0{,}557$ ($P_o = 58{,}73\%$, MAE = $0{,}540$) -- *Acuerdo aceptable*.
  * $D_2$ Alucinaciones: $\kappa = 0{,}327$ / $\kappa_{\text{lin}} = 0{,}382$ / $\kappa_{\text{quad}} = 0{,}413$ ($P_o = 88{,}89\%$, MAE = $0{,}262$) -- *Acuerdo aceptable*.
  * $D_7$ Directrices: $\kappa = 0{,}086$ / $\kappa_{\text{lin}} = 0{,}164$ / $\kappa_{\text{quad}} = 0{,}221$ ($P_o = 68{,}25\%$, MAE = $0{,}532$) -- *Acuerdo leve*.
  * $D_4$ Feedback: $\kappa = 0{,}066$ / $\kappa_{\text{lin}} = 0{,}129$ / $\kappa_{\text{quad}} = 0{,}207$ ($P_o = 38{,}89\%$, MAE = $0{,}754$) -- *Acuerdo leve*.
  * $D_3$ Claridad: $\kappa = 0{,}076$ / $\kappa_{\text{lin}} = 0{,}078$ / $\kappa_{\text{quad}} = 0{,}070$ ($P_o = 51{,}59\%$, MAE = $0{,}587$) -- *Acuerdo leve*.
  * $D_6$ Nivel: $\kappa = -0{,}026$ / $\kappa_{\text{lin}} = -0{,}017$ / $\kappa_{\text{quad}} = -0{,}012$ ($P_o = 47{,}62\%$, MAE = $0{,}627$) -- *Sin acuerdo*.
* **Auditoría Safety-First (Matriz de confusión de respuestas críticas con intervalos de Wilson 95%):**
  * Exactitud global: **$88{,}89\%$** (112 / 126 respuestas coincidentes: TP=8, TN=104, FP=6, FN=8).
  * Sensibilidad ante respuestas críticas (Recall crítico): **$50{,}00\%$** [IC 95%: $28{,}00\% - 72{,}00\%$] (detecta 8 de 16 respuestas críticas).
  * Especificidad: **$94{,}55\%$** [IC 95%: $88{,}61\% - 97{,}48\%$] (104 de 110 respuestas conformes).
* **Conclusión metodológica:** El juez automático con Qwen 14B aproxima de manera robusta directrices explícitas de seguridad ($100\%$ detección de ceros en $D_5$, especificidad $94{,}55\%$, $90{,}93\%$ de juicios a distancia $|\Delta| \le 1$), pero presenta sensibilidad limitada ante fallos factuales sutiles (detectando el $50{,}0\%$ de fallos críticos, con FNR del $50{,}0\%$). Por ello, no es apto para operar como evaluador autónomo y queda acotado a herramienta de triaje preliminar en arquitecturas supervisadas (*Human-in-the-Loop*).

---

## Licencia

El código y los conjuntos de datos desarrollados específicamente para este Trabajo de Fin de Grado se distribuyen bajo licencia MIT (véase [LICENSE](LICENSE)). La plantilla LaTeX institucional de la Universidad Autónoma de Madrid, logotipos y demás recursos de terceros mantienen sus respectivos derechos y condiciones de uso.
