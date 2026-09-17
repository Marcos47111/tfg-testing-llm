# Código Fuente y Scripts de Soporte

Módulos en Python para automatizar el ciclo de vida del testing experimental.

## Módulos

* **`evaluador/`**: Cliente para enviar las baterías de prompts a los LLMs (mediante API de Ollama local o APIs compatibles con OpenAI), registrar latencias, respuestas y metadatos.
* **`analisis/`**: Cálculo automático de estadísticas agregadas, promedios por categoría, detección de correlaciones y generación de datasets consolidados.
* **`visualizacion/`**: Scripts con `matplotlib` / `seaborn` para generar figuras vectoriales y gráficos para la memoria (diagramas de radar, barras por dimensión, etc.).
* **`utils/`**: Lectura y escritura de ficheros JSON, CSV y generadores de tablas en formato LaTeX / Markdown.
