"""
Módulo independiente de visualización para el prototipo experimental LLM-as-a-Judge.
Genera gráficos vectoriales y de alta resolución (DPI=300) para el análisis de
concordancia humano-IA, distribución de discrepancias y matriz de confusión 4x4.
"""

import json
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

RESULTS_DIR = PROJECT_ROOT / "results"
GRAFICOS_DIR = RESULTS_DIR / "graficos"
INFORMES_DIR = RESULTS_DIR / "informes"
FIGURAS_MEMORIA_DIR = PROJECT_ROOT / "docs" / "memoria" / "figuras"
IMG_MEMORIA_DIR = PROJECT_ROOT / "docs" / "memoria" / "img"

# Configuración estética global de matplotlib
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8


def cargar_informe_concordancia() -> dict:
    informe_path = INFORMES_DIR / "concordancia_llm_judge.json"
    if not informe_path.exists():
        raise FileNotFoundError(f"No se encontró el informe de concordancia: {informe_path}")
    with open(informe_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generar_grafico_concordancia_dimensional(datos: dict):
    """
    Genera un gráfico de barras comparativo de Cohen's Kappa por dimensión
    entre LLM-as-a-Judge vs E1, LLM-as-a-Judge vs E2, y la referencia humana E1 vs E2.
    """
    dims = [
        ("D1_correccion_factual", "D1: Factualidad"),
        ("D2_control_alucinaciones", "D2: Alucinaciones"),
        ("D3_claridad_didactica", "D3: Claridad"),
        ("D4_utilidad_pedagogica", "D4: Feedback"),
        ("D5_robustez_seguridad", "D5: Seguridad"),
        ("D6_adaptacion_nivel", "D6: Nivel"),
        ("D7_seguimiento_instrucciones", "D7: Directrices")
    ]
    
    etiquetas = [d[1] for d in dims]
    k_j_e1 = [datos["concordancia_por_dimension"][d[0]]["kappa_judge_vs_e1"] for d in dims]
    k_j_e2 = [datos["concordancia_por_dimension"][d[0]]["kappa_judge_vs_e2"] for d in dims]
    k_e1_e2 = [datos["concordancia_por_dimension"][d[0]]["kappa_humano_e1_vs_e2"] for d in dims]
    
    x = np.arange(len(etiquetas))
    width = 0.26
    
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    
    # Barras
    rects1 = ax.bar(x - width, k_j_e1, width, label=r"Juez vs $E_1$", color="#337ab7", alpha=0.9, edgecolor="#1f4e78")
    rects2 = ax.bar(x, k_j_e2, width, label=r"Juez vs $E_2$", color="#5bc0de", alpha=0.9, edgecolor="#31708f")
    rects3 = ax.bar(x + width, k_e1_e2, width, label=r"Humano ($E_1$ vs $E_2$)", color="#5cb85c", alpha=0.9, edgecolor="#3e8f3e")
    
    # Líneas de referencia metodológicas
    ax.axhline(0.80, color="#27ae60", linestyle="--", linewidth=1.0, alpha=0.7, label=r"Acuerdo Casi Perfecto ($\kappa \geq 0.80$)")
    ax.axhline(0.60, color="#f0ad4e", linestyle=":", linewidth=1.0, alpha=0.7, label=r"Acuerdo Sustancial ($\kappa \geq 0.60$)")
    ax.axhline(0.00, color="#888888", linestyle="-", linewidth=0.8, alpha=0.5)
    
    ax.set_ylabel(r"Coeficiente Kappa de Cohen ($\kappa$)", fontsize=11, fontweight="bold")
    ax.set_title(r"Concordancia Inter-Evaluador por Dimensión: LLM-as-a-Judge vs Evaluadores Humanos", fontsize=12, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas, fontsize=9.5)
    ax.set_ylim(-0.15, 1.08)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(loc="upper right", fontsize=8.5, framealpha=0.95)
    
    # Etiquetas de valor en barras
    for rect in rects1:
        h = rect.get_height()
        va = "bottom" if h >= 0 else "top"
        y_pos = h + 0.02 if h >= 0 else h - 0.06
        ax.annotate(f"{h:.2f}",
                    xy=(rect.get_x() + rect.get_width() / 2, y_pos),
                    ha="center", va=va, fontsize=7.5, fontweight="bold", color="#1f4e78")
        
    for rect in rects2:
        h = rect.get_height()
        va = "bottom" if h >= 0 else "top"
        y_pos = h + 0.02 if h >= 0 else h - 0.06
        ax.annotate(f"{h:.2f}",
                    xy=(rect.get_x() + rect.get_width() / 2, y_pos),
                    ha="center", va=va, fontsize=7.5, fontweight="bold", color="#286090")
                    
    for rect in rects3:
        h = rect.get_height()
        va = "bottom" if h >= 0 else "top"
        y_pos = h + 0.02 if h >= 0 else h - 0.06
        ax.annotate(f"{h:.2f}",
                    xy=(rect.get_x() + rect.get_width() / 2, y_pos),
                    ha="center", va=va, fontsize=7.5, fontweight="bold", color="#255625")
    
    plt.tight_layout()
    
    for d in [GRAFICOS_DIR, FIGURAS_MEMORIA_DIR, IMG_MEMORIA_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        fig.savefig(d / "concordancia_llm_judge.pdf", bbox_inches="tight")
        fig.savefig(d / "concordancia_llm_judge.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  ✅ Gráfico de concordancia dimensional generado: concordancia_llm_judge.pdf / .png")


def generar_grafico_matriz_confusion(datos: dict):
    """
    Genera un mapa de calor para la matriz de confusión 4x4 (E1 vs Juez, N=882).
    """
    matriz = np.array(datos["matriz_confusion_global_4x4_filas_e1_columnas_juez"])
    
    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=300)
    
    im = ax.imshow(matriz, cmap="Blues", interpolation="nearest")
    
    # Barra de color
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel("Número de Juicios", rotation=-90, va="bottom", fontsize=10)
    
    # Ejes
    ax.set_xticks(np.arange(4))
    ax.set_yticks(np.arange(4))
    ax.set_xticklabels([f"Nivel {i}" for i in range(4)], fontsize=10)
    ax.set_yticklabels([f"Nivel {i}" for i in range(4)], fontsize=10)
    
    ax.set_xlabel("Puntuación Juez Automático (LLM-as-a-Judge)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel(r"Puntuación Evaluador Humano $E_1$", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title(r"Matriz de Confusión Global: $E_1$ vs LLM-as-a-Judge ($N_\kappa=882$)", fontsize=11.5, fontweight="bold", pad=12)
    
    # Anotar recuentos
    threshold = matriz.max() / 2.0
    for i in range(4):
        for j in range(4):
            val = matriz[i, j]
            color = "white" if val > threshold else "black"
            pct = (val / 882.0) * 100
            txt = f"{val}\n({pct:.1f}%)" if val > 0 else "0"
            ax.text(j, i, txt, ha="center", va="center", color=color, fontsize=9.5, fontweight="bold" if i==j else "normal")
            
    plt.tight_layout()
    
    for d in [GRAFICOS_DIR, FIGURAS_MEMORIA_DIR, IMG_MEMORIA_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        fig.savefig(d / "matriz_confusion_llm_judge.pdf", bbox_inches="tight")
        fig.savefig(d / "matriz_confusion_llm_judge.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  ✅ Gráfico de matriz de confusión generado: matriz_confusion_llm_judge.pdf / .png")


def generar_grafico_distribucion_discrepancias(datos: dict):
    """
    Genera un gráfico circular o de barras con la distribución deltas (|Δ| in {0, 1, 2, 3}).
    """
    deltas = datos["analisis_discrepancias_deltas"]["juez_vs_e1"]
    
    etiquetas = [
        r"Acuerdo Exacto ($|\Delta| = 0$)",
        r"Discrepancia Menor ($|\Delta| = 1$)",
        r"Discrepancia Moderada ($|\Delta| = 2$)",
        r"Discrepancia Severa ($|\Delta| = 3$)"
    ]
    recuentos = [
        deltas["acuerdo_exacto_delta_0"]["recuento"],
        deltas["discrepancia_menor_delta_1"]["recuento"],
        deltas["discrepancia_moderada_delta_2"]["recuento"],
        deltas["discrepancia_severa_delta_3"]["recuento"]
    ]
    colores = ["#5cb85c", "#5bc0de", "#f0ad4e", "#d9534f"]
    
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    
    bars = ax.barh(etiquetas, recuentos, color=colores, edgecolor="#333333", height=0.55)
    ax.set_xlabel("Número de Juicios Pareados ($N=882$)", fontsize=10.5, fontweight="bold")
    ax.set_title(r"Distribución de la Magnitud de Discrepancias ($|P_{juez} - P_{E1}|$)", fontsize=11.5, fontweight="bold", pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_xlim(0, 950)
    
    for bar in bars:
        w = bar.get_width()
        pct = (w / 882.0) * 100
        ax.text(w + 12, bar.get_y() + bar.get_height()/2, f"{w} ({pct:.1f}%)",
                va="center", fontsize=9.5, fontweight="bold")
                
    plt.tight_layout()
    
    for d in [GRAFICOS_DIR, FIGURAS_MEMORIA_DIR, IMG_MEMORIA_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        fig.savefig(d / "distribucion_deltas_llm_judge.pdf", bbox_inches="tight")
        fig.savefig(d / "distribucion_deltas_llm_judge.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  ✅ Gráfico de distribución de deltas generado: distribucion_deltas_llm_judge.pdf / .png")


def generar_todos_los_graficos_llm_judge():
    print("=" * 65)
    print("  GENERACIÓN DE GRÁFICOS EXPERIMENTALES LLM-AS-A-JUDGE")
    print("=" * 65)
    datos = cargar_informe_concordancia()
    generar_grafico_concordancia_dimensional(datos)
    generar_grafico_matriz_confusion(datos)
    generar_grafico_distribucion_discrepancias(datos)
    print("🎉 Todos los gráficos del Juez Automático han sido generados con éxito.")
    print("=" * 65)


if __name__ == "__main__":
    generar_todos_los_graficos_llm_judge()
