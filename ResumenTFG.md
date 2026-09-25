# Resumen Ejecutivo y Guía de Decisiones del Trabajo de Fin de Grado (TFG)

**Título:** Metodología para testing de IA Generativa de texto en educación  
**Autor:** Marcos Tomás Jiménez Meléndez  
**Grado:** Grado en Ingeniería Informática (UAM / EPS)  
**Versión experimental de referencia:** **v1.0.12-tfg**

---

## 1. Idea central del trabajo

### ¿Qué problema se intenta resolver?

El problema de partida es de **ingeniería del software**: los mecanismos clásicos de testing funcionan especialmente bien cuando existe un oráculo determinista, es decir, cuando para una entrada concreta existe una salida esperada que puede comprobarse mediante una aserción booleana.

En un sistema basado en un Large Language Model (LLM), esa lógica deja de ser suficiente. Ante una misma consulta pueden existir múltiples respuestas válidas en lenguaje natural, con formulaciones diferentes, y la generación depende de un proceso probabilístico. Por tanto, una comprobación del tipo “salida generada = salida esperada” no permite determinar de forma adecuada si una respuesta es correcta, segura o pedagógicamente útil.

En educación el problema es todavía más exigente, porque no basta con comprobar si una respuesta “suena bien” o contiene información relevante. Un chatbot puede:

- producir una respuesta lingüísticamente fluida pero conceptualmente falsa;
- validar una premisa inventada o una referencia inexistente;
- entregar directamente la solución de un ejercicio y sustituir el razonamiento del alumno;
- no detectar el error conceptual que está cometiendo el estudiante;
- utilizar un nivel de complejidad inadecuado;
- incumplir restricciones explícitas;
- ceder ante prompt injection, jailbreaks o peticiones de fraude académico.

Por tanto, el TFG plantea la siguiente pregunta de fondo:

> **¿Cómo puede auditarse de forma sistemática un chatbot educativo basado en LLMs cuando no existe una única respuesta textual correcta y, además, deben evaluarse simultáneamente calidad conceptual, seguridad y utilidad pedagógica?**

---

## 2. ¿Para qué se realiza el trabajo y qué aporta?

El objetivo no es crear un nuevo LLM ni entrenar uno desde cero. La aportación consiste en **diseñar y validar preliminarmente una metodología de testing de caja negra para sistemas conversacionales educativos basados en LLMs**.

El trabajo aporta:

1. **Un marco multidimensional de evaluación**, que separa la calidad en siete dimensiones observables en lugar de reducirla a una única medida general.
2. **Una rúbrica analítica 0–3** con descriptores conductuales para convertir respuestas abiertas en puntuaciones comparables.
3. **Una batería estructurada de 42 casos de prueba**, incluyendo casos curriculares, trampas con premisas falsas, restricciones de formato y escenarios adversariales.
4. **Métricas agregadas de calidad y riesgo**, entre ellas medias dimensionales, tasas de cumplimiento, CFR, HR e IQE.
5. **Un criterio Safety-First**, que impide que una puntuación global alta oculte fallos críticos de factualidad, alucinación o seguridad.
6. **Un estudio experimental real** sobre Meta-Llama-3-8B-Instruct con tres perfiles conversacionales distintos.
7. **Un paquete de software en Python** que automatiza la carga de casos, ejecución, agregación, cálculo de métricas, concordancia y visualización.
8. **Un conjunto de datos abierto y trazable**, con los 126 registros de inferencia, evaluaciones y resultados consolidados.
9. **Una demostración empírica de una idea importante de testing:** mejorar la calidad media de una respuesta no implica necesariamente reducir los fallos críticos.

La aportación central no es afirmar que el Tutor Socrático sea “el mejor chatbot educativo” de forma universal. La aportación consiste en demostrar que el marco permite **detectar diferencias, fortalezas y riesgos que quedarían ocultos si únicamente se utilizara una puntuación global**.

---

## 3. Objetivo general y preguntas de investigación

### Objetivo general

Diseñar, formalizar y evaluar experimentalmente una metodología de testing para sistemas conversacionales basados en LLMs utilizados como apoyo al aprendizaje, capaz de medir:

- corrección factual;
- control de alucinaciones;
- claridad didáctica;
- utilidad pedagógica;
- robustez y seguridad;
- adaptación al nivel educativo;
- seguimiento de instrucciones.

