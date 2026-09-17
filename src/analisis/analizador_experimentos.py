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

from src.analisis.metricas_tfg import generar_informe_sintetico, PESOS_DIMENSIONES

EVALUACIONES_DIR = PROJECT_ROOT / "data" / "evaluaciones"
RESULTS_DIR = PROJECT_ROOT / "results"
INFORMES_DIR = RESULTS_DIR / "informes"
TABLAS_DIR = RESULTS_DIR / "tablas"


def analizar_todos_los_experimentos() -> Dict[str, Any]:
    """Genera el análisis comparativo global de todos los perfiles evaluados."""
    INFORMES_DIR.mkdir(parents=True, exist_ok=True)
    TABLAS_DIR.mkdir(parents=True, exist_ok=True)
    
    archivos_eval = sorted(EVALUACIONES_DIR.glob("evaluacion_*.json"))
    resumen_global = {}
    filas_tabla_comparativa = []
    
    for ar in archivos_eval:
        perfil = ar.stem.replace("evaluacion_", "")
        with open(ar, "r", encoding="utf-8") as f:
            evaluaciones = json.load(f)
            
        informe = generar_informe_sintetico(evaluaciones)
        resumen_global[perfil] = informe
        
        fila = {
            "Perfil": perfil,
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
        
    # Guardar informe global en JSON
    with open(INFORMES_DIR / "resumen_comparativo_global.json", "w", encoding="utf-8") as f:
        json.dump(resumen_global, f, indent=2, ensure_ascii=False)
        
    # Guardar tabla comparativa en CSV y Markdown manual
    df_comp = pd.DataFrame(filas_tabla_comparativa)
    df_comp.to_csv(TABLAS_DIR / "tabla_comparativa_modelos.csv", index=False)
    
    # Generador de tabla Markdown nativo sin dependencia de tabulate
    columnas = list(df_comp.columns)
    lineas_md = [
        "| " + " | ".join(columnas) + " |",
        "| " + " | ".join([":---" if i == 0 else ":---:" for i in range(len(columnas))]) + " |"
    ]
    for _, row in df_comp.iterrows():
        lineas_md.append("| " + " | ".join(str(row[c]) for c in columnas) + " |")
        
    with open(TABLAS_DIR / "tabla_comparativa_modelos.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_md) + "\n")
        
    print(f"📈 Análisis experimental completado con éxito. Resultados en {TABLAS_DIR} e {INFORMES_DIR}")
    return resumen_global


if __name__ == "__main__":
    analizar_todos_los_experimentos()
