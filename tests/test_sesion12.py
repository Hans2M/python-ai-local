"""Pruebas de la extension Sesion 12 sin Ollama y sin internet."""
import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import motor

class Sesion12Tests(unittest.TestCase):
    def test_aliases(self):
        for t in ("sesion12", "sesion 12", "trafico", "analisis_trafico"):
            self.assertEqual(motor.normalizar_tema(t), "26_sesion12_trafico")

    def test_tema_automatico(self):
        for t in ("Tema: sesion12\nNecesito analizar un CSV",
                  "Analizar trafico.csv", "Analisis de registros de tráfico"):
            self.assertEqual(motor.detectar_tema(t), "26_sesion12_trafico")

    def test_conocimiento_y_recuperacion(self):
        registros = [d for d in motor.cargar_base() if d["id"].startswith("S12-")]
        self.assertEqual(len(registros), 16)
        docs, tema = motor.materiales("Tema: sesion12\n contar accion origen bytes")
        self.assertEqual(tema, "26_sesion12_trafico")
        self.assertTrue(docs)
        self.assertTrue(all(d["tema"] == tema for d in docs))

    def test_ejemplo_real(self):
        carpeta = ROOT / "ejemplos" / "sesion12_trafico"
        p = subprocess.run([sys.executable, "analizar_trafico.py"], cwd=carpeta,
                           capture_output=True, text=True, check=True)
        self.assertIn("Eventos: 8", p.stdout)
        self.assertIn("Bytes: 7925", p.stdout)
        p2 = subprocess.run([sys.executable, "analizar_trafico_por_servicio.py"], cwd=carpeta,
                            capture_output=True, text=True, check=True)
        self.assertIn("Por servicio:", p2.stdout)

if __name__ == "__main__": unittest.main()
