"""Pruebas sin internet ni modelo: se simula solo la generación de Ollama."""
import ast
import io
import os
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import cliente
import motor
import servidor


class TestsLocal(unittest.TestCase):
    def test_indice_curso(self):
        with motor.KB.open(encoding='utf-8') as f:
            entradas = [line for line in f if line.strip()]
        self.assertGreaterEqual(len(entradas), 14)
        refs, topic = motor.materiales('Desarrolle una función para convertir segundos en minutos', 'funciones')
        self.assertEqual(topic, '05_funciones')
        self.assertTrue(any('Conversión de tiempo' in r['titulo'] for r in refs))
        refs, topic = motor.materiales('Programa para registrar asistencia en archivos', 'archivos')
        self.assertTrue(any('Registro de asistencia' in r['titulo'] for r in refs))
        refs, topic = motor.materiales('Semana 1 - reporte técnico de switch')
        self.assertTrue(all(r['tema'] in ('01_fundamentos', '02_operadores', '07_casos_practicos') for r in refs))

    def test_codigo_en_bloques(self):
        val = cliente.codigo_valido('Análisis\n```python\nx = 2\nprint(x)\n```\nExplicación')
        self.assertEqual(val, 'x = 2\nprint(x)\n')
        self.assertIsNone(cliente.codigo_valido('```python\nx =\n```'))

    def test_progresivo_sin_mensajes(self):
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td) / 'codigo.py'
            salida = io.StringIO()
            with redirect_stdout(salida):
                res = cliente.escritura_progresiva('x = 1\nprint(x)\n', dest, 0, 0, False)
            self.assertTrue(res)
            self.assertEqual(dest.read_text(encoding='utf-8'), 'x = 1\nprint(x)\n')
            self.assertNotIn('esperando', dest.read_text(encoding='utf-8').lower())
            ast.parse(dest.read_text(encoding='utf-8'))

    def test_http_y_archivos_resolver_revisar_corregir(self):
        def mock_generar(modo, contenido, archivo, tema='', timeout=390):
            if modo == 'revisar':
                return 'Error encontrado: faltaba validación.'
            return 'Solución:\n```python\nn = 5\nprint(n)\n```\nExplicación.'
        with patch.object(servidor, 'modelo_disponible', return_value=(True,'Ollama simulado')), \
             patch.object(servidor, 'generar', side_effect=mock_generar):
            server = ThreadingHTTPServer(('127.0.0.1', 0), servidor.Handler)
            host, port = server.server_address
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            old_url = cliente.URL
            cliente.URL = f'http://{host}:{port}'
            try:
                with tempfile.TemporaryDirectory() as td:
                    old_cwd = Path.cwd()
                    os.chdir(td)
                    try:
                        Path('ejercicio.txt').write_text('Tema: funciones\nCalcular promedio.',encoding='utf-8')
                        Path('main.py').write_text('print(3)', encoding='utf-8')
                        with redirect_stdout(io.StringIO()):
                            self.assertEqual(cliente.main(['resolver','ejercicio.txt','--escribir','--intervalo','0','--no-abrir']), 0)
                            self.assertEqual(cliente.main(['revisar','main.py']), 0)
                            self.assertEqual(cliente.main(['corregir','main.py']), 0)
                        salida = Path('soluciones')
                        self.assertEqual((salida/'ejercicio_solucion.py').read_text(encoding='utf-8'), 'n = 5\nprint(n)\n')
                        self.assertTrue((salida/'main_revision.md').is_file())
                        self.assertTrue((salida/'main_corregido.py').is_file())
                        self.assertEqual(Path('main.py').read_text(), 'print(3)')
                    finally:
                        os.chdir(old_cwd)
            finally:
                cliente.URL = old_url
                server.shutdown();server.server_close();thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()
