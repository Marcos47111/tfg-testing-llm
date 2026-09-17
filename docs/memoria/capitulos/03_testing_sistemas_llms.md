# 3. Testing de sistemas basados en LLMs

## 3.1. Fundamentos del testing tradicional de software
El testing clásico (ISO/IEC/IEEE 29119, ISO/IEC 25010) parte de funciones deterministas $Y = f(X)$ evaluables mediante aserciones booleanas directas (`assert output == expected`).

## 3.2. Diferencias entre testing tradicional y testing de LLMs
Los LLMs sufren el **Problema del Oráculo** (*The Oracle Problem*, Barr et al., 2015):
* Espacio de salida infinito y abierto en lenguaje natural.
* Inadecuación de métricas sintácticas como BLEU/ROUGE para juzgar el valor didáctico.
* No determinismo y variabilidad estocástica.

## 3.3. Evaluación de respuestas generadas por IA
Se combinan la evaluación humana experta y la evaluación automática por jueces LLM (*LLM-as-a-Judge*, Zheng et al., 2023) sobre rúbricas analíticas estructuradas.

## 3.4. Benchmarks y métodos de evaluación existentes
Revisión de MMLU (Hendrycks et al., 2021), TruthfulQA (Lin et al., 2022) y MT-Bench (Zheng et al., 2023).

## 3.5. Necesidad de una metodología específica para contextos educativos
Los benchmarks generales no evalúan la dimensión formativa: andamiaje, diagnóstico de errores del estudiante, adecuación por edad y preservación de la honestidad académica.
