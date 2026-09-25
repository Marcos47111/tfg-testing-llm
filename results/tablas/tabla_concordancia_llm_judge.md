# Tabla Comparativa de Concordancia Humano-IA (LLM-as-a-Judge)

**Kappa Global Juez vs E1 ($\kappa$):** 0.19 (Po = 0.6349, Pe = 0.5493, MAE = 0.494) - *Acuerdo leve*
**Kappa Global Juez vs E2 ($\kappa$):** 0.1856 (Po = 0.6327, Pe = 0.5489, MAE = 0.499)
**Referencia Humana E1 vs E2 ($\kappa$):** 0.9818
**Total juicios emparejados:** 882 pares.

| Dimensión | Kappa (Juez vs E1) | P_o | P_e | MAE | Kappa (Juez vs E2) | Kappa (E1 vs E2) | Media E1 | Media Juez | Sesgo | Nivel de Acuerdo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| D1: Factualidad | 0.2613 | 0.5873 | 0.4413 | 0.54 | 0.2458 | 0.9802 | 2.516 | 2.23 | -0.286 | Acuerdo aceptable |
| D2: Alucinaciones | 0.3265 | 0.8889 | 0.835 | 0.262 | 0.3262 | 0.9132 | 2.865 | 2.683 | -0.182 | Acuerdo aceptable |
| D3: Claridad | 0.0758 | 0.5159 | 0.4762 | 0.587 | 0.0473 | 0.8937 | 2.881 | 2.405 | -0.476 | Acuerdo leve |
| D4: Feedback Pedagógico | 0.0663 | 0.3889 | 0.3455 | 0.754 | 0.0685 | 0.9853 | 2.198 | 2.206 | +0.008 | Acuerdo leve |
| D5: Seguridad | 0.4207 | 0.9048 | 0.8356 | 0.159 | 0.4207 | 1.0 | 2.817 | 2.786 | -0.031 | Acuerdo moderado |
| D6: Adaptación al Nivel | -0.0259 | 0.4762 | 0.4894 | 0.627 | -0.0146 | 0.982 | 2.667 | 2.437 | -0.23 | Sin acuerdo (discrepancia sistemática) |
| D7: Directrices | 0.086 | 0.6825 | 0.6527 | 0.532 | 0.086 | 1.0 | 2.762 | 2.516 | -0.246 | Acuerdo leve |
