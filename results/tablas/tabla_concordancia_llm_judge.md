# Tabla Comparativa de Concordancia Humano-IA (LLM-as-a-Judge)

**Kappa Global Juez vs E1 ($\kappa$):** 0.8286 (Po = 0.941, Pe = 0.656, MAE = 0.088) - *Acuerdo casi perfecto / Excelente*
**Kappa Global Juez vs E2 ($\kappa$):** 0.8487 (Po = 0.9478, Pe = 0.6554, MAE = 0.082)
**Referencia Humana E1 vs E2 ($\kappa$):** 0.9818
**Total juicios emparejados:** 126 respuestas $\times$ 7 dimensiones = 882 pares.

| Dimensión | Kappa (Juez vs E1) | P_o | P_e | MAE | Kappa (Juez vs E2) | Kappa (E1 vs E2) | Media E1 | Media Juez | Sesgo | Nivel de Acuerdo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| D1: Factualidad | 0.57 | 0.8651 | 0.6863 | 0.222 | 0.5955 | 0.9802 | 2.516 | 2.738 | +0.222 | Acuerdo moderado |
| D2: Alucinaciones | 0.9132 | 0.9921 | 0.9086 | 0.008 | 1.0 | 0.9132 | 2.865 | 2.873 | +0.008 | Acuerdo casi perfecto / Excelente |
| D3: Claridad | -0.0176 | 0.9127 | 0.9142 | 0.135 | 0.2939 | 0.8937 | 2.881 | 2.984 | +0.103 | Sin acuerdo (discrepancia sistemática) |
| D4: Feedback Pedagógico | 0.8761 | 0.9365 | 0.4876 | 0.071 | 0.8926 | 0.9853 | 2.198 | 2.254 | +0.056 | Acuerdo casi perfecto / Excelente |
| D5: Seguridad | 0.5789 | 0.9365 | 0.8492 | 0.079 | 0.5789 | 1.0 | 2.817 | 2.833 | +0.016 | Acuerdo moderado |
| D6: Adaptación al Nivel | 0.982 | 0.9921 | 0.5582 | 0.008 | 1.0 | 0.982 | 2.667 | 2.675 | +0.008 | Acuerdo casi perfecto / Excelente |
| D7: Directrices | 0.65 | 0.9524 | 0.8639 | 0.095 | 0.65 | 1.0 | 2.762 | 2.857 | +0.095 | Acuerdo sustancial |
