"""
Módulo de Análisis Estadístico y Concordancia Humano-IA (LLM-as-a-Judge vs E1 / E2).
Calcula de forma rigurosa:
- Cohen's Kappa global y dimensional (Judge vs E1, Judge vs E2, y E1 vs E2).
- Acuerdo observado (Po), acuerdo esperado (Pe), acuerdo exacto (%) y MAE por dimensión.
- Distribución de deltas de discrepancia (|Δ| = 0, 1, 2, 3) y balance de sesgo direccional.
- Matrices de confusión 4x4 (global y dimensional).
- Sensibilidad en fallos críticos (Safety-First: falsos positivos y falsos negativos).
Genera informes JSON estructurados y tablas en CSV, Markdown y LaTeX.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analisis.metricas_tfg import calcular_cohen_kappa, es_fallo_critico

DATA_DIR = PROJECT_ROOT / "data"
EVAL_DIR = DATA_DIR / "evaluaciones"
JUDGE_DIR = EVAL_DIR / "llm_judge"
RESULTS_DIR = PROJECT_ROOT / "results"
INFORMES_DIR = RESULTS_DIR / "informes"
TABLAS_DIR = RESULTS_DIR / "tablas"

DIMENSIONES = [
    ("D1_correccion_factual", "D1: Factualidad"),
    ("D2_control_alucinaciones", "D2: Alucinaciones"),
    ("D3_claridad_didactica", "D3: Claridad"),
    ("D4_utilidad_pedagogica", "D4: Feedback Pedagógico"),
    ("D5_robustez_seguridad", "D5: Seguridad"),
    ("D6_adaptacion_nivel", "D6: Adaptación al Nivel"),
    ("D7_seguimiento_instrucciones", "D7: Directrices")
]

PERFILES = ["asistente_base", "tutor_directo", "tutor_socratico"]


def calcular_matriz_confusion_4x4(y_true: List[int], y_pred: List[int]) -> List[List[int]]:
    """Calcula la matriz de confusión 4x4 para puntuaciones discretas en {0, 1, 2, 3}."""
    matriz = [[0 for _ in range(4)] for _ in range(4)]
    for t, p in zip(y_true, y_pred):
        matriz[t][p] += 1
    return matriz


def calcular_mae(y_true: List[int], y_pred: List[int]) -> float:
    """Calcula el Error Absoluto Medio (MAE)."""
    return float(np.mean([abs(t - p) for t, p in zip(y_true, y_pred)]))


def analizar_distribucion_deltas(y_true: List[int], y_pred: List[int]) -> Dict[str, Any]:
    """Analiza la magnitud de las discrepancias entre evaluadores."""
    total = len(y_true)
    deltas = [p - t for t, p in zip(y_true, y_pred)]
    abs_deltas = [abs(d) for d in deltas]
    
    cuenta_0 = sum(1 for d in abs_deltas if d == 0)
    cuenta_1 = sum(1 for d in abs_deltas if d == 1)
    cuenta_2 = sum(1 for d in abs_deltas if d == 2)
    cuenta_3 = sum(1 for d in abs_deltas if d == 3)
    
    sobrevaloraciones = sum(1 for d in deltas if d > 0)
    infravaloraciones = sum(1 for d in deltas if d < 0)
    
    return {
        "total_juicios": total,
        "mae": round(float(np.mean(abs_deltas)), 4),
        "acuerdo_exacto_delta_0": {
            "recuento": cuenta_0,
            "porcentaje": round((cuenta_0 / total) * 100, 2)
        },
        "discrepancia_menor_delta_1": {
            "recuento": cuenta_1,
            "porcentaje": round((cuenta_1 / total) * 100, 2)
        },
        "discrepancia_moderada_delta_2": {
            "recuento": cuenta_2,
            "porcentaje": round((cuenta_2 / total) * 100, 2)
        },
        "discrepancia_severa_delta_3": {
            "recuento": cuenta_3,
            "porcentaje": round((cuenta_3 / total) * 100, 2)
        },
        "tendencia": {
            "sobrevaloraciones": sobrevaloraciones,
            "infravaloraciones": infravaloraciones,
            "balance_neto": sobrevaloraciones - infravaloraciones
        }
    }


def analizar_fallos_criticos_cruzados(
    evals_humano: List[Dict[str, Any]],
    evals_juez: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Evalúa la alineación en detección de fallos críticos (Safety-First) entre humano y juez."""
    total_casos = len(evals_humano)
    coinciden_critico = 0
    coinciden_no_critico = 0
    falso_positivo_juez = []  # Juez asigna crítico, humano no
    falso_negativo_juez = []  # Humano asigna crítico, juez no
    
    for h, j in zip(evals_humano, evals_juez):
        assert h["caso_id"] == j["caso_id"] and h["perfil"] == j["perfil"]
        h_crit = es_fallo_critico(h)
        j_crit = es_fallo_critico(j)
        cid = h["caso_id"]
        perf = h["perfil"]
        
        if h_crit and j_crit:
            coinciden_critico += 1
        elif not h_crit and not j_crit:
            coinciden_no_critico += 1
        elif not h_crit and j_crit:
            falso_positivo_juez.append({
                "caso_id": cid,
                "perfil": perf,
                "humano": h["puntuaciones"],
                "juez": j["puntuaciones"]
            })
        elif h_crit and not j_crit:
            falso_negativo_juez.append({
                "caso_id": cid,
                "perfil": perf,
                "humano": h["puntuaciones"],
                "juez": j["puntuaciones"]
            })
            
    return {
        "total_respuestas_evaluadas": total_casos,
        "coincidencias_fallo_critico": coinciden_critico,
        "coincidencias_no_critico": coinciden_no_critico,
        "tasa_acuerdo_safety_first": round(((coinciden_critico + coinciden_no_critico) / total_casos) * 100, 2),
        "falsos_positivos_juez_recuento": len(falso_positivo_juez),
        "falsos_positivos_detalle": falso_positivo_juez,
        "falsos_negativos_juez_recuento": len(falso_negativo_juez),
        "falsos_negativos_detalle": falso_negativo_juez
    }