### Preguntas de investigación

**PI1.** ¿Cómo estructurar un protocolo de testing para LLMs que evalúe simultáneamente rigor conceptual y calidad del andamiaje pedagógico mediante criterios observables?

**PI2.** ¿Hasta qué punto la configuración del System Prompt, comparando una estrategia expositiva directa con otra socrática, condiciona la seguridad, las alucinaciones y la orientación formativa?

**PI3.** ¿Puede una rúbrica analítica discreta sin punto neutro reducir la ambigüedad del problema del oráculo y producir una concordancia inter-evaluador suficientemente alta en respuestas abiertas?

---

## 4. Fundamentos que sostienen la propuesta

La metodología combina dos familias de fundamentos.

### 4.1. Ingeniería de software y evaluación de LLMs

- ISO/IEC 25010:2023 como referencia para características de calidad de producto.
- ISO/IEC/IEEE 29119-1:2022 para conceptos generales de testing.
- Problema del oráculo en software.
- Literatura sobre alucinaciones, incertidumbre y factualidad.
- Benchmarks y metodologías de evaluación de LLMs como MMLU, TruthfulQA, MT-Bench, Chatbot Arena e IFEval.
- Literatura sobre prompt injection y jailbreaks.

### 4.2. Fundamentos pedagógicos

- Zona de Desarrollo Próximo de Vygotsky.
- Andamiaje tutorial de Wood, Bruner y Ross.
- Retroalimentación formativa de Hattie y Timperley.
- Taxonomía de Bloom y revisión de Anderson y Krathwohl.
- Concepto de cognitive offloading para justificar el riesgo del solucionismo directo.

La metodología no copia literalmente ninguno de estos marcos. Los utiliza para **construir una adaptación propia orientada al testing de chatbots educativos**.

---

## 5. Solución metodológica propuesta

### 5.1. Siete dimensiones de evaluación

**D1 — Corrección Factual y Rigor Conceptual**  
Comprueba si la información proporcionada es disciplinarmente correcta y suficientemente completa.

**D2 — Control de Alucinaciones y Manejo de Incertidumbre**  
Evalúa si el sistema evita inventar información, valida o rechaza premisas falsas y gestiona correctamente situaciones de incertidumbre.

**D3 — Claridad Didáctica y Estructura Explicativa**  
Valora organización, progresión lógica, comprensibilidad y uso pertinente de ejemplos o analogías.

**D4 — Utilidad Pedagógica, Detección de Errores y Feedback**  
Mide si el chatbot identifica el error real del estudiante y lo orienta mediante pistas o preguntas en lugar de limitarse a proporcionar una solución.

**D5 — Robustez, Seguridad e Integridad Académica**  
Comprueba la resistencia frente a prompt injection, jailbreaks y peticiones de fraude académico.

**D6 — Adaptación al Nivel Educativo, Complejidad Cognitiva y Registro**  
Valora si vocabulario, profundidad y demanda cognitiva se ajustan al nivel del estudiante.

**D7 — Seguimiento de Instrucciones y Restricciones**  
Comprueba restricciones objetivas de formato, longitud, léxico y estructura.

---

## 6. Rúbrica de valoración

Se utiliza una escala discreta de cuatro niveles:

- **0 — Crítico / Inaceptable:** fallo grave o incumplimiento esencial.
- **1 — Deficiente / Parcial:** respuesta con problemas importantes o cumplimiento insuficiente.
- **2 — Aceptable / Correcto:** respuesta adecuada aunque mejorable.
- **3 — Excelente / Óptimo:** comportamiento correcto, completo y especialmente sólido respecto al criterio evaluado.

### Decisión: eliminar el punto medio neutro

Se eligió una escala par 0–3 para obligar al evaluador a discriminar entre una respuesta insuficiente y una respuesta aceptable, evitando utilizar sistemáticamente una categoría central neutral.

No se afirma que una escala de cuatro niveles sea universalmente superior. Es una **decisión metodológica de esta validación**, acompañada de descriptores conductuales explícitos para reducir la ambigüedad.

### Decisión adicional en D1

Para recibir D1 = 3 en casos conceptuales no basta con “no decir nada incorrecto”. La respuesta debe ser también **suficientemente completa respecto a lo solicitado**. Esto evita premiar con la máxima puntuación respuestas que eluden el contenido factual principal.

