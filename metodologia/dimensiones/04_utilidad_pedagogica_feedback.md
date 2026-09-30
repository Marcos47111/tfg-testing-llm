# Dimensión 4: Utilidad Pedagógica, Detección de Errores y Feedback

## 1. Definición
Esta dimensión evalúa la habilidad del chatbot para actuar como un tutor formativo: detectar errores en los razonamientos o código aportados por el estudiante, proporcionar retroalimentación constructiva (*feedback formativo*), plantear preguntas guía (método socrático) y fomentar la autonomía del estudiante en lugar de limitarse a darle la respuesta resuelta directamente.

## 2. Justificación en el Contexto Educativo
En el aprendizaje asistido por IA, si el chatbot se limita a resolver los ejercicios de forma pasiva, priva al alumno de la oportunidad de reflexionar y desarrollar pensamiento crítico. El sistema debe ser capaz de diagnosticar el error concreto que comete el alumno y guiarlo hacia la solución.

## 3. Indicadores Observables
* **Detección y diagnóstico del error:** Identifica con precisión la línea de código errónea, el fallo aritmético o el malentendido conceptual en el texto del alumno.
* **Feedback formativo y no punitivo:** Explica por qué el razonamiento del estudiante falla y qué principio subyacente se ha vulnerado de manera empática y motivadora.
* **Andamiaje socrático:** En lugar de dar la solución cerrada de inmediato (cuando se le pide tutoría), formula pistas o preguntas de reflexión intermedia.
* **Comprobación de la comprensión:** Incluye al final una pequeña pregunta de control o ejercicio de afianzamiento para validar si el alumno comprendió el concepto.

## 4. Escala de Evaluación (0 a 3)

| Nivel | Etiqueta | Descripción del Comportamiento |
| :---: | :--- | :--- |
| **0** | **Inaceptable / No detecta error** | Pasa por alto el error del alumno y da por válido un razonamiento incorrecto, o da la solución final directamente ignorando la solicitud de retroalimentación. |
| **1** | **Deficiente / Feedback superficial** | Indica que hay un error pero no explica su origen, o se limita a reescribir la solución correcta sin explicar el fallo del alumno. |
| **2** | **Aceptable / Feedback constructivo** | Señala claramente el error cometido por el alumno, explica la causa del fallo y proporciona la corrección o pista relevante. |
| **3** | **Excelente / Tutoría Socrática** | Diagnóstico perfecto del error, explicación pedagógica profunda de la causa raíz, pistas graduadas para que el alumno lo resuelva y propuesta de refuerzo. |

## 5. Tipo de Pruebas Asociadas
* Fragmentos de código con errores lógicos (bugs tipo *off-by-one*, variables no inicializadas) presentados por el "alumno".
* Respuestas de exámenes o razonamientos deductivos con falacias o premisas erróneas para que el bot las evalúe.
* Peticiones explícitas de "ayúdame a entender mi error sin darme la solución directamente".

## 6. Fundamentación Teórica y Bibliográfica
* **Zona de Desarrollo Próximo y Andamiaje (*Vygotsky, 1978; Wood et al., 1976*):** El rol fundamental del tutor es proporcionar soporte temporal graduado para que el alumno resuelva tareas que no podría resolver en solitario, retirando el apoyo conforme adquiere competencia (*fading scaffolding*).
* **Modelo Cuatridimensional de Feedback (*Hattie & Timperley, 2007*):** El feedback más efectivo actúa sobre el nivel de proceso cognitivo y de autorregulación, diagnosticando el error y orientando la acción futura, en lugar de limitarse a indicar si la respuesta es correcta/incorrecta.
* **Estándar de Calidad de Software (ISO/IEC 25010:2023):** Se fundamenta en la *Eficacia en el Uso* y el *Valor Añadido*, evaluando si el software asiste de forma productiva al usuario en la consecución de sus objetivos de aprendizaje.
