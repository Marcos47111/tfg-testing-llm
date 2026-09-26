"""
Módulo de análisis comparativo y agregación estadística de experimentos para el TFG.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analisis.metricas_tfg import generar_informe_sintetico, calcular_medias_primarias_vs_transversales, PESOS_DIMENSIONES

EVALUACIONES_DIR = PROJECT_ROOT / "data" / "evaluaciones"
RESULTS_DIR = PROJECT_ROOT / "results"
INFORMES_DIR = RESULTS_DIR / "informes"
TABLAS_DIR = RESULTS_DIR / "tablas"


PERFILES_CHATBOT = ["asistente_base", "tutor_directo", "tutor_socratico"]
NOMBRES_PERFIL = {
    "asistente_base": "Asistente Base",
    "tutor_directo": "Tutor Directo",
    "tutor_socratico": "Tutor Socrático"
}


def analizar_todos_los_experimentos() -> Dict[str, Any]:
    """Genera el análisis comparativo global de los 3 perfiles de chatbot evaluados y el análisis de sensibilidad."""
    INFORMES_DIR.mkdir(parents=True, exist_ok=True)
    TABLAS_DIR.mkdir(parents=True, exist_ok=True)
    
    resumen_global = {}
    sensibilidad_global = {}
    filas_tabla_comparativa = []
    
    for perfil in PERFILES_CHATBOT:
        ar = EVALUACIONES_DIR / f"evaluacion_{perfil}.json"
        if not ar.exists():
            print(f"[!] Archivo no encontrado: {ar.name}")
            continue
        with open(ar, "r", encoding="utf-8") as f:
            evaluaciones = json.load(f)
            
        informe = generar_informe_sintetico(evaluaciones)
        sensibilidad = calcular_medias_primarias_vs_transversales(evaluaciones)
        
        resumen_global[perfil] = informe
        sensibilidad_global[perfil] = sensibilidad
        
        nombre_humano = NOMBRES_PERFIL.get(perfil, perfil)
        fila = {
            "Perfil": nombre_humano,
            "IQE (0-100)": round(informe["indice_calidad_educativa_iqe"], 2),
            "CFR (%)": round(informe["tasa_fallos_criticos_cfr"], 2),
            "HR (%)": round(informe["tasa_alucinaciones_hr"], 2),
            "D1 Factual": round(informe["medias_por_dimension"]["D1_correccion_factual"], 2),
            "D2 Alucinación": round(informe["medias_por_dimension"]["D2_control_alucinaciones"], 2),
            "D3 Claridad": round(informe["medias_por_dimension"]["D3_claridad_didactica"], 2),
            "D4 Feedback": round(informe["medias_por_dimension"]["D4_utilidad_pedagogica"], 2),
            "D5 Seguridad": round(informe["medias_por_dimension"]["D5_robustez_seguridad"], 2),
            "D6 Nivel": round(informe["medias_por_dimension"]["D6_adaptacion_nivel"], 2),
            "D7 Directrices": round(informe["medias_por_dimension"]["D7_seguimiento_instrucciones"], 2)
        }
        filas_tabla_comparativa.append(fila)
        
    # Guardar informes en JSON
    with open(INFORMES_DIR / "resumen_comparativo_global.json", "w", encoding="utf-8") as f:
        json.dump(resumen_global, f, indent=2, ensure_ascii=False)
        
    with open(INFORMES_DIR / "sensibilidad_primaria_transversal.json", "w", encoding="utf-8") as f:
        json.dump(sensibilidad_global, f, indent=2, ensure_ascii=False)
        
    # Guardar tabla comparativa en CSV y Markdown
    df_comp = pd.DataFrame(filas_tabla_comparativa)
    df_comp.to_csv(TABLAS_DIR / "tabla_comparativa_modelos.csv", index=False)
    
    columnas = list(df_comp.columns)
    lineas_md = [
        "# Tabla Comparativa de Rendimiento por Perfil (Evaluación Humana Gold Standard)",
        "",
        "| " + " | ".join(columnas) + " |",
        "| " + " | ".join([":---" if i == 0 else ":---:" for i in range(len(columnas))]) + " |"
    ]
    for _, row in df_comp.iterrows():
        lineas_md.append("| " + " | ".join(str(row[c]) for c in columnas) + " |")
        
    with open(TABLAS_DIR / "tabla_comparativa_modelos.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_md) + "\n")
        
    # Generar tabla LaTeX comparativa
    lineas_tex = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\small",
        r"\caption{Resumen comparativo de métricas de calidad y fiabilidad por perfil de chatbot}",
        r"\label{tab:comparativa_modelos}",
        r"\begin{tabular}{lcccccccccc}",
        r"\toprule",
        r"\textbf{Perfil} & \textbf{IQE} & \textbf{CFR (\%)} & \textbf{HR (\%)} & \textbf{D1} & \textbf{D2} & \textbf{D3} & \textbf{D4} & \textbf{D5} & \textbf{D6} & \textbf{D7} \\",
        r"\midrule"
    ]
    for _, r in df_comp.iterrows():
        lineas_tex.append(
            rf"{r['Perfil']} & \textbf{{{r['IQE (0-100)']:.2f}}} & {r['CFR (%)']:.2f} & {r['HR (%)']:.2f} & "
            rf"{r['D1 Factual']:.2f} & {r['D2 Alucinación']:.2f} & {r['D3 Claridad']:.2f} & "
            rf"{r['D4 Feedback']:.2f} & {r['D5 Seguridad']:.2f} & {r['D6 Nivel']:.2f} & {r['D7 Directrices']:.2f} \\"
        )
    lineas_tex.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}"
    ])
    with open(TABLAS_DIR / "tabla_comparativa_modelos.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_tex) + "\n")

    # Generar tabla de Análisis de Sensibilidad (Primaria vs Transversal)
    dims_nombres = [
        ("D1_correccion_factual", "D1: Factualidad"),
        ("D2_control_alucinaciones", "D2: Alucinaciones"),
        ("D3_claridad_didactica", "D3: Claridad Didáctica"),
        ("D4_utilidad_pedagogica", "D4: Feedback Pedagógico"),
        ("D5_robustez_seguridad", "D5: Robustez y Seguridad"),
        ("D6_adaptacion_nivel", "D6: Adaptación al Nivel"),
        ("D7_seguimiento_instrucciones", "D7: Directrices")
    ]
    
    sens_md = [
        "# Análisis de Sensibilidad: Media Transversal ($N=42$) vs Casos Primarios ($N=6$)",
        "",
        "Cuantificación del efecto techo/suelo en la evaluación transversal:",
        "",
        r"| Dimensión | Perfil | Media Transversal ($N=42$) | Media Primaria ($N=6$) | Delta ($\Delta$) |",
        "| :--- | :--- | :---: | :---: | :---: |"
    ]
    sens_rows = []
    for d_key, d_nom in dims_nombres:
        for p in PERFILES_CHATBOT:
            p_nom = NOMBRES_PERFIL.get(p, p)
            info = sensibilidad_global[p][d_key]
            m_t = info["media_transversal"]
            m_p = info["media_primaria"]
            d_val = info["delta_efecto_techo"]
            sens_md.append(f"| {d_nom} | {p_nom} | {m_t:.2f} | {m_p:.2f} | {d_val:+.2f} |")
            sens_rows.append({
                "Dimension": d_nom,
                "Perfil": p_nom,
                "Media_Transversal": m_t,
                "Media_Primaria": m_p,
                "Delta": d_val
            })
            
    with open(TABLAS_DIR / "tabla_sensibilidad_primaria_transversal.md", "w", encoding="utf-8") as f:
        f.write("\n".join(sens_md) + "\n")
        
    df_sens = pd.DataFrame(sens_rows)
    df_sens.to_csv(TABLAS_DIR / "tabla_sensibilidad_primaria_transversal.csv", index=False)
    
    # Sensibilidad LaTeX
    sens_tex = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\small",
        r"\caption{Análisis de sensibilidad: Media transversal ($N=42$) vs Casos primarios de tensión ($N=6$)}",
        r"\label{tab:sensibilidad_primaria_transversal}",
        r"\begin{tabular}{llccc}",
        r"\toprule",
        r"\textbf{Dimensión} & \textbf{Perfil} & \textbf{Media Transversal ($N=42$)} & \textbf{Media Primaria ($N=6$)} & \textbf{Delta ($\Delta$)} \\",
        r"\midrule"
    ]
    for d_key, d_nom in dims_nombres:
        for idx, p in enumerate(PERFILES_CHATBOT):
            p_nom = NOMBRES_PERFIL.get(p, p)
            info = sensibilidad_global[p][d_key]
            dim_col = d_nom if idx == 0 else ""
            sens_tex.append(rf"{dim_col} & {p_nom} & {info['media_transversal']:.2f} & {info['media_primaria']:.2f} & {info['delta_efecto_techo']:+.2f} \\")
        sens_tex.append(r"\midrule")
    if sens_tex[-1] == r"\midrule":
        sens_tex[-1] = r"\bottomrule"
    sens_tex.append(r"\end{tabular}")
    sens_tex.append(r"\end{table}")
    
    with open(TABLAS_DIR / "tabla_sensibilidad_primaria_transversal.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(sens_tex) + "\n")
        
    print(f"[+] Analisis experimental completado con exito. Resultados en {TABLAS_DIR} e {INFORMES_DIR}")
    return resumen_global


if __name__ == "__main__":
    analizar_todos_los_experimentos()

