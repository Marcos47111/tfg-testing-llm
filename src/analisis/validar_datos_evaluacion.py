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
from typing import List, Dict, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.loader_prompts import cargar_todos_los_prompts

DATA_DIR = PROJECT_ROOT / "data"
EVAL_DIR = DATA_DIR / "evaluaciones"
RAW_DIR = EVAL_DIR / "raw"

RAW_INDEP_DIR = EVAL_DIR / "raw_independientes"

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


def validar_dataset_evaluacion(items: List[Dict[str, Any]], nombre_archivo: str, evaluador_esperado: str = None, total_casos_esperado: Optional[int] = None) -> List[str]:
    """Valida un conjunto de evaluaciones contra el esquema y las reglas del marco metodológico."""
    errores = []
    
    if not isinstance(items, list):
        return [f"[{nombre_archivo}] El contenido raíz debe ser una lista de evaluaciones."]
    
    if len(items) == 0:
        return [f"[{nombre_archivo}] El archivo está vacío."]
        
    if total_casos_esperado is not None and len(items) != total_casos_esperado:
        errores.append(f"[{nombre_archivo}] Número incorrecto de registros: {len(items)} (esperados: {total_casos_esperado}).")
    
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
            errores.append(f"{prefijo} 'caso_id' '{cid}' no existe en el banco de {len(prompts)} prompts.")
            
        if perfil not in PERFILES_ESPERADOS:
            errores.append(f"{prefijo} 'perfil' '{perfil}' no es uno de los {len(PERFILES_ESPERADOS)} perfiles válidos.")
            
        if evaluador_esperado:
            if isinstance(evaluador_esperado, (list, tuple, set)):
                if ev_id not in evaluador_esperado:
                    errores.append(f"{prefijo} 'evaluador_id' esperado en {evaluador_esperado}, encontrado '{ev_id}'.")
            elif ev_id != evaluador_esperado:
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


def validar_csv_raw(csv_path: Path, evaluador_esperado: str, total_esperado: int) -> List[str]:
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
                col_score = d if d in row else f"puntuacion_{d}"
                if col_score not in row:
                    errores.append(f"[{csv_path.name} fila {idx+1}] Falta columna {d} o puntuacion_{d}.")
                else:
                    try:
                        val = int(row[col_score])
                        if val not in [0, 1, 2, 3]:
                            errores.append(f"[{csv_path.name} fila {idx+1}] Valor fuera de rango en {col_score}: {val}")
                    except ValueError:
                        errores.append(f"[{csv_path.name} fila {idx+1}] Valor no numérico en {col_score}: {row[col_score]}")
                        
    if filas != total_esperado:
        errores.append(f"[{csv_path.name}] Número incorrecto de filas: {filas} (esperadas: {total_esperado}).")
        
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
            col_score = d if d in row else f"puntuacion_{d}"
            csv_val = int(row[col_score])
            json_val = j_item["puntuaciones"][d]
            if csv_val != json_val:
                errores.append(f"Discrepancia de puntuación en ({cid}, {perf}, {d}): CSV={csv_val} vs JSON={json_val}")
                
            # Comparar justificaciones
            just_csv = row.get(f"justificacion_{d}", "").strip()
            just_json = j_item["justificaciones"].get(d, "").strip()
            if just_csv and just_json and just_csv != just_json:
                errores.append(f"Discrepancia de justificación en ({cid}, {perf}, {d}): CSV='{just_csv}' vs JSON='{just_json}'")
                
    return errores


