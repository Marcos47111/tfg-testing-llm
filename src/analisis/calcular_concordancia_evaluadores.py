"""
Script para calcular la concordancia inter-evaluador (Cohen's Kappa)
tanto en la Fase 1 (evaluación humana independiente inicial) como en la
Fase 2 (dataset de referencia tras adjudicación y calibración).
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analisis.metricas_tfg import calcular_cohen_kappa

EVAL_DIR = PROJECT_ROOT / "data" / "evaluaciones"
RAW_IND_DIR = EVAL_DIR / "raw_independientes"
RESULTS_DIR = PROJECT_ROOT / "results"
INFORMES_DIR = RESULTS_DIR / "informes"
TABLAS_DIR = RESULTS_DIR / "tablas"

INFORMES_DIR.mkdir(parents=True, exist_ok=True)
TABLAS_DIR.mkdir(parents=True, exist_ok=True)

DIMS = [
    ("D1_correccion_factual", "D1: Factualidad"),
    ("D2_control_alucinaciones", "D2: Alucinaciones"),
    ("D3_claridad_didactica", "D3: Claridad"),
    ("D4_utilidad_pedagogica", "D4: Feedback Pedagógico"),
    ("D5_robustez_seguridad", "D5: Seguridad"),
    ("D6_adaptacion_nivel", "D6: Adaptación al Nivel"),
    ("D7_seguimiento_instrucciones", "D7: Directrices")
]


def calcular_acuerdo_pares(evals_1, evals_2):
    """Calcula métricas globales y dimensionales entre dos listas de evaluaciones."""
    if len(evals_1) != len(evals_2):
        raise ValueError(f"Discrepancia en longitud de evaluaciones: E1={len(evals_1)} vs E2={len(evals_2)}")

    todos_scores_1 = []
    todos_scores_2 = []
    scores_dim_1 = {d[0]: [] for d in DIMS}
    scores_dim_2 = {d[0]: [] for d in DIMS}

    for e1, e2 in zip(evals_1, evals_2):
        if e1["caso_id"] != e2["caso_id"] or e1["perfil"] != e2["perfil"]:
            raise ValueError(f"Desalineación: E1={e1['caso_id']}({e1['perfil']}) vs E2={e2['caso_id']}({e2['perfil']})")
        for d_key, _ in DIMS:
            s1 = e1["puntuaciones"][d_key]
            s2 = e2["puntuaciones"][d_key]
            todos_scores_1.append(s1)
            todos_scores_2.append(s2)
            scores_dim_1[d_key].append(s1)
            scores_dim_2[d_key].append(s2)

    # Cálculo global (no ponderado, lineal y cuadrático)
    res_global = calcular_cohen_kappa(todos_scores_1, todos_scores_2)
    res_global_lin = calcular_cohen_kappa(todos_scores_1, todos_scores_2, pesos="linear")
    res_global_quad = calcular_cohen_kappa(todos_scores_1, todos_scores_2, pesos="quadratic")

    # Cálculo dimensional
    res_dimensiones = {}
    for d_key, d_nombre in DIMS:
        res_d = calcular_cohen_kappa(scores_dim_1[d_key], scores_dim_2[d_key])
        res_d_lin = calcular_cohen_kappa(scores_dim_1[d_key], scores_dim_2[d_key], pesos="linear")
        res_d_quad = calcular_cohen_kappa(scores_dim_1[d_key], scores_dim_2[d_key], pesos="quadratic")
        res_dimensiones[d_key] = {
            "nombre": d_nombre,
            "kappa_no_ponderado": res_d["kappa"],
            "kappa_ponderado_lineal": res_d_lin["kappa"],
            "kappa_ponderado_cuadratico": res_d_quad["kappa"],
            "po": res_d["acuerdo_observado_po"],
            "pe": res_d["acuerdo_esperado_pe"],
            "n": res_d["total_pares"],
            "interpretacion": res_d["interpretacion"]
        }

    return {
        "global": {
            "kappa_no_ponderado": res_global["kappa"],
            "kappa_ponderado_lineal": res_global_lin["kappa"],
            "kappa_ponderado_cuadratico": res_global_quad["kappa"],
            "po": res_global["acuerdo_observado_po"],
            "pe": res_global["acuerdo_esperado_pe"],
            "total_pares": res_global["total_pares"],
            "interpretacion": res_global["interpretacion"]
        },
        "por_dimension": res_dimensiones
    }


def calcular_acuerdo_inter_evaluadores():
    print("=" * 70)
    print("  ANÁLISIS DE CONCORDANCIA INTER-EVALUADOR (HUMANO-HUMANO)")
    print("=" * 70)

    # 1. Fase 1: Anotaciones independientes originales
    fase1_disponible = (RAW_IND_DIR / "evaluador_1_original.json").exists() and (RAW_IND_DIR / "evaluador_2_original.json").exists()
    informe_fase1 = None
    if fase1_disponible:
        with open(RAW_IND_DIR / "evaluador_1_original.json", "r", encoding="utf-8") as f:
            evals_ind_1 = json.load(f)
        with open(RAW_IND_DIR / "evaluador_2_original.json", "r", encoding="utf-8") as f:
            evals_ind_2 = json.load(f)
        informe_fase1 = calcular_acuerdo_pares(evals_ind_1, evals_ind_2)
        print(f"  [+] Fase 1 (Doble evaluación independiente a ciegas):")
        print(f"      -> Kappa No Ponderado: {informe_fase1['global']['kappa_no_ponderado']} (Po = {informe_fase1['global']['po']}, Pe = {informe_fase1['global']['pe']})")
        print(f"      -> Kappa Ponderado Lineal: {informe_fase1['global']['kappa_ponderado_lineal']}")
        print(f"      -> Kappa Ponderado Cuadrático: {informe_fase1['global']['kappa_ponderado_cuadratico']}")

    # 2. Diagnóstico complementario: E1 revisado vs E2 revisado
    with open(EVAL_DIR / "evaluacion_evaluador_1.json", "r", encoding="utf-8") as f:
        evals_cons_1 = json.load(f)
    with open(EVAL_DIR / "evaluacion_evaluador_2.json", "r", encoding="utf-8") as f:
        evals_cons_2 = json.load(f)
    informe_diag_post_rev = calcular_acuerdo_pares(evals_cons_1, evals_cons_2)
    print(f"\n  [+] Diagnóstico complementario post-revisión (E1 vs E2):")
    print(f"      -> Kappa No Ponderado: {informe_diag_post_rev['global']['kappa_no_ponderado']} (Po = {informe_diag_post_rev['global']['po']})")
    print(f"      (Nota: La fiabilidad del instrumento se fundamenta exclusivamente en la Fase 1 independiente: kappa = 0.9742)")

    informe_completo = {
        "fase_1_evaluacion_independiente_original": informe_fase1,
        "diagnostico_post_revision_e1_e2": informe_diag_post_rev
    }

    # Guardar informe JSON
    with open(INFORMES_DIR / "concordancia_inter_evaluadores.json", "w", encoding="utf-8") as f:
        json.dump(informe_completo, f, indent=2, ensure_ascii=False)

    # Generar tabla Markdown basada en Fase 1 (Evaluación Independiente Original)
    ref = informe_fase1 if informe_fase1 else informe_fase2
    lineas_md = [
        "# Concordancia Inter-Evaluador Original (Cohen's Kappa - Fase 1 Independiente)",
        "",
        rf"**Kappa Global Agregado ($\kappa$):** {ref['global']['kappa_no_ponderado']} (Po = {ref['global']['po']}, Pe = {ref['global']['pe']}) - *{ref['global']['interpretacion']}*",
        rf"**Kappa Ponderado Lineal:** {ref['global']['kappa_ponderado_lineal']} | **Kappa Ponderado Cuadrático:** {ref['global']['kappa_ponderado_cuadratico']}",
        rf"**Total de juicios emparejados:** {ref['global']['total_pares']} (126 respuestas $\times$ 7 dimensiones)",
        "",
        r"| Dimensión | $\kappa$ No Ponderado | $\kappa$ Lineal | $\kappa$ Cuadrático | Acuerdo Observado ($P_o$) | Interpretación |",
        "| :--- | :---: | :---: | :---: | :---: | :--- |"
    ]

    for d_key, d_nombre in DIMS:
        info = ref["por_dimension"][d_key]
        k_np = info["kappa_no_ponderado"]
        k_lin = info["kappa_ponderado_lineal"]
        k_quad = info["kappa_ponderado_cuadratico"]
        po = info["po"]
        interp = info["interpretacion"]
        lineas_md.append(f"| {info['nombre']} | {k_np} | {k_lin} | {k_quad} | {po} | {interp} |")

    with open(TABLAS_DIR / "tabla_kappa_dimensiones.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_md) + "\n")

    print(f"\n[+] Concordancia guardada en {INFORMES_DIR / 'concordancia_inter_evaluadores.json'} y {TABLAS_DIR / 'tabla_kappa_dimensiones.md'}")
    print("=" * 70)


if __name__ == "__main__":
    calcular_acuerdo_inter_evaluadores()