---

## 7. Diseño de la batería de pruebas

Cada caso se representa mediante:

$C_i = \langle id, dimensión\_ppal, materia, nivel, prompt, ground\_truth, criterio\_crítico \rangle$

La batería contiene **42 casos**, distribuidos de forma equilibrada:

- 7 dimensiones;
- 6 casos cuya dimensión principal corresponde a cada dimensión;
- total: 42 casos.

### ¿Por qué 42 casos y seis por dimensión?

Se decidió utilizar una distribución simétrica de seis casos por dimensión para:

- garantizar que todas las dimensiones principales estuvieran representadas de forma equivalente;
- facilitar la comparación entre dimensiones;
- mantener un tamaño que permitiera una revisión manual exhaustiva de todas las respuestas.

Se trata de una **validación preliminar**, no de un benchmark masivo.

### Tipologías incluidas

La batería incorpora:

- pruebas nominales de conocimiento curricular;
- pruebas de frontera con restricciones combinadas;
- preguntas trampa con premisas falsas;
- casos adversariales y de seguridad.

---

## 8. Decisión clave: evaluación transversal de las siete dimensiones

Aunque cada caso tiene una **dimensión principal**, todas las respuestas se califican en las siete dimensiones.

La razón es que un sistema educativo real debe mantener simultáneamente múltiples propiedades. Por ejemplo, una respuesta a un caso diseñado para D7 debe seguir siendo factual, no alucinar y respetar la seguridad.

Por ello:

- 42 respuestas por perfil;
- 7 puntuaciones por respuesta;
- 294 juicios dimensionales por perfil;
- 882 puntuaciones por evaluador para los tres perfiles.

### Consecuencia y limitación

Esta decisión permite una visión integral, pero puede producir **saturación** en dimensiones que un caso no tensiona directamente. La memoria reconoce esta limitación y propone como trabajo futuro emplear esquemas de aplicabilidad condicional o pesos dinámicos según el tipo de caso.

---

## 9. Perfiles conversacionales comparados

Se emplea **el mismo modelo base** y se modifican únicamente las directrices de sistema. Esto permite aislar, en la medida del diseño experimental, el efecto de las instrucciones de rol.

### Perfil 1 — Asistente Base

Directriz general sin condicionamiento pedagógico específico:

“You are a helpful assistant”.

Funciona como línea de control del comportamiento por defecto del modelo Instruct.

### Perfil 2 — Tutor Directo

Enfoque expositivo:

- respuesta clara;
- rigor conceptual;
- adaptación al estudiante;
- ejemplos;
- sin prohibición específica de entregar directamente soluciones completas.

### Perfil 3 — Tutor Socrático

Enfoque de andamiaje:

- no entregar soluciones completas;
- diagnosticar errores;
- formular preguntas;
- proporcionar pistas graduadas;
- orientar el razonamiento del estudiante.

### ¿Por qué estos tres perfiles?

Para comparar:

1. una línea base sin directrices educativas específicas;
2. una estrategia pedagógica expositiva;
3. una estrategia pedagógica socrática.

Todo ello manteniendo constante modelo, batería y parámetros de inferencia.

---

## 10. Selección del modelo y entorno experimental

### Modelo

**Meta-Llama-3-8B-Instruct**

Configuración utilizada:

- tag Ollama: llama3:8b;
- cuantización: Q4_0;
- digest: 365c0bd3c000;
- motor de inferencia: Ollama v0.1.32;
- ejecución mediante API REST local /api/chat.

### ¿Por qué este modelo?

La selección responde a criterios operativos y metodológicos:

- pesos disponibles para ejecución local;
- posibilidad de conservar un entorno auditable y trazable;
- tamaño de 8B compatible con los recursos disponibles;
- variante Instruct preparada para seguimiento de instrucciones y diálogo;
- posibilidad de ejecutar exactamente el mismo modelo bajo los tres perfiles.

No se afirma que sea el mejor modelo educativo ni que represente a todos los LLMs.

---

## 11. Decisiones sobre los parámetros de inferencia

Se fijaron los mismos parámetros para los tres perfiles:

- temperatura: **T = 0,20**;
- top-p: **0,90**;
- repeat penalty: **1,10**;
- seed: **42**;
- num_ctx: **2048**.

### Razón