def validar_dataset_llm_judge(total_evaluaciones_esperadas: int, total_prompts: int) -> List[str]:
    """
    Valida exhaustivamente la integridad estructural, criptográfica y metodológica
    del dataset experimental generado por LLM-as-a-Judge.
    """
    print("  [Opcional] Validando dataset experimental LLM-as-a-Judge...")
    judge_dir = EVAL_DIR / "llm_judge"
    raw_dir = judge_dir / "raw"
    errores = []
    
    # Cargar pares canónicos de referencia desde Evaluador 1
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
        if len(raw_data) != total_evaluaciones_esperadas:
            errores.append(f"[raw_judge] Número de trazas incorrecto: {len(raw_data)} (esperados: {total_evaluaciones_esperadas}).")
        else:
            # Validar consistencia interna del dataset raw
            modelos = {t.get("judge_model") for t in raw_data}
            proveedores = {t.get("provider") for t in raw_data}
            prompt_vers = {t.get("prompt_version") for t in raw_data}
            prompt_hashes = {t.get("prompt_template_sha256", t.get("judge_prompt_sha256")) for t in raw_data}
            rubric_vers = {t.get("rubric_version") for t in raw_data}
            rubric_hashes = {t.get("rubric_sha256") for t in raw_data}
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
            if pares_esperados and pares_raw != pares_esperados:
                diff = pares_esperados ^ pares_raw
                errores.append(f"[raw_judge] Los pares (caso_id, perfil) en raw no coinciden con la referencia humana E1: discrepancias={len(diff)}")
                
            if not errores:
                print(f"    [+] {raw_file.name}: {total_evaluaciones_esperadas} trazas raw validadas (Proveedor: {list(proveedores)[0]}, Modelo: {list(modelos)[0]}).")
                
    # 2. Validar JSON normalizado
    norm_file = judge_dir / "evaluacion_llm_judge.json"
    if not norm_file.exists():
        errores.append(f"Archivo normalizado del juez no encontrado ({norm_file.name}). Ejecuta primero: python3 src/evaluador/evaluador_llm_judge.py --mode ollama --model qwen2.5:14b-instruct --temperature 0")
    else:
        with open(norm_file, "r", encoding="utf-8") as f:
            norm_data = json.load(f)
        if len(norm_data) != total_evaluaciones_esperadas:
            errores.append(f"[norm_judge] Número de registros incorrecto: {len(norm_data)} (esperados: {total_evaluaciones_esperadas}).")
        errs = validar_dataset_evaluacion(norm_data, norm_file.name, evaluador_esperado="LLM_JUDGE", total_casos_esperado=total_evaluaciones_esperadas)
        errores.extend(errs)
        
        # 3. Validar correspondencia biunívoca raw <-> normalizado
        if raw_data and norm_data and len(raw_data) == total_evaluaciones_esperadas and len(norm_data) == total_evaluaciones_esperadas:
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
                print(f"    [+] {norm_file.name}: {total_evaluaciones_esperadas} registros normalizados validados (Correspondencia exacta raw <-> JSON).")
                
    # 4. Validar particiones por perfil del juez
    for perfil in PERFILES_ESPERADOS:
        p_file = judge_dir / f"evaluacion_llm_judge_{perfil}.json"
        if p_file.exists():
            with open(p_file, "r", encoding="utf-8") as f:
                p_data = json.load(f)
            if len(p_data) != total_prompts:
                errores.append(f"[particion_judge] Longitud incorrecta para {p_file.name}: {len(p_data)} (esperados: {total_prompts}).")
            else:
                print(f"    [+] {p_file.name}: {total_prompts} casos del perfil '{perfil}' validados.")
                
    # 5. Validar manifiesto de ejecución si existe
    manifest_file = judge_dir / "run_manifest.json"
    if manifest_file.exists():
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        if manifest_data.get("volumen_evaluado", {}).get("total_respuestas") != total_evaluaciones_esperadas:
            errores.append(f"[manifest_judge] Discrepancia en volumen_evaluado.total_respuestas: {manifest_data.get('volumen_evaluado', {}).get('total_respuestas')} vs {total_evaluaciones_esperadas}")
        else:
            print(f"    [+] {manifest_file.name}: Manifiesto del Juez verificado.")
                
    return errores


