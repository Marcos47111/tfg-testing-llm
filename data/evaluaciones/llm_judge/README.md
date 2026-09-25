# Evaluación Automática Experimental mediante LLM-as-a-Judge

Este directorio está reservado para las evaluaciones experimentales generadas por el modelo de lenguaje actuando como juez automático (*LLM-as-a-Judge*). Los datasets se incorporarán en esta ubicación tras ejecutar la inferencia real mediante `Qwen2.5-14B-Instruct`.

---

## Objetivo de la Extensión Experimental
Investigar la viabilidad y fiabilidad de automatizar la aplicación de la rúbrica analítica multidimensional ($D_1$ a $D_7$, escala $0$ a $3$) mediante un modelo de lenguaje evaluador, contrastando estadísticamente sus asignaciones con los dos evaluadores humanos independientes de referencia ($E_1$ y $E_2$).

> **NOTA METODOLÓGICA FUNDAMENTAL:**  
> Esta evaluación constituye una extensión exploratoria del TFG. Las evaluaciones humanas ($E_1$ y $E_2$) custodiadas en `data/evaluaciones/` representan la referencia canónica inmutable del experimento principal y no son modificadas ni sustituidas por este módulo.

---

## Especificación Técnica del Protocolo del Juez
* **Modelo Juez de Referencia:** Qwen2.5-14B-Instruct (`qwen2.5:14b` mediante API REST de Ollama o endpoints compatibles con OpenAI).
* **Parámetros de Inferencia:** Temperatura $T = 0{,}0$ (búsqueda codiciosa/determinista), $\text{top-}p = 0{,}90$, $\text{seed} = 42$.
* **Cegamiento Metodológico:** Evaluación ciega respecto al perfil generador y a las evaluaciones humanas (el prompt no incluye la etiqueta del perfil conversacional ni calificaciones previas).
* **Estructura del Prompt:** Inyección del prompt discente, respuesta generada, solución canónica (`ground_truth`), criterio crítico de fallo y matriz canónica de rúbricas $D_1 \dots D_7$ (versión `judge_prompt_v1`).
* **Formato de Salida:** JSON estructurado estricto con puntuaciones enteras en $\{0, 1, 2, 3\}$ y justificación cualitativa por dimensión.
* **Volumen Evaluado:** 126 respuestas $\times$ 7 dimensiones = 882 juicios automáticos.

---

## Estructura de Ficheros (Prevista tras Ejecución Real)
* `raw/evaluaciones_llm_judge_raw.json`: Trazas directas con los metadatos de ejecución, latencias reales, timestamps y cadenas JSON originales emitidas por el modelo.
* `evaluacion_llm_judge.json`: Dataset consolidado normalizado con las 126 evaluaciones del juez.
* `evaluacion_llm_judge_asistente_base.json`: 42 evaluaciones del perfil Asistente Base.
* `evaluacion_llm_judge_tutor_directo.json`: 42 evaluaciones del perfil Tutor Directo.
* `evaluacion_llm_judge_tutor_socratico.json`: 42 evaluaciones del perfil Tutor Socrático.

---

## Instrucciones de Ejecución

Para ejecutar la inferencia experimental real con Qwen2.5-14B-Instruct:
```bash
python3 src/evaluador/evaluador_llm_judge.py --mode ollama --model qwen2.5:14b --temperature 0
```

Para validar los datasets generados y calcular la concordancia estadistica:
```bash
python3 src/analisis/validar_datos_evaluacion.py --incluir-judge
python3 src/analisis/analizar_concordancia_llm_judge.py
python3 src/visualizacion/generar_graficos_llm_judge.py
```
