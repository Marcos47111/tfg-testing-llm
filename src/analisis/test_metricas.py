"""
Tests unitarios para el cálculo de métricas de evaluación del TFG.
"""

import unittest
from src.analisis.metricas_tfg import (
    calcular_puntuacion_media,
    calcular_tasa_aprobado,
    es_fallo_critico,
    calcular_tasa_fallos_criticos,
    calcular_tasa_alucinaciones,
    calcular_iqe,
    generar_informe_sintetico,
    PESOS_DIMENSIONES
)


class TestMetricasTFG(unittest.TestCase):

    def test_suma_pesos_es_uno(self):
        """Verifica que la suma de ponderaciones del IQE sea exactamente 1.0 (100%)."""
        total_pesos = sum(PESOS_DIMENSIONES.values())
        self.assertAlmostEqual(total_pesos, 1.0, places=5)

    def test_puntuacion_media(self):
        self.assertEqual(calcular_puntuacion_media([3, 3, 3]), 3.0)
        self.assertEqual(calcular_puntuacion_media([0, 2, 1]), 1.0)
        self.assertEqual(calcular_puntuacion_media([]), 0.0)

    def test_tasa_aprobado(self):
        # 3 aprobados (>=2) de 4 -> 75%
        self.assertEqual(calcular_tasa_aprobado([3, 2, 2, 1]), 75.0)
        self.assertEqual(calcular_tasa_aprobado([0, 1]), 0.0)

    def test_fallo_critico(self):
        caso_critico_factual = {"puntuaciones": {"D1_correccion_factual": 0, "D3_claridad_didactica": 3}}
        caso_critico_aluc = {"puntuaciones": {"D2_control_alucinaciones": 0}}
        caso_critico_seguridad = {"puntuaciones": {"D5_robustez_seguridad": 0}}
        caso_valido = {"puntuaciones": {"D1_correccion_factual": 2, "D2_control_alucinaciones": 3, "D5_robustez_seguridad": 2}}

        self.assertTrue(es_fallo_critico(caso_critico_factual))
        self.assertTrue(es_fallo_critico(caso_critico_aluc))
        self.assertTrue(es_fallo_critico(caso_critico_seguridad))
        self.assertFalse(es_fallo_critico(caso_valido))

    def test_iqe_perfecto_e_invalido(self):
        medias_perfectas = {dim: 3.0 for dim in PESOS_DIMENSIONES}
        self.assertAlmostEqual(calcular_iqe(medias_perfectas), 100.0, places=2)

        medias_cero = {dim: 0.0 for dim in PESOS_DIMENSIONES}
        self.assertAlmostEqual(calcular_iqe(medias_cero), 0.0, places=2)

    def test_informe_sintetico(self):
        evaluaciones = [
            {
                "id": "FACT_001",
                "categoria": "01_correccion_factual",
                "puntuaciones": {"D1_correccion_factual": 3, "D3_claridad_didactica": 3}
            },
            {
                "id": "ALUC_001",
                "categoria": "02_deteccion_alucinaciones",
                "puntuaciones": {"D2_control_alucinaciones": 0, "D3_claridad_didactica": 2}
            }
        ]
        informe = generar_informe_sintetico(evaluaciones)
        self.assertEqual(informe["total_casos_evaluados"], 2)
        self.assertEqual(informe["tasa_fallos_criticos_cfr"], 50.0)
        self.assertEqual(informe["tasa_alucinaciones_hr"], 100.0)


if __name__ == "__main__":
    unittest.main()
