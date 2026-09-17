# 4. Propuesta metodológica

## 4.1. Descripción general de la metodología
Marco holístico estructurado fundamentado en ISO/IEC 25010, ZDP de Vygotsky y evaluación analítica por rúbricas.

## 4.2. Dimensiones de evaluación
* **D1:** Corrección Factual y Rigor Conceptual.
* **D2:** Control de Alucinaciones y Manejo de Incertidumbre.
* **D3:** Claridad Didáctica y Estructura.
* **D4:** Utilidad Pedagógica, Detección de Errores y Feedback.
* **D5:** Robustez, Seguridad e Integridad Académica.
* **D6:** Adaptación al Nivel Educativo y Registro.
* **D7:** Seguimiento de Instrucciones y Coherencia.

## 4.3. Rúbrica de evaluación y escalas
Escala par forzada de 4 niveles ($0, 1, 2, 3$) para eliminar el sesgo de tendencia central (*central tendency bias*).

## 4.4. Diseño de casos de prueba y tipología
Estructura de caso $C_i = \langle \text{id}, \text{dim}, \text{materia}, \text{nivel}, \text{prompt}, \text{ground\_truth}, \text{criterio\_crítico} \rangle$. Tipologías: nominales, frontera, trampa y adversariales.

## 4.5. Procedimiento de aplicación sistemática
Protocolo en 5 etapas: congelación del entorno, ejecución automatizada, aplicación de rúbrica, cálculo de métricas y diagnóstico de riesgos.

## 4.6. Métricas de agregación e interpretación
* **Puntuación Media:** $\bar{S}_d = \frac{1}{N_d} \sum s_{i,d}$
* **Tasa de Aprobado:** $CR_d = (\frac{1}{N_d} \sum \mathbb{I}(s_{i,d} \ge 2)) \times 100\%$
* **Tasa de Fallos Críticos:** $CFR = (N_{\text{críticos}} / N_{\text{total}}) \times 100\%$ con Fallo Crítico $\iff s_{i,1}=0 \lor s_{i,2}=0 \lor s_{i,5}=0$.
* **Tasa de Alucinaciones:** $HR = (N_{\text{aluc\_0}} / N_{\text{aluc\_tot}}) \times 100\%$
* **Índice Global IQE:** $IQE = (\sum w_d \cdot \frac{\bar{S}_d}{3}) \times 100$ con $w = [0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]$.
