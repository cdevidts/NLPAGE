"""Gemini API (Google AI Studio) desde el contenedor o un turno programado.

Clave: variable de entorno GEMINI_API_KEY (Cris la crea en https://aistudio.google.com/apikey
y la deja en la configuración del entorno). Nunca se escribe en archivos ni commits.

Gratis (free tier de la API):
    python3 -I scripts/gemini/gemini.py estado
    python3 -I scripts/gemini/gemini.py texto "pregunta"            # o "-" para leer de stdin
    python3 -I scripts/gemini/gemini.py voz --texto "..." --salida x.wav [--voz Charon] [--estilo "..."]
    python3 -I scripts/gemini/gemini.py dialogo guion.json --salida x.wav   # 2 voces, tipo podcast
    python3 -I scripts/gemini/gemini.py youtube _BUAF1B1JXI --prompt "..." [--salida x.md]   # ve el video por fotogramas
        (gratis, ~30 s por Short; id o URL de YouTube; --archivo prompt.md en vez de --prompt)

Pagado (imagen, video): solo con --pago y si el tope del mes en docs/gemini/config.json alcanza.
Nivel pagado activo desde 2026-11-06 (Cris ligó la facturación; saldo prepagado + créditos de AI Pro).
El tope del mes está en docs/gemini/config.json; subirlo requiere el OK de Cris.
    python3 -I scripts/gemini/gemini.py imagen --prompt "..." --salida x.jpg [--aspecto 4:3] --pago
    python3 -I scripts/gemini/gemini.py video --ficha docs/video-ia/fichas/x.json --ensayo     # arma y revisa el prompt, no gasta
    python3 -I scripts/gemini/gemini.py video --ficha docs/video-ia/fichas/x.json --revisar    # segunda opinión de un modelo de texto
    python3 -I scripts/gemini/gemini.py video --ficha docs/video-ia/fichas/x.json --salida x.mp4 --pago
        Video SOLO con ficha (skill .claude/skills/video-ia-prompteo): nada de prompts sueltos.

Cada llamada pagada queda en docs/gemini/gasto.csv con su costo estimado.

Claves: GEMINI_API_KEY_FREE (proyecto sin facturación) para todo lo gratis; GEMINI_API_KEY (con
facturación) solo para imagen y video pagados. Si falta la gratis, todo usa GEMINI_API_KEY.
"""
import argparse, base64, csv, datetime, json, os, ssl, sys, time, urllib.error, urllib.request, wave

API = os.environ.get('GEMINI_API_BASE', 'https://generativelanguage.googleapis.com/v1beta')
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG = os.path.join(RAIZ, 'docs', 'gemini', 'config.json')
GASTO = os.path.join(RAIZ, 'docs', 'gemini', 'gasto.csv')

# Precios estimados (aistudio.google.com/docs/pricing, releídos 2026-11-06). Solo para el tope.
PRECIO = {
    'gemini-3.1-flash-lite-image': 0.034,  # por imagen 1K
    'gemini-nano-banana-2.1': 0.050,       # por imagen 2K
    'gemini-3.1-flash-image': 0.067,       # por imagen 1K
    'gemini-3-pro-image': 0.134,
    'gemini-omni-1.1-flash': 0.10,         # por segundo de video 720p (desde 3-dic-2026 se enruta a 1.2)
    'gemini-omni-1.2-flash': 0.07,         # por segundo de video 720p (360p ~0.023)
}


def config():
    c = {'texto': 'gemini-3.6-flash', 'texto_respaldo': [], 'voz': 'gemini-3.8-flash-tts', 'imagen': 'gemini-3.1-flash-lite-image',
         'video': 'gemini-omni-1.1-flash', 'tope_mes_usd': 0}
    if os.path.exists(CONFIG):
        c.update(json.load(open(CONFIG, encoding='utf8')))
    return c


# Dos claves (Cris, 2026-11-06): GEMINI_API_KEY_FREE es de un proyecto SIN facturación (texto, voz,
# revisiones y YouTube quedan gratis); GEMINI_API_KEY tiene facturación y se usa solo para imagen y video
# pagados. Sin la clave gratis, todo cae en GEMINI_API_KEY (y lo gratis se cobra a tarifa de pago).
PAGADO = False
# Si la clave gratis no está en el entorno, se lee de este archivo fuera de git (carpeta compartida del
# proyecto; Cris lo autorizó el 2026-11-07). Nunca se copia al repo.
SECRETOS = os.environ.get('GEMINI_SECRETOS', '/mnt/project-files/.secretos/gemini.env')


