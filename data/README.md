# Conjunto de Datos y Pruebas Experimentales

Estructura de datos para almacenar el banco de pruebas, respuestas generadas y evaluaciones.

## Estructura

* **`prompts/`**: Casos de prueba almacenados en formato estructurado (JSON/CSV) o ficheros individuales organizados por dimensión:
  * `01_correccion_factual/`
  * `02_deteccion_alucinaciones/`
  * `03_claridad_y_pedagogia/`
  * `04_robustez_y_seguridad/`
  * `05_adaptacion_nivel/`
  * `06_seguimiento_instrucciones/`
* **`configuraciones_chatbot/`**: Prompts de sistema (system prompts) empleados para simular los roles de tutor/profesor virtual, parámetros (temperatura, top_p, seed) y modelos evaluados.
* **`respuestas_obtenidas/raw/`**: Ficheros JSON con las salidas directas generadas por los modelos durante los ensayos.
* **`evaluaciones/`**: Ficheros con las puntuaciones de las rúbricas aplicadas a cada respuesta registrada.