def ejecutar_auditoria_completa_evaluaciones(incluir_judge: bool = False):
    """Ejecuta la validación exhaustiva de todos los archivos de evaluación humana y opcionalmente LLM-as-a-Judge."""
    prompts = cargar_todos_los_prompts()
    total_prompts = len(prompts)
    total_evaluaciones_esperadas = total_prompts * len(PERFILES_ESPERADOS)
    total_juicios = total_evaluaciones_esperadas * len(DIMENSIONES_ESPERADAS)

    print("=" * 68)
    print("  AUDITORÍA Y VALIDACIÓN DE INTEGRIDAD DE EVALUACIONES EXPERIMENTALES")
    print(f"  Banco de casos: {total_prompts} | Perfiles: {len(PERFILES_ESPERADOS)} | Total evals/evaluador: {total_evaluaciones_esperadas}")
    print("=" * 68)
    
    total_errores = []
    
    # 1. Validar Fase 1: Anotaciones Independientes Originales (raw_independientes)
    print("  [1/5] Validando Fase 1: Anotaciones independientes originales (raw_independientes)...")
    archivos_independientes = [
        ("evaluador_1_original.csv", "evaluador_1_original.json", "evaluador_1"),
        ("evaluador_2_original.csv", "evaluador_2_original.json", "evaluador_2"),
    ]
    for csv_name, json_name, ev_id in archivos_independientes:
        csv_path = RAW_INDEP_DIR / csv_name
        json_path = RAW_INDEP_DIR / json_name
        
        # Validar CSV
        errs_csv = validar_csv_raw(csv_path, ev_id, total_evaluaciones_esperadas)
        total_errores.extend(errs_csv)
        if not errs_csv:
            print(f"    [+] {csv_name}: {total_evaluaciones_esperadas} anotaciones independientes validadas ({ev_id}).")
            
        # Validar JSON
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                datos_indep = json.load(f)
            errs_json = validar_dataset_evaluacion(datos_indep, json_name, evaluador_esperado=ev_id, total_casos_esperado=total_evaluaciones_esperadas)
            total_errores.extend(errs_json)
            if not errs_json:
                print(f"    [+] {json_name}: {len(datos_indep)} registros independientes JSON validados ({ev_id}).")
                
        # Validar sincronía CSV <-> JSON
        errs_sync = comparar_csv_con_json(csv_path, json_path)
        total_errores.extend(errs_sync)
        if not errs_sync:
            print(f"    [+] {csv_name} <-> {json_name}: correspondencia exacta {total_evaluaciones_esperadas}/{total_evaluaciones_esperadas} (0 discrepancias).")

    # 2. Validar Fase 2: Datasets Consolidados (raw CSV)
    print("  [2/5] Validando Fase 2: Ficheros CSV raw consolidados...")
    ficheros_csv_fase2 = [
        ("evaluador_1", "anotaciones_evaluador_1_raw.csv"),
        ("evaluador_2", "anotaciones_evaluador_2_raw.csv"),
        ("gold_standard", "anotaciones_gold_standard_raw.csv")
    ]
    for ev_id, fname in ficheros_csv_fase2:
        csv_path = RAW_DIR / fname
        errs = validar_csv_raw(csv_path, ev_id, total_evaluaciones_esperadas)
        total_errores.extend(errs)
        if not errs:
            print(f"    [+] {fname}: {total_evaluaciones_esperadas} anotaciones consolidadas validadas ({ev_id}).")
            
    # 3. Validar Fase 2: Datasets JSON Consolidados (Gold Standard, Evaluador 1 y 2)
    print("  [3/5] Validando Fase 2: Datasets normalizados JSON (Gold Standard, Evaluador 1 y 2)...")
    archivos_evaluador = {
        "evaluacion_gold_standard.json": ("gold_standard", total_evaluaciones_esperadas),
        "evaluacion_evaluador_1.json": ("evaluador_1", total_evaluaciones_esperadas),
        "evaluacion_evaluador_2.json": ("evaluador_2", total_evaluaciones_esperadas),
    }
    for fname, (ev_id, total_esperado) in archivos_evaluador.items():
        fpath = EVAL_DIR / fname
        if not fpath.exists():
            total_errores.append(f"Archivo crítico no encontrado: {fpath}")
            continue
            
        with open(fpath, "r", encoding="utf-8") as f:
            datos = json.load(f)
            
        errs = validar_dataset_evaluacion(datos, fname, evaluador_esperado=ev_id, total_casos_esperado=total_esperado)
        total_errores.extend(errs)
        if not errs:
            print(f"    [+] {fname}: {len(datos)} registros validados ({ev_id}).")
            
    # Comparación exacta campo a campo raw CSV <-> normalizado JSON
    comparaciones = [
        ("anotaciones_gold_standard_raw.csv", "evaluacion_gold_standard.json"),
        ("anotaciones_evaluador_1_raw.csv", "evaluacion_evaluador_1.json"),
        ("anotaciones_evaluador_2_raw.csv", "evaluacion_evaluador_2.json")
    ]
    for csv_name, json_name in comparaciones:
        errs_comp = comparar_csv_con_json(RAW_DIR / csv_name, EVAL_DIR / json_name)
        total_errores.extend(errs_comp)
        if not errs_comp:
            print(f"    [+] {csv_name} <-> {json_name}: correspondencia exacta {total_evaluaciones_esperadas}/{total_evaluaciones_esperadas} (0 discrepancias).")

    # Validar tabla de adjudicaciones del Gold Standard
    adj_csv = EVAL_DIR / "adjudicaciones_gold_standard.csv"
    if adj_csv.exists():
        with open(adj_csv, "r", encoding="utf-8") as f:
            r_adj = list(csv.DictReader(f))
        map_adj = {(r["caso_id"].strip(), r["perfil"].strip(), r["dimension"].strip()): int(r["score_gold"]) for r in r_adj}
        
        with open(EVAL_DIR / "evaluacion_evaluador_1.json", "r", encoding="utf-8") as f:
            e1_data = { (x["caso_id"], x["perfil"]): x["puntuaciones"] for x in json.load(f) }
        with open(EVAL_DIR / "evaluacion_evaluador_2.json", "r", encoding="utf-8") as f:
            e2_data = { (x["caso_id"], x["perfil"]): x["puntuaciones"] for x in json.load(f) }
        with open(EVAL_DIR / "evaluacion_gold_standard.json", "r", encoding="utf-8") as f:
            gold_data = { (x["caso_id"], x["perfil"]): x["puntuaciones"] for x in json.load(f) }
            
        discrepancias_detectadas = 0
        for k, p1 in e1_data.items():
            p2 = e2_data[k]
            pg = gold_data[k]
            cid, perf = k
            for d in DIMENSIONES_ESPERADAS:
                if p1[d] != p2[d]:
                    discrepancias_detectadas += 1
                    clave_d = (cid, perf, d)
                    if clave_d not in map_adj:
                        total_errores.append(f"[adjudicacion_gold] Discrepancia no registrada en {adj_csv.name}: {clave_d}")
                    else:
                        if pg[d] != map_adj[clave_d]:
                            total_errores.append(f"[adjudicacion_gold] Puntuación en Gold Standard no coincide con adjudicación en {clave_d}: Gold={pg[d]} vs Adj={map_adj[clave_d]}")
                else:
                    if pg[d] != p1[d]:
                        total_errores.append(f"[adjudicacion_gold] En caso de acuerdo unánime {k}/{d}, Gold Standard difiere de evaluadores: Gold={pg[d]} vs E1/E2={p1[d]}")
        print(f"    [+] {adj_csv.name}: {len(r_adj)} adjudicaciones explícitas auditadas sobre {discrepancias_detectadas} discrepancias inter-evaluador.")
    else:
        total_errores.append(f"Archivo crítico no encontrado: {adj_csv}")
            
    # 4. Validar particiones por perfil (derivadas del Gold Standard)
    print("  [4/5] Validando particiones por perfil (derivadas del Gold Standard)...")
    for perfil in PERFILES_ESPERADOS:
        fname = f"evaluacion_{perfil}.json"
        fpath = EVAL_DIR / fname
        if not fpath.exists():
            total_errores.append(f"Archivo de perfil no encontrado: {fpath}")
            continue
            
        with open(fpath, "r", encoding="utf-8") as f:
            datos_perfil = json.load(f)
            
        errs = validar_dataset_evaluacion(datos_perfil, fname, evaluador_esperado=["gold_standard", "evaluador_1"], total_casos_esperado=total_prompts)
        total_errores.extend(errs)
        if not errs:
            print(f"    [+] {fname}: {len(datos_perfil)} casos del perfil '{perfil}' validados.")
            
    # 5. Opcional: Validar LLM Judge
    if incluir_judge:
        print("  [5/5] Validando extensión experimental LLM-as-a-Judge...")
        errs_j = validar_dataset_llm_judge(total_evaluaciones_esperadas, total_prompts)
        total_errores.extend(errs_j)
            
    # Resumen final
    print("-" * 68)
    if total_errores:
        print(f"[-] Se encontraron {len(total_errores)} errores de validación:")
        for e in total_errores[:20]:
            print(f"   - {e}")
        if len(total_errores) > 20:
            print(f"   ... y {len(total_errores)-20} errores más.")
        return False
    else:
        print("  Todos los conjuntos de evaluacion cumplen el estandar metodologico.")
        print("  Trazabilidad completa: raw independientes -> raw consolidados -> JSON -> métricas.")
        print(f"  Total de pares evaluados pareados: {total_evaluaciones_esperadas} casos x {len(DIMENSIONES_ESPERADAS)} dimensiones = {total_juicios} puntuaciones.")
    print("=" * 68)
    return len(total_errores) == 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validador de Integridad de Evaluaciones")
    parser.add_argument("--incluir-judge", action="store_true", help="Incluir validación del dataset LLM-as-a-Judge")
    args = parser.parse_args()
    
    exito = ejecutar_auditoria_completa_evaluaciones(incluir_judge=args.incluir_judge)
    if not exito:
        sys.exit(1)


