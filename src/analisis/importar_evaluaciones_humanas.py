"""
Script para importar, validar y normalizar las anotaciones humanas originales (raw CSV)
de Evaluador 1 y Evaluador 2 hacia los datasets JSON del pipeline analítico del TFG.
"""

import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.loader_prompts import cargar_todos_los_prompts

DATA_DIR = PROJECT_ROOT / "data"
EVAL_DIR = DATA_DIR / "evaluaciones"
RAW_DIR = EVAL_DIR / "raw"

DIMENSIONES = [
    "D1_correccion_factual",
    "D2_control_alucinaciones",
    "D3_claridad_didactica",
    "D4_utilidad_pedagogica",
    "D5_robustez_seguridad",
    "D6_adaptacion_nivel",
    "D7_seguimiento_instrucciones"
]

PERFILES = ["asistente_base", "tutor_directo", "tutor_socratico"]


def importar_csv_evaluador(csv_path: Path, evaluador_id_esperado: str) -> List[Dict[str, Any]]:
    """Lee y estructura un archivo CSV de anotaciones humanas raw."""
    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontró el fichero de anotaciones: {csv_path}")
        
    registros = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row["caso_id"].strip()
            perfil = row["perfil"].strip()
            ev_id = row.get("evaluador_id", evaluador_id_esperado).strip()
            
            puntuaciones = {}
            justificaciones = {}
            for d in DIMENSIONES:
                val = int(row[d])
                if val not in [0, 1, 2, 3]:
                    raise ValueError(f"Puntuación fuera de rango en {cid}/{perfil}/{d}: {val}")
                puntuaciones[d] = val
                
                just_key = f"justificacion_{d}"
                just = row.get(just_key, row.get("justificacion_observaciones", "")).strip()
                if not just:
                    just = "Comportamiento evaluado conforme a los descriptores de la rúbrica."
                justificaciones[d] = just
                
            item = {
                "caso_id": cid,
                "perfil": perfil,
                "evaluador_id": ev_id,
                "dimension_principal": row.get("dimension_principal", ""),
                "categoria": row.get("categoria", row.get("dimension_principal", "")),
                "materia": row.get("materia", ""),
                "nivel_educativo": row.get("nivel_educativo", ""),
                "puntuaciones": puntuaciones,
                "justificaciones": justificaciones
            }
            registros.append(item)
            
    if len(registros) != 126:
        raise ValueError(f"Se esperaban 126 registros en {csv_path.name}, pero se leyeron {len(registros)}.")
        
    return registros


def ejecutar_importacion_y_normalizacion():
    """Importa los CSV raw de ambos evaluadores y genera los datasets JSON normalizados."""
    print("=" * 65)
    print("  IMPORTACIÓN DE ANOTACIONES HUMANAS (RAW CSV -> JSON PIPELINE)")
    print("=" * 65)
    
    # 1. Cargar metadatos de prompts
    prompts = {c["id"]: c for c in cargar_todos_los_prompts()}
    
    # 2. Importar CSVs originales
    e1_csv = RAW_DIR / "anotaciones_evaluador_1_raw.csv"
    e2_csv = RAW_DIR / "anotaciones_evaluador_2_raw.csv"
    
    eval_1 = importar_csv_evaluador(e1_csv, "evaluador_1")
    eval_2 = importar_csv_evaluador(e2_csv, "evaluador_2")
    
    # Completar metadatos si faltan
    for dataset in [eval_1, eval_2]:
        for item in dataset:
            cid = item["caso_id"]
            if cid in prompts:
                p_info = prompts[cid]
                if not item["dimension_principal"]:
                    item["dimension_principal"] = p_info["dimension_principal"]
                if not item["categoria"]:
                    item["categoria"] = p_info.get("categoria_directorio", p_info["dimension_principal"])
                if not item["materia"]:
                    item["materia"] = p_info["materia"]
                if not item["nivel_educativo"]:
                    item["nivel_educativo"] = p_info["nivel_educativo"]
                    
    # 3. Construir Dataset Unificado Gold Standard
    eval_gold_standard = []
    for item in eval_1:
        gold_item = {
            "caso_id": item["caso_id"],
            "perfil": item["perfil"],
            "evaluador_id": "gold_standard",
            "dimension_principal": item["dimension_principal"],
            "categoria": item["categoria"],
            "materia": item["materia"],
            "nivel_educativo": item["nivel_educativo"],
            "puntuaciones": dict(item["puntuaciones"]),
            "justificaciones": dict(item["justificaciones"])
        }
        eval_gold_standard.append(gold_item)

    # 4. Guardar JSONs canónicos
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    with open(EVAL_DIR / "evaluacion_gold_standard.json", "w", encoding="utf-8") as f:
        json.dump(eval_gold_standard, f, indent=2, ensure_ascii=False)
    print(f"  [+] Exportado: {EVAL_DIR / 'evaluacion_gold_standard.json'} (126 registros - Gold Standard Canónico)")

    with open(EVAL_DIR / "evaluacion_evaluador_1.json", "w", encoding="utf-8") as f:
        json.dump(eval_1, f, indent=2, ensure_ascii=False)
    print(f"  [+] Exportado: {EVAL_DIR / 'evaluacion_evaluador_1.json'} (126 registros)")
    
    with open(EVAL_DIR / "evaluacion_evaluador_2.json", "w", encoding="utf-8") as f:
        json.dump(eval_2, f, indent=2, ensure_ascii=False)
    print(f"  [+] Exportado: {EVAL_DIR / 'evaluacion_evaluador_2.json'} (126 registros)")
    
    # 5. Exportar CSV raw del Gold Standard
    gold_csv = RAW_DIR / "anotaciones_gold_standard_raw.csv"
    with open(gold_csv, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["caso_id", "perfil", "evaluador_id", "dimension_principal", "categoria", "materia", "nivel_educativo"]
        for d in DIMENSIONES:
            fieldnames.append(d)
        for d in DIMENSIONES:
            fieldnames.append(f"justificacion_{d}")
            
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for g in eval_gold_standard:
            row = {
                "caso_id": g["caso_id"],
                "perfil": g["perfil"],
                "evaluador_id": "gold_standard",
                "dimension_principal": g["dimension_principal"],
                "categoria": g["categoria"],
                "materia": g["materia"],
                "nivel_educativo": g["nivel_educativo"],
            }
            for d in DIMENSIONES:
                row[d] = g["puntuaciones"][d]
                row[f"justificacion_{d}"] = g["justificaciones"][d]
            writer.writerow(row)
    print(f"  [+] Exportado: {gold_csv} (126 registros)")

    # 6. Particiones por perfil (derivadas formalmente del Gold Standard)
    for perfil in PERFILES:
        items_perfil = [item for item in eval_gold_standard if item["perfil"] == perfil]
        with open(EVAL_DIR / f"evaluacion_{perfil}.json", "w", encoding="utf-8") as f:
            json.dump(items_perfil, f, indent=2, ensure_ascii=False)
        print(f"  [+] Exportado: {EVAL_DIR / f'evaluacion_{perfil}.json'} ({len(items_perfil)} casos desde Gold Standard)")
        
    print("-" * 65)
    print("  Importacion y consolidacion del Gold Standard completada con exito.")
    print("=" * 65)


if __name__ == "__main__":
    ejecutar_importacion_y_normalizacion()