Los valores actúan como **variables de control**. No fueron optimizados para maximizar la puntuación de ninguno de los perfiles.

- T = 0,20 y top-p = 0,90: valores conservadores para reducir variabilidad manteniendo cierto margen de diversidad.
- repeat penalty = 1,10: penalización moderada de repeticiones.
- seed = 42: semilla arbitraria pero fija para favorecer comparabilidad.
- num_ctx = 2048: suficiente para la extensión de todos los casos y dentro de la capacidad del modelo.

### Decisión: una ejecución por caso

Cada caso se ejecutó una sola vez con semilla fija.

Esto permite un experimento controlado y trazable, pero **no permite interpretar HR como una probabilidad universal de alucinación**. Las tasas representan los fallos observados en esa ejecución concreta.

La repetición con múltiples semillas se deja para trabajo futuro.

---

## 12. Proceso experimental completo

El flujo final es:

1. **Diseño de los 42 casos de prueba.**
2. **Configuración del perfil conversacional.**
3. **Ejecución real mediante Ollama.**
4. **Almacenamiento de la respuesta completa y metadatos en JSON.**
5. **Evaluación manual con rúbrica 0–3 en D1–D7.**
6. **Normalización y validación de las anotaciones.**
7. **Cálculo automático de métricas.**
8. **Cálculo de concordancia inter-evaluador.**
9. **Generación de tablas y gráficos.**
10. **Aplicación de la regla Safety-First e interpretación de resultados.**

Se obtuvieron:

- 42 casos × 3 perfiles = **126 interacciones reales**;
- 126 × 7 = **882 puntuaciones por evaluador**.

---

## 13. Decisiones sobre la evaluación humana

### Dos evaluadores

Las 126 respuestas fueron evaluadas mediante la misma rúbrica por dos evaluadores.

- **Evaluador 1:** autor del trabajo y evaluador de referencia.
- **Evaluador 2:** segundo evaluador independiente con formación técnica en Informática.

### ¿Por qué se utilizan las puntuaciones de E1 para las métricas principales?

E1 se estableció como evaluador de referencia porque fue el responsable del diseño y operacionalización de la rúbrica.

E2 se utilizó para comprobar si otra persona podía aplicar el instrumento de forma suficientemente consistente.

### Decisión de cegamiento

Los evaluadores no accedieron:

- a las valoraciones del otro evaluador;
- a la etiqueta explícita del perfil de origen durante la calificación.

La etiqueta de perfil se restauró posteriormente en los datos estructurados para mantener la trazabilidad.

### Limitación del cegamiento

El cegamiento no puede considerarse absoluto: el estilo de ciertas respuestas podía permitir inferir indirectamente qué configuración había producido la salida.

---

## 14. Decisión sobre Kappa de Cohen

Se utilizó **Kappa de Cohen no ponderado** para evaluar acuerdo exacto.

$N_\kappa = 126 \times 7 = 882$

### ¿Por qué no ponderado si la escala 0–3 es ordinal?

Porque se decidió penalizar por igual cualquier discrepancia categorial y medir acuerdo exacto entre evaluadores.

Se reconoce que un Kappa ponderado podría aprovechar la naturaleza ordinal de la escala y se propone como extensión futura.

### Resultado

- $P_o = 0,9932$
- $P_e = 0,6260$
- $\kappa = 0,982$

La interpretación correcta es **alta consistencia de aplicación de la rúbrica en esta muestra**.

No significa que las puntuaciones sean necesariamente verdaderas desde el punto de vista disciplinar: dos evaluadores podrían coincidir en un mismo error.

---

## 15. Métricas utilizadas

### Media dimensional

Mide el comportamiento promedio en cada dimensión D1–D7 sobre las 42 respuestas de cada perfil.

### CR — Tasa de cumplimiento

Proporción de respuestas con puntuación igual o superior a 2 en una dimensión.

### CFR — Critical Failure Rate

Un caso se considera crítico cuando:

$s_{i,1}=0$ o $s_{i,2}=0$ o $s_{i,5}=0$.

D1, D2 y D5 se consideran no negociables porque corresponden respectivamente a:

- corrección factual;
- control de alucinaciones;
- seguridad e integridad.

### HR — Hallucination Rate

Se calcula específicamente sobre los casos de la subbatería de alucinaciones y cuenta aquellos en los que D2 = 0.

### IQE — Índice de Calidad Educativa

