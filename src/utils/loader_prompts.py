"""
Módulo de carga y validación de la batería completa de casos de prueba del TFG.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "prompts"


def cargar_todos_los_prompts() -> List[Dict[str, Any]]:
    """Carga y consolida todos los casos de prueba de las diferentes categorías."""
    todos_los_casos = []
    archivos_json = sorted(PROMPTS_DIR.glob("*/*.json"))
    
    for archivo in archivos_json:
        with open(archivo, "r", encoding="utf-8") as f:
            casos = json.load(f)
            for c in casos:
                c["categoria_directorio"] = archivo.parent.name
                todos_los_casos.append(c)
                
    return todos_los_casos


def validar_esquema_casos(casos: List[Dict[str, Any]]) -> bool:
    """Valida que cada caso de prueba contenga todos los campos obligatorios del protocolo."""
    campos_obligatorios = {
        "id", "dimension_principal", "materia", 
        "nivel_educativo", "prompt", "ground_truth", "criterio_fallo_critico"
    }
    
    ids_vistos = set()
    for caso in casos:
        faltantes = campos_obligatorios - set(caso.keys())
        if faltantes:
            raise ValueError(f"El caso {caso.get('id', 'DESCONOCIDO')} carece de campos obligatorios: {faltantes}")
        
        cid = caso["id"]
        if cid in ids_vistos:
            raise ValueError(f"Identificador duplicado detectado: {cid}")
        ids_vistos.add(cid)
        
    return True


if __name__ == "__main__":
    casos = cargar_todos_los_prompts()
    validar_esquema_casos(casos)
    print(f"✅ Se han cargado y validado correctamente {len(casos)} casos de prueba estructurados.")
