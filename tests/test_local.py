"""Pruebas sin internet ni modelo. Simulamos generación de Ollama."""
import ast
import io
import json
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
    def test_biblioteca_general(self):
        docs = motor.cargar_base()
        self.assertGreaterEqual(len(docs), 60)
        self.assertGreaterEqual(len(motor.TEMAS), 20)
        self.assertEqual(len({d['id'] for d in docs}), len(docs))
        temas = set(motor.TEMAS)
        self.assertTrue(all(d['tema'] in temas for d in docs))
        for doc in docs:
            if doc.get('codigo'):
                ast.parse(doc['codigo'])

    def test_temas_y_consultas_diversas(self):
        temas = {
            'POO': '12_poo',
            'sqlite': '16_bases_datos',
            'json_csv': '14_json_csv',
            'diccionarios': '08_diccionarios_conjuntos',
            '08_diccionarios_conjuntos': '08_diccionarios_conjuntos',
            'bases de datos': '16_bases_datos',
            'funciones': '05_funciones',
            '25_redes': '25_redes',
        }
        for consulta, esperado in temas.items():
            with self.subTest(consulta=consulta):
                self.assertEqual(motor.normalizar_tema(consulta), esperado)
        refs, topic = motor.materiales('Resolver con clase y método para productos', 'poo')
        self.assertEqual(topic, '12_poo')
        self.assertTrue(refs)
        self.assertTrue(all(r['tema'] == topic for r in refs[:2]))
        refs, topic = motor.materiales('Consultar una API REST que devuelve JSON', '')
        self.assertTrue(refs)
        self.assertEqual(topic, '')

    def test_restricciones_enunciado_no_dan_orden_curso(self):
        # El motor es universal y no limita el problema a las guías de redes.
        from inspect import getsource
        fuente = getsource(motor.generar)
        self.assertIn('cualquier temática', fuente)
        self.assertIn('Respeta instrucciones específicas', fuente)
        self.assertNotIn('tutor del curso', fuente)

    def test_codigo_en_bloques(self):
        val = cliente.codigo_valido('Análisis\n```python\nx = 2\nprint(x)\n```\nExplicación')
        self.assertEqual(val, 'x = 2\nprint(x)\n')
        self.assertIsNone(cliente.codigo_valido('```python\nx =\n```'))

    def test_progresivo_sin_mensajes(self):
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td) / 'codigo.py'
            salida = io.StringIO()
            with redirect_stdout(salida):
                res = cliente.escritura_progresiva('# comentario\nx = 1\n\nprint(x)\n', dest, 0, 0, False)
            self.assertTrue(res)
            self.assertEqual(dest.read_text(encoding='utf-8'), '# comentario\nx = 1\n\nprint(x)\n')
            self.assertNotIn('esperando', dest.read_text(encoding='utf-8').lower())
            ast.parse(dest.read_text(encoding='utf-8'))

    def test_http_y_archivos_resolver_revisar_corregir(self):
        def mock_generar(modo, contenido, archivo, tema='', timeout=390):
            if modo == 'revisar':
                return 'Error encontrado: falta validación.'
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
                        Path('ejercicio.txt').write_text('Tema: diccionarios\nContar palabras.', encoding='utf-8')
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
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()