Convierte las medias dimensionales en una medida sintética 0–100.

Pesos definidos a priori:

- D1: 0,25;
- D2: 0,20;
- D3: 0,15;
- D4: 0,15;
- D5: 0,10;
- D6: 0,10;
- D7: 0,05.

---

## 16. Decisión sobre los pesos del IQE

Los pesos **no proceden de una estimación empírica ni se presentan como universales**.

Son una parametrización de referencia definida a priori.

### Criterio seguido

Se otorga mayor peso a:

1. factualidad;
2. control de alucinaciones;

porque una respuesta pedagógicamente atractiva pierde valor si transmite información falsa.

Claridad y feedback reciben un peso intermedio y aspectos como formato reciben menor peso.

### ¿Cómo se comprueba que el resultado no depende sólo de estos pesos?

Se realizó un análisis de sensibilidad empleando pesos iguales:

$w_d = 1/7$

Resultados equiponderados:

- Base: **83,7**
- Directo: **89,1**
- Socrático: **94,4**

La comparación relativa se mantiene, por lo que el orden observado no depende críticamente del vector de pesos elegido.

---

## 17. Decisión Safety-First

El IQE resume calidad, pero **no se utiliza como única regla de aceptación**.

Se define un criterio Safety-First:

> Si existe algún fallo crítico en D1, D2 o D5, el perfil no puede considerarse apto para despliegue docente autónomo, independientemente de que su IQE sea elevado.

### ¿Por qué?

Porque un promedio puede compensar matemáticamente un fallo grave.

Ejemplo conceptual:

- un chatbot puede ser excelente en claridad, adaptación y formato;
- pero si inventa información o cede ante fraude académico;
- una media elevada no debería ocultar ese riesgo.

Esta separación entre **calidad global** y **riesgo crítico** constituye una de las ideas principales del trabajo.

---

## 18. Resultados experimentales

| Perfil | IQE | CFR | HR | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Asistente Base** | **84,1** | **11,9 %** | **33,3 %** | 2,55 | 2,86 | 2,83 | 1,86 | 2,76 | 2,00 | 2,71 |
| **Tutor Directo** | **87,9** | **14,3 %** | **33,3 %** | 2,52 | 2,86 | 2,88 | 1,93 | 2,76 | 3,00 | 2,76 |
| **Tutor Socrático** | **93,0** | **11,9 %** | **16,7 %** | 2,48 | 2,88 | 2,93 | **2,81** | **2,93** | 3,00 | **2,81** |

### Subbatería específica de feedback

Media D4 en FEED:

- Base: **1,17**
- Directo: **1,50**
- Socrático: **1,67**

El Socrático obtiene la mayor media de feedback, aunque no resuelve correctamente todos los diagnósticos.

---

## 19. Qué demuestran realmente los resultados

### 19.1. El System Prompt modifica el comportamiento

El mismo modelo base produce comportamientos diferentes cuando se modifica la directriz de sistema.

El Tutor Socrático mejora especialmente en:

- D4;
- D5;
- D7;
- calidad global IQE.

### 19.2. Una mejora global no implica menor riesgo

El Tutor Directo obtiene mayor IQE que la línea Base:

- Base: 84,1
- Directo: 87,9

pero presenta **mayor CFR**:

- Base: 11,9 %
- Directo: 14,3 %

Esto muestra que una única métrica agregada no es suficiente.

### 19.3. El Socrático tampoco es “seguro” por defecto

Aunque obtiene IQE = 93,0 y la mayor D4, mantiene CFR = 11,9 %.

Por ello tampoco supera Safety-First.

### Conclusión experimental principal

> **Ninguno de los tres perfiles puede considerarse apto para un despliegue docente autónomo sin salvaguardas adicionales bajo el criterio definido en este trabajo.**

---

## 20. Qué NO demuestra el experimento

Es importante no sobreinterpretar los resultados.

El trabajo **no demuestra** que:

- Llama 3 tenga una probabilidad universal de alucinación del 16,7 % o 33,3 %;
- el Tutor Socrático sea universalmente superior en todos los contextos;
- D4 = 2,81 implique que los estudiantes aprendan más;
- los pesos del IQE sean universales;
- los siete constructos sean completamente independientes;
- 42 casos sean suficientes para certificar un sistema educativo;
- los resultados se generalicen automáticamente a otros modelos;
- la metodología sustituya una evaluación pedagógica con estudiantes reales.

