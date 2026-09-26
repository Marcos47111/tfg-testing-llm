# Registro de Anotaciones Humanas Revisadas y Consolidadas — Fase 2 (Gold Standard)

Este directorio contiene las hojas de datos tabulares (CSV) correspondientes al conjunto de anotaciones humanas **revisadas, calibradas y consolidadas (Fase 2 - Gold Standard)** tras la auditoría experimental.

> **Nota de integridad y trazabilidad:**
> Las anotaciones independientes originales registradas durante la **Fase 1** (doble anotación a ciegas previa al proceso de calibración y auditoría) se encuentran preservadas de forma inmutable en `data/evaluaciones/raw_independientes/`.

---

## Panel de Evaluadores
1. **Evaluador 1 (Anotador de Referencia / Autor):** Marcos Tomás Jiménez Meléndez.
2. **Evaluador 2 (Anotador Independiente):** Graduado en Ingeniería Informática ajeno al diseño de las directivas de sistema (*system prompts*).

---

## Protocolo de Evaluación y Consolidación
* **Cegamiento original (Fase 1):** Los evaluadores calificaron las 126 respuestas generadas por Meta-Llama-3-8B-Instruct sin conocer la etiqueta del perfil de procedencia (`asistente_base`, `tutor_directo`, `tutor_socratico`).
* **Auditoría y consolidación (Fase 2):** Se realizó un proceso sistemático de revisión y calibración frente a la solución canónica de referencia (`ground_truth`), criterios críticos de fallo y la rúbrica multidimensional ($D_1$--$D_7$), consolidando el conjunto de referencia definitivo (*Gold Standard*).
* **Instrumento:** Rúbrica analítica multidimensional en escala discreta de cuatro niveles ($0, 1, 2, 3$) formalizada en `metodologia/rubricas/rubrica_general.md` y `metodologia/rubricas/guia_evaluador.md`.
* **Cobertura:** 126 respuestas evaluadas sobre 7 dimensiones analíticas (**882 juicios emparejados** por evaluador).

---

## Ficheros de Datos
* `anotaciones_evaluador_1_raw.csv`: 126 filas con las puntuaciones y justificaciones consolidadas del Evaluador 1.
* `anotaciones_evaluador_2_raw.csv`: 126 filas con las puntuaciones y justificaciones consolidadas del Evaluador 2.

---

## Flujo de Trazabilidad
El pipeline de ingestión y análisis procesa estos datos de la siguiente manera:
```
data/evaluaciones/raw/*.csv
  └──> src/analisis/importar_evaluaciones_humanas.py
         ├──> data/evaluaciones/evaluacion_evaluador_1.json
         ├──> data/evaluaciones/evaluacion_evaluador_2.json
         └──> data/evaluaciones/evaluacion_<perfil>.json
                ├──> src/analisis/validar_datos_evaluacion.py (Auditoría cruzada raw <-> JSON)
                ├──> src/analisis/analizador_experimentos.py (IQE, CFR, HR, S_d)
                └──> src/analisis/calcular_concordancia_evaluadores.py (Cohen's Kappa κ)
```
