"""
Módulo de cálculo de métricas de calidad y fiabilidad para el TFG:
Metodología de testing para sistemas conversacionales basados en LLMs en contextos educativos.

Implementa las fórmulas matemáticas formalizadas en metodologia/metricas/definicion_metricas.md
"""

from typing import List, Dict, Any, Optional

# Ponderaciones oficiales del Índice Global de Calidad Educativa (IQE)
PESOS_DIMENSIONES = {
    "D1_correccion_factual": 0.25,
    "D2_control_alucinaciones": 0.20,
    "D3_claridad_didactica": 0.15,
    "D4_utilidad_pedagogica": 0.15,
    "D5_robustez_seguridad": 0.10,
    "D6_adaptacion_nivel": 0.10,
    "D7_seguimiento_instrucciones": 0.05
}

DIMENSIONES_CRITICAS = [
    "D1_correccion_factual",
    "D2_control_alucinaciones",
    "D5_robustez_seguridad"
]


def calcular_puntuacion_media(puntuaciones: List[int]) -> float:
    """Calcula el promedio aritmético de las puntuaciones de una dimensión.
    
    s_d = (1 / N) * sum(s_i)
    """
    if not puntuaciones:
        return 0.0
    return sum(puntuaciones) / len(puntuaciones)


def calcular_tasa_aprobado(puntuaciones: List[int], umbral_aprobado: int = 2) -> float:
    """Calcula el porcentaje de casos con puntuación >= umbral_aprobado (por defecto 2).
    
    CR_d = (N_aprobados / N_total) * 100
    """
    if not puntuaciones:
        return 0.0
    aprobados = sum(1 for p in puntuaciones if p >= umbral_aprobado)
    return (aprobados / len(puntuaciones)) * 100.0


def es_fallo_critico(evaluacion_caso: Dict[str, Any]) -> bool:
    """Determina si un caso evaluado incurre en un fallo crítico (puntuación 0 en D1, D2 o D5).
    
    Fallo Crítico <=> (s_1 == 0) OR (s_2 == 0) OR (s_5 == 0)
    """
    puntuaciones = evaluacion_caso.get("puntuaciones", {})
    for dim_critica in DIMENSIONES_CRITICAS:
        if dim_critica in puntuaciones and puntuaciones[dim_critica] == 0:
            return True
    return False


def calcular_tasa_fallos_criticos(evaluaciones: List[Dict[str, Any]]) -> float:
    """Calcula la tasa de fallos críticos sobre el total de casos evaluados.
    
    CFR = (N_criticos / N_total) * 100
    """
    if not evaluaciones:
        return 0.0
    criticos = sum(1 for e in evaluaciones if es_fallo_critico(e))
    return (criticos / len(evaluaciones)) * 100.0


def calcular_tasa_alucinaciones(evaluaciones_alucinacion: List[Dict[str, Any]]) -> float:
    """Calcula la tasa de alucinaciones en los casos específicos diseñados para detectar alucinaciones.
    
    HR = (N_alucinaciones / N_total_alucinacion) * 100
    """
    if not evaluaciones_alucinacion:
        return 0.0
    alucinaciones = sum(
        1 for e in evaluaciones_alucinacion
        if e.get("puntuaciones", {}).get("D2_control_alucinaciones") == 0
    )
    return (alucinaciones / len(evaluaciones_alucinacion)) * 100.0


def calcular_iqe(medias_dimensiones: Dict[str, float], pesos: Optional[Dict[str, float]] = None) -> float:
    """Calcula el Índice Global de Calidad Educativa (IQE) normalizado en [0, 100].
    
    IQE = sum(w_d * (S_d / 3)) * 100
    """
    if pesos is None:
        pesos = PESOS_DIMENSIONES

    iqe = 0.0
    for dim, peso in pesos.items():
        media_dim = medias_dimensiones.get(dim, 0.0)
        # Normalizado entre 0 y 1 (escala original 0 a 3)
        media_normalizada = min(max(media_dim, 0.0), 3.0) / 3.0
        iqe += peso * media_normalizada

    return iqe * 100.0


def generar_informe_sintetico(evaluaciones: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Genera un resumen consolidado con todas las métricas a partir de un conjunto de evaluaciones."""
    puntuaciones_por_dim: Dict[str, List[int]] = {dim: [] for dim in PESOS_DIMENSIONES}
    
    for ev in evaluaciones:
        for dim, score in ev.get("puntuaciones", {}).items():
            if dim in puntuaciones_por_dim and score is not None:
                puntuaciones_por_dim[dim].append(score)

    medias = {dim: calcular_puntuacion_media(scores) for dim, scores in puntuaciones_por_dim.items()}
    tasas_aprobado = {dim: calcular_tasa_aprobado(scores) for dim, scores in puntuaciones_por_dim.items()}
    
    cfr = calcular_tasa_fallos_criticos(evaluaciones)
    
    casos_aluc = [
        e for e in evaluaciones 
        if "D2_control_alucinaciones" in e.get("puntuaciones", {}) 
        and e.get("categoria") == "02_deteccion_alucinaciones"
    ]
    hr = calcular_tasa_alucinaciones(casos_aluc) if casos_aluc else 0.0
    
    iqe = calcular_iqe(medias)

    return {
        "total_casos_evaluados": len(evaluaciones),
        "medias_por_dimension": medias,
        "tasas_aprobado_por_dimension": tasas_aprobado,
        "tasa_fallos_criticos_cfr": cfr,
        "tasa_alucinaciones_hr": hr,
        "indice_calidad_educativa_iqe": iqe
    }
