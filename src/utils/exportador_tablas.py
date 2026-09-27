"""
Exportador de tablas en formato LaTeX normalizado con booktabs para la memoria del TFG.
"""

from pathlib import Path
from typing import Union, Optional
import pandas as pd

TABLAS_DIR = Path(__file__).resolve().parent.parent.parent / "results" / "tablas"


def generar_tabla_latex_comparativa(
    csv_path: Optional[Union[str, Path, pd.DataFrame]] = None,
    output_path: Optional[Union[str, Path, bool]] = None
) -> str:
    """
    Convierte los resultados comparativos cuantitativos por perfil de chatbot a sintaxis LaTeX booktabs.
    Si output_path es None, escribe por defecto en results/tablas/tabla_comparativa_modelos.tex.
    Si output_path es False, únicamente devuelve la cadena LaTeX sin escribir en disco.
    """
    if csv_path is None:
        csv_path = TABLAS_DIR / "tabla_comparativa_modelos.csv"
    if output_path is None:
        output_path = TABLAS_DIR / "tabla_comparativa_modelos.tex"
        
    if isinstance(csv_path, pd.DataFrame):
        df = csv_path
    else:
        df = pd.read_csv(Path(csv_path))
    
    lineas = [
        "\\begin{table}[htbp]",
        "\\centering",
        "\\small",
        "\\caption{Resumen comparativo de métricas de calidad y fiabilidad por perfil de chatbot}",
        "\\label{tab:comparativa_modelos}",
        "\\begin{tabular}{lcccccccccc}",
        "\\toprule",
        "\\textbf{Perfil} & \\textbf{IQE} & \\textbf{CFR (\\%)} & \\textbf{HR (\\%)} & \\textbf{D1} & \\textbf{D2} & \\textbf{D3} & \\textbf{D4} & \\textbf{D5} & \\textbf{D6} & \\textbf{D7} \\\\",
        "\\midrule"
    ]
    
    for _, r in df.iterrows():
        nombre = str(r["Perfil"]).replace("_", "\\_")
        iqe = f"{float(r['IQE (0-100)']):.2f}"
        cfr = f"{float(r['CFR (%)']):.2f}"
        hr = f"{float(r['HR (%)']):.2f}"
        d1 = f"{float(r['D1 Factual']):.2f}"
        d2 = f"{float(r['D2 Alucinación']):.2f}"
        d3 = f"{float(r['D3 Claridad']):.2f}"
        d4 = f"{float(r['D4 Feedback']):.2f}"
        d5 = f"{float(r['D5 Seguridad']):.2f}"
        d6 = f"{float(r['D6 Nivel']):.2f}"
        d7 = f"{float(r['D7 Directrices']):.2f}"
        
        lineas.append(
            f"{nombre} & \\textbf{{{iqe}}} & {cfr} & {hr} & {d1} & {d2} & {d3} & {d4} & {d5} & {d6} & {d7} \\\\"
        )
        
    lineas.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}"
    ])
    
    codigo_latex = "\n".join(lineas) + "\n"
    if output_path is not False and output_path is not None:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(codigo_latex)
        print(f"  [+] Tabla LaTeX generada en {out_file}")
        
    return codigo_latex


if __name__ == "__main__":
    generar_tabla_latex_comparativa()