Lo que sí demuestra es que **la metodología resulta viable y suficientemente sensible para identificar diferencias relevantes entre configuraciones en esta validación preliminar**.

---

## 21. Limitaciones asumidas deliberadamente

1. **Un único modelo:** Meta-Llama-3-8B-Instruct.
2. **42 casos:** volumen suficiente para una validación preliminar, pero no para un benchmark exhaustivo.
3. **Una ejecución por caso:** no se estudia variabilidad entre semillas.
4. **Seed fija = 42:** facilita comparabilidad, pero no caracteriza toda la distribución de comportamiento.
5. **Predominio del español con un modelo cuya documentación prioriza inglés.**
6. **Sólo texto y código:** se excluyen imágenes, diagramas y otros escenarios multimodales.
7. **D4 es una operacionalización del comportamiento pedagógico**, no una medición del aprendizaje real de estudiantes.
8. **Los casos son escenarios de testing**, no conversaciones longitudinales naturales de aula.
9. **Posible efecto techo**, especialmente en perfiles instruidos.
10. **Posible saturación transversal**, porque las siete dimensiones se califican en todos los casos.
11. **Dependencia parcial entre constructos**, especialmente D1 y D2.
12. **Posible sesgo del investigador**, ya que E1 es también el autor.
13. **Panel reducido de evaluadores**, sin especialistas independientes para cada dominio curricular.
14. **Cegamiento imperfecto**, porque el estilo lingüístico podría revelar indirectamente el perfil.
15. **No estacionariedad de modelos comerciales y ecosistemas de IA.**

---

## 22. Decisiones metodológicas: registro consolidado

| Decisión | Elección realizada | Motivo | Consecuencia / límite |
|---|---|---|---|
| Tipo de evaluación | Caja negra sobre comportamiento conversacional | Evaluar el sistema desde la salida observable | No se estudian pesos internos |
| Modalidad | Texto y código | Delimitar el alcance | No se cubre multimodalidad |
| Nº de dimensiones | 7 | Integrar software, seguridad y pedagogía | Algunas dimensiones pueden correlacionar |
| Escala | 0–3 sin punto medio | Forzar discriminación entre insuficiente/aceptable | No elimina todos los sesgos |
| Nivel 3 en D1 | Correcto + suficientemente completo | Evitar premiar evasión o respuestas incompletas | Requiere juicio disciplinar |
| Nº de casos | 42 | Equilibrio entre cobertura y auditabilidad manual | Validación preliminar |
| Casos por dimensión principal | 6 | Simetría de cobertura | Muestra limitada |
| Evaluación transversal | D1–D7 para todas las respuestas | Exigir calidad integral | Puede generar saturación |
| Perfiles | Base, Directo y Socrático | Comparar control + dos enfoques pedagógicos | No cubre todas las estrategias posibles |
| Modelo | Meta-Llama-3-8B-Instruct | Local, auditable, 8B, Instruct | No representa a todos los LLM |
| Runtime | Ollama local | Control y trazabilidad | Dependencia del entorno local |
| Cuantización | Q4_0 | Viabilizar ejecución con recursos disponibles | Puede diferir del modelo a precisión completa |
| Temperatura | 0,20 | Reducir variabilidad | No es un óptimo universal |
| top-p | 0,90 | Muestreo conservador con diversidad | No fue optimizado |
| repeat penalty | 1,10 | Penalización moderada de repetición | Elección operacional |
| seed | 42 | Comparabilidad | No estudia variabilidad estocástica |
| num_ctx | 2048 | Suficiente para todos los casos | No explota la ventana máxima |
| Nº de ejecuciones | 1 por caso y perfil | Experimento controlado y manejable | HR no es probabilidad universal |
| Evaluador de referencia | E1 | Responsable del diseño de la rúbrica | Posible sesgo del investigador |
| Segundo evaluador | E2 para consistencia | Estimar reproducibilidad de aplicación | Panel reducido |
| Cegamiento | Etiqueta explícita del perfil oculta | Reducir sesgo de expectativa | El estilo podía delatar perfil |
| Kappa | Cohen no ponderado | Medir acuerdo exacto | No aprovecha distancia ordinal |
| N de Kappa | 882 pares | 126 respuestas × 7 dimensiones | Acuerdo sobre esta muestra |
| Pesos IQE | 0,25/0,20/0,15/0,15/0,10/0,10/0,05 | Priorizar factualidad y alucinaciones | Parametrización propia |
| Sensibilidad | Repetición con pesos iguales | Comprobar dependencia del vector de pesos | No sustituye validación externa |
| Dimensiones críticas | D1, D2 y D5 | Factualidad, alucinaciones y seguridad no negociables | Regla conservadora |
| Safety-First | CFR > 0 impide despliegue autónomo | Evitar compensación de fallos graves por medias altas | No equivale a norma institucional |
| HR | D2 = 0 en subbatería de alucinaciones | Aislar fallos explícitos ante premisas falsas | Muestra de seis casos |
| Métricas principales | Puntuaciones de E1 | Evaluador de referencia | Se contrasta con Kappa de E2 |
| Datos | Respuestas y anotaciones versionadas | Trazabilidad y réplica | La réplica puede variar por entorno |
| Código | Python modular | Automatizar análisis y visualización | Evaluación cualitativa sigue siendo humana |
| Regla de despliegue | Diagnóstico, no certificación | Proporcionar evidencia para una decisión | No sustituye validación institucional |

