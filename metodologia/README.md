# Propuesta Metodológica de Testing

Este directorio contiene la formalización teórica y práctica de la metodología de evaluación de chatbots educativos.

## Estructura y Documentación

* **[`justificacion_y_fundamentos.md`](justificacion_y_fundamentos.md)**: Fundamentación científica, teórica (ISO 25010, ZDP de Vygotsky, Bloom, Hattie), psicométrica y matemática de todas las decisiones metodológicas.
* **`dimensiones/`**: Fichas descriptivas de cada dimensión evaluada (Definición, Justificación pedagógica, Indicadores observables, Criterios de aprobado/fallo).
  * `01_correccion_factual.md`
  * `02_control_alucinaciones.md`
  * `03_claridad_didactica.md`
  * `04_utilidad_pedagogica_feedback.md`
  * `05_robustez_seguridad.md`
  * `06_adaptacion_nivel.md`
  * `07_seguimiento_instrucciones.md`
* **`rubricas/`**: Rúbricas estandarizadas con niveles cualitativos (escala forzada 0 a 3), matriz general y guía del evaluador.
* **`metricas/`**: Fórmulas matemáticas para calcular puntuación media por dimensión ($\bar{S}_d$), tasa de cumplimiento ($CR_d$), tasa de fallos críticos ($CFR$), tasa de alucinación ($HR$) e índice global ponderado ($IQE$).
