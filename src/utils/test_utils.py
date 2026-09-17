"""
Tests unitarios para los módulos de utilidad del TFG (loader de prompts y exportador de tablas).
"""

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.loader_prompts import cargar_todos_los_prompts
from src.utils.exportador_tablas import generar_tabla_latex_comparativa


class TestUtilsTFG(unittest.TestCase):

    def test_cargar_todos_los_prompts(self):
        """Verifica que se carguen exactamente los 42 casos de prueba y contengan las claves requeridas."""
        prompts = cargar_todos_los_prompts()
        self.assertEqual(len(prompts), 42)
        
        claves_requeridas = {"id", "materia", "nivel_educativo", "prompt", "ground_truth", "dimension_principal"}
        for p in prompts:
            self.assertTrue(claves_requeridas.issubset(p.keys()), f"Faltan claves en el caso {p.get('id')}")

    def test_generar_tabla_latex(self):
        """Verifica la generación del archivo LaTeX de la tabla comparativa."""
        tex = generar_tabla_latex_comparativa()
        self.assertIn("\\begin{table}", tex)
        self.assertIn("\\end{table}", tex)
        self.assertIn("asistente\\_base", tex)


if __name__ == "__main__":
    unittest.main()
