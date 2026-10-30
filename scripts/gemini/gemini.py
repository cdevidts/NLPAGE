"""Gemini API (Google AI Studio) desde el contenedor o un turno programado.

Clave: variable de entorno GEMINI_API_KEY (Cris la crea en https://aistudio.google.com/apikey
y la deja en la configuración del entorno). Nunca se escribe en archivos ni commits.

Gratis (free tier de la API):
    python3 -I scripts/gemini/gemini.py estado
    python3 -I scripts/gemini/gemini.py texto "pregunta"            # o "-" para leer de stdin
    python3 -I scripts/gemini/gemini.py voz --texto "..." --salida x.wav [--voz Charon] [--estilo "..."]
    python3 -I scripts/gemini/gemini.py dialogo guion.json --salida x.wav   # 2 voces, tipo podcast

Pagado (imagen, video): solo con --pago y si el tope del mes en docs/gemini/config.json alcanza.
El tope parte en 0: se sube cuando Cris activa los créditos de Google AI Pro y da el OK.
    python3 -I scripts/gemini/gemini.py imagen --prompt "..." --salida x.jpg [--aspecto 4:3] --pago
    python3 -I scripts/gemini/gemini.py video --prompt "..." --salida x.mp4 [--aspecto 9:16] [--imagen ref.jpg] --pago

Cada llamada pagada queda en docs/gemini/gasto.csv con su costo estimado.
"""
import argparse, base64, csv, datetime, json, os, ssl, sys, time, urllib.error, urllib.request, wave

API = os.environ.get('GEMINI_API_BASE', 'https://generativelanguage.googleapis.com/v1beta')
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG = os.path.join(RAIZ, 'docs', 'gemini', 'config.json')
GASTO = os.path.join(RAIZ, 'docs', 'gemini', 'gasto.csv')

# Precios estimados (ai.google.dev/gemini-api/docs/pricing, leído 2026-10-30). Solo para el tope.
PRECIO = {
    'gemini-3.1-flash-lite-image': 0.034,  # por imagen 1K
    'gemini-nano-banana-2.1': 0.050,       # por imagen 2K
    'gemini-3.1-flash-image': 0.067,       # por imagen 1K
    'gemini-3-pro-image': 0.134,
    'gemini-omni-1.1-flash': 0.10,         # por segundo de video 720p
}
SEG_VIDEO = 10  # la doc no fija la duración; se cobra el peor caso al tope


def config():
    c = {'texto': 'gemini-3.8-flash', 'voz': 'gemini-3.8-flash-tts', 'imagen': 'gemini-3.1-flash-lite-image',
         'video': 'gemini-omni-1.1-flash', 'tope_mes_usd': 0}
    if os.path.exists(CONFIG):
        c.update(json.load(open(CONFIG, encoding='utf8')))
    return c


def clave():
    k = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if not k:
        sys.exit('Falta GEMINI_API_KEY en el entorno. Cris la crea en https://aistudio.google.com/apikey '
                 'y la agrega en la configuración del entorno (ver docs/gemini/README.md).')
    return k


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
        raise SystemExit(f'Gemini {e.code} en {ruta}: {msg}')


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
    return llamar('POST', 'interactions', cuerpo)


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
    for uso in ('texto', 'voz', 'imagen', 'video'):
        print(f'  {uso:6} {c[uso]:32} {"disponible" if c[uso] in modelos else "NO aparece en la lista"}')
    r = interaccion(c['texto'], 'Responde solo: ok')
    print('  prueba de texto:', ''.join(b.get('text', '') for b in bloques(r)).strip()[:40])
    print(f'Gasto pagado este mes: US${gastado_mes():.2f} de un tope de US${float(c["tope_mes_usd"]):.2f}')


def cmd_texto(args):
    prompt = sys.stdin.read() if args.prompt == '-' else args.prompt
    if args.sistema:
        prompt = f'{args.sistema}\n\n{prompt}'
    r = interaccion(args.modelo or config()['texto'], prompt)
    print(''.join(b.get('text', '') for b in bloques(r) if b.get('type') == 'text').strip())


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


def cmd_video(args):
    modelo = args.modelo or config()['video']
    usd = PRECIO.get(modelo, 0.5) * SEG_VIDEO
    autorizar(args, modelo, usd)
    entrada = args.prompt
    if args.imagen:
        mime = 'image/png' if args.imagen.lower().endswith('.png') else 'image/jpeg'
        entrada = [{'type': 'image', 'data': base64.b64encode(open(args.imagen, 'rb').read()).decode(), 'mime_type': mime},
                   {'type': 'text', 'text': args.prompt}]
    r = interaccion(modelo, entrada, {'type': 'video', 'aspect_ratio': args.aspecto, 'resolution': args.resolucion,
                                      'delivery': 'uri'})
    os.makedirs(os.path.dirname(os.path.abspath(args.salida)), exist_ok=True)
    open(args.salida, 'wb').write(binario(r, 'video'))
    anotar('video', modelo, usd, args.salida, args.prompt)
    print(args.salida)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('estado')
    t = sub.add_parser('texto'); t.add_argument('prompt'); t.add_argument('--modelo'); t.add_argument('--sistema')
    v = sub.add_parser('voz'); v.add_argument('--texto', required=True); v.add_argument('--salida', required=True)
    v.add_argument('--voz', default='Charon'); v.add_argument('--estilo'); v.add_argument('--modelo')
    d = sub.add_parser('dialogo'); d.add_argument('guion'); d.add_argument('--salida', required=True); d.add_argument('--modelo')
    i = sub.add_parser('imagen'); i.add_argument('--prompt', required=True); i.add_argument('--salida', required=True)
    i.add_argument('--aspecto', default='4:3'); i.add_argument('--tamano', default='1K'); i.add_argument('--modelo')
    i.add_argument('--pago', action='store_true')
    vi = sub.add_parser('video'); vi.add_argument('--prompt', required=True); vi.add_argument('--salida', required=True)
    vi.add_argument('--aspecto', default='9:16'); vi.add_argument('--resolucion', default='720p'); vi.add_argument('--imagen')
    vi.add_argument('--modelo'); vi.add_argument('--pago', action='store_true')
    a = p.parse_args()
    globals()[f'cmd_{a.cmd}'](a)


if __name__ == '__main__':
    main()
