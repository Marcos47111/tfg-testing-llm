# Dimensión 7: Seguimiento de Instrucciones y Coherencia Contextual

## 1. Definición
Esta dimensión evalúa el grado de fidelidad con el que el sistema sigue las restricciones explícitas de formato, longitud, rol pedagógico y restricciones negativas impuestas en el prompt del usuario o en el prompt de sistema (*system prompt*), así como el mantenimiento de la coherencia en conversaciones multi-turno.

## 2. Justificación en el Contexto Educativo
En tareas académicas estructuradas, a menudo se exige al chatbot generar salidas bajo formatos concretos (ej. una rúbrica en formato tabla, un cuestionario de 3 preguntas de opción múltiple, un resumen de exactamente 150 palabras, o responder únicamente en un idioma determinado). Si el modelo no respeta estas directrices, la herramienta pierde su valor para integrarse en flujos de aprendizaje estructurados.

## 3. Indicadores Observables
* **Cumplimiento de restricciones de formato:** Generación exacta de tablas Markdown, listas numeradas, bloques de código o JSON según lo requerido.
* **Control de longitud y concisión:** Respeto estricto a límites de palabras, párrafos o líneas indicados en el prompt.
* **Cumplimiento de restricciones negativas:** Capacidad para acatar órdenes como *"no uses la palabra X"*, *"no des la respuesta numérica final"*, o *"no uses jerga técnica"*.
* **Coherencia multi-turno:** Retención del contexto previo de la sesión educativa sin contradecirse ni olvidar las preferencias establecidas.

## 4. Escala de Evaluación (0 a 3)

| Nivel | Etiqueta | Descripción del Comportamiento |
| :---: | :--- | :--- |
| **0** | **Inaceptable / Incumplimiento Total** | Ignora sistemáticamente las directrices de formato, longitud y restricciones negativas, respondiendo en un formato libre e incoherente. |
| **1** | **Deficiente / Cumplimiento Parcial** | Cumple parte de las instrucciones (ej. hace la tabla pero excede ampliamente la longitud o incluye elementos prohibidos). |
| **2** | **Aceptable / Cumplimiento Adecuado** | Respeta todas las restricciones principales de formato, rol y longitud con desviaciones mínimas sin relevancia. |
| **3** | **Excelente / Cumplimiento Riguroso** | Fidelidad absoluta a todas las instrucciones de formato, restricciones negativas y especificaciones de diseño didáctico. |

## 5. Tipo de Pruebas Asociadas
* Generación de material docente con restricciones complejas (ej. *"Crea una tabla comparativa de 3 columnas con exactamente 4 filas"*).
* Pruebas con restricciones negativas (ej. *"Explica qué es un átomo sin utilizar las palabras protón, neutrón ni electrón"*).
* Pruebas de memoria contextual en conversaciones de 3 a 5 turnos.

## 6. Fundamentación Teórica y Bibliográfica
* **Evaluación Multi-Turno y Seguimiento de Directrices (*Zheng et al., 2023 - MT-Bench*):** Demostración de que la consistencia conversacional y la capacidad de acatar restricciones complejas definen la utilidad práctica de un LLM en tareas interactivas.
* **Alineamiento y Cumplimiento de Restricciones Negativas (*Achiam et al., 2023*):** El seguimiento estricto de instrucciones de sistema previene comportamientos no deseados y garantiza la reproducibilidad de los flujos de trabajo.
* **Estándar de Calidad de Software (ISO/IEC 25010:2023):** Se fundamenta en la *Conformidad Funcional y de Interfaz*, verificando que el software se ciñe rigurosamente a las especificaciones y requisitos operacionales dados.
