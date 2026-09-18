"""
Script de validación de integridad, estructura y consistencia para los datasets de evaluación humana.
Comprueba que las anotaciones de Evaluador 1 y Evaluador 2 cumplen rigurosamente:
- Esquema de campos requerido.
- Integridad de los 42 casos por perfil (126 evaluaciones por evaluador).
- Puntuaciones discretas válidas en escala [0, 3] para las 7 dimensiones analíticas.
- Presencia de justificaciones cualitativas.
- Coherencia cruzada entre el dataset global y las particiones por perfil.
"""

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


def ejecutar_auditoria_completa_evaluaciones():
    """Ejecuta la validación exhaustiva de todos los archivos de evaluación humana."""
    print("=" * 65)
    print("  AUDITORÍA Y VALIDACIÓN DE INTEGRIDAD DE EVALUACIONES HUMANAS")
    print("=" * 65)
    
    archivos_evaluador = {
        "evaluacion_evaluador_1.json": ("evaluador_1", 126),
        "evaluacion_evaluador_2.json": ("evaluador_2", 126),
    }
    
    total_errores = []
    
    # 1. Validar archivos de Evaluador 1 y 2
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
            print(f"  ✅ {fname}: {len(datos)} registros validados correctamente ({ev_id}).")
            
    # 2. Validar particiones por perfil (Evaluador 1)
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
            print(f"  ✅ {fname}: {len(datos_perfil)} casos del perfil '{perfil}' validados.")
            
    # 3. Resumen final
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
        print(f"   Total de pares evaluados pareados: 126 casos x 7 dimensiones = 882 puntuaciones.")
    print("=" * 65)


if __name__ == "__main__":
    ejecutar_auditoria_completa_evaluaciones()