---

## 23. Arquitectura del software

El proyecto separa responsabilidades:

- **src/utils/loader_prompts.py:** carga de casos.
- **src/evaluador/ejecutor_pruebas.py:** ejecución de inferencias vía Ollama.
- **src/analisis/metricas_tfg.py:** métricas matemáticas.
- **src/analisis/analizador_experimentos.py:** agregación global.
- **src/analisis/calcular_concordancia_evaluadores.py:** Kappa global y por dimensión.
- **src/analisis/importar_evaluaciones_humanas.py:** normalización de anotaciones.
- **src/analisis/validar_datos_evaluacion.py:** validación de integridad.
- **src/evaluador/evaluador_llm_judge.py:** motor independiente de evaluación automática LLM-as-a-Judge.
- **src/analisis/analizar_concordancia_llm_judge.py:** pipeline estadístico de concordancia Humano-IA.
- **src/visualizacion/generar_graficos.py:** generación de gráficos principales.
- **src/visualizacion/generar_graficos_llm_judge.py:** generación de gráficos vectoriales del juez automático.
- **tests unitarios:** comprobación de fórmulas, parser y condiciones de frontera.

La automatización **no sustituye el juicio humano de la rúbrica**; automatiza la ejecución, validación, agregación, cálculo y visualización.

---

## 24. Extensión experimental: Evaluación automática mediante LLM-as-a-Judge

### Motivación y cuello de botella humano
En el marco principal del TFG, la generación de respuestas, almacenamiento y cálculo de métricas están automatizados, pero la aplicación de la rúbrica $D_1$--$D_7$ requiere evaluación manual. Para estudiar la escalabilidad de la metodología frente a baterías masivas de pruebas, se incorporó una extensión experimental basada en **LLM-as-a-Judge**.

### Arquitectura y salvaguardas metodológicas
1. **Evaluación ciega respecto al perfil generador y a las evaluaciones humanas**: El juez recibe el prompt discente, ground truth, criterio de fallo crítico y la rúbrica completa 0–3, pero **no conoce el perfil** que generó la respuesta (Base, Directo o Socrático) para evitar sesgos pedagógicos preconcebidos.
2. **Aislamiento de datos**: El juez **nunca recibe las calificaciones de E1 ni E2**. Sus salidas se custodian en `data/evaluaciones/llm_judge/` (separando trazas raw y JSON normalizado), manteniendo intactos los datos humanos de referencia.
3. **Prompt congelado**: Se utiliza `judge_prompt_v1`, congelado antes del análisis para evitar optimizar el prompt contra el conjunto de validación.
4. **Modelo juez independiente**: Se establece como modelo de referencia `Qwen2.5-14B-Instruct` (configuración de baja variabilidad, $T=0.0$, top-p=0.9, seed=42) para evitar autopreferencia con el evaluado `Meta-Llama-3-8B-Instruct`.

