"""
Script para calcular la concordancia inter-evaluador (Cohen's Kappa)
entre las calificaciones independientes de Evaluador 1 y Evaluador 2.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analisis.metricas_tfg import calcular_cohen_kappa

EVAL_DIR = PROJECT_ROOT / "data" / "evaluaciones"
RESULTS_DIR = PROJECT_ROOT / "results"
INFORMES_DIR = RESULTS_DIR / "informes"
TABLAS_DIR = RESULTS_DIR / "tablas"

INFORMES_DIR.mkdir(parents=True, exist_ok=True)
TABLAS_DIR.mkdir(parents=True, exist_ok=True)


def calcular_acuerdo_inter_evaluadores():
    with open(EVAL_DIR / "evaluacion_evaluador_1.json", "r", encoding="utf-8") as f:
        evals_1 = json.load(f)
    with open(EVAL_DIR / "evaluacion_evaluador_2.json", "r", encoding="utf-8") as f:
        evals_2 = json.load(f)

    dims = [
        ("D1_correccion_factual", "D1: Factualidad"),
        ("D2_control_alucinaciones", "D2: Alucinaciones"),
        ("D3_claridad_didactica", "D3: Claridad"),
        ("D4_utilidad_pedagogica", "D4: Feedback Pedagógico"),
        ("D5_robustez_seguridad", "D5: Seguridad"),
        ("D6_adaptacion_nivel", "D6: Adaptación al Nivel"),
        ("D7_seguimiento_instrucciones", "D7: Directrices")
    ]

    # Recopilar puntuaciones globales y dimensionales
    todos_scores_1 = []
    todos_scores_2 = []

    scores_dim_1 = {d[0]: [] for d in dims}
    scores_dim_2 = {d[0]: [] for d in dims}

    for e1, e2 in zip(evals_1, evals_2):
        assert e1["caso_id"] == e2["caso_id"] and e1["perfil"] == e2["perfil"]
        for d_key, _ in dims:
            s1 = e1["puntuaciones"][d_key]
            s2 = e2["puntuaciones"][d_key]
            todos_scores_1.append(s1)
            todos_scores_2.append(s2)
            scores_dim_1[d_key].append(s1)
            scores_dim_2[d_key].append(s2)

    # Cálculo global
    res_global = calcular_cohen_kappa(todos_scores_1, todos_scores_2)

    # Cálculo dimensional
    res_dimensiones = {}
    for d_key, d_nombre in dims:
        res_d = calcular_cohen_kappa(scores_dim_1[d_key], scores_dim_2[d_key])
        res_dimensiones[d_key] = {
            "nombre": d_nombre,
            "kappa": res_d["kappa"],
            "po": res_d["acuerdo_observado_po"],
            "pe": res_d["acuerdo_esperado_pe"],
            "n": res_d["total_pares"],
            "interpretacion": res_d["interpretacion"]
        }

    informe_final = {
        "global": res_global,
        "por_dimension": res_dimensiones
    }

    # Guardar informe JSON
    with open(INFORMES_DIR / "concordancia_inter_evaluadores.json", "w", encoding="utf-8") as f:
        json.dump(informe_final, f, indent=2, ensure_ascii=False)

    # Generar tabla Markdown
    lineas_md = [
        "# Concordancia Inter-Evaluador (Cohen's Kappa)",
        "",
        rf"**Kappa Global ($\kappa$):** {res_global['kappa']} (Po = {res_global['acuerdo_observado_po']}, Pe = {res_global['acuerdo_esperado_pe']}) - *{res_global['interpretacion']}*",
        rf"**Total de juicios emparejados:** {res_global['total_pares']} (126 respuestas $\times$ 7 dimensiones)",
        "",
        r"| Dimensión | Kappa ($\kappa$) | Acuerdo Observado ($P_o$) | Acuerdo Esperado ($P_e$) | Interpretación |",
        "| :--- | :---: | :---: | :---: | :--- |"
    ]

    for d_key, d_nombre in dims:
        info = res_dimensiones[d_key]
        lineas_md.append(f"| {info['nombre']} | {info['kappa']} | {info['po']} | {info['pe']} | {info['interpretacion']} |")

    with open(TABLAS_DIR / "tabla_kappa_dimensiones.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_md) + "\n")

    print(f"✅ Concordancia calculada exitosamente:")
    print(f"   -> Kappa Global: {res_global['kappa']} ({res_global['interpretacion']})")
    for d_key, d_nombre in dims:
        print(f"   -> {d_nombre}: kappa = {res_dimensiones[d_key]['kappa']}")


if __name__ == "__main__":
    calcular_acuerdo_inter_evaluadores()
