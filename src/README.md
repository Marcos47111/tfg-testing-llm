# Código Fuente y Scripts de Soporte

Módulos en Python para automatizar el ciclo de vida del testing experimental.

## Módulos

* **`evaluador/`**: Cliente para enviar las baterías de prompts a los LLMs mediante la API REST local de Ollama (`/api/chat`), registrando latencias, respuestas y metadatos.
* **`analisis/`**: Cálculo automatizado de métricas analíticas ($\bar{S}_d$, $CR_d$, $CFR$, $HR$, $IQE$), análisis comparativo de experimentos, auditoría de consistencia inter-evaluador ($\kappa$ de Cohen) y tests unitarios.
* **`visualizacion/`**: Generación de gráficos vectoriales mediante `matplotlib` (diagramas de radar multidimensional y gráficos de barras comparativos).
* **`utils/`**: Carga y validación de ficheros JSON con casos de prueba y exportación de datos.
