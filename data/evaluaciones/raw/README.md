# Registro de Anotaciones Humanas Originales (Raw)

Este directorio contiene las hojas de datos de anotación cualitativa y cuantitativa registradas de forma independiente por el panel de evaluadores durante la sesión de auditoría experimental.

---

## 👥 Panel de Evaluadores
1. **Evaluador 1 (Anotador de Referencia / Autor):** Marcos Tomás Jiménez Meléndez.
2. **Evaluador 2 (Anotador Independiente):** Graduado en Ingeniería Informática ajeno al desarrollo del system prompt.

---

## 🔒 Protocolo de Evaluación y Cegamiento
* **Cegamiento:** Los evaluadores dispusieron de las 126 respuestas generadas por Meta-Llama-3-8B-Instruct presentadas sin la etiqueta explícita del perfil de procedencia (`asistente_base`, `tutor_directo`, `tutor_socratico`).
* **Instrumento:** Rúbrica analítica multidimensional de 4 niveles discretos ($0, 1, 2, 3$) definida en `metodologia/rubricas/rubrica_general.md` y `metodologia/rubricas/guia_evaluador.md`.
* **Criterio de Oráculo:** Cada caso de prueba cuenta con su correspondiente solución canónica de referencia (`ground_truth`) y criterio de fallo crítico.
* **Cobertura:** Las 126 respuestas fueron calificadas independientemente sobre las 7 dimensiones analíticas, totalizando **882 juicios emparejados** por evaluador.

---

## 📁 Ficheros de Datos
* `anotaciones_evaluador_1_raw.csv`: 126 filas con las puntuaciones y justificaciones asignadas por el Evaluador 1.
* `anotaciones_evaluador_2_raw.csv`: 126 filas con las puntuaciones y justificaciones asignadas por el Evaluador 2.

---

## 🔄 Flujo de Trazabilidad
El pipeline de ingestión y análisis procesa estos datos de la siguiente manera:
```
data/evaluaciones/raw/*.csv
  └──> src/analisis/importar_evaluaciones_humanas.py
         ├──> data/evaluaciones/evaluacion_evaluador_1.json
         ├──> data/evaluaciones/evaluacion_evaluador_2.json
         └──> data/evaluaciones/evaluacion_<perfil>.json
                ├──> src/analisis/analizador_experimentos.py (IQE, CFR, HR, S_d)
                └──> src/analisis/calcular_concordancia_evaluadores.py (Cohen's Kappa κ)
```
