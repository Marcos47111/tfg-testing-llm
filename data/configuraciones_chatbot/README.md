# Configuraciones de Chatbot y Parámetros Experimentales

Este directorio contiene las definiciones formales de los perfiles de chatbot y los parámetros de inferencia utilizados para asegurar la reproducibilidad de los experimentos.

## Perfiles Evaluados

1. **`asistente_base.json`**: Línea base sin directrices pedagógicas (`"You are a helpful assistant."`). Permite medir el comportamiento crudo del modelo base.
2. **`tutor_directo.json`**: Tutor expositivo tradicional que responde de forma exhaustiva y didáctica resolviendo la duda del estudiante.
3. **`tutor_socratico.json`**: Tutor formativo con restricciones de andamiaje (*scaffolding*) y feedback constructivo que no entrega respuestas resueltas de ejercicios directamente.

## Control de Parámetros de Inferencia y Reproducibilidad
Para garantizar que los resultados de las pruebas sean reproducibles:
* **Temperatura (`0.2`):** Nivel bajo de estocasticidad para favorecer la determinismo conceptual sin perder coherencia sintáctica.
* **Top-p (`0.9`):** Filtro de muestreo de núcleo (*nucleus sampling*).
* **Seed (`42`):** Semilla pseudoaleatoria fija para facilitar la reproducibilidad de las pruebas.
