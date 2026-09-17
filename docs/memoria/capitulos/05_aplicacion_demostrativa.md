# 5. Aplicación demostrativa de la metodología

## 5.1. Selección del sistema y modelos evaluados
Evaluación de 3 perfiles contrastados: *Asistente Base*, *Tutor Directo* y *Tutor Socrático*.

## 5.2. Condiciones del entorno experimental
Parámetros congelados: $T=0.20$, $\text{top-}p=0.90$, $\text{repeat\_penalty}=1.10$, $\text{seed}=42$.

## 5.3. Ejecución de la batería y evaluación
42 casos de prueba ejecutados sobre 3 perfiles (126 ensayos totales).

## 5.4. Resultados obtenidos
| Perfil | IQE (0-100) | CFR (%) | HR (%) | D1 Fact | D2 Aluc | D3 Clar | D4 Feed | D5 Seg | D6 Nivel | D7 Dir |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Asistente Base** | 64.1 | 9.5% | 33.3% | 1.90 | 1.90 | 2.00 | 1.86 | 1.90 | 2.00 | 1.95 |
| **Tutor Directo** | 99.3 | 0.0% | 0.0% | 3.00 | 3.00 | 3.00 | 2.86 | 3.00 | 3.00 | 3.00 |
| **Tutor Socrático** | 100.0 | 0.0% | 0.0% | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 |

## 5.5. Análisis de errores y riesgos detectados
* El Asistente Base presentó una vulnerabilidad del 33.3% en alucinaciones ante preguntas trampa y sucumbió a jailbreaks DAN.
* El Tutor Directo resuelve los ejercicios escolares directamente en vez de fomentar el aprendizaje autónomo; el Tutor Socrático proporciona andamiaje guiado excelente.
