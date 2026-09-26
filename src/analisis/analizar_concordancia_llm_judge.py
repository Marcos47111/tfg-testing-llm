"""
Módulo de Análisis Estadístico y Concordancia Humano-IA (LLM-as-a-Judge vs Juicio Humano Experto Gold Standard).
Calcula de forma rigurosa:
- Cohen's Kappa global y dimensional (no ponderado, ponderado lineal y ponderado cuadrático).
- Acuerdo observado (Po), acuerdo esperado (Pe), acuerdo exacto (%) y MAE por dimensión.
- Distribución de deltas de discrepancia (|Δ| = 0, 1, 2, 3) y balance de sesgo direccional.
- Matrices de confusión 4x4 (global y dimensional).
- Sensibilidad en fallos críticos (Safety-First: Falsos Positivos, Falsos Negativos, Recall, Especificidad e Intervalos Wilson 95%).
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

from src.analisis.metricas_tfg import (
    calcular_cohen_kappa,
    calcular_cohen_kappa_ponderado,
    calcular_intervalo_wilson,
    es_fallo_critico
)

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
    """Analiza la magnitud de las discrepancias entre el juicio humano y el juez automático."""
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
            "sobrevaloraciones_juez": sobrevaloraciones,
            "infravaloraciones_juez": infravaloraciones,
            "balance_neto": sobrevaloraciones - infravaloraciones
        }
    }


def analizar_fallos_criticos_cruzados(
    evals_humano: List[Dict[str, Any]],
    evals_juez: List[Dict[str, Any]],
    nombre_humano_ref: str = "Humano (Gold Standard)"
) -> Dict[str, Any]:
    """
    Evalúa la alineación en detección de fallos críticos (Safety-First: D1=0, D2=0 o D5=0)
    entre el evaluador humano de referencia (Gold Standard) y el juez automático.
    """
    total_casos = len(evals_humano)
    coinciden_critico = 0
    coinciden_no_critico = 0
    falso_positivo_juez = []  # Juez asigna crítico, humano no
    falso_negativo_juez = []  # Humano asigna crítico, juez no
    
    for h, j in zip(evals_humano, evals_juez):
        if h["caso_id"] != j["caso_id"] or h["perfil"] != j["perfil"]:
            raise ValueError(f"Desalineación entre datasets: Humano={h['caso_id']}({h['perfil']}) vs Juez={j['caso_id']}({j['perfil']})")
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
                "humano_referencia": h["puntuaciones"],
                "juez": j["puntuaciones"]
            })
        elif h_crit and not j_crit:
            falso_negativo_juez.append({
                "caso_id": cid,
                "perfil": perf,
                "humano_referencia": h["puntuaciones"],
                "juez": j["puntuaciones"]
            })
            
    # Detección por dimensión crítica individual (D1, D2, D5 con puntuación 0)
    det_por_dim = {}
    for dim_crit in ["D1_correccion_factual", "D2_control_alucinaciones", "D5_robustez_seguridad"]:
        h_ceros = sum(1 for h in evals_humano if h["puntuaciones"].get(dim_crit) == 0)
        j_coincide_cero = sum(1 for h, j in zip(evals_humano, evals_juez) if h["puntuaciones"].get(dim_crit) == 0 and j["puntuaciones"].get(dim_crit) == 0)
        tasa_det = round((j_coincide_cero / h_ceros * 100), 2) if h_ceros > 0 else 100.0
        wilson_dim = calcular_intervalo_wilson(j_coincide_cero, h_ceros) if h_ceros > 0 else {"ci_low_pct": 100.0, "ci_high_pct": 100.0}
        det_por_dim[dim_crit] = {
            "ceros_humano_referencia": h_ceros,
            "ceros_detectados_por_juez": j_coincide_cero,
            "tasa_deteccion_sensibilidad_pct": tasa_det,
            "intervalo_confianza_wilson_95": {
                "ci_low_pct": wilson_dim["ci_low_pct"],
                "ci_high_pct": wilson_dim["ci_high_pct"]
            }
        }

    tp = coinciden_critico
    tn = coinciden_no_critico
    fp = len(falso_positivo_juez)
    fn = len(falso_negativo_juez)
    
    sensibilidad = round((tp / (tp + fn)) * 100, 2) if (tp + fn) > 0 else 0.0
    especificidad = round((tn / (tn + fp)) * 100, 2) if (tn + fp) > 0 else 0.0
    fnr = round((fn / (tp + fn)) * 100, 2) if (tp + fn) > 0 else 0.0
    fpr = round((fp / (tn + fp)) * 100, 2) if (tn + fp) > 0 else 0.0
    accuracy = round(((tp + tn) / total_casos) * 100, 2)
    
    wilson_sens = calcular_intervalo_wilson(tp, tp + fn) if (tp + fn) > 0 else {"ci_low_pct": 0.0, "ci_high_pct": 0.0}
    wilson_esp = calcular_intervalo_wilson(tn, tn + fp) if (tn + fp) > 0 else {"ci_low_pct": 0.0, "ci_high_pct": 0.0}
            
    return {
        "evaluador_humano_referencia": nombre_humano_ref,
        "total_respuestas_evaluadas": total_casos,
        "matriz_confusion_2x2": {
            "verdaderos_positivos_TP": tp,
            "falsos_negativos_FN": fn,
            "falsos_positivos_FP": fp,
            "verdaderos_negativos_TN": tn
        },
        "exactitud_accuracy_pct": accuracy,
        "sensibilidad_recall_critico_pct": sensibilidad,
        "intervalo_sensibilidad_wilson_95": {
            "ci_low_pct": wilson_sens["ci_low_pct"],
            "ci_high_pct": wilson_sens["ci_high_pct"]
        },
        "especificidad_pct": especificidad,
        "intervalo_especificidad_wilson_95": {
            "ci_low_pct": wilson_esp["ci_low_pct"],
            "ci_high_pct": wilson_esp["ci_high_pct"]
        },
        "tasa_falsos_negativos_fnr_pct": fnr,
        "tasa_falsos_positivos_fpr_pct": fpr,
        "deteccion_fallos_criticos_por_dimension": det_por_dim,
        "falsos_positivos_detalle": falso_positivo_juez,
        "falsos_negativos_detalle": falso_negativo_juez
    }


def ejecutar_analisis_concordancia_llm_judge():
    """Ejecuta el pipeline completo de concordancia y análisis estadístico Humano (Gold Standard) vs LLM-as-a-Judge."""
    INFORMES_DIR.mkdir(parents=True, exist_ok=True)
    TABLAS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Cargar datasets y alinear por clave canónica (caso_id, perfil)
    judge_file = JUDGE_DIR / "evaluacion_llm_judge.json"
    if not judge_file.exists():
        print(f"[-] Error: No se encontró el dataset del juez en {judge_file}.")
        print("    Para generarlo mediante inferencia real con Qwen2.5-14B-Instruct, ejecuta:")
        print("    python3 src/evaluador/evaluador_llm_judge.py --mode ollama --model qwen2.5:14b-instruct --temperature 0")
        return None

    with open(EVAL_DIR / "evaluacion_evaluador_1.json", "r", encoding="utf-8") as f:
        evals_humano_list = json.load(f)
    with open(judge_file, "r", encoding="utf-8") as f:
        evals_judge_list = json.load(f)
        
    map_humano = {(x["caso_id"], x["perfil"]): x for x in evals_humano_list}
    map_judge = {(x["caso_id"], x["perfil"]): x for x in evals_judge_list}
    
    claves_ordenadas = sorted(map_humano.keys())
    evals_humano = [map_humano[k] for k in claves_ordenadas]
    evals_judge = [map_judge[k] for k in claves_ordenadas]
        
    print("=" * 70)
    print("  ANÁLISIS DE CONCORDANCIA HUMANO-IA (LLM-AS-A-JUDGE vs GOLD STANDARD)")
    print("=" * 70)
    
    # Recopilar vectores de puntuaciones
    scores_humano_global = []
    scores_judge_global = []
    
    scores_dim_humano = {d[0]: [] for d in DIMENSIONES}
    scores_dim_judge = {d[0]: [] for d in DIMENSIONES}
    
    for h, j in zip(evals_humano, evals_judge):
        if h["caso_id"] != j["caso_id"] or h["perfil"] != j["perfil"]:
            raise ValueError(f"Desalineación entre datasets: Humano={h['caso_id']}, Juez={j['caso_id']}")
        for d_key, _ in DIMENSIONES:
            s_h = h["puntuaciones"][d_key]
            s_j = j["puntuaciones"][d_key]
            
            scores_humano_global.append(s_h)
            scores_judge_global.append(s_j)
            
            scores_dim_humano[d_key].append(s_h)
            scores_dim_judge[d_key].append(s_j)
            
    n_global = len(scores_humano_global)
            
    # 2. Kappa Global (No Ponderado, Lineal, Cuadrático)
    kappa_global_unweighted = calcular_cohen_kappa(scores_humano_global, scores_judge_global)
    kappa_global_linear = calcular_cohen_kappa_ponderado(scores_humano_global, scores_judge_global, tipo_ponderacion="lineal")
    kappa_global_quadratic = calcular_cohen_kappa_ponderado(scores_humano_global, scores_judge_global, tipo_ponderacion="cuadratico")
    mae_global = calcular_mae(scores_humano_global, scores_judge_global)
    
    # 3. Kappa y Métricas Dimensionales
    concordancia_dimensional = {}
    matrices_confusion_dim = {}
    filas_tabla = []
    
    for d_key, d_nombre in DIMENSIONES:
        k_unw = calcular_cohen_kappa(scores_dim_humano[d_key], scores_dim_judge[d_key])
        k_lin = calcular_cohen_kappa_ponderado(scores_dim_humano[d_key], scores_dim_judge[d_key], tipo_ponderacion="lineal")
        k_quad = calcular_cohen_kappa_ponderado(scores_dim_humano[d_key], scores_dim_judge[d_key], tipo_ponderacion="cuadratico")
        
        mae_dim = calcular_mae(scores_dim_humano[d_key], scores_dim_judge[d_key])
        mat_dim = calcular_matriz_confusion_4x4(scores_dim_humano[d_key], scores_dim_judge[d_key])
        matrices_confusion_dim[d_key] = mat_dim
        
        media_humano = round(float(np.mean(scores_dim_humano[d_key])), 3)
        media_judge = round(float(np.mean(scores_dim_judge[d_key])), 3)
        sesgo = round(media_judge - media_humano, 3)
        acuerdo_exacto_pct = round(k_unw["acuerdo_observado_po"] * 100, 2)
        
        concordancia_dimensional[d_key] = {
            "nombre": d_nombre,
            "kappa_no_ponderado": k_unw["kappa"],
            "kappa_ponderado_lineal": k_lin["kappa_ponderado"],
            "kappa_ponderado_cuadratico": k_quad["kappa_ponderado"],
            "po": k_unw["acuerdo_observado_po"],
            "pe": k_unw["acuerdo_esperado_pe"],
            "acuerdo_exacto_pct": acuerdo_exacto_pct,
            "mae": round(mae_dim, 4),
            "interpretacion": k_unw["interpretacion"],
            "media_humano_gold_standard": media_humano,
            "media_judge": media_judge,
            "sesgo_juez_menos_humano": sesgo
        }
        
        filas_tabla.append({
            "Dimensión": d_nombre,
            "Kappa (No pond.)": k_unw["kappa"],
            "Kappa (Lineal)": k_lin["kappa_ponderado"],
            "Kappa (Cuadrático)": k_quad["kappa_ponderado"],
            "P_o": k_unw["acuerdo_observado_po"],
            "P_e": k_unw["acuerdo_esperado_pe"],
            "MAE": round(mae_dim, 3),
            "Media Humano": media_humano,
            "Media Juez": media_judge,
            "Sesgo": f"{'+' if sesgo > 0 else ''}{sesgo}",
            "Nivel de Acuerdo": k_unw["interpretacion"]
        })
        
    # 4. Distribución de Deltas y Matrices de Confusión
    deltas_global = analizar_distribucion_deltas(scores_humano_global, scores_judge_global)
    matriz_conf_global = calcular_matriz_confusion_4x4(scores_humano_global, scores_judge_global)
    
    # 5. Alineación de Fallos Críticos (Safety-First)
    safety_first = analizar_fallos_criticos_cruzados(evals_humano, evals_judge, nombre_humano_ref="Humano (Gold Standard)")
    
    # 6. Compilar Informe Consolidado
    informe_completo = {
        "concordancia_global": {
            "total_pares_comparados": len(scores_humano_global),
            "mae_global": round(mae_global, 4),
            "kappa_no_ponderado": kappa_global_unweighted,
            "kappa_ponderado_lineal": kappa_global_linear,
            "kappa_ponderado_cuadratico": kappa_global_quadratic
        },
        "concordancia_por_dimension": concordancia_dimensional,
        "analisis_discrepancias_deltas": deltas_global,
        "matriz_confusion_global_4x4_filas_humano_columnas_juez": matriz_conf_global,
        "matrices_confusion_por_dimension": matrices_confusion_dim,
        "analisis_safety_first_fallos_criticos": safety_first
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
        "# Tabla de Concordancia Humano-IA (Gold Standard vs LLM-as-a-Judge)",
        "",
        rf"**Kappa Global no ponderado ($\kappa$):** {kappa_global_unweighted['kappa']} (Po = {kappa_global_unweighted['acuerdo_observado_po']}, Pe = {kappa_global_unweighted['acuerdo_esperado_pe']}, MAE = {mae_global:.3f}) - *{kappa_global_unweighted['interpretacion']}*",
        rf"**Kappa Global ponderado lineal ($\kappa_{{\text{{lin}}}}$):** {kappa_global_linear['kappa_ponderado']} - *{kappa_global_linear['interpretacion']}*",
        rf"**Kappa Global ponderado cuadrático ($\kappa_{{\text{{quad}}}}$):** {kappa_global_quadratic['kappa_ponderado']} - *{kappa_global_quadratic['interpretacion']}*",
        rf"**Total juicios emparejados:** {n_global} calificaciones dimensionales.",
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
        r"\caption{Concordancia inter-evaluador entre el Juez Automático (Qwen2.5-14B) y el Juicio Humano Experto de Referencia}",
        r"\label{tab:concordancia_llm_judge}",
        r"\begin{tabular}{lcccccrc}",
        r"\toprule",
        r"\textbf{Dimensión} & \textbf{$\kappa$ (Simple)} & \textbf{$\kappa_{\text{lin}}$} & \textbf{$\kappa_{\text{quad}}$} & \textbf{$P_o$} & \textbf{$P_e$} & \textbf{MAE} & \textbf{Nivel de Acuerdo} \\",
        r"\midrule"
    ]
    for _, r in df_tab.iterrows():
        k1 = f"{r['Kappa (No pond.)']:.3f}" if isinstance(r['Kappa (No pond.)'], (float, int)) else str(r['Kappa (No pond.)'])
        k_lin_val = f"{r['Kappa (Lineal)']:.3f}" if isinstance(r['Kappa (Lineal)'], (float, int)) else str(r['Kappa (Lineal)'])
        k_quad_val = f"{r['Kappa (Cuadrático)']:.3f}" if isinstance(r['Kappa (Cuadrático)'], (float, int)) else str(r['Kappa (Cuadrático)'])
        po = f"{r['P_o']:.4f}" if isinstance(r['P_o'], (float, int)) else str(r['P_o'])
        pe = f"{r['P_e']:.4f}" if isinstance(r['P_e'], (float, int)) else str(r['P_e'])
        mae_val = f"{r['MAE']:.3f}" if isinstance(r['MAE'], (float, int)) else str(r['MAE'])
        interp = r['Nivel de Acuerdo']
        lineas_tex.append(rf"{r['Dimensión']} & {k1} & {k_lin_val} & {k_quad_val} & {po} & {pe} & {mae_val} & {interp} \\")
        
    lineas_tex.extend([
        r"\midrule",
        rf"\textbf{{Global ($N_\kappa={n_global}$)}} & \textbf{{{kappa_global_unweighted['kappa']:.3f}}} & \textbf{{{kappa_global_linear['kappa_ponderado']:.3f}}} & \textbf{{{kappa_global_quadratic['kappa_ponderado']:.3f}}} & \textbf{{{kappa_global_unweighted['acuerdo_observado_po']:.4f}}} & \textbf{{{kappa_global_unweighted['acuerdo_esperado_pe']:.4f}}} & \textbf{{{mae_global:.3f}}} & \textbf{{{kappa_global_unweighted['interpretacion']}}} \\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}"
    ])
    
    with open(TABLAS_DIR / "tabla_concordancia_llm_judge.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_tex) + "\n")
        
    tp = safety_first["matriz_confusion_2x2"]["verdaderos_positivos_TP"]
    fn = safety_first["matriz_confusion_2x2"]["falsos_negativos_FN"]
    fp = safety_first["matriz_confusion_2x2"]["falsos_positivos_FP"]
    tn = safety_first["matriz_confusion_2x2"]["verdaderos_negativos_TN"]
    acc = safety_first["exactitud_accuracy_pct"]
    sens = safety_first["sensibilidad_recall_critico_pct"]
    esp = safety_first["especificidad_pct"]
    
    det_dim = safety_first["deteccion_fallos_criticos_por_dimension"]
    
    print(f"  [+] Tablas exportadas en {TABLAS_DIR}")
    print("\n  Resumen de Resultados Principales:")
    print(f"   -> Kappa Global No Ponderado: {kappa_global_unweighted['kappa']} ({kappa_global_unweighted['interpretacion']})")
    print(f"   -> Kappa Global Ponderado Lineal: {kappa_global_linear['kappa_ponderado']} ({kappa_global_linear['interpretacion']})")
    print(f"   -> Kappa Global Ponderado Cuadrático: {kappa_global_quadratic['kappa_ponderado']} ({kappa_global_quadratic['interpretacion']})")
    print(f"   -> MAE Global: {mae_global:.4f}")
    print(f"   -> Acuerdo exacto (|Δ|=0): {deltas_global['acuerdo_exacto_delta_0']['recuento']}/{n_global} ({deltas_global['acuerdo_exacto_delta_0']['porcentaje']}%)")
    print(f"   -> Discrepancia menor (|Δ|=1): {deltas_global['discrepancia_menor_delta_1']['recuento']}/{n_global} ({deltas_global['discrepancia_menor_delta_1']['porcentaje']}%)")
    print(f"   -> Discrepancias mayores (|Δ|>=2): {deltas_global['discrepancia_moderada_delta_2']['recuento'] + deltas_global['discrepancia_severa_delta_3']['recuento']}/{n_global}")
    print(f"   -> Safety-First Accuracy: {acc}% (TP={tp}, TN={tn}, FP={fp}, FN={fn})")
    print(f"   -> Safety-First Sensibilidad (Recall Crítico): {sens}% [IC 95%: {safety_first['intervalo_sensibilidad_wilson_95']['ci_low_pct']}% - {safety_first['intervalo_sensibilidad_wilson_95']['ci_high_pct']}%] (detecta {tp}/{tp+fn} respuestas críticas)")
    print(f"   -> Safety-First Especificidad: {esp}% [IC 95%: {safety_first['intervalo_especificidad_wilson_95']['ci_low_pct']}% - {safety_first['intervalo_especificidad_wilson_95']['ci_high_pct']}%] (detecta {tn}/{tn+fp} respuestas conformes)")
    print(f"   -> Detección Ceros D1 Factualidad: {det_dim['D1_correccion_factual']['ceros_detectados_por_juez']}/{det_dim['D1_correccion_factual']['ceros_humano_referencia']} ({det_dim['D1_correccion_factual']['tasa_deteccion_sensibilidad_pct']}%)")
    print(f"   -> Detección Ceros D2 Alucinaciones: {det_dim['D2_control_alucinaciones']['ceros_detectados_por_juez']}/{det_dim['D2_control_alucinaciones']['ceros_humano_referencia']} ({det_dim['D2_control_alucinaciones']['tasa_deteccion_sensibilidad_pct']}%)")
    print(f"   -> Detección Ceros D5 Seguridad: {det_dim['D5_robustez_seguridad']['ceros_detectados_por_juez']}/{det_dim['D5_robustez_seguridad']['ceros_humano_referencia']} ({det_dim['D5_robustez_seguridad']['tasa_deteccion_sensibilidad_pct']}%)")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_analisis_concordancia_llm_judge()

