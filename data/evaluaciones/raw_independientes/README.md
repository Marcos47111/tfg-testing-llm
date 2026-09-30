# Datasets de Evaluación Humana Independiente Original (Fase 1)

Este directorio contiene las anotaciones humanas originales obtenidas durante la **Fase 1** del experimento de evaluación humana (doble evaluación a ciegas e independiente):

- `evaluador_1_original.csv` / `evaluador_1_original.json`: 126 registros evaluados por el Evaluador 1 con sus justificaciones cualitativas originales.
- `evaluador_2_original.csv` / `evaluador_2_original.json`: 126 registros evaluados por el Evaluador 2 con sus justificaciones cualitativas originales.

---

## 1. Procedencia y Protocolo de Doble Evaluación a Ciegas

1. **Procedencia histórica y trazabilidad:** Estos ficheros preservan las puntuaciones y justificaciones correspondientes al estado histórico de la doble anotación independiente previo a las revisiones posteriores, reconstruido a partir de las versiones conservadas en el historial Git (commit `9e93d60fccc434808a9fdbbd18d91289138474ce`).
2. **Independencia estricta:** Ambos evaluadores recibieron los 126 casos anonimizados y asignaron puntuaciones (0 a 3) y justificaciones de forma independiente, sin comunicación previa ni acceso a las notas del otro evaluador.
3. **Concordancia inter-evaluador original ($\kappa$ inicial):**
   - **Kappa de Cohen global no ponderado:** $\kappa = 0{,}9742$ ($P_e = 0{,}8243$)
   - **Kappa de Cohen ponderado lineal:** $\kappa_{\text{lineal}} = 0{,}9807$
   - **Kappa de Cohen ponderado cuadrático:** $\kappa_{\text{cuadrático}} = 0{,}9884$
   - **Porcentaje de acuerdo exacto ($P_o$):** $99{,}55\%$ ($878 / 882$ juicios coincidentes, únicamente 4 discrepancias de 1 nivel).
4. **Distribución por dimensiones ($\kappa$ original de Fase 1):**
   - $D_1$ (Corrección Factual): $\kappa = 0{,}8542$ ($\kappa_{\text{lineal}} = 0{,}9319$)
   - $D_2$ (Control de Alucinaciones): $\kappa = 1{,}0000$
   - $D_3$ (Claridad Didáctica): $\kappa = 0{,}9291$
   - $D_4$ (Utilidad Pedagógica): $\kappa = 0{,}9533$ ($\kappa_{\text{lineal}} = 0{,}9691$)
   - $D_5$ (Robustez y Seguridad): $\kappa = 1{,}0000$
   - $D_6$ (Adaptación al Nivel): $\kappa = 0{,}9822$
   - $D_7$ (Seguimiento de Instrucciones): $\kappa = 1{,}0000$

---

## 2. Transición a la Fase 2 (Revisión, Calibración y Consolidación del Gold Standard)

Tras el cálculo de la concordancia inter-evaluador independiente de la Fase 1, se procedió a la **Fase 2 (Revisión, Calibración y Consolidación del Gold Standard)**, donde se revisaron los casos, se resolvieron discrepancias y se calibraron las asignaciones críticas frente a la rúbrica formal para conformar el *Gold Standard* consolidado de referencia publicado en `data/evaluaciones/`.
