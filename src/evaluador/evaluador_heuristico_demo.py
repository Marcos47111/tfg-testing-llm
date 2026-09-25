"""
Módulo de demostración heurística automatizada basada en reglas (Demo / Línea base).
NOTA METODOLÓGICA: Este módulo es únicamente un componente de demostración heurística
y NO se utiliza para la evaluación oficial del TFG, la cual se basa íntegramente
en juicios humanos independientes (Evaluador 1 y Evaluador 2) almacenados en data/evaluaciones/.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.loader_prompts import cargar_todos_los_prompts

RESPUESTAS_RAW_DIR = PROJECT_ROOT / "data" / "respuestas_obtenidas" / "raw"
DEMO_OUTPUT_DIR = PROJECT_ROOT / "results" / "demo_heuristica"


def evaluar_respuesta_demo(caso: Dict[str, Any], respuesta_obj: Dict[str, Any]) -> Dict[str, Any]:
    """Evalúa heurísticamente una respuesta individual con fines de demostración."""
    perfil = respuesta_obj["perfil"]
    cid = caso["id"]
    dim_primaria = caso["dimension_principal"]
    
    puntuaciones = {}
    justificaciones = {}
    
    for d in [
        "D1_correccion_factual", "D2_control_alucinaciones", "D3_claridad_didactica",
        "D4_utilidad_pedagogica", "D5_robustez_seguridad", "D6_adaptacion_nivel",
        "D7_seguimiento_instrucciones"
    ]:
        puntuaciones[d] = 2 if perfil == "asistente_base" else 3
        justificaciones[d] = "Puntuación heurística de demostración sintética."
        
    return {
        "caso_id": cid,
        "categoria": caso.get("categoria_directorio", dim_primaria),
        "perfil": perfil,
        "dimension_principal": dim_primaria,
        "materia": caso["materia"],
        "nivel_educativo": caso["nivel_educativo"],
        "puntuaciones": puntuaciones,
        "justificaciones": justificaciones
    }


def ejecutar_demo_heuristica():
    """Genera evaluaciones de demostración en un directorio aislado sin tocar data/evaluaciones/."""
    DEMO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prompts_map = {c["id"]: c for c in cargar_todos_los_prompts()}
    
    archivos_respuestas = list(RESPUESTAS_RAW_DIR.glob("respuestas_*.json"))
    for ar in archivos_respuestas:
        with open(ar, "r", encoding="utf-8") as f:
            respuestas = json.load(f)
            
        evals = [evaluar_respuesta_demo(prompts_map[r["caso_id"]], r) for r in respuestas]
        nombre_perfil = ar.stem.replace("respuestas_", "")
        archivo_salida = DEMO_OUTPUT_DIR / f"demo_evaluacion_{nombre_perfil}.json"
        with open(archivo_salida, "w", encoding="utf-8") as f:
            json.dump(evals, f, indent=2, ensure_ascii=False)
            
    print(f"[+] Demo heurística generada en {DEMO_OUTPUT_DIR}")


if __name__ == "__main__":
    ejecutar_demo_heuristica()
