"""
Tests unitarios para el módulo de evaluación automática LLM-as-a-Judge y su análisis de concordancia.
"""

import json
import unittest
from pathlib import Path
from src.evaluador.evaluador_llm_judge import (
    parsear_y_validar_salida_juez,
    construir_prompt_evaluacion,
    MockJudgeProvider,
    DIMENSIONES,
    RUBRICA_SISTEMA
)
from src.analisis.analizar_concordancia_llm_judge import (
    analizar_distribucion_deltas,
    calcular_matriz_confusion_4x4,
    calcular_mae,
    analizar_fallos_criticos_cruzados
)


class TestLLMJudge(unittest.TestCase):

    def test_parsear_salida_valida(self):
        json_sample = json.dumps({
            "evaluaciones": {
                d: {"score": 3, "justificacion": f"Justificacion para {d}"} for d in DIMENSIONES
            }
        })
        res = parsear_y_validar_salida_juez(json_sample)
        self.assertEqual(len(res["puntuaciones"]), 7)
        self.assertEqual(len(res["justificaciones"]), 7)
        self.assertEqual(res["puntuaciones"]["D1_correccion_factual"], 3)

    def test_parsear_salida_con_bloques_markdown(self):
        json_sample = "```json\n" + json.dumps({
            "evaluaciones": {
                d: {"score": 2, "justificacion": "Correcto"} for d in DIMENSIONES
            }
        }) + "\n```"
        res = parsear_y_validar_salida_juez(json_sample)
        self.assertEqual(res["puntuaciones"]["D2_control_alucinaciones"], 2)

    def test_parsear_salida_invalida_score_fuera_rango(self):
        json_bad_score = json.dumps({
            "evaluaciones": {
                d: {"score": 4 if d == "D1_correccion_factual" else 2, "justificacion": "Test"} for d in DIMENSIONES
            }
        })
        with self.assertRaises(ValueError):
            parsear_y_validar_salida_juez(json_bad_score)

    def test_parsear_salida_falta_dimension(self):
        json_missing = json.dumps({
            "evaluaciones": {
                "D1_correccion_factual": {"score": 2, "justificacion": "Ok"}
            }
        })
        with self.assertRaises(ValueError):
            parsear_y_validar_salida_juez(json_missing)

    def test_blind_prompt_no_incluye_perfil(self):
        caso = {
            "id": "FACT_001",
            "dimension_principal": "D1_correccion_factual",
            "materia": "Matemáticas",
            "nivel_educativo": "Secundaria",
            "prompt": "¿Cuánto es 2+2?",
            "ground_truth": "4",
            "criterio_fallo_critico": "Afirmar distinto de 4"
        }
        prompt = construir_prompt_evaluacion(caso, "4")
        self.assertNotIn("asistente_base", prompt)
        self.assertNotIn("tutor_directo", prompt)
        self.assertNotIn("tutor_socratico", prompt)
        self.assertNotIn("evaluador_1", prompt)
        self.assertNotIn("evaluador_2", prompt)

    def test_analizar_distribucion_deltas(self):
        y_true = [0, 1, 2, 3, 2]
        y_pred = [0, 1, 3, 3, 0]  # deltas: 0, 0, +1, 0, -2
        deltas = analizar_distribucion_deltas(y_true, y_pred)
        self.assertEqual(deltas["total_juicios"], 5)
        self.assertEqual(deltas["acuerdo_exacto_delta_0"]["recuento"], 3)
        self.assertEqual(deltas["discrepancia_menor_delta_1"]["recuento"], 1)
        self.assertEqual(deltas["discrepancia_moderada_delta_2"]["recuento"], 1)
        self.assertEqual(deltas["tendencia"]["sobrevaloraciones"], 1)
        self.assertEqual(deltas["tendencia"]["infravaloraciones"], 1)

    def test_calcular_mae(self):
        y_true = [0, 1, 2, 3]
        y_pred = [0, 2, 2, 0]  # abs deltas: 0, 1, 0, 3 -> mean = 4/4 = 1.0
        mae = calcular_mae(y_true, y_pred)
        self.assertEqual(mae, 1.0)

    def test_matriz_confusion_4x4(self):
        y_true = [0, 1, 2, 3]
        y_pred = [0, 1, 2, 2]
        m = calcular_matriz_confusion_4x4(y_true, y_pred)
        self.assertEqual(m[0][0], 1)
        self.assertEqual(m[1][1], 1)
        self.assertEqual(m[2][2], 1)
        self.assertEqual(m[3][2], 1)
        self.assertEqual(m[3][3], 0)

    def test_mock_judge_provider(self):
        provider = MockJudgeProvider()
        raw_json = provider.evaluar(RUBRICA_SISTEMA, "dummy user prompt")
        eval_res = parsear_y_validar_salida_juez(raw_json)
        self.assertEqual(len(eval_res["puntuaciones"]), 7)
        self.assertIn(eval_res["puntuaciones"]["D1_correccion_factual"], [0, 1, 2, 3])


if __name__ == "__main__":
    unittest.main()
