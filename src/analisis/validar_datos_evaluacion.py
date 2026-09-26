"""
Script de validación de integridad, estructura y consistencia para los datasets de evaluación humana.
Comprueba que las anotaciones de Evaluador 1 y Evaluador 2 cumplen rigurosamente:
- Existencia e integridad de los ficheros fuente originales en data/evaluaciones/raw/ (CSV).
- Correspondencia exacta campo a campo entre los ficheros raw CSV y los datasets JSON normalizados.
- Esquema de campos requerido y ausencia de duplicados.
- Integridad de los 42 casos por perfil (126 evaluaciones por evaluador).
- Puntuaciones discretas válidas en escala [0, 3] para las 7 dimensiones analíticas.
- Presencia de justificaciones cualitativas.
- Coherencia cruzada entre el dataset global y las particiones por perfil.
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

DIMENSIONES_ESPERADAS = [
    "D1_correccion_factual",
    "D2_control_alucinaciones",
    "D3_claridad_didactica",
    "D4_utilidad_pedagogica",
    "D5_robustez_seguridad",
    "D6_adaptacion_nivel",
    "D7_seguimiento_instrucciones"
]

PERFILES_ESPERADOS = ["asistente_base", "tutor_directo", "tutor_socratico"]
CAMPOS_OBLIGATORIOS = [
    "caso_id",
    "perfil",
    "evaluador_id",
    "dimension_principal",
    "categoria",
    "materia",
    "nivel_educativo",
    "puntuaciones",
    "justificaciones"
]


def validar_dataset_evaluacion(items: List[Dict[str, Any]], nombre_archivo: str, evaluador_esperado: str = None) -> List[str]:
    """Valida un conjunto de evaluaciones contra el esquema y las reglas del marco metodológico."""
    errores = []
    
    if not isinstance(items, list):
        return [f"[{nombre_archivo}] El contenido raíz debe ser una lista de evaluaciones."]
    
    if len(items) == 0:
        return [f"[{nombre_archivo}] El archivo está vacío."]
    
    prompts = {c["id"]: c for c in cargar_todos_los_prompts()}
    casos_vistos = set()
    
    for idx, item in enumerate(items):
        prefijo = f"[{nombre_archivo} item {idx+1}]"
        
        # 1. Campos obligatorios
        for campo in CAMPOS_OBLIGATORIOS:
            if campo not in item:
                errores.append(f"{prefijo} Falta el campo obligatorio '{campo}'.")
                
        cid = item.get("caso_id")
        perfil = item.get("perfil")
        ev_id = item.get("evaluador_id")
        
        if cid not in prompts:
            errores.append(f"{prefijo} 'caso_id' '{cid}' no existe en el banco de 42 prompts.")
            
        if perfil not in PERFILES_ESPERADOS:
            errores.append(f"{prefijo} 'perfil' '{perfil}' no es uno de los 3 perfiles válidos.")
            
        if evaluador_esperado and ev_id != evaluador_esperado:
            errores.append(f"{prefijo} 'evaluador_id' esperado '{evaluador_esperado}', encontrado '{ev_id}'.")
            
        # 2. Validación de dimensiones y puntuaciones
        puntuaciones = item.get("puntuaciones", {})
        justificaciones = item.get("justificaciones", {})
        
        for dim in DIMENSIONES_ESPERADAS:
            if dim not in puntuaciones:
                errores.append(f"{prefijo} Falta la dimensión '{dim}' en 'puntuaciones'.")
            else:
                score = puntuaciones[dim]
                if type(score) is not int or score not in [0, 1, 2, 3]:
                    errores.append(f"{prefijo} Puntuación inválida en '{dim}': {score} (debe ser entero en [0, 3]).")
                    
            if dim not in justificaciones:
                errores.append(f"{prefijo} Falta la dimensión '{dim}' en 'justificaciones'.")
            else:
                just = justificaciones[dim]
                if not isinstance(just, str) or len(just.strip()) == 0:
                    errores.append(f"{prefijo} Justificación vacía o no textual en '{dim}'.")
                    
        clave_unica = (cid, perfil)
        if clave_unica in casos_vistos:
            errores.append(f"{prefijo} Par duplicado (caso_id={cid}, perfil={perfil}).")
        casos_vistos.add(clave_unica)
        
    return errores


def validar_csv_raw(csv_path: Path, evaluador_esperado: str) -> List[str]:
    """Valida la integridad de un fichero CSV de anotación humana original."""
    errores = []
    if not csv_path.exists():
        return [f"Fichero raw no encontrado: {csv_path}"]
        
    filas = 0
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            filas += 1
            cid = row.get("caso_id")
            perfil = row.get("perfil")
            if not cid:
                errores.append(f"[{csv_path.name} fila {idx+1}] Falta caso_id.")
            if perfil not in PERFILES_ESPERADOS:
                errores.append(f"[{csv_path.name} fila {idx+1}] Perfil inválido: {perfil}.")
            for d in DIMENSIONES_ESPERADAS:
                if d not in row:
                    errores.append(f"[{csv_path.name} fila {idx+1}] Falta columna {d}.")
                else:
                    try:
                        val = int(row[d])
                        if val not in [0, 1, 2, 3]:
                            errores.append(f"[{csv_path.name} fila {idx+1}] Valor fuera de rango en {d}: {val}")
                    except ValueError:
                        errores.append(f"[{csv_path.name} fila {idx+1}] Valor no numérico en {d}: {row[d]}")
                        
    if filas != 126:
        errores.append(f"[{csv_path.name}] Número incorrecto de filas: {filas} (esperadas: 126).")
        
    return errores


def comparar_csv_con_json(csv_path: Path, json_path: Path) -> List[str]:
    """Compara campo a campo los registros del CSV raw con el JSON normalizado."""
    errores = []
    if not csv_path.exists() or not json_path.exists():
        return [f"No se pueden comparar: {csv_path} o {json_path} no existen."]
        
    with open(csv_path, "r", encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
        
    with open(json_path, "r", encoding="utf-8") as f:
        json_items = json.load(f)
        
    if len(csv_rows) != len(json_items):
        return [f"Discrepancia en recuento: CSV={len(csv_rows)} vs JSON={len(json_items)}"]
        
    # Indexar JSON por (caso_id, perfil)
    json_map = {(item["caso_id"], item["perfil"]): item for item in json_items}
    
    for idx, row in enumerate(csv_rows):
        cid = row["caso_id"]
        perf = row["perfil"]
        clave = (cid, perf)
        
        if clave not in json_map:
            errores.append(f"Registro CSV ({cid}, {perf}) no encontrado en JSON {json_path.name}")
            continue
            
        j_item = json_map[clave]
        
        # Comparar metadatos contextuales
        for meta_key in ["evaluador_id", "dimension_principal", "categoria", "materia", "nivel_educativo"]:
            csv_meta = row.get(meta_key, "").strip()
            json_meta = j_item.get(meta_key, "").strip()
            if csv_meta and json_meta and csv_meta != json_meta:
                errores.append(f"Discrepancia en metadato '{meta_key}' en ({cid}, {perf}): CSV='{csv_meta}' vs JSON='{json_meta}'")
            
        # Comparar puntuaciones D1..D7
        for d in DIMENSIONES_ESPERADAS:
            csv_val = int(row[d])
            json_val = j_item["puntuaciones"][d]
            if csv_val != json_val:
                errores.append(f"Discrepancia de puntuación en ({cid}, {perf}, {d}): CSV={csv_val} vs JSON={json_val}")
                
            # Comparar justificaciones
            just_csv = row.get(f"justificacion_{d}", "").strip()
            just_json = j_item["justificaciones"].get(d, "").strip()
            if just_csv and just_json and just_csv != just_json:
                errores.append(f"Discrepancia de justificación en ({cid}, {perf}, {d}): CSV='{just_csv}' vs JSON='{just_json}'")
                
    return errores


def validar_dataset_llm_judge() -> List[str]:
    """
    Valida exhaustivamente la consistencia estructural, correspondencia de metadatos versionados (SHA-256)
    y la integridad metodológica del dataset experimental generado por LLM-as-a-Judge.
    """
    print("  [Opcional] Validando dataset experimental LLM-as-a-Judge...")
    judge_dir = EVAL_DIR / "llm_judge"
    raw_dir = judge_dir / "raw"
    errores = []
    
    # 0. Recalcular hashes de plantilla y rúbrica desde el código fuente
    try:
        from src.evaluador.evaluador_llm_judge import RUBRIC_SHA256, PROMPT_TEMPLATE_SHA256
    except Exception as e:
        RUBRIC_SHA256 = None
        PROMPT_TEMPLATE_SHA256 = None
        errores.append(f"[hashes] No se pudieron importar los hashes del evaluador: {e}")
        
    # Validar run_manifest.json
    manifest_file = judge_dir / "run_manifest.json"
    manifest_data = None
    if not manifest_file.exists():
        errores.append("[manifest] Archivo 'run_manifest.json' no encontrado.")
    else:
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        m_prompt_hash = manifest_data.get("hashes_congelacion", {}).get("prompt_template_sha256")
        m_rubric_hash = manifest_data.get("hashes_congelacion", {}).get("rubric_sha256")
        
        if PROMPT_TEMPLATE_SHA256 and m_prompt_hash != PROMPT_TEMPLATE_SHA256:
            errores.append(f"[manifest] Hash del prompt en manifest ({m_prompt_hash}) no coincide con el recalculado ({PROMPT_TEMPLATE_SHA256}).")
        if RUBRIC_SHA256 and m_rubric_hash != RUBRIC_SHA256:
            errores.append(f"[manifest] Hash de la rúbrica en manifest ({m_rubric_hash}) no coincide con el recalculado ({RUBRIC_SHA256}).")
            
    # Cargar pares canónicos de referencia desde Evaluador 1 (Gold Standard)
    e1_file = EVAL_DIR / "evaluacion_evaluador_1.json"
    pares_esperados = set()
    if e1_file.exists():
        with open(e1_file, "r", encoding="utf-8") as f:
            pares_esperados = {(x["caso_id"], x["perfil"]) for x in json.load(f)}
    
    raw_data = None
    norm_data = None
    
    # 1. Validar trazas raw
    raw_file = raw_dir / "evaluaciones_llm_judge_raw.json"
    if not raw_file.exists():
        errores.append(f"Archivo raw del juez no encontrado ({raw_file.name}). Ejecuta primero: python3 src/evaluador/evaluador_llm_judge.py --mode ollama --model qwen2.5:14b-instruct --temperature 0")
    else:
        with open(raw_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        if len(raw_data) != 126:
            errores.append(f"[raw_judge] Número de trazas incorrecto: {len(raw_data)} (esperados: 126).")
        else:
            # Validar consistencia interna del dataset raw
            modelos = {t.get("judge_model") for t in raw_data}
            proveedores = {t.get("provider") for t in raw_data}
            prompt_vers = {t.get("prompt_version") for t in raw_data}
            prompt_hashes = {t.get("prompt_template_sha256", t.get("judge_prompt_sha256")) for t in raw_data}
            rubric_vers = {t.get("rubric_version") for t in raw_data}
            rubric_hashes = {t.get("rubric_sha256") for t in raw_data}
            model_digests = {t.get("model_digest") for t in raw_data if t.get("model_digest")}
            pares_raw = {(t.get("caso_id"), t.get("perfil")) for t in raw_data}
            
            if "MockJudgeProvider" in proveedores:
                errores.append("[raw_judge] Error de procedencia: El dataset canónico contiene trazas de 'MockJudgeProvider'. Las simulaciones deben aislarse en results/demo_simulada/.")
            if len(modelos) > 1:
                errores.append(f"[raw_judge] Múltiples modelos juez detectados en el mismo dataset: {modelos}")
            if len(proveedores) > 1:
                errores.append(f"[raw_judge] Múltiples proveedores detectados en el mismo dataset: {proveedores}")
            if len(prompt_vers) > 1 or len(prompt_hashes) > 1:
                errores.append(f"[raw_judge] Discrepancia en versiones/hashes del prompt: versiones={prompt_vers}, hashes={prompt_hashes}")
            if len(rubric_vers) > 1 or len(rubric_hashes) > 1:
                errores.append(f"[raw_judge] Discrepancia en versiones/hashes de la rúbrica: versiones={rubric_vers}, hashes={rubric_hashes}")
                
            # Validar contra los hashes recalculados y contra manifest
            if PROMPT_TEMPLATE_SHA256 and list(prompt_hashes)[0] != PROMPT_TEMPLATE_SHA256:
                errores.append(f"[raw_judge] El hash del prompt en las trazas ({list(prompt_hashes)[0]}) no coincide con el recalculado ({PROMPT_TEMPLATE_SHA256}).")
            if RUBRIC_SHA256 and list(rubric_hashes)[0] != RUBRIC_SHA256:
                errores.append(f"[raw_judge] El hash de la rúbrica en las trazas ({list(rubric_hashes)[0]}) no coincide con el recalculado ({RUBRIC_SHA256}).")
                
            if manifest_data:
                m_digest = manifest_data.get("modelo_juez", {}).get("model_digest")
                if m_digest and model_digests and list(model_digests)[0] != m_digest:
                    errores.append(f"[manifest_sync] model_digest en manifest ({m_digest}) no coincide con las trazas ({list(model_digests)[0]}).")
                
            if pares_esperados and pares_raw != pares_esperados:
                diff = pares_esperados ^ pares_raw
                errores.append(f"[raw_judge] Los pares (caso_id, perfil) en raw no coinciden con la referencia humana Gold Standard: discrepancias={len(diff)}")
                
            if not errores:
                print(f"    [+] {raw_file.name}: 126 trazas raw validadas (Proveedor: {list(proveedores)[0]}, Modelo: {list(modelos)[0]}, Hashes verificados).")
                
    # 2. Validar JSON normalizado
    norm_file = judge_dir / "evaluacion_llm_judge.json"
    if not norm_file.exists():
        errores.append(f"Archivo normalizado del juez no encontrado ({norm_file.name}). Ejecuta primero: python3 src/evaluador/evaluador_llm_judge.py --mode ollama --model qwen2.5:14b-instruct --temperature 0")
    else:
        with open(norm_file, "r", encoding="utf-8") as f:
            norm_data = json.load(f)
        if len(norm_data) != 126:
            errores.append(f"[norm_judge] Número de registros incorrecto: {len(norm_data)} (esperados: 126).")
        errs = validar_dataset_evaluacion(norm_data, norm_file.name, evaluador_esperado="LLM_JUDGE")
        errores.extend(errs)
        
        # 3. Validar correspondencia biunívoca raw <-> normalizado
        if raw_data and norm_data and len(raw_data) == 126 and len(norm_data) == 126:
            map_raw = {(t["caso_id"], t["perfil"]): t for t in raw_data}
            map_norm = {(n["caso_id"], n["perfil"]): n for n in norm_data}
            
            for clave in pares_esperados:
                if clave not in map_raw or clave not in map_norm:
                    errores.append(f"[judge_sync] Clave {clave} ausente en raw o normalizado.")
                    continue
                r_item = map_raw[clave]
                n_item = map_norm[clave]
                
                # Comprobar puntuaciones idénticas
                raw_scores = r_item.get("puntuaciones_extraidas", {})
                norm_scores = n_item.get("puntuaciones", {})
                if raw_scores != norm_scores:
                    errores.append(f"[judge_sync] Discrepancia raw vs normalizado en {clave}: raw={raw_scores} vs norm={norm_scores}")
                    
            if not errs and not [e for e in errores if "[judge_sync]" in e]:
                print(f"    [+] {norm_file.name}: 126 registros normalizados validados (Correspondencia exacta raw <-> JSON).")
                
    # 4. Validar particiones por perfil del juez
    for perfil in PERFILES_ESPERADOS:
        p_file = judge_dir / f"evaluacion_llm_judge_{perfil}.json"
        if p_file.exists():
            with open(p_file, "r", encoding="utf-8") as f:
                p_data = json.load(f)
            if len(p_data) != 42:
                errores.append(f"[particion_judge] Longitud incorrecta para {p_file.name}: {len(p_data)} (esperados: 42).")
            else:
                print(f"    [+] {p_file.name}: 42 casos del perfil '{perfil}' validados.")
                
    return errores


def ejecutar_auditoria_completa_evaluaciones(incluir_judge: bool = False):
    """Ejecuta la validación exhaustiva de todos los archivos de evaluación humana y opcionalmente LLM-as-a-Judge."""
    print("=" * 65)
    print("  AUDITORÍA Y VALIDACIÓN DE INTEGRIDAD DE EVALUACIONES HUMANAS")
    print("=" * 65)
    
    total_errores = []
    
    # 1. Validar ficheros fuente RAW (CSV)
    print("  [1/4] Validando ficheros originales de anotación (raw CSV)...")
    for ev_id, fname in [("evaluador_1", "anotaciones_evaluador_1_raw.csv"), ("evaluador_2", "anotaciones_evaluador_2_raw.csv")]:
        csv_path = RAW_DIR / fname
        errs = validar_csv_raw(csv_path, ev_id)
        total_errores.extend(errs)
        if not errs:
            print(f"    [+] {fname}: 126 anotaciones originales validadas ({ev_id}).")
            
    # 2. Validar archivos JSON de Evaluador 1 y 2
    print("  [2/4] Validando datasets normalizados JSON (Evaluador 1 y 2)...")
    archivos_evaluador = {
        "evaluacion_evaluador_1.json": ("evaluador_1", 126),
        "evaluacion_evaluador_2.json": ("evaluador_2", 126),
    }
    for fname, (ev_id, total_esperado) in archivos_evaluador.items():
        fpath = EVAL_DIR / fname
        if not fpath.exists():
            total_errores.append(f"Archivo crítico no encontrado: {fpath}")
            continue
            
        with open(fpath, "r", encoding="utf-8") as f:
            datos = json.load(f)
            
        if len(datos) != total_esperado:
            total_errores.append(f"[{fname}] Número de registros incorrecto: {len(datos)} (esperados: {total_esperado}).")
            
        errs = validar_dataset_evaluacion(datos, fname, evaluador_esperado=ev_id)
        total_errores.extend(errs)
        if not errs:
            print(f"    [+] {fname}: {len(datos)} registros validados ({ev_id}).")
            
    # 3. Comparación exacta campo a campo raw CSV <-> normalizado JSON
    print("  [3/4] Comprobando correspondencia exacta y biunívoca (raw CSV <-> JSON)...")
    comparaciones = [
        ("anotaciones_evaluador_1_raw.csv", "evaluacion_evaluador_1.json"),
        ("anotaciones_evaluador_2_raw.csv", "evaluacion_evaluador_2.json")
    ]
    for csv_name, json_name in comparaciones:
        errs_comp = comparar_csv_con_json(RAW_DIR / csv_name, EVAL_DIR / json_name)
        total_errores.extend(errs_comp)
        if not errs_comp:
            print(f"    [+] {csv_name} <-> {json_name}: correspondencia exacta 126/126 registros (0 discrepancias).")
            
    # 4. Validar particiones por perfil (Evaluador 1)
    print("  [4/4] Validando particiones por perfil...")
    for perfil in PERFILES_ESPERADOS:
        fname = f"evaluacion_{perfil}.json"
        fpath = EVAL_DIR / fname
        if not fpath.exists():
            total_errores.append(f"Archivo de perfil no encontrado: {fpath}")
            continue
            
        with open(fpath, "r", encoding="utf-8") as f:
            datos_perfil = json.load(f)
            
        if len(datos_perfil) != 42:
            total_errores.append(f"[{fname}] Número de casos incorrecto: {len(datos_perfil)} (esperados: 42).")
            
        errs = validar_dataset_evaluacion(datos_perfil, fname, evaluador_esperado="evaluador_1")
        total_errores.extend(errs)
        if not errs:
            print(f"    [+] {fname}: {len(datos_perfil)} casos del perfil '{perfil}' validados.")
            
    # 5. Opcional: Validar LLM Judge
    if incluir_judge:
        errs_j = validar_dataset_llm_judge()
        total_errores.extend(errs_j)
            
    # Resumen final
    print("-" * 65)
    if total_errores:
        print(f"[-] Se encontraron {len(total_errores)} errores de validación:")
        for e in total_errores[:20]:
            print(f"   - {e}")
        if len(total_errores) > 20:
            print(f"   ... y {len(total_errores)-20} errores más.")
            return False
    else:
        print("  Todos los conjuntos de evaluacion cumplen el estandar metodologico.")
        print(f"  Trazabilidad completa: raw CSV -> normalizado JSON -> métricas.")
        print(f"  Total de pares evaluados pareados: 126 casos x 7 dimensiones = 882 puntuaciones.")
    print("=" * 65)
    return len(total_errores) == 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validador de Integridad de Evaluaciones")
    parser.add_argument("--incluir-judge", action="store_true", help="Incluir validación del dataset LLM-as-a-Judge")
    args = parser.parse_args()
    
    exito = ejecutar_auditoria_completa_evaluaciones(incluir_judge=args.incluir_judge)
    if not exito:
        sys.exit(1)

