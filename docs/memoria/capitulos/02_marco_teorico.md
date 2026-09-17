# 2. Marco teórico

## 2.1. Inteligencia artificial generativa
La IAG representa un cambio de paradigma: aprende la distribución de probabilidad subyacente $P(X)$ sobre corpus masivos para generar muestras inéditas. El hito fundacional moderno es la arquitectura Transformer (Vaswani et al., 2017) y el mecanismo de auto-atención (*Self-Attention*).

## 2.2. Modelos de lenguaje de gran tamaño (LLMs)
El ciclo de vida de los LLMs comprende:
1. **Preentrenamiento no supervisado (*Pre-training*):** Predicción del siguiente token sobre billones de palabras.
2. **Ajuste fino de instrucciones (*Supervised Fine-Tuning - SFT*):** Aprendizaje de seguimiento de consignas conversacionales.
3. **Alineamiento por refuerzo (*RLHF*):** Optimización mediante modelos de recompensa humana para utilidad, honestidad y seguridad (Achiam et al., 2023).

## 2.3. Chatbots basados en LLMs: arquitectura y componentes
Arquitectura por capas:
* **Frontend:** Interfaz de usuario conversacional (Open WebUI, LibreChat).
* **Middleware:** Orquestación, gestión de contexto y ensamblado del System Prompt.
* **Módulos RAG:** Recuperación aumentada para anclar el conocimiento a fuentes fiables.
* **Backend:** Motor de inferencia (Ollama, vLLM, APIs) bajo control estocástico ($T, \text{top-}p, \text{seed}$).

## 2.4. Uso de LLMs en contextos educativos
Potencial formativo: personalización cognitiva, andamiaje socrático en la ZDP (Vygotsky, 1978) y generación de material didáctico estructurado (Kasneci et al., 2023).

## 2.5. Riesgos y limitaciones de los LLMs en educación
Riesgos críticos: alucinaciones intrínsecas y extrínsecas (Ji et al., 2023), sobreconfianza sintomática (Lin et al., 2022) y vulnerabilidad a jailbreaks y fraude académico (Wei et al., 2023; UNESCO, 2023).
