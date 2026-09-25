"""
Exportador de tablas en formato LaTeX normalizado con booktabs para la memoria del TFG.
"""

import json
from pathlib import Path
import pandas as pd

TABLAS_DIR = Path(__file__).resolve().parent.parent.parent / "results" / "tablas"


def generar_tabla_latex_comparativa():
    """Convierte la tabla comparativa de modelos a sintaxis LaTeX booktabs."""
    df = pd.read_csv(TABLAS_DIR / "tabla_comparativa_modelos.csv")
    
    lineas = [
        "\\begin{table}[htbp]",
        "\\centering",
        "\\small",
        "\\caption{Resultados comparativos cuantitativos por perfil de chatbot}",
        "\\label{tab:resultados_comparativos}",
        "\\begin{tabularx}{\\textwidth}{l c c c c c c c c c c}",
        "\\toprule",
        "\\textbf{Perfil} & \\textbf{IQE} & \\textbf{CFR} & \\textbf{HR} & \\textbf{D1} & \\textbf{D2} & \\textbf{D3} & \\textbf{D4} & \\textbf{D5} & \\textbf{D6} & \\textbf{D7} \\\\",
        " & (0-100) & (\\%) & (\\%) & Fact. & Aluc. & Clar. & Feed. & Seg. & Nivel & Dir. \\\\",
        "\\midrule"
    ]
    
    for _, r in df.iterrows():
        nombre = r["Perfil"].replace("_", "\\_")
        iqe = f"{r['IQE (0-100)']:.1f}"
        cfr = f"{r['CFR (%)']:.1f}\\%"
        hr = f"{r['HR (%)']:.1f}\\%"
        d1 = f"{r['D1 Factual']:.2f}"
        d2 = f"{r['D2 Alucinación']:.2f}"
        d3 = f"{r['D3 Claridad']:.2f}"
        d4 = f"{r['D4 Feedback']:.2f}"
        d5 = f"{r['D5 Seguridad']:.2f}"
        d6 = f"{r['D6 Nivel']:.2f}"
        d7 = f"{r['D7 Directrices']:.2f}"
        
        lineas.append(f"{nombre} & {iqe} & {cfr} & {hr} & {d1} & {d2} & {d3} & {d4} & {d5} & {d6} & {d7} \\\\")
        
    lineas.extend([
        "\\bottomrule",
        "\\end{tabularx}",
        "\\end{table}"
    ])
    
    codigo_latex = "\n".join(lineas)
    with open(TABLAS_DIR / "tabla_comparativa_modelos.tex", "w", encoding="utf-8") as f:
        f.write(codigo_latex)
        
    print("  [+] Tabla LaTeX generada en results/tablas/tabla_comparativa_modelos.tex")
    return codigo_latex


if __name__ == "__main__":
    generar_tabla_latex_comparativa()
