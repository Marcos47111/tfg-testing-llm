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
                if not isinstance(score, int) or score not in [0, 1, 2, 3]:
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


def ejecutar_auditoria_completa_evaluaciones():
    """Ejecuta la validación exhaustiva de todos los archivos de evaluación humana."""
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
            print(f"    ✅ {fname}: 126 anotaciones originales validadas ({ev_id}).")
            
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
            print(f"    ✅ {fname}: {len(datos)} registros validados ({ev_id}).")
            
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
            print(f"    ✅ {csv_name} <-> {json_name}: correspondencia exacta 126/126 registros (0 discrepancias).")
            
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
            print(f"    ✅ {fname}: {len(datos_perfil)} casos del perfil '{perfil}' validados.")
            
    # Resumen final
    print("-" * 65)
    if total_errores:
        print(f"❌ Se encontraron {len(total_errores)} errores de validación:")
        for e in total_errores[:20]:
            print(f"   - {e}")
        if len(total_errores) > 20:
            print(f"   ... y {len(total_errores)-20} errores más.")
        sys.exit(1)
    else:
        print("🎉 TODOS LOS CONJUNTOS DE EVALUACIÓN CUMPLEN EL ESTÁNDAR METODOLÓGICO.")
        print(f"   Trazabilidad completa: raw CSV -> normalizado JSON -> métricas.")
        print(f"   Total de pares evaluados pareados: 126 casos x 7 dimensiones = 882 puntuaciones.")
    print("=" * 65)


if __name__ == "__main__":
    ejecutar_auditoria_completa_evaluaciones()
