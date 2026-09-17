"""
Módulo de generación de visualizaciones vectoriales y gráficos para la memoria del TFG.
Utiliza matplotlib para generar figuras de alta calidad académica (DPI=300).
"""

import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent.parent / "results"
GRAFICOS_DIR = RESULTS_DIR / "graficos"
FIGURAS_MEMORIA_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "memoria" / "figuras"
IMG_MEMORIA_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "memoria" / "img"
INFORMES_DIR = RESULTS_DIR / "informes"

# Configuración estética global de matplotlib
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8


def cargar_datos_resumen() -> dict:
    with open(INFORMES_DIR / "resumen_comparativo_global.json", "r", encoding="utf-8") as f:
        return json.load(f)


def generar_grafico_radar(datos: dict):
    """Genera un gráfico de radar comparando las 7 dimensiones entre los 3 perfiles."""
    categorias = [
        "D1: Factualidad",
        "D2: Alucinaciones",
        "D3: Claridad",
        "D4: Feedback",
        "D5: Seguridad",
        "D6: Nivel",
        "D7: Directrices"
    ]
    claves_dim = [
        "D1_correccion_factual",
        "D2_control_alucinaciones",
        "D3_claridad_didactica",
        "D4_utilidad_pedagogica",
        "D5_robustez_seguridad",
        "D6_adaptacion_nivel",
        "D7_seguimiento_instrucciones"
    ]
    
    N = len(categorias)
    angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angulos += angulos[:1]  # Cerrar el polígono
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)
    
    colores = {
        "asistente_base": "#d9534f",
        "tutor_directo": "#337ab7",
        "tutor_socratico": "#5cb85c"
    }
    etiquetas = {
        "asistente_base": "Asistente Base (Sin System Prompt)",
        "tutor_directo": "Tutor Directo (Expositivo)",
        "tutor_socratico": "Tutor Socrático (Andamiaje)"
    }
    
    for perfil, color in colores.items():
        if perfil in datos:
            valores = [datos[perfil]["medias_por_dimension"][k] for k in claves_dim]
            valores += valores[:1]
            ax.plot(angulos, valores, color=color, linewidth=2, label=etiquetas[perfil])
            ax.fill(angulos, valores, color=color, alpha=0.15)
            
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angulos[:-1]), categorias, fontsize=10, fontweight="bold")
    ax.set_ylim(0, 3.2)
    ax.set_yticks([1.0, 2.0, 3.0])
    ax.set_yticklabels(["1,0 (Deficiente)", "2,0 (Aceptable)", "3,0 (Óptimo)"], fontsize=9, color="#555555")
    ax.grid(color="#cccccc", linestyle="--", alpha=0.7)
    
    plt.title("Comparativa Multidimensional del Rendimiento Educativo", size=14, weight="bold", y=1.08)
    plt.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=9)
    plt.tight_layout()
    
    for d in [GRAFICOS_DIR, FIGURAS_MEMORIA_DIR, IMG_MEMORIA_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        plt.savefig(d / "radar_dimensiones.png", bbox_inches="tight")
        plt.savefig(d / "radar_dimensiones.pdf", bbox_inches="tight")
    plt.close()
    print("  ✅ Gráfico de radar generado correctamente.")


def generar_grafico_barras_metricas(datos: dict):
    """Genera un gráfico de barras comparativo de IQE, CFR y HR."""
    perfiles = ["asistente_base", "tutor_directo", "tutor_socratico"]
    nombres_perfil = ["Asistente Base", "Tutor Directo", "Tutor Socrático"]
    
    iqe_vals = [datos[p]["indice_calidad_educativa_iqe"] for p in perfiles]
    cfr_vals = [datos[p]["tasa_fallos_criticos_cfr"] for p in perfiles]
    hr_vals = [datos[p]["tasa_alucinaciones_hr"] for p in perfiles]
    
    x = np.arange(len(perfiles))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    
    rects1 = ax.bar(x - width, iqe_vals, width, label="Índice Global IQE (0-100)", color="#2b5c8f")
    rects2 = ax.bar(x, cfr_vals, width, label="Tasa Fallos Críticos CFR (%)", color="#d9534f")
    rects3 = ax.bar(x + width, hr_vals, width, label="Tasa Alucinaciones HR (%)", color="#f0ad4e")
    
    ax.set_ylabel("Valor Normalizado / Porcentaje (%)", fontsize=11, fontweight="bold")
    ax.set_title("Comparativa de Índices Globales y Tasas de Riesgo por Perfil", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(nombres_perfil, fontsize=11, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.set_ylim(0, 115)
    
    # Añadir valores numéricos encima de las barras con coma decimal en español
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            val_str = f"{height:.1f}".replace(".", ",")
            ax.annotate(val_str,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9, fontweight="bold")
                        
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    
    plt.tight_layout()
    for d in [GRAFICOS_DIR, FIGURAS_MEMORIA_DIR, IMG_MEMORIA_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        plt.savefig(d / "barras_metricas_globales.png", bbox_inches="tight")
        plt.savefig(d / "barras_metricas_globales.pdf", bbox_inches="tight")
    plt.close()
    print("  ✅ Gráfico de barras de métricas globales generado correctamente.")


def generar_todas_las_figuras():
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURAS_MEMORIA_DIR.mkdir(parents=True, exist_ok=True)
    IMG_MEMORIA_DIR.mkdir(parents=True, exist_ok=True)
    
    datos = cargar_datos_resumen()
    generar_grafico_radar(datos)
    generar_grafico_barras_metricas(datos)
    print(f"📊 Todas las figuras han sido exportadas a {GRAFICOS_DIR}, {FIGURAS_MEMORIA_DIR} e {IMG_MEMORIA_DIR}")


if __name__ == "__main__":
    generar_todas_las_figuras()
