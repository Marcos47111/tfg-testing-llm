# Datasets de Evaluación Humana Independiente Original (Fase 1)

Este directorio contiene las anotaciones humanas originales obtenidas durante la **Fase 1** del experimento de evaluación humana (doble evaluación a ciegas e independiente):

- `evaluador_1_original.csv` / `evaluador_1_original.json`: 126 registros evaluados por el Evaluador 1 con sus justificaciones cualitativas originales.
- `evaluador_2_original.csv` / `evaluador_2_original.json`: 126 registros evaluados por el Evaluador 2 con sus justificaciones cualitativas originales.

---

## 1. Procedencia y Protocolo de Doble Evaluación a Ciegas

1. **Independencia estricta:** Ambos evaluadores recibieron los 126 casos anonimizados y asignaron puntuaciones (0 a 3) y justificaciones de forma independiente, sin comunicación previa ni acceso a las notas del otro evaluador.
2. **Concordancia inter-evaluador original ($\kappa$ inicial):**
   - **Kappa de Cohen global no ponderado:** $\kappa = 0{,}9742$
   - **Kappa de Cohen ponderado lineal:** $\kappa_{\text{lineal}} = 0{,}9807$
   - **Kappa de Cohen ponderado cuadrático:** $\kappa_{\text{cuadrático}} = 0{,}9884$
   - **Porcentaje de acuerdo exacto ($P_o$):** $99{,}55\%$ ($878 / 882$ juicios coincidentes, únicamente 4 discrepancias de 1 nivel).
3. **Distribución por dimensiones ($\kappa$ original):**
   - $D_1$ (Corrección Factual): $\kappa = 0{,}8542$
   - $D_2$ (Control de Alucinaciones): $\kappa = 1{,}0000$
   - $D_3$ (Claridad Didáctica): $\kappa = 0{,}9291$
   - $D_4$ (Utilidad Pedagógica): $\kappa = 0{,}9533$
   - $D_5$ (Robustez y Seguridad): $\kappa = 1{,}0000$
   - $D_6$ (Adaptación al Nivel): $\kappa = 0{,}9822$
   - $D_7$ (Seguimiento de Instrucciones): $\kappa = 1{,}0000$

---

## 2. Transición a la Fase 2 (Adjudicación y Consolidación)

Tras el cálculo de la concordancia inter-evaluador sobre estos datos independientes, se procedió a la **Fase 2 (Adjudicación y Calibración de Consenso)**, donde se revisaron los casos discrepantes y se calibraron las asignaciones críticas para conformar el *Gold Standard* consolidado de referencia publicado en `data/evaluaciones/`.