### Pipeline de análisis de concordancia Humano--IA
- **Pipeline de concordancia ($N_\kappa=882$):** Cálculo de $\kappa(\text{Juez}, E_1)$ y $\kappa(\text{Juez}, E_2)$, acuerdo observado ($P_o$), acuerdo esperado ($P_e$) y $\text{MAE}$ por dimensión.
- **Análisis de granularidad:** Desglose de distribución de deltas ($|\Delta| \in \{0, 1, 2, 3\}$), matrices de confusión $4 \times 4$ y análisis de discrepancias direccionales.
- **Control de fallos críticos (Safety-First):** Cálculo de la tasa de falsos negativos en $D_1$, $D_2$ y $D_5$ para verificar que el juez no apruebe respuestas con alucinaciones o vulneraciones de seguridad ética.

### Propuesta futura: Sistema híbrido Humano-in-the-Loop
El juez automático no reemplaza la supervisión humana, sino que actúa como **filtro de triaje masivo de primer nivel**:
$$\text{LLM Judge (100\% pruebas)} \longrightarrow \begin{cases} \text{Aprobación directa}, & \text{si cumple todas las dimensiones con alta certidumbre} \\ \text{Auditoría Humana}, & \text{si detecta fallo crítico ($S_d=0$), baja confianza o discrepancias} \end{cases}$$

---

## 25. Aportaciones principales

### Aportación metodológica

Un marco operativo que traduce un problema abierto de lenguaje natural a dimensiones y criterios observables.

### Aportación de testing

Separar:

- calidad global;
- fallos críticos;
- alucinaciones.

### Aportación pedagógica

No tratar un tutor educativo como un simple sistema de question answering: se evalúa si diagnostica, guía y adapta.

### Aportación experimental

Una batería real aplicada a 126 interacciones de un modelo ejecutado localmente, complementada con un protocolo de evaluación automática mediante LLM-as-a-Judge.

### Aportación software

Una implementación reproducible y versionada para repetir el análisis y extenderlo.

### Aportación de datos

Casos, respuestas, anotaciones humanas y trazas experimentales disponibles para inspección y réplica.

---

## 26. Trabajo futuro derivado de las decisiones actuales

Las limitaciones del diseño conducen directamente a las siguientes extensiones:

- sistemas híbridos de triaje Humano-in-the-Loop;
- ensambles de jueces automáticos y especialización de modelos por dimensión;
- paneles multidisciplinares de evaluadores;
- más modelos y materias;
- múltiples semillas por caso;
- casos adversariales más difíciles;
- pesos o aplicabilidad condicional por dimensión;
- Kappa ponderado;
- evaluación multimodal;
- testing metamórfico;
- generación automática de variantes de prompts;
- integración continua CI/CD;
- evaluación de RAG y fidelidad de fuentes;
- estudios con estudiantes reales para medir eficacia educativa.

---

## 27. Cómo explicar el TFG en una defensa

### En 20 segundos

> El trabajo aborda un problema de testing: un chatbot basado en LLM no tiene una única salida correcta y, en educación, una respuesta puede ser fluida pero falsa, insegura o pedagógicamente inadecuada. Por eso diseño una metodología multidimensional con rúbricas, casos de prueba, métricas de calidad y un criterio Safety-First, la valido sobre tres configuraciones del mismo Llama 3, y formulo una extensión experimental para automatizar la rúbrica mediante LLM-as-a-Judge.

### En una frase

> **El TFG propone una forma sistemática de comprobar no sólo si un chatbot educativo responde bien, sino si responde de forma factual, segura y pedagógicamente adecuada, evitando que una nota media alta oculte fallos críticos.**

### Hallazgo que conviene recordar

> **El Tutor Directo mejora el IQE respecto al Asistente Base, pero empeora la tasa de fallos críticos; por tanto, mejorar la calidad global no implica necesariamente reducir el riesgo.**

---

## 27. Mensaje final

El proyecto no pretende declarar que un determinado LLM es “bueno” o “malo” para educación de forma universal.

Su aportación es proporcionar una **metodología de ingeniería del software para producir evidencia estructurada sobre su comportamiento**, haciendo visibles de forma separada:

- calidad conceptual;
- calidad pedagógica;
- cumplimiento;
- seguridad;
- fallos críticos.

La idea final del TFG es que **la adopción de IA generativa en educación no debería decidirse únicamente por lo convincente que parezca una respuesta ni por una puntuación global**, sino mediante pruebas sistemáticas que permitan identificar explícitamente qué funciona, qué falla y qué riesgos siguen siendo inaceptables.
