"""Comando 'bot': consulta servidor local y guarda soluciones en el proyecto actual."""
from __future__ import annotations

import argparse
import ast
import io
import tokenize
import uuid
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

from motor import KB, TEMAS, materiales, normalizar_tema

BASE = Path(__file__).resolve().parent
URL = 'http://127.0.0.1:8765'


def peticion(ruta: str, datos: dict | None = None, timeout: int = 420) -> dict:
    req = urllib.request.Request(URL + ruta)
    if datos is not None:
        req = urllib.request.Request(URL + ruta,
            data=json.dumps(datos, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json'}, method='POST')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as ex:
        try:
            detalle = json.load(ex).get('error', ex.reason)
        except Exception:
            detalle = ex.reason
        raise RuntimeError(f'Servidor devolvió {ex.code}: {detalle}') from ex
    except (urllib.error.URLError, TimeoutError) as ex:
        raise RuntimeError('No se pudo conectar con el servidor local. Comprueba la tarea '
                           'de Windows o ejecuta: python servidor.py\nDetalle: ' + str(ex)) from ex


def codigo_valido(texto: str) -> str | None:
    bloques = re.findall(r'```(?:python|py)\s*\n(.*?)```', texto,
                         flags=re.IGNORECASE | re.DOTALL)
    for raw in bloques:
        codigo = raw.strip('\n') + '\n'
        try:
            ast.parse(codigo)
            return codigo
        except SyntaxError:
            continue
    return None


def nombre_libre(ruta: Path) -> Path:
    if not ruta.exists():
        return ruta
    n = 2
    while True:
        candidata = ruta.with_name(f'{ruta.stem}_{n}{ruta.suffix}')
        if not candidata.exists():
            return candidata
        n += 1


def abrir_vscode(ruta: Path) -> bool:
    ejecutable = shutil.which('code') or shutil.which('code.cmd')
    if not ejecutable:
        return False
    try:
        if os.name == 'nt':
            flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            subprocess.Popen(['cmd.exe', '/d', '/c', 'code', '--reuse-window', str(ruta)],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, creationflags=flags)
        else:
            subprocess.Popen([ejecutable, '--reuse-window', str(ruta)],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        return True
    except OSError:
        return False



def abrir_carpeta_vscode(carpeta: Path) -> bool:
    """Abre otra ventana de VS Code, sin reemplazar el proyecto actual."""
    ejecutable = shutil.which('code') or shutil.which('code.cmd')
    if not ejecutable:
        return False
    try:
        if os.name == 'nt':
            flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            subprocess.Popen(['cmd.exe', '/d', '/c', 'code', '-n', str(carpeta)],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, creationflags=flags)
        else:
            subprocess.Popen([ejecutable, '-n', str(carpeta)],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        return True
    except OSError:
        return False


def exportar_archivo_python(origen: Path, destino: str = '', abrir: bool = True) -> Path:
    """Exporta UN .py, sin reportes ni carpetas auxiliares, a destino elegido."""
    origen = origen.expanduser().resolve()
    if not origen.is_file() or origen.suffix.lower() != '.py':
        raise ValueError(f'El archivo de origen debe ser un .py existente: {origen}')
    if not destino.strip():
        try:
            destino = input('Escribe la ruta de la carpeta donde exportar el .py: ').strip()
        except EOFError as ex:
            raise ValueError('Indica una ruta con --destino "C:\\Mis_Ejercicios".') from ex
    # Acepta rutas Windows copiadas entre comillas desde el Explorador.
    destino = destino.strip().strip('"').strip("'")
    if not destino:
        raise ValueError('No se indicó ninguna carpeta de exportación.')
    carpeta = Path(destino).expanduser().resolve()
    if carpeta.exists() and not carpeta.is_dir():
        raise ValueError(f'El destino existe, pero no es una carpeta: {carpeta}')
    carpeta.mkdir(parents=True, exist_ok=True)
    archivo = nombre_libre(carpeta / origen.name)
    # No sobrescribir el original: proteger incluso si las rutas coinciden.
    if archivo == origen:
        raise ValueError('Selecciona otra carpeta: el archivo ya está en ese destino.')
    for intento in range(8):
        try:
            shutil.copy2(origen, archivo)
            break
        except PermissionError:
            if intento == 7:
                raise
            time.sleep(.2 * (intento + 1))
    print(f'ARCHIVO EXPORTADO: {archivo}')
    print(f'CARPETA DE DESTINO: {carpeta}')
    print('Se exportó únicamente el archivo .py (sin el informe .md).')
    if abrir:
        if abrir_carpeta_vscode(carpeta):
            print('Abriendo la carpeta en otra ventana de VS Code...')
        else:
            print(f'Para abrirlo manualmente, ejecuta: code -n "{carpeta}"')
    return archivo


def guardar_atomico(ruta: Path, contenido: str) -> None:
    """Publicar una copia completa, nunca anexar usando un puntero que otro editor mueva."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_name(f'.{ruta.name}.{uuid.uuid4().hex}.tmp')
    try:
        temporal.write_text(contenido, encoding='utf-8', newline='')
        os.replace(temporal, ruta)
    finally:
        temporal.unlink(missing_ok=True)


def ack_actual(ack: Path, max_edad: float = 3.0) -> bool:
    try:
        return time.time() - ack.stat().st_mtime < max_edad
    except OSError:
        return False


def guardar_con_reintentos(ruta: Path, contenido: str, intentos: int = 16) -> bool:
    """Copia completa recuperable aunque Windows bloquee brevemente el archivo."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    for intento in range(intentos):
        temporal = ruta.with_name(f'.{ruta.name}.{uuid.uuid4().hex}.tmp')
        try:
            temporal.write_text(contenido, encoding='utf-8', newline='')
            os.replace(temporal, ruta)
            return True
        except (PermissionError, OSError):
            time.sleep(min(.05 * (intento + 1), .4))
        finally:
            try:
                temporal.unlink(missing_ok=True)
            except OSError:
                pass
    try:
        # Los editores pueden negar el reemplazo, pero permitir la escritura normal.
        ruta.write_text(contenido, encoding='utf-8', newline='')
        return True
    except OSError:
        return False


def ack_version(ack: Path) -> int:
    try:
        if time.time() - ack.stat().st_mtime > 3.0:
            return -1
        return int(json.loads(ack.read_text(encoding='utf-8')).get('version', -1))
    except (OSError, ValueError, TypeError):
        return -1


def lineas_de_codigo(codigo: str) -> set[int]:
    """Líneas que contienen instrucciones; # aislados y blancos no consumen intervalo.

    tokenize distingue comentarios reales de los # que están dentro de cadenas.
    Las docstrings se consideran código. Los comentarios al final de una
    instrucción no hacen que esa instrucción pierda su intervalo.
    """
    significativas = set()
    try:
        for token in tokenize.generate_tokens(io.StringIO(codigo).readline):
            if token.type in {tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE,
                              tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER,
                              tokenize.ENCODING}:
                continue
            inicio, final = token.start[0], token.end[0]
            # Un token de cadena puede abarcar varias líneas reales.
            significativas.update(range(inicio, max(inicio + 1, final + 1)))
    except tokenize.TokenError:
        # El cliente ya comprueba la sintaxis de la respuesta del modelo.
        return {i for i, linea in enumerate(codigo.splitlines(), 1)
                if linea.strip() and not linea.lstrip().startswith('#')}
    return significativas


def escritura_progresiva(codigo: str, salida: Path, segundos: float, variacion: float,
                         abrir: bool, pausa_inicial: float = 0) -> bool:
    """Publica una solución maestra inmutable con pausa/reanudación.

    Controles: F6/F7 desde VS Code (extensión v1.3) o P/R en la terminal.
    La pausa no cancela Ollama, cliente ni servidor; solo congela el avance.
    """
    lineas = codigo.splitlines(keepends=True)
    relevantes = lineas_de_codigo(codigo)
    salida.parent.mkdir(parents=True, exist_ok=True)
    if salida.exists():
        raise FileExistsError(f'No se sobrescribe el archivo existente: {salida}')
    salida.touch()
    print('Archivo Python:', salida)
    if abrir:
        if abrir_vscode(salida):
            print('Abriendo el archivo en VS Code...')
        else:
            print('Puedes abrir el archivo manualmente en VS Code.')

    raiz = Path.cwd().resolve()
    sesiones = raiz / '.bot_sesiones'
    sesiones.mkdir(parents=True, exist_ok=True)
    sid = uuid.uuid4().hex
    ack = sesiones / f'{sid}.ack'
    control = sesiones / f'{sid}.paused'
    respaldo = sesiones / f'{sid}_solucion_original.py'
    respaldo.write_text(codigo, encoding='utf-8')
    prefijo = ''
    seq = 0

    def publicar(finalizado=False) -> bool:
        datos = {
            'magic': 'PYTHON_AI_LOCAL_V3', 'id': sid, 'version': seq,
            'archivo': str(salida.resolve()), 'contenido': prefijo,
            'terminado': finalizado,
        }
        estado = sesiones / f'{sid}_v{seq:08d}.json'
        temporal = sesiones / f'.{sid}_v{seq:08d}_{uuid.uuid4().hex}.tmp'
        try:
            temporal.write_text(json.dumps(datos, ensure_ascii=False), encoding='utf-8')
            os.rename(temporal, estado)
            return True
        except OSError:
            return False
        finally:
            try:
                temporal.unlink(missing_ok=True)
            except OSError:
                pass

    def leer_tecla_terminal() -> None:
        # msvcrt no necesita Enter; funciona si PowerShell está en primer plano.
        if os.name != 'nt':
            return
        try:
            import msvcrt
            while msvcrt.kbhit():
                tecla = msvcrt.getwch().lower()
                if tecla == 'p':
                    control.touch(exist_ok=True)
                elif tecla == 'r':
                    control.unlink(missing_ok=True)
        except (OSError, ImportError):
            pass

    pausa_anunciada = False

    def pausado() -> bool:
        nonlocal pausa_anunciada
        leer_tecla_terminal()
        estado = control.exists()
        if estado and not pausa_anunciada:
            print('PAUSADO. F7 en VS Code o R en la terminal para continuar.', flush=True)
        elif not estado and pausa_anunciada:
            print('REANUDADO.', flush=True)
        pausa_anunciada = estado
        return estado

    def esperar(segundos_restantes: float) -> None:
        # El contador no avanza durante una pausa; permite pausar a mitad
        # de cualquier intervalo y reanudar conservando el tiempo restante.
        while segundos_restantes > 0 or pausado():
            if pausado():
                time.sleep(.10)
                continue
            lapso = min(.10, segundos_restantes)
            inicio = time.monotonic()
            time.sleep(lapso)
            segundos_restantes = max(0.0, segundos_restantes - (time.monotonic() - inicio))

    publicar()
    extension = False
    if abrir:
        for _ in range(30):
            if ack_version(ack) >= 0:
                extension = True
                break
            time.sleep(.15)
    if extension:
        print('Editor sincronizado: F6 pausa / F7 reanuda (o P / R en terminal).')
    else:
        print('Modo archivo: P pausa / R reanuda desde esta terminal.')

    try:
        if pausa_inicial:
            esperar(pausa_inicial)
        hay_codigo_anterior = False
        for i, linea in enumerate(lineas, 1):
            # Se esperan intervalos solo ANTES de las líneas de código
            # posteriores a la primera. Los comentarios y blancos se escriben
            # sin añadir un intervalo adicional.
            if i in relevantes:
                if hay_codigo_anterior and segundos > 0:
                    esperar(segundos * random.uniform(1 - variacion, 1 + variacion))
                hay_codigo_anterior = True
            while pausado():
                time.sleep(.10)
            prefijo += linea
            seq += 1
            entregado = publicar(finalizado=(i == len(lineas)))
            extension = ack_version(ack) >= 0
            if not extension or not entregado:
                if not guardar_con_reintentos(salida, prefijo):
                    print('Aviso: archivo temporalmente bloqueado; copia maestra a salvo.',
                          file=sys.stderr)
        if not lineas:
            publicar(finalizado=True)
        if extension:
            for _ in range(30):
                if ack_version(ack) >= seq:
                    break
                time.sleep(.1)
        if ack_version(ack) < seq:
            if not guardar_con_reintentos(salida, prefijo):
                emergencia = salida.with_name(salida.stem + '_respaldo_bot.py')
                emergencia.write_text(codigo, encoding='utf-8')
                print('El editor estaba bloqueado; copia completa:', emergencia)
    except KeyboardInterrupt:
        publicar(finalizado=True)
        guardar_con_reintentos(salida, prefijo)
        print('\nEscritura cancelada; el contenido parcial y el respaldo se conservaron.',
              file=sys.stderr)
        return False
    finally:
        try:
            control.unlink(missing_ok=True)
        except OSError:
            pass
    print(f'Escritura completada: {len(lineas)} líneas físicas; '
          f'{sum(i in relevantes for i in range(1, len(lineas)+1))} líneas con código.')
    return True


def temas() -> None:
    cnt = Counter()
    if KB.is_file():
        with KB.open(encoding='utf-8') as f:
            for linea in f:
                if linea.strip():
                    d = json.loads(linea)
                    cnt[d['tema']] += 1
    print('TEMAS — PYTHON AI LOCAL (biblioteca general)')
    for slug, descripcion in TEMAS.items():
        print(f'  {slug:22s} {cnt[slug]:3d} registros — {descripcion}')
    print('Usa: bot buscar "manejar JSON" --tema json_csv')


def buscar(texto: str, tema: str = '') -> None:
    docs, detectado = materiales(texto, tema, max_refs=6)
    print('Tema:', detectado or 'no especificado')
    if not docs:
        print('No se encontraron materiales coincidentes.')
    for d in docs:
        print(f"[{d['id']}] {d['titulo']} | {d['tema']} | {d['fuente']}")


def agregar(ruta: Path, tema: str) -> None:
    t = normalizar_tema(tema)
    if not t:
        raise ValueError('El tema no existe. Usa: bot temas')
    if not ruta.is_file() or ruta.suffix.lower() not in {'.txt', '.md', '.py'}:
        raise ValueError('Agrega un archivo existente .txt, .md o .py')
    if ruta.stat().st_size > 30000:
        raise ValueError('El archivo de material excede 30 KB')
    contenido = ruta.read_text(encoding='utf-8-sig')
    if not contenido.strip():
        raise ValueError('El archivo está vacío')
    nueva = {'id': 'usuario-' + str(int(time.time() * 1000)), 'tipo': 'material_propio',
             'tema': t, 'titulo': ruta.stem, 'nivel': 'personalizado',
             'fuente': f'Material agregado: {ruta.name}', 'contenido': contenido}
    KB.parent.mkdir(parents=True, exist_ok=True)
    with KB.open('a', encoding='utf-8') as f:
        f.write(json.dumps(nueva, ensure_ascii=False) + '\n')
    print(f'Material añadido a {t}. Ya está disponible para las búsquedas locales.')


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog='bot',
        description='Asistente local de Python: resolver, revisar y corregir ejercicios')
    p.add_argument('modo', choices=['resolver', 'revisar', 'corregir', 'reproducir', 'exportar', 'estado', 'temas', 'buscar', 'agregar'])
    p.add_argument('archivo', nargs='?', help='Archivo .txt/.py o consulta en modo buscar')
    p.add_argument('--tema', default='', help='Tema (ej: funciones, archivos, bucles, operadores)')
    p.add_argument('--escribir', action='store_true', help='Guardar código línea por línea en VS Code')
    p.add_argument('--intervalo', type=float, default=5.0,
                   help='Segundos entre líneas, usado con --escribir. Ej: 60')
    p.add_argument('--variacion', type=float, default=0.0,
                   help='Variación del intervalo: 0 fijo, hasta 0.8 aleatorio')
    p.add_argument('--tiempo-max', type=int, default=390,
                   help='Tiempo máximo de consulta a Ollama, entre 30 y 900 segundos')
    p.add_argument('--no-abrir', action='store_true',
                   help='No abrir el archivo progresivo automáticamente en VS Code')
    p.add_argument('--exportar', action='store_true',
                   help='Exportar también el .py al finalizar la solución')
    p.add_argument('--destino', default='',
                   help='Carpeta de exportación del .py; si falta se solicita por teclado')
    p.add_argument('--no-abrir-exportacion', action='store_true',
                   help='No abrir otra ventana de VS Code después de exportar')
    p.add_argument('--salida', default='soluciones',
                   help='Carpeta de resultados, relativa a la ubicación actual')
    a = p.parse_args(argv)
    try:
        if a.modo == 'exportar':
            if not a.archivo:
                p.error('Ejemplo: bot exportar .\\soluciones\\ejercicio_solucion.py')
            exportar_archivo_python(Path(a.archivo), a.destino,
                                   abrir=not a.no_abrir_exportacion)
            return 0
        if a.modo == 'temas':
            temas(); return 0
        if a.modo == 'buscar':
            if not a.archivo: p.error('Ejemplo: bot buscar "clasificar latencia"')
            buscar(a.archivo, a.tema); return 0
        if a.modo == 'agregar':
            if not a.archivo or not a.tema:
                p.error('Ejemplo: bot agregar ejercicio_resuelto.md --tema funciones')
            agregar(Path(a.archivo).resolve(), a.tema); return 0
        if a.modo == 'estado':
            info = peticion('/estado', timeout=12)
            print('Servidor:', info['servidor'])
            print('Modelo:', info['modelo'])
            print('Ollama:', info['detalle'])
            return 0 if info['listo'] else 1

        if a.modo == 'reproducir':
            if not a.archivo:
                p.error('Ejemplo: bot reproducir .\\soluciones\\ejercicio_solucion.md --intervalo 5')
            md = Path(a.archivo).expanduser().resolve()
            if not md.is_file() or md.suffix.lower() != '.md':
                raise ValueError('Indica un archivo Markdown existente de solución del bot.')
            respuesta = md.read_text(encoding='utf-8-sig')
            codigo = codigo_valido(respuesta)
            if not codigo:
                raise ValueError('El Markdown no contiene un bloque de código Python válido.')
            nombre = md.stem.replace('_solucion', '')
            salida = nombre_libre(md.parent / f'{nombre}_recuperado.py')
            if a.intervalo < 0 or not 0 <= a.variacion <= .8:
                raise ValueError('Intervalo o variación inválidos.')
            if a.escribir:
                escritura_progresiva(codigo, salida, a.intervalo, a.variacion,
                                    abrir=not a.no_abrir)
            else:
                salida.write_text(codigo, encoding='utf-8')
                print('Código restaurado:', salida)
            if a.exportar:
                exportar_archivo_python(salida, a.destino,
                                       abrir=not a.no_abrir_exportacion)
            return 0

        if a.exportar and a.modo not in {'resolver', 'corregir'}:
            raise ValueError('--exportar está disponible al resolver o corregir archivos.')
        if not a.archivo: p.error('Debes indicar el archivo, por ejemplo: bot resolver ejercicio.txt')
        if not 30 <= a.tiempo_max <= 900:
            raise ValueError('--tiempo-max debe estar entre 30 y 900 segundos')
        if a.intervalo < 0 or not 0 <= a.variacion <= 0.8:
            raise ValueError('--intervalo debe ser >= 0 y --variacion entre 0 y 0.8')
        archivo = Path(a.archivo).expanduser().resolve()
        if not archivo.is_file():
            raise ValueError(f'No existe el archivo: {archivo}')
        if archivo.stat().st_size > 50000:
            raise ValueError('Archivo mayor que el límite de 50 KB')
        contenido = archivo.read_text(encoding='utf-8-sig').strip()
        if not contenido:
            raise ValueError('El archivo está vacío')
        print(f'Consultando IA local: {a.modo} {archivo.name}...')
        respuesta = peticion('/consulta', {
            'modo': a.modo, 'archivo': archivo.name, 'contenido': contenido,
            'tema': a.tema, 'tiempo_max': a.tiempo_max,
        }, timeout=a.tiempo_max + 30)['respuesta']
        destino = Path(a.salida).expanduser().resolve()
        destino.mkdir(parents=True, exist_ok=True)
        sufijos = {'resolver':'solucion','revisar':'revision','corregir':'correccion'}
        inf = nombre_libre(destino / f'{archivo.stem}_{sufijos[a.modo]}.md')
        inf.write_text(respuesta.rstrip() + '\n', encoding='utf-8')
        print('Explicación:', inf)
        if a.modo in {'resolver', 'corregir'}:
            codigo = codigo_valido(respuesta)
            if codigo is None:
                print('El modelo no proporcionó un bloque Python sintácticamente válido.')
                print('Consulta el archivo Markdown. No se escribió código incompleto.')
                return 2
            suf = 'solucion' if a.modo == 'resolver' else 'corregido'
            ruta_py = nombre_libre(destino / f'{archivo.stem}_{suf}.py')
            if a.escribir:
                completo = escritura_progresiva(codigo, ruta_py, a.intervalo,
                               a.variacion, abrir=not a.no_abrir)
                if not completo:
                    return 130
            else:
                ruta_py.write_text(codigo, encoding='utf-8')
                print('Código:', ruta_py)
            if a.exportar:
                exportar_archivo_python(ruta_py, a.destino,
                                       abrir=not a.no_abrir_exportacion)
        print('Finalizado. El código generado no se ha ejecutado.')
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print('ERROR:', error, file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('\nCancelado por teclado.', file=sys.stderr)
        return 130


if __name__ == '__main__':
    raise SystemExit(main())
