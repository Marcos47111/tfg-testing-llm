# Memoria del Trabajo de Fin de Grado

Estructura modular en LaTeX para la redacción y compilación de la memoria académica.

## Capítulos (`capitulos/`)

* **`01_introduccion.tex`**: Contexto, motivación, planteamiento del problema, justificación, objetivos, preguntas de investigación y alcance.
* **`02_marco_teorico.tex`**: Estado del arte: IA generativa, Transformers, LLMs, arquitectura de chatbots educativos y riesgos asociados.
* **`03_testing_sistemas_llms.tex`**: Testing tradicional vs testing de LLMs, problema del oráculo, benchmarks existentes y carencias en educación.
* **`04_propuesta_metodologica.tex`**: Marco metodológico, 7 dimensiones analíticas, rúbricas, casos de prueba, métricas ($IQE$, $CFR$, $HR$) y protocolo $\kappa$.
* **`05_aplicacion_demostrativa.tex`**: Entorno experimental, perfiles con Meta-Llama-3-8B-Instruct, resultados cuantitativos, análisis cualitativo y concordancia.
* **`06_discusion.tex`**: Interpretación de resultados, fortalezas del marco, amenazas a la validez y comparación con benchmarks.
* **`07_conclusiones.tex`**: Conclusiones principales, grado de cumplimiento de objetivos, aportaciones y líneas futuras.
* **`08_anexos.tex`**: Rúbrica completa multidimensional, catálogo de 42 casos de prueba y directivas de sistema (*system prompts*).

## Bibliografía

* `referencias.bib`: Fichero BibTeX con las 34 referencias bibliográficas utilizadas en el documento.

## Compilación

Para compilar la memoria completa:
```bash
./compilar_memoria.sh
```
