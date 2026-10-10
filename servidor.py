"""Servicio local. Solo acepta conexiones desde esta computadora."""
from __future__ import annotations

import json
import os
import logging
import shutil
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

from motor import MODELO, generar, modelo_disponible

BASE = Path(__file__).resolve().parent
LOGS = BASE / "logs"
LOGS.mkdir(exist_ok=True)
handlers = [logging.FileHandler(LOGS / "servidor.log", encoding="utf-8")]
if sys.stdout is not None:
    handlers.append(logging.StreamHandler(sys.stdout))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=handlers,
)
logger = logging.getLogger("python-ai-local")
MODELO_LOCK = Lock()


def iniciar_ollama_si_necesario():
    ok, mensaje = modelo_disponible()
    if ok:
        logger.info(mensaje)
        return
    # Si responde la API pero falta el modelo, no lanzar otra instancia.
    if "falta el modelo" in mensaje:
        logger.warning(mensaje)
        return

    binario = shutil.which("ollama")
    if not binario and sys.platform == "win32":
        candidato = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe"
        if candidato.is_file():
            binario = str(candidato)
    if not binario:
        logger.error("Ollama no encontrado. Instala Ollama antes de usar este servicio.")
        return

    logger.info("Intentando iniciar Ollama localmente...")
    try:
        registro = (LOGS / "ollama.log").open("a", encoding="utf-8")
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        subprocess.Popen([binario, "serve"], stdin=subprocess.DEVNULL,
                         stdout=registro, stderr=subprocess.STDOUT,
                         creationflags=flags,
                         env={**os.environ, "OLLAMA_NO_CLOUD": "1"})
        registro.close()
        for _ in range(30):
            ok, mensaje = modelo_disponible()
            if ok or "falta el modelo" in mensaje:
                logger.info(mensaje)
                return
            time.sleep(1)
        logger.warning("No se pudo verificar Ollama despues de 30 segundos")
    except OSError as error:
        logger.error("No se pudo iniciar Ollama: %s", error)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, formato, *args):
        logger.info("%s %s", self.address_string(), formato % args)

    def enviar(self, status: int, datos: dict):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        if self.path != "/estado":
            self.enviar(404, {"error": "Ruta inexistente"})
            return
        ok, detalle = modelo_disponible()
        self.enviar(200, {"servidor": "activo", "modelo": MODELO,
                          "listo": ok, "detalle": detalle})

    def do_POST(self):
        if self.path != "/consulta":
            self.enviar(404, {"error": "Ruta inexistente"})
            return
        try:
            longitud = int(self.headers.get("Content-Length", "0"))
            if longitud <= 0 or longitud > 70000:
                self.enviar(413, {"error": "Solicitud vacia o demasiado grande"})
                return
            datos = json.loads(self.rfile.read(longitud).decode("utf-8"))
            modo = datos.get("modo", "")
            contenido = datos.get("contenido", "")
            archivo = datos.get("archivo", "")
            tema = datos.get("tema", "")
            tiempo_max = datos.get("tiempo_max", 390)
            if (modo not in {"resolver", "revisar", "corregir"}
                    or not isinstance(contenido, str)
                    or not 0 < len(contenido) <= 50000
                    or not isinstance(archivo, str) or len(archivo) > 250
                    or not isinstance(tema, str) or len(tema) > 70
                    or not isinstance(tiempo_max, int) or not 30 <= tiempo_max <= 900):
                self.enviar(400, {"error": "Solicitud invalida"})
                return
            ok, detalle = modelo_disponible()
            if not ok:
                self.enviar(503, {"error": detalle})
                return
            # Evita que varias consultas saturen un equipo con poca RAM.
            with MODELO_LOCK:
                texto = generar(modo, contenido, archivo, tema=tema, timeout=tiempo_max)
            self.enviar(200, {"respuesta": texto})
        except (OSError, ValueError, KeyError, RuntimeError) as error:
            logger.exception("Error en consulta")
            self.enviar(500, {"error": str(error)})


def main():
    iniciar_ollama_si_necesario()
    try:
        with ThreadingHTTPServer(("127.0.0.1", 8765), Handler) as servidor:
            logger.info("PYTHON AI LOCAL escuchando en http://127.0.0.1:8765")
            servidor.serve_forever()
    except OSError as error:
        logger.error("No se pudo iniciar el servicio (¿ya esta activo?): %s", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
