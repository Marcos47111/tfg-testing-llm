# Registro de Anotaciones Humanas Originales (Raw)

Este directorio contiene las hojas de datos de anotación cualitativa y cuantitativa registradas de forma independiente por el panel de evaluadores durante la sesión de auditoría experimental.

---

## Panel de Evaluadores
1. **Evaluador 1 (Anotador de Referencia / Autor):** Marcos Tomás Jiménez Meléndez.
2. **Evaluador 2 (Anotador Independiente):** Graduado en Ingeniería Informática ajeno al diseño de las directivas de sistema (*system prompts*).

---

## Protocolo de Evaluación y Cegamiento
* **Cegamiento:** Los evaluadores dispusieron de las 126 respuestas conversacionales generadas por Meta-Llama-3-8B-Instruct presentadas sin la etiqueta explícita del perfil de procedencia (`asistente_base`, `tutor_directo`, `tutor_socratico`).
* **Trazabilidad post-evaluación:** Los ficheros CSV publicados constituyen la exportación estructurada de las anotaciones de ambos evaluadores. La columna `perfil` se incorporó con posterioridad a la sesión de evaluación para restaurar la trazabilidad con el corpus experimental; dicha etiqueta no fue visible durante el proceso de calificación.
* **Instrumento:** Rúbrica analítica multidimensional en escala discreta de cuatro niveles ($0, 1, 2, 3$) formalizada en `metodologia/rubricas/rubrica_general.md` y `metodologia/rubricas/guia_evaluador.md`.
* **Criterio de Oráculo:** Cada caso de prueba cuenta con su correspondiente solución canónica de referencia (`ground_truth`) y criterio de fallo crítico.
* **Cobertura:** Las 126 respuestas fueron calificadas independientemente sobre las 7 dimensiones analíticas, totalizando **882 juicios emparejados** por evaluador ($126 \times 7 = 882$).

---

## Ficheros de Datos
* `anotaciones_evaluador_1_raw.csv`: 126 filas con las puntuaciones y justificaciones asignadas por el Evaluador 1.
* `anotaciones_evaluador_2_raw.csv`: 126 filas con las puntuaciones y justificaciones asignadas por el Evaluador 2.

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