def clave_libre():
    if os.environ.get('GEMINI_API_KEY_FREE'):
        return os.environ['GEMINI_API_KEY_FREE']
    try:
        for linea in open(SECRETOS, encoding='utf-8'):
            nombre, _, valor = linea.strip().partition('=')
            if nombre == 'GEMINI_API_KEY_FREE' and valor:
                return valor.strip().strip('"\'')
    except OSError:
        pass
    return None


def clave():
    libre = clave_libre()
    pago = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    k = pago if PAGADO else (libre or pago)
    if not k:
        sys.exit('Falta GEMINI_API_KEY en el entorno. Cris la crea en https://aistudio.google.com/apikey '
                 'y la agrega en la configuración del entorno (ver docs/gemini/README.md).')
    return k


class Ocupado(Exception):
    """503/429 o sin respuesta: el modelo está saturado; se prueba el siguiente."""


def llamar(metodo, ruta, cuerpo=None, timeout=300):
    ctx = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE') or os.environ.get('REQUESTS_CA_BUNDLE') or None)
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    req = urllib.request.Request(f'{API}/{ruta}', data=datos, method=metodo,
                                 headers={'x-goog-api-key': clave(), 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        cuerpo_err = e.read().decode(errors='replace')
        try:
            msg = json.loads(cuerpo_err)['error']['message']
        except Exception:
            msg = cuerpo_err[:500]
        if e.code in (429, 503):
            raise Ocupado(f'Gemini {e.code}: {msg}')
        raise SystemExit(f'Gemini {e.code} en {ruta}: {msg}')
    except TimeoutError:
        raise Ocupado(f'Gemini no respondió en {timeout} s')


def bloques(resp):
    """Bloques de salida del modelo (texto, audio, imagen, video), sin los pensamientos."""
    out = []
    for paso in resp.get('steps', []):
        if paso.get('type') not in (None, 'model_output'):
            continue
        out.extend(paso.get('content', []))
    # Respuesta del formato viejo (generateContent), por si la API la devuelve.
    for cand in resp.get('candidates', []):
        for p in cand.get('content', {}).get('parts', []):
            if 'text' in p and not p.get('thought'):
                out.append({'type': 'text', 'text': p['text']})
            elif 'inlineData' in p:
                mime = p['inlineData'].get('mimeType', '')
                out.append({'type': mime.split('/')[0], 'data': p['inlineData']['data'], 'mime_type': mime})
    return out


def interaccion(modelo, entrada, formato=None, extra=None):
    cuerpo = {'model': modelo, 'input': entrada, 'store': False}
    if formato:
        cuerpo['response_format'] = formato
    cuerpo.update(extra or {})
    # Tier 1 de pago: TTS tiene tope de 10 pedidos por minuto (429 del 6-nov con un Short de 16 líneas).
    for intento in range(6):
        try:
            return llamar('POST', 'interactions', cuerpo)
        except Ocupado as e:
            # El tope por día (free tier: 10 voces al día) no se arregla esperando un minuto.
            if '429' not in str(e) or 'per day' in str(e) or intento == 5:
                raise
            print(f'{e} -> espero {10 * (intento + 1)} s', file=sys.stderr)
            time.sleep(10 * (intento + 1))


def texto(prompt, modelo=None):
    """Texto con respaldo: si un modelo está saturado (pasó con 3.8 Flash el 30-oct), el siguiente."""
    c = config()
    modelos = [modelo] if modelo else [c['texto'], *c.get('texto_respaldo', [])]
    for m in modelos:
        try:
            r = llamar('POST', 'interactions', {'model': m, 'input': prompt, 'store': False}, timeout=90)
            return ''.join(b.get('text', '') for b in bloques(r) if b.get('type') == 'text').strip()
        except Ocupado as e:
            print(f'{m}: {e}', file=sys.stderr)
    sys.exit('Todos los modelos de texto están saturados; reintentar más tarde.')


def youtube(video, prompt, modelo=None, temperatura=0.2):
    """Mira un video público de YouTube (fotogramas 1/s + audio) y responde al prompt. Gratis en el free tier.
    Probado 2026-11-06: 3.6 Flash analiza un Short de 46 s en ~25-30 s (4,3 k tokens de video)."""
    url = video if video.startswith('http') else f'https://www.youtube.com/watch?v={video}'
    cuerpo = {'contents': [{'parts': [{'file_data': {'file_uri': url}}, {'text': prompt}]}],
              'generationConfig': {'temperature': temperatura}}
    c = config()
    modelos = [modelo] if modelo else [c['texto'], *c.get('texto_respaldo', [])]
    for m in modelos:
        try:
            r = llamar('POST', f'models/{m}:generateContent', cuerpo, timeout=400)
            out = ''.join(b.get('text', '') for b in bloques(r) if b.get('type') == 'text').strip()
            uso = r.get('usageMetadata', {})
            print(f'{m}: {uso.get("totalTokenCount", "?")} tokens', file=sys.stderr)
            return out
        except Ocupado as e:
            print(f'{m}: {e}', file=sys.stderr)
    sys.exit('Todos los modelos están saturados; reintentar más tarde.')


def binario(resp, tipo):
    for b in bloques(resp):
        if b.get('type') == tipo and b.get('data'):
            return base64.b64decode(b['data'])
        if b.get('type') == tipo and b.get('uri'):
            return descargar_uri(b['uri'])
    sys.exit(f'La respuesta no trae {tipo}: {json.dumps(resp)[:600]}')


def descargar_uri(uri):
    fid = uri.split('/files/')[-1].split(':')[0].split('?')[0]
    for _ in range(120):
        if llamar('GET', f'files/{fid}').get('state') == 'ACTIVE':
            break
        time.sleep(5)
    req = urllib.request.Request(f'{API}/files/{fid}:download?alt=media', headers={'x-goog-api-key': clave()})
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read()


def guardar_wav(audio, salida):
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    if audio[:4] == b'RIFF':
        open(salida, 'wb').write(audio)
    else:  # PCM crudo: 24 kHz, mono, 16 bit
        with wave.open(salida, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(audio)


# --- Gasto (solo lo pagado) -------------------------------------------------------

def gastado_mes():
    if not os.path.exists(GASTO):
        return 0.0
    mes = datetime.date.today().strftime('%Y-%m')
    return sum(float(f['usd']) for f in csv.DictReader(open(GASTO, encoding='utf8')) if f['fecha'].startswith(mes))


def autorizar(args, modelo, usd):
    if not args.pago:
        sys.exit(f'{modelo} es pagado (~US${usd:.3f}). Agrega --pago; además el tope del mes debe alcanzar.')
    tope, ya = float(config()['tope_mes_usd']), gastado_mes()
    if ya + usd > tope:
        sys.exit(f'Tope del mes: US${tope:.2f}, gastado US${ya:.2f}, esta llamada ~US${usd:.3f}. '
                 'Subir el tope en docs/gemini/config.json requiere el OK de Cris (regla de plata).')


def anotar(tipo, modelo, usd, salida, prompt):
    nuevo = not os.path.exists(GASTO)
    with open(GASTO, 'a', newline='', encoding='utf8') as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(['fecha', 'tipo', 'modelo', 'usd', 'salida', 'prompt'])
        w.writerow([datetime.datetime.now().isoformat(timespec='seconds'), tipo, modelo, f'{usd:.3f}',
                    os.path.relpath(salida, RAIZ), prompt[:120]])


# --- Comandos -------------------------------------------------------------------------

def cmd_estado(args):
    c = config()
    modelos = []
    token = ''
    while True:
        r = llamar('GET', 'models?pageSize=200' + (f'&pageToken={token}' if token else ''))
        modelos += [m['name'].removeprefix('models/') for m in r.get('models', [])]
        token = r.get('nextPageToken')
        if not token:
            break
    print(f'Clave OK: {len(modelos)} modelos visibles.')
    print(f'  gratis: {"GEMINI_API_KEY_FREE" + ("" if os.environ.get("GEMINI_API_KEY_FREE") else " (archivo .secretos)") if clave_libre() else "FALTA GEMINI_API_KEY_FREE: lo gratis se cobra en la clave con facturación"}'
          f' · pagado: {"GEMINI_API_KEY" if os.environ.get("GEMINI_API_KEY") else "falta GEMINI_API_KEY"}')
    for uso in ('texto', 'voz', 'imagen', 'video'):
        print(f'  {uso:6} {c[uso]:32} {"disponible" if c[uso] in modelos else "NO aparece en la lista"}')
    print('  prueba de texto:', texto('Responde solo: ok')[:40])
    print(f'Gasto pagado este mes: US${gastado_mes():.2f} de un tope de US${float(c["tope_mes_usd"]):.2f}')


def cmd_texto(args):
    prompt = sys.stdin.read() if args.prompt == '-' else args.prompt
    if args.sistema:
        prompt = f'{args.sistema}\n\n{prompt}'
    print(texto(prompt, args.modelo))


def cmd_youtube(args):
    prompt = open(args.archivo, encoding='utf8').read() if args.archivo else args.prompt
    if not prompt:
        sys.exit('Falta --prompt o --archivo.')
    out = youtube(args.video, prompt, args.modelo)
    if args.salida:
        os.makedirs(os.path.dirname(os.path.abspath(args.salida)) or '.', exist_ok=True)
        open(args.salida, 'w', encoding='utf8').write(out + '\n')
        print(args.salida)
    else:
        print(out)


def cmd_voz(args):
    meta = {'type': 'speech_metadata'}
    if args.estilo:
        meta['style'] = args.estilo
    contenido = {'type': 'text', 'text': args.texto}
    if args.estilo:
        contenido['annotations'] = [meta]
    r = interaccion(args.modelo or config()['voz'], [{'type': 'user_input', 'content': [contenido]}],
                    {'type': 'audio'}, {'generation_config': {'speech_config': [{'voice': args.voz}]}})
    guardar_wav(binario(r, 'audio'), args.salida)
    print(args.salida)


def cmd_dialogo(args):
    """guion.json: {"voces": {"Ana": "Kore", "Leo": "Charon"}, "turnos": [{"quien": "Ana", "dice": "...", "estilo": "..."}]}"""
    g = json.load(open(args.guion, encoding='utf8'))
    contenido = []
    for t in g['turnos']:
        meta = {'type': 'speech_metadata', 'speaker': t['quien']}
        if t.get('estilo'):
            meta['style'] = t['estilo']
        contenido.append({'type': 'text', 'text': t['dice'], 'annotations': [meta]})
    voces = [{'speaker': q, 'voice': v} for q, v in g['voces'].items()]
    r = interaccion(args.modelo or config()['voz'], [{'type': 'user_input', 'content': contenido}],
                    {'type': 'audio'}, {'generation_config': {'speech_config': {'speakers': voces}}})
    guardar_wav(binario(r, 'audio'), args.salida)
    print(args.salida)


def cmd_imagen(args):
    global PAGADO
    PAGADO = True
    modelo = args.modelo or config()['imagen']
    usd = PRECIO.get(modelo, 0.15)
    autorizar(args, modelo, usd)
    mime = 'image/png' if args.salida.lower().endswith('.png') else 'image/jpeg'
    r = interaccion(modelo, args.prompt, {'type': 'image', 'mime_type': mime, 'aspect_ratio': args.aspecto,
                                          'image_size': args.tamano})
    os.makedirs(os.path.dirname(os.path.abspath(args.salida)), exist_ok=True)
    open(args.salida, 'wb').write(binario(r, 'image'))
    anotar('imagen', modelo, usd, args.salida, args.prompt)
    print(args.salida)


CAMPOS_FICHA = ('short', 'momento', 'fuente', 'objetivo', 'duracion', 'estilo', 'lugar', 'luz', 'paleta', 'lente',
                'continuidad', 'tomas', 'audio', 'evitar')
CAMPOS_TOMA = ('desde', 'hasta', 'plano', 'camara', 'sujeto', 'accion', 'foco')


def validar_ficha(f):
    """Una ficha incompleta no se paga (skill video-ia-prompteo). Devuelve la lista de problemas."""
    mal = [f'falta "{c}"' for c in CAMPOS_FICHA if not f.get(c)]
    if mal:
        return mal
    dur = float(f['duracion'])
    if not 3 <= dur <= 10:
        mal.append('duracion fuera de 3-10 s')
    tomas = f['tomas']
    if not 1 <= len(tomas) <= 6:
        mal.append('entre 1 y 6 tomas (3 es lo normal en 8 s; 5-6 solo en secuencia rápida)')
    t0 = 0.0
    for i, t in enumerate(tomas, 1):
        mal += [f'toma {i}: falta "{c}"' for c in CAMPOS_TOMA if t.get(c) in (None, '')]
        if t.get('desde') is not None and abs(float(t['desde']) - t0) > 0.01:
            mal.append(f'toma {i}: empieza en {t["desde"]} s y debía empezar en {t0:g} s (sin huecos)')
        if t.get('hasta') is not None:
            if float(t['hasta']) - float(t.get('desde') or 0) < 1.2:
                mal.append(f'toma {i}: menos de 1,2 s no se lee')
            t0 = float(t['hasta'])
        for c in ('sujeto', 'accion'):
            if len(str(t.get(c, '')).split()) < 4:
                mal.append(f'toma {i}: "{c}" demasiado vago (mínimo 4 palabras concretas)')
    if tomas and abs(t0 - dur) > 0.01:
        mal.append(f'las tomas terminan en {t0:g} s y la duración es {dur:g} s')
    for c in ('luz', 'lugar', 'continuidad'):
        if len(str(f.get(c, '')).split()) < 6:
            mal.append(f'"{c}" demasiado vago (mínimo 6 palabras)')
    if not isinstance(f['evitar'], list) or len(f['evitar']) < 3:
        mal.append('"evitar" debe ser una lista de al menos 3 negativos')
    return mal


def prompt_de_ficha(f):
    """Prompt en inglés según la guía oficial de Omni Flash (aistudio.google.com/docs/omni#prompt-guide)."""
    dur, tomas = float(f['duracion']), f['tomas']
    cortes = ', '.join(f'{t["hasta"]:g}s' for t in tomas[:-1])
    if len(tomas) == 1:
        estructura = f'A single continuous {dur:g}-second shot. No scene cuts.'
    else:
        articulo = 'An' if str(int(dur)).startswith('8') or int(dur) in (11, 18) else 'A'
        estructura = (f'{articulo} {dur:g}-second sequence of exactly {len(tomas)} shots with hard cuts at {cortes}. '
                      'No other cuts, no transitions, no extra shots.')
    lineas = [f'{f["estilo"]}. {estructura}',
              f'Location: {f["lugar"]}.',
              f'Lighting: {f["luz"]}. Color palette: {f["paleta"]}. Lens and texture: {f["lente"]}.',
              f'Continuity across every shot: {f["continuidad"]}.']
    for i, t in enumerate(tomas, 1):
        luz = f' Lighting in this shot: {t["luz"].rstrip(". ")}.' if t.get('luz') else ''
        lineas.append(f'[{float(t["desde"]):g}-{float(t["hasta"]):g}s] Shot {i}: {t["plano"]}, {t["camara"]}. '
                      f'Subject: {t["sujeto"].rstrip(". ")}. Action: {t["accion"].rstrip(". ")}. Focus: {t["foco"].rstrip(". ")}.{luz}')
    if f.get('texto_en_pantalla'):
        lineas.append(f'Writing that physically exists in the scene: {f["texto_en_pantalla"]} '
                      'No overlay captions, titles, subtitles, watermark or logos.')
    else:
        lineas.append('No on-screen text, no captions, no subtitles, no watermark, no logos.')
    lineas.append(f'Sound design: {f["audio"]}')
    # "Mismo lugar y momento" contradecía las fichas con tomas en sitios u horas distintas (revisión 6-nov):
    # la continuidad la dice la ficha; "detalle" (o "detalle_fondo") reemplaza la frase de época.
    lineas.append('Consider micro-detail, lighting continuity and timing; every shot must keep the continuity described '
                  'above and the same camera package. '
                  + (f.get('detalle') or f.get('detalle_fondo') or 'Include plenty of appropriate period-correct background detail so it feels real.'))
    # Sin doble negación ("Do not: no music" confunde al modelo, revisión 2026-11-06).
    import re
    evitar = [re.sub(r'^(no|not|without)\s+', '', e.strip(), flags=re.I) for e in f['evitar']]
    evitar = [re.sub(r',\s*no\s+', ', ', e, flags=re.I) for e in evitar]
    lineas.append('Avoid all of the following: ' + '; '.join(evitar) + '.')
    return '\n'.join(lineas)


def cargar_ficha(ruta):
    f = json.load(open(ruta, encoding='utf8'))
    mal = validar_ficha(f)
    if mal:
        sys.exit('Ficha incompleta, no se genera nada:\n  - ' + '\n  - '.join(mal))
    return f


def tira(salida):
    """Hoja de fotogramas (2 por segundo) para revisar la toma completa antes de usarla."""
    import subprocess
    hoja = os.path.splitext(salida)[0] + '.tira.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', salida, '-vf', 'fps=2,scale=180:-1,tile=10x2',
                    '-frames:v', '1', hoja], check=False)
    return hoja


def cmd_video(args):
    if not args.ficha:
        sys.exit('El video con IA solo se genera con --ficha (skill .claude/skills/video-ia-prompteo).')
    f = cargar_ficha(args.ficha)
    modelo = args.modelo or f.get('modelo') or config()['video']
    dur = float(f['duracion'])
    usd = PRECIO.get(modelo, 0.5) * dur
    prompt = prompt_de_ficha(f)
    if args.ensayo or args.revisar:
        print(prompt)
        print(f'\n~US${usd:.2f} ({modelo}, {dur:g} s). Gastado este mes: US${gastado_mes():.2f} de US${float(config()["tope_mes_usd"]):.2f}.')
        if args.revisar:
            guia = open(os.path.join(RAIZ, '.claude', 'skills', 'video-ia-prompteo', 'SKILL.md'), encoding='utf8').read()
            print('\n--- Revisión ---\n' + texto(
                'Eres director de fotografía y revisas un prompt para Gemini Omni Flash antes de pagarlo. '
                'Compáralo con la guía y con la ficha. Enumera SOLO problemas concretos que arruinarían la toma '
                '(ambigüedad, contradicciones, cosas imposibles en el tiempo dado, datos que contradicen la ficha, '
                'riesgos de que el modelo meta texto, gente o cortes no pedidos) y la corrección exacta. '
                'Si no hay problemas, responde "SIN PROBLEMAS".\n\nGUÍA:\n' + guia +
                '\n\nFICHA:\n' + json.dumps(f, ensure_ascii=False, indent=1) + '\n\nPROMPT:\n' + prompt))
        return
    if not args.salida:
        sys.exit('Falta --salida.')
    autorizar(args, modelo, usd)
    global PAGADO
    PAGADO = True
    entrada = prompt
    imagen = args.imagen or f.get('imagen')
    if imagen:
        mime = 'image/png' if imagen.lower().endswith('.png') else 'image/jpeg'
        entrada = [{'type': 'image', 'data': base64.b64encode(open(imagen, 'rb').read()).decode(), 'mime_type': mime},
                   {'type': 'text', 'text': prompt}]
    # delivery 'uri' exige store=true (error 400 del 2026-11-06).
    r = interaccion(modelo, entrada, {'type': 'video', 'aspect_ratio': f.get('aspecto', '9:16'),
                                      'resolution': f.get('resolucion', '720p'), 'duration': f'{int(round(dur))}s',
                                      'delivery': 'uri'}, {'store': True})
    os.makedirs(os.path.dirname(os.path.abspath(args.salida)), exist_ok=True)
    open(args.salida, 'wb').write(binario(r, 'video'))
    open(os.path.splitext(args.salida)[0] + '.prompt.txt', 'w', encoding='utf8').write(prompt + '\n')
    anotar('video', modelo, usd, args.salida, f'ficha {args.ficha}')
    print(args.salida)
    print(tira(args.salida))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('estado')
    t = sub.add_parser('texto'); t.add_argument('prompt'); t.add_argument('--modelo'); t.add_argument('--sistema')
    y = sub.add_parser('youtube'); y.add_argument('video'); y.add_argument('--prompt'); y.add_argument('--archivo')
    y.add_argument('--salida'); y.add_argument('--modelo')
    v = sub.add_parser('voz'); v.add_argument('--texto', required=True); v.add_argument('--salida', required=True)
    v.add_argument('--voz', default='Charon'); v.add_argument('--estilo'); v.add_argument('--modelo')
    d = sub.add_parser('dialogo'); d.add_argument('guion'); d.add_argument('--salida', required=True); d.add_argument('--modelo')
    i = sub.add_parser('imagen'); i.add_argument('--prompt', required=True); i.add_argument('--salida', required=True)
    i.add_argument('--aspecto', default='4:3'); i.add_argument('--tamano', default='1K'); i.add_argument('--modelo')
    i.add_argument('--pago', action='store_true')
    vi = sub.add_parser('video'); vi.add_argument('--ficha'); vi.add_argument('--salida'); vi.add_argument('--imagen')
    vi.add_argument('--modelo'); vi.add_argument('--pago', action='store_true')
    vi.add_argument('--ensayo', action='store_true'); vi.add_argument('--revisar', action='store_true')
    a = p.parse_args()
    try:
        globals()[f'cmd_{a.cmd}'](a)
    except Ocupado as e:
        sys.exit(f'{e}. Reintentar más tarde.')


if __name__ == '__main__':
    main()
