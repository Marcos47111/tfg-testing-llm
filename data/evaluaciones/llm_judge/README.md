# Evaluación Automática Experimental mediante LLM-as-a-Judge

Este directorio contiene las evaluaciones generadas por el modelo de lenguaje actuando como juez automático (*LLM-as-a-Judge*) sobre las 126 respuestas conversacionales del corpus experimental.

---

## 🎯 Objetivo de la Extensión Experimental
Investigar la viabilidad y fiabilidad de automatizar la aplicación de la rúbrica analítica multidimensional ($D_1$ a $D_7$, escala $0$ a $3$) mediante un modelo de lenguaje evaluador, contrastando estadísticamente sus asignaciones con los dos evaluadores humanos independientes de referencia ($E_1$ y $E_2$).

> **NOTA METODOLÓGICA FUNDAMENTAL:**  
> Esta evaluación es una extensión exploratoria del TFG. Las evaluaciones humanas ($E_1$ y $E_2$) almacenadas en `data/evaluaciones/` constituyen la referencia canónica inmutable del experimento principal y no son modificadas ni sustituidas por este módulo.

---

## ⚙️ Especificación Técnica del Modelo Juez
* **Modelo Juez de Referencia:** Meta-Llama-3-8B-Instruct (cuantización Q4_0) / Arquitectura Transformer autorregresiva.
* **Parámetros de Inferencia:** Temperatura $T = 0{,}0$ (búsqueda codiciosa/determinista), $\text{top-}p = 0{,}90$, $\text{seed} = 42$.
* **Estructura del Prompt:** Inyección completa de prompt discente, respuesta generada, solución canónica (`ground_truth`), criterio crítico de fallo y matriz completa de rúbricas $D_1 \dots D_7$.
* **Formato de Salida:** JSON estructurado estricto con puntuaciones enteras en $\{0, 1, 2, 3\}$ y justificación cualitativa por dimensión.
* **Volumen Evaluado:** 126 respuestas $\times$ 7 dimensiones = 882 juicios automáticos.

---

## 📁 Estructura de Ficheros
* `raw/evaluaciones_llm_judge_raw.json`: Trazas directas con los metadatos de ejecución, latencias, timestamps y cadenas JSON originales emitidas por el modelo.
* `evaluacion_llm_judge.json`: Dataset consolidado normalizado con las 126 evaluaciones del juez.
* `evaluacion_llm_judge_asistente_base.json`: 42 evaluaciones del perfil Asistente Base.
* `evaluacion_llm_judge_tutor_directo.json`: 42 evaluaciones del perfil Tutor Directo.
* `evaluacion_llm_judge_tutor_socratico.json`: 42 evaluaciones del perfil Tutor Socrático.

---

## 🔄 Flujo de Procesamiento y Análisis
```
data/respuestas_obtenidas/raw/*.json + data/prompts/
  └──> src/evaluador/evaluador_llm_judge.py
         ├──> data/evaluaciones/llm_judge/raw/evaluaciones_llm_judge_raw.json
         └──> data/evaluaciones/llm_judge/evaluacion_llm_judge.json
                └──> src/analisis/analizar_concordancia_llm_judge.py
                       ├──> results/informes/concordancia_llm_judge.json
                       ├──> results/tablas/tabla_concordancia_llm_judge.csv/.tex/.md
                       └──> results/graficos/concordancia_llm_judge.pdf
```
