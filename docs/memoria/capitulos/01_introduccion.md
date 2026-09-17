# 1. Introducción

## 1.1. Contexto y motivación
En los últimos años, la Inteligencia Artificial Generativa (IAG) y, en particular, los Modelos de Lenguaje de Gran Tamaño (*Large Language Models*, LLMs) han experimentado una evolución sin precedentes (Vaswani et al., 2017; Achiam et al., 2023). Su capacidad para procesar, sintetizar y generar lenguaje natural con una fluidez notable ha propiciado su rápida adopción en múltiples sectores socioeconómicos, destacando con especial fuerza en el ámbito de la educación y el aprendizaje asistido (Kasneci et al., 2023).

Los asistentes conversacionales basados en LLMs ofrecen oportunidades formativas extraordinarias: tutoría personalizada disponible las 24 horas, adaptación del ritmo de estudio a las necesidades individuales del alumnado, resolución interactiva de dudas y generación instantánea de explicaciones pedagógicas multimodales. Sin embargo, su despliegue masivo en las aulas plantea profundos desafíos técnicos, pedagógicos y éticos que exigen respuestas rigurosas desde la Ingeniería del Software.

## 1.2. Planteamiento del problema
A diferencia del software informático clásico, donde el comportamiento del sistema está gobernado por algoritmos deterministas con reglas lógicas explícitas, los LLMs operan como modelos estadísticos de muestreo de distribuciones probabilísticas sobre secuencias de tokens. Esta naturaleza intrínsecamente estocástica y generativa genera problemas críticos:

1. **Generación de alucinaciones y desinformación:** Los modelos tienden a generar afirmaciones falsas, fórmulas incorrectas o fuentes bibliográficas ficticias presentadas con un elevado tono de seguridad (*syndromic overconfidence*) (Ji et al., 2023; Lin et al., 2022).
2. **Inadecuación pedagógica y descarga cognitiva:** Un chatbot que se limite a entregar soluciones resueltas directamente fomenta la pasividad y la dependencia cognitiva (*cognitive offloading*), anulando el pensamiento crítico del estudiante.
3. **Vulnerabilidades de seguridad e integridad académica:** La susceptibilidad ante inyecciones de instrucciones (*prompt injection*) o técnicas de evasión (*jailbreaks*) compromete la integridad académica y la seguridad del alumnado (Wei et al., 2023; UNESCO, 2023).
4. **El Problema del Oráculo en el Testing:** En la disciplina de verificación y validación tradicional, el *Problema del Oráculo* (*The Oracle Problem*) (Barr et al., 2015) impide validar las salidas de los LLMs mediante aserciones binarias exactas (`assert output == expected`), requiriendo nuevos marcos de evaluación multidimensional.

## 1.3. Justificación del trabajo
Resulta imperativo dotar a la comunidad académica, docente e ingenieril de una metodología de testing estructurada, reproducible y científicamente fundamentada que permita evaluar de forma sistemática y holística la calidad, fiabilidad, seguridad y valor didáctico de los chatbots educativos antes y durante su despliegue formativo.

Este Trabajo de Fin de Grado aborda esta necesidad desarrollando un marco metodológico integral, fundamentado en los estándares internacionales de calidad del software (ISO/IEC 25010), las teorías pedagógicas consolidadas (Zona de Desarrollo Próximo de Vygotsky y modelos de feedback formativo de Hattie & Timperley) y los avances punteros en evaluación de modelos generativos (Zheng et al., 2023).

## 1.4. Objetivos del trabajo
### 1.4.1. Objetivo general
Diseñar, formalizar y validar experimentalmente una metodología sistemática de testing para evaluar sistemas conversacionales basados en LLMs en contextos educativos o de asistencia al aprendizaje, orientada a medir su corrección conceptual, control de alucinaciones, claridad didáctica, utilidad formativa, robustez de seguridad y adaptación al nivel del discente.

### 1.4.2. Objetivos específicos
1. Analizar las diferencias epistemológicas y operacionales entre el testing de software tradicional y la evaluación de sistemas basados en LLMs.
2. Formalizar un conjunto ortogonal de 7 dimensiones de calidad educativa alineadas con el estándar ISO/IEC 25010 y la literatura de AIED.
3. Diseñar una matriz de rúbricas de evaluación cualitativa en escala forzada (0 a 3) que mitigue el sesgo de tendencia central y estandarice la evaluación humana y automática.
4. Definir un conjunto de métricas cuantitativas y un Índice Global de Calidad Educativa ($IQE$) basado en el principio *Safety-First*.
5. Construir una batería calibrada de casos de prueba estructurados y aplicarla experimentalmente sobre diferentes configuraciones de chatbot para validar la aplicabilidad del marco.

## 1.5. Preguntas de investigación
* **PI1:** ¿Cómo se puede estructurar una metodología de testing para LLMs que evalúe simultáneamente el rigor factual y la calidad pedagógica?
* **PI2:** ¿En qué medida el diseño del *system prompt* (expositivo vs socrático) condiciona la seguridad y el andamiaje del chatbot educativo?
* **PI3:** ¿Es posible mitigar el impacto del problema del oráculo mediante rúbricas analíticas normalizadas?

## 1.6. Alcance y limitaciones iniciales
El trabajo se acota a la evaluación externa del comportamiento conversacional (caja negra) en texto en lengua española e inglesa en dominios académicos multidisciplinares. Queda fuera del alcance el entrenamiento desde cero de modelos fundacionales.

## 1.7. Estructura del documento
La memoria se organiza en 8 capítulos que cubren desde los fundamentos teóricos hasta la propuesta metodológica, experimentación, discusión y anexos detallados.