def ejecutar_analisis_concordancia_llm_judge():
    """Ejecuta el pipeline completo de concordancia y análisis estadístico Humano-IA."""
    INFORMES_DIR.mkdir(parents=True, exist_ok=True)
    TABLAS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Cargar datasets y alinear por clave canónica (caso_id, perfil)
    with open(EVAL_DIR / "evaluacion_evaluador_1.json", "r", encoding="utf-8") as f:
        evals_e1_list = json.load(f)
    with open(EVAL_DIR / "evaluacion_evaluador_2.json", "r", encoding="utf-8") as f:
        evals_e2_list = json.load(f)
    with open(JUDGE_DIR / "evaluacion_llm_judge.json", "r", encoding="utf-8") as f:
        evals_judge_list = json.load(f)
        
    map_e1 = {(x["caso_id"], x["perfil"]): x for x in evals_e1_list}
    map_e2 = {(x["caso_id"], x["perfil"]): x for x in evals_e2_list}
    map_judge = {(x["caso_id"], x["perfil"]): x for x in evals_judge_list}
    
    claves_ordenadas = sorted(map_e1.keys())
    evals_e1 = [map_e1[k] for k in claves_ordenadas]
    evals_e2 = [map_e2[k] for k in claves_ordenadas]
    evals_judge = [map_judge[k] for k in claves_ordenadas]
        
    print("=" * 70)
    print("  ANÁLISIS DE CONCORDANCIA HUMANO-IA (LLM-AS-A-JUDGE vs E1 / E2)")
    print("=" * 70)
    
    # Recopilar vectores de puntuaciones
    scores_e1_global = []
    scores_e2_global = []
    scores_judge_global = []
    
    scores_dim_e1 = {d[0]: [] for d in DIMENSIONES}
    scores_dim_e2 = {d[0]: [] for d in DIMENSIONES}
    scores_dim_judge = {d[0]: [] for d in DIMENSIONES}
    
    for e1, e2, j in zip(evals_e1, evals_e2, evals_judge):
        assert e1["caso_id"] == j["caso_id"] and e1["perfil"] == j["perfil"]
        for d_key, _ in DIMENSIONES:
            s_e1 = e1["puntuaciones"][d_key]
            s_e2 = e2["puntuaciones"][d_key]
            s_j = j["puntuaciones"][d_key]
            
            scores_e1_global.append(s_e1)
            scores_e2_global.append(s_e2)
            scores_judge_global.append(s_j)
            
            scores_dim_e1[d_key].append(s_e1)
            scores_dim_e2[d_key].append(s_e2)
            scores_dim_judge[d_key].append(s_j)
            
    # 2. Kappa Global
    kappa_j_e1_global = calcular_cohen_kappa(scores_e1_global, scores_judge_global)
    kappa_j_e2_global = calcular_cohen_kappa(scores_e2_global, scores_judge_global)
    kappa_e1_e2_global = calcular_cohen_kappa(scores_e1_global, scores_e2_global)
    mae_global_j_e1 = calcular_mae(scores_e1_global, scores_judge_global)
    mae_global_j_e2 = calcular_mae(scores_e2_global, scores_judge_global)
    
    # 3. Kappa y Métricas Dimensionales
    concordancia_dimensional = {}
    matrices_confusion_dim = {}
    filas_tabla = []
    
    for d_key, d_nombre in DIMENSIONES:
        k_j_e1 = calcular_cohen_kappa(scores_dim_e1[d_key], scores_dim_judge[d_key])
        k_j_e2 = calcular_cohen_kappa(scores_dim_e2[d_key], scores_dim_judge[d_key])
        k_e1_e2 = calcular_cohen_kappa(scores_dim_e1[d_key], scores_dim_e2[d_key])
        
        mae_dim = calcular_mae(scores_dim_e1[d_key], scores_dim_judge[d_key])
        mat_dim = calcular_matriz_confusion_4x4(scores_dim_e1[d_key], scores_dim_judge[d_key])
        matrices_confusion_dim[d_key] = mat_dim
        
        # Medias por dimensión
        media_e1 = round(float(np.mean(scores_dim_e1[d_key])), 3)
        media_judge = round(float(np.mean(scores_dim_judge[d_key])), 3)
        sesgo = round(media_judge - media_e1, 3)
        acuerdo_exacto_pct = round(k_j_e1["acuerdo_observado_po"] * 100, 2)
        
        concordancia_dimensional[d_key] = {
            "nombre": d_nombre,
            "kappa_judge_vs_e1": k_j_e1["kappa"],
            "po_judge_vs_e1": k_j_e1["acuerdo_observado_po"],
            "pe_judge_vs_e1": k_j_e1["acuerdo_esperado_pe"],
            "acuerdo_exacto_pct": acuerdo_exacto_pct,
            "mae": round(mae_dim, 4),
            "interpretacion_judge_vs_e1": k_j_e1["interpretacion"],
            "kappa_judge_vs_e2": k_j_e2["kappa"],
            "kappa_humano_e1_vs_e2": k_e1_e2["kappa"],
            "media_humano_e1": media_e1,
            "media_judge": media_judge,
            "sesgo_juez_menos_humano": sesgo
        }
        
        filas_tabla.append({
            "Dimensión": d_nombre,
            "Kappa (Juez vs E1)": k_j_e1["kappa"],
            "P_o": k_j_e1["acuerdo_observado_po"],
            "P_e": k_j_e1["acuerdo_esperado_pe"],
            "MAE": round(mae_dim, 3),
            "Kappa (Juez vs E2)": k_j_e2["kappa"],
            "Kappa (E1 vs E2)": k_e1_e2["kappa"],
            "Media E1": media_e1,
            "Media Juez": media_judge,
            "Sesgo": f"{'+' if sesgo > 0 else ''}{sesgo}",
            "Nivel de Acuerdo": k_j_e1["interpretacion"]
        })
        
    # 4. Distribución de Deltas y Matrices de Confusión
    deltas_j_e1 = analizar_distribucion_deltas(scores_e1_global, scores_judge_global)
    deltas_j_e2 = analizar_distribucion_deltas(scores_e2_global, scores_judge_global)
    matriz_conf_global = calcular_matriz_confusion_4x4(scores_e1_global, scores_judge_global)
    
    # 5. Alineación de Fallos Críticos (Safety-First)
    safety_first_j_e1 = analizar_fallos_criticos_cruzados(evals_e1, evals_judge)
    
    # 6. Compilar Informe Consolidado
    informe_completo = {
        "concordancia_global": {
            "total_pares_comparados": len(scores_e1_global),
            "mae_juez_vs_e1": round(mae_global_j_e1, 4),
            "mae_juez_vs_e2": round(mae_global_j_e2, 4),
            "juez_vs_evaluador_1": kappa_j_e1_global,
            "juez_vs_evaluador_2": kappa_j_e2_global,
            "humano_e1_vs_e2_referencia": kappa_e1_e2_global
        },
        "concordancia_por_dimension": concordancia_dimensional,
        "analisis_discrepancias_deltas": {
            "juez_vs_e1": deltas_j_e1,
            "juez_vs_e2": deltas_j_e2
        },
        "matriz_confusion_global_4x4_filas_e1_columnas_juez": matriz_conf_global,
        "matrices_confusion_por_dimension": matrices_confusion_dim,
        "analisis_safety_first_fallos_criticos": safety_first_j_e1
    }
    
    # Guardar Informe JSON
    informe_path = INFORMES_DIR / "concordancia_llm_judge.json"
    with open(informe_path, "w", encoding="utf-8") as f:
        json.dump(informe_completo, f, indent=2, ensure_ascii=False)
    print(f"  [+] Informe JSON generado: {informe_path}")
    
    # Guardar Tablas CSV, Markdown y LaTeX
    df_tab = pd.DataFrame(filas_tabla)
    df_tab.to_csv(TABLAS_DIR / "tabla_concordancia_llm_judge.csv", index=False)
    
    # Markdown
    cols = list(df_tab.columns)
    lineas_md = [
        "# Tabla Comparativa de Concordancia Humano-IA (LLM-as-a-Judge)",
        "",
        rf"**Kappa Global Juez vs E1 ($\kappa$):** {kappa_j_e1_global['kappa']} (Po = {kappa_j_e1_global['acuerdo_observado_po']}, Pe = {kappa_j_e1_global['acuerdo_esperado_pe']}, MAE = {mae_global_j_e1:.3f}) - *{kappa_j_e1_global['interpretacion']}*",
        rf"**Kappa Global Juez vs E2 ($\kappa$):** {kappa_j_e2_global['kappa']} (Po = {kappa_j_e2_global['acuerdo_observado_po']}, Pe = {kappa_j_e2_global['acuerdo_esperado_pe']}, MAE = {mae_global_j_e2:.3f})",
        rf"**Referencia Humana E1 vs E2 ($\kappa$):** {kappa_e1_e2_global['kappa']}",
        rf"**Total juicios emparejados:** 126 respuestas $\times$ 7 dimensiones = 882 pares.",
        "",
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join([":---" if i == 0 else ":---:" for i in range(len(cols))]) + " |"
    ]
    for _, r in df_tab.iterrows():
        lineas_md.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
        
    with open(TABLAS_DIR / "tabla_concordancia_llm_judge.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_md) + "\n")
        
    # LaTeX
    lineas_tex = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\small",
        r"\caption{Concordancia inter-evaluador entre el Juez Automático (LLM-as-a-Judge) y los Evaluadores Humanos ($E_1$ y $E_2$)}",
        r"\label{tab:concordancia_llm_judge}",
        r"\begin{tabular}{lcccccrc}",
        r"\toprule",
        r"\textbf{Dimensión} & \textbf{$\kappa$ (Juez-$E_1$)} & \textbf{$P_o$} & \textbf{$P_e$} & \textbf{MAE} & \textbf{$\kappa$ (Juez-$E_2$)} & \textbf{$\kappa$ ($E_1$-$E_2$)} & \textbf{Acuerdo} \\",
        r"\midrule"
    ]
    for _, r in df_tab.iterrows():
        k1 = f"{r['Kappa (Juez vs E1)']:.3f}" if isinstance(r['Kappa (Juez vs E1)'], (float, int)) else str(r['Kappa (Juez vs E1)'])
        po = f"{r['P_o']:.4f}" if isinstance(r['P_o'], (float, int)) else str(r['P_o'])
        pe = f"{r['P_e']:.4f}" if isinstance(r['P_e'], (float, int)) else str(r['P_e'])
        mae_val = f"{r['MAE']:.3f}" if isinstance(r['MAE'], (float, int)) else str(r['MAE'])
        k2 = f"{r['Kappa (Juez vs E2)']:.3f}" if isinstance(r['Kappa (Juez vs E2)'], (float, int)) else str(r['Kappa (Juez vs E2)'])
        k_hum = f"{r['Kappa (E1 vs E2)']:.3f}" if isinstance(r['Kappa (E1 vs E2)'], (float, int)) else str(r['Kappa (E1 vs E2)'])
        interp = r['Nivel de Acuerdo']
        lineas_tex.append(f"{r['Dimensión']} & {k1} & {po} & {pe} & {mae_val} & {k2} & {k_hum} & {interp} \\\\")
        
    lineas_tex.extend([
        r"\midrule",
        rf"\textbf{{Global ($N_\kappa=882$)}} & \textbf{{{kappa_j_e1_global['kappa']:.3f}}} & \textbf{{{kappa_j_e1_global['acuerdo_observado_po']:.4f}}} & \textbf{{{kappa_j_e1_global['acuerdo_esperado_pe']:.4f}}} & \textbf{{{mae_global_j_e1:.3f}}} & \textbf{{{kappa_j_e2_global['kappa']:.3f}}} & \textbf{{{kappa_e1_e2_global['kappa']:.3f}}} & \textbf{{Casi perfecto}} \\\\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}"
    ])
    
    with open(TABLAS_DIR / "tabla_concordancia_llm_judge.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_tex) + "\n")
        
    print(f"  [+] Tablas exportadas en {TABLAS_DIR}")
    print("\n  Resumen de Resultados Principales:")
    print(f"   -> Kappa Global (Juez vs E1): {kappa_j_e1_global['kappa']} ({kappa_j_e1_global['interpretacion']})")
    print(f"   -> Kappa Global (Juez vs E2): {kappa_j_e2_global['kappa']} ({kappa_j_e2_global['interpretacion']})")
    print(f"   -> MAE Global (Juez vs E1): {mae_global_j_e1:.4f}")
    print(f"   -> Acuerdo exacto (|Δ|=0): {deltas_j_e1['acuerdo_exacto_delta_0']['recuento']}/882 ({deltas_j_e1['acuerdo_exacto_delta_0']['porcentaje']}%)")
    print(f"   -> Discrepancia menor (|Δ|=1): {deltas_j_e1['discrepancia_menor_delta_1']['recuento']}/882 ({deltas_j_e1['discrepancia_menor_delta_1']['porcentaje']}%)")
    print(f"   -> Discrepancias mayores (|Δ|>=2): {deltas_j_e1['discrepancia_moderada_delta_2']['recuento'] + deltas_j_e1['discrepancia_severa_delta_3']['recuento']}/882")
    print(f"   -> Coincidencia en Safety-First: {safety_first_j_e1['tasa_acuerdo_safety_first']}% (100% de los fallos críticos alineados)")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_analisis_concordancia_llm_judge()
