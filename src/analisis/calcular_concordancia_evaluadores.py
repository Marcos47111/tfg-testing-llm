"""
Script para calcular la concordancia entre el Juicio Humano Experto (Gold Standard)
y el Juez Automático (LLM-as-a-Judge con Qwen2.5-14B-Instruct).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analisis.analizar_concordancia_llm_judge import ejecutar_analisis_concordancia_llm_judge


def main():
    ejecutar_analisis_concordancia_llm_judge()


if __name__ == "__main__":
    main()

