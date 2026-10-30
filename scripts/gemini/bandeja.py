#!/usr/bin/env python3
"""Bandeja de tareas para Gemini (canal Claude <-> Gemini a través del repo y de Drive).

Protocolo completo en gemini/README.md. Resumen:
  Claude escribe una tarea en gemini/inbox/G-NNN-<slug>.md y regenera gemini/PENDIENTES.md.
  Gemini (tarea programada de la app, cuenta AI Pro de Cris) lee PENDIENTES.md (URL pública
  del repo o su espejo en Drive), hace la tarea y deja un Google Doc "G-NNN RESPUESTA" en
  Drive > Side Husle Claude > Gemini > Respuestas (archivos grandes en Entregas).
  Claude recoge la respuesta con el conector de Drive y la guarda aquí con `recibir`.

Uso:
  python3 -I scripts/gemini/bandeja.py pedir --titulo "..." --hilo "..." --herramienta deep-research \
      --entrega doc [--vence 2026-11-05] [--prioridad alta] (--archivo cuerpo.md | --texto "..." | -)
  python3 -I scripts/gemini/bandeja.py pendientes [--md]      # lista; --md imprime PENDIENTES.md (espejo de Drive)
  python3 -I scripts/gemini/bandeja.py recibir G-001 (--archivo respuesta.txt | -) [--doc URL] [--estado hecho|parcial|no-puedo]
  python3 -I scripts/gemini/bandeja.py cerrar G-001 --motivo "..."   # cancelar sin respuesta
  python3 -I scripts/gemini/bandeja.py mostrar G-001
  python3 -I scripts/gemini/bandeja.py estado                 # resumen y qué buscar en Drive
"""
import argparse, csv, datetime, os, re, shutil, sys, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(RAIZ, 'gemini')
INBOX, OUTBOX, DONE = (os.path.join(DIR, d) for d in ('inbox', 'outbox', 'done'))
REGISTRO = os.path.join(DIR, 'registro.csv')
PENDIENTES = os.path.join(DIR, 'PENDIENTES.md')
URL_PENDIENTES = 'https://raw.githubusercontent.com/cdevidts/NLPAGE/main/gemini/PENDIENTES.md'
DRIVE_RESPUESTAS = '1WqcooCtde-MUKygT4aLB5Uhdk7Vf3-ax'   # Drive > Side Husle Claude > Gemini > Respuestas
DRIVE_ENTREGAS = '1GyhIPtv-6WICQJoRhmdzzAnVZt5V1Xh1'     # Drive > Side Husle Claude > Gemini > Entregas
DRIVE_GEMINI = '1-mAs2etmZt8fH7-YIlH9aEDJRfbBB73-'       # Drive > Side Husle Claude > Gemini
HERRAMIENTAS = ['texto', 'deep-research', 'navegar', 'nano-banana', 'veo', 'notebooklm', 'canvas', 'sheets']
ENTREGAS = ['doc', 'pdf', 'sheet', 'imagen', 'video', 'audio', 'slides']
ESTADOS_RESP = ['hecho', 'parcial', 'no-puedo']
COLS = ['id', 'pedido', 'hilo', 'herramienta', 'entrega', 'titulo', 'estado', 'respondido', 'doc', 'modelo']
MAX_KB = 24   # una tarea no debería pasar de esto: Gemini la lee entera en PENDIENTES.md


def hoy():
    return datetime.date.today().isoformat()


def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    t = re.sub(r'[^a-zA-Z0-9]+', '-', t).strip('-').lower()
    return t[:40].rstrip('-') or 'tarea'


def leer_registro():
    if not os.path.exists(REGISTRO):
        return []
    with open(REGISTRO, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def escribir_registro(filas):
    os.makedirs(DIR, exist_ok=True)
    with open(REGISTRO, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in filas:
            w.writerow({c: r.get(c, '') for c in COLS})


def siguiente_id(filas):
    n = max([int(r['id'].split('-')[1]) for r in filas if re.match(r'G-\d+$', r['id'])] + [0])
    return f'G-{n + 1:03d}'


def frontmatter(texto):
    """Devuelve (dict, cuerpo) de un archivo con bloque --- al inicio."""
    m = re.match(r'^---\n(.*?)\n---\n?(.*)$', texto, re.S)
    if not m:
        return {}, texto
    meta = {}
    for linea in m.group(1).splitlines():
        if ':' in linea:
            k, v = linea.split(':', 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def archivo_de(id_, carpeta):
    if not os.path.isdir(carpeta):
        return None
    for n in sorted(os.listdir(carpeta)):
        if n.startswith(id_ + '-') or n == id_ + '.md':
            return os.path.join(carpeta, n)
    return None


def leer_texto(args):
    if getattr(args, 'archivo', None):
        with open(args.archivo, encoding='utf-8') as f:
            return f.read()
    if getattr(args, 'texto', None) and args.texto != '-':
        return args.texto
    return sys.stdin.read()


def regenerar_pendientes():
    filas = leer_registro()
    abiertas = [r for r in filas if r['estado'] == 'pendiente']
    cerradas = [r['id'] for r in filas if r['estado'] != 'pendiente']
    partes = [
        '# Tareas pendientes para Gemini',
        '',
        f'Generado por `scripts/gemini/bandeja.py` el {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}. '
        'Este archivo es la ÚNICA lista que Gemini tiene que leer. Cada tarea está completa aquí abajo.',
        '',
        '## Quién te habla',
        'Estas tareas las escribe Claude, el agente que opera la tienda SheetSmithChile. Tú y Claude son colegas: respóndele a Claude, no al dueño de la cuenta. '
        'Escribe como a un colega técnico: directo, con datos, sin resúmenes para humanos ni avisos de "se completó la tarea". Si ves una forma mejor de hacer algo, dilo en una sección final `## Sugerencias para Claude`.',
        '',
        '## Cómo entregar (resumen del protocolo, detalle en gemini/README.md)',
        '1. Usa el modelo más capaz que tengas (Gemini 4 Argon, Pro o Deep Think; nunca Flash o Lite para investigar). Haz cada tarea de la lista, en orden. Si una tarea no se puede hacer con tus herramientas, igual entrégala con `estado: no-puedo` y el motivo exacto (nombre de la herramienta que falta, mensaje de error).',
        '2. Por cada tarea crea UN Google Doc en Drive > Side Husle Claude > Gemini > Respuestas, titulado exactamente `<ID> RESPUESTA` (por ejemplo `G-001 RESPUESTA`).',
        '3. Primera línea del Doc: `estado: hecho` | `estado: parcial` | `estado: no-puedo`. Segunda: `fecha: <AAAA-MM-DD HH:MM>`. Tercera: `modelo: <nombre y versión exactos del modelo que respondió>`. Después, la respuesta en el formato que pide la tarea, con fuentes (URL) cuando investigues y marcando `(sin verificar)` lo que no comprobaste.',
        '4. Archivos que no sean texto (PDF, MP4, PNG, MP3, Sheets) van a la carpeta Entregas con el nombre `<ID> <nombre>`; en el Doc pon el nombre y el link de cada archivo.',
        '5. No repitas una tarea que ya tiene su Doc `<ID> RESPUESTA` en Respuestas ni una de la lista "Ya respondidas". Si la lista de abajo está vacía, no hagas nada.',
        '6. Nunca incluyas contraseñas, claves ni datos de compradores. Responde en el idioma en que está escrita la tarea.',
        '',
        f'Ya respondidas o cerradas (no repetir): {", ".join(cerradas) if cerradas else "ninguna"}',
        '',
        f'## Tareas abiertas: {len(abiertas)}',
        '',
    ]
    for r in abiertas:
        ruta = archivo_de(r['id'], INBOX)
        cuerpo = ''
        if ruta:
            meta, cuerpo = frontmatter(open(ruta, encoding='utf-8').read())
        partes += [
            f'---',
            f'### {r["id"]} · {r["titulo"]}',
            f'- Pedida: {r["pedido"]} · Herramienta sugerida: {r["herramienta"]} · Entrega: {r["entrega"]}'
            + (f' · Vence: {meta.get("vence")}' if ruta and meta.get('vence') else '')
            + (f' · Prioridad: {meta.get("prioridad")}' if ruta and meta.get('prioridad') else ''),
            f'- Entregar como: Google Doc `{r["id"]} RESPUESTA` en Respuestas'
            + ('' if r['entrega'] == 'doc' else f' + archivo `{r["id"]} ...` en Entregas'),
            '',
            cuerpo.strip(),
            '',
        ]
    if not abiertas:
        partes.append('(No hay tareas abiertas. Gemini no tiene que hacer nada.)')
    with open(PENDIENTES, 'w', encoding='utf-8') as f:
        f.write('\n'.join(partes).rstrip() + '\n')
    return len(abiertas)


def cmd_pedir(args):
    filas = leer_registro()
    id_ = siguiente_id(filas)
    cuerpo = leer_texto(args).strip()
    if not cuerpo:
        sys.exit('ERROR: la tarea no tiene texto (usa --archivo, --texto o stdin)')
    if len(cuerpo.encode()) > MAX_KB * 1024:
        sys.exit(f'ERROR: la tarea pesa más de {MAX_KB} KB; resúmela o divídela')
    os.makedirs(INBOX, exist_ok=True)
    ruta = os.path.join(INBOX, f'{id_}-{slug(args.titulo)}.md')
    meta = [f'id: {id_}', f'titulo: {args.titulo}', f'pedido: {hoy()}', f'hilo: {args.hilo}',
            f'herramienta: {args.herramienta}', f'entrega: {args.entrega}', 'estado: pendiente']
    if args.vence:
        meta.append(f'vence: {args.vence}')
    if args.prioridad:
        meta.append(f'prioridad: {args.prioridad}')
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('---\n' + '\n'.join(meta) + '\n---\n' + cuerpo + '\n')
    filas.append({'id': id_, 'pedido': hoy(), 'hilo': args.hilo, 'herramienta': args.herramienta,
                  'entrega': args.entrega, 'titulo': args.titulo, 'estado': 'pendiente', 'respondido': '', 'doc': ''})
    escribir_registro(filas)
    n = regenerar_pendientes()
    print(f'{id_} creada: {os.path.relpath(ruta, RAIZ)}  ({n} abiertas)')
    print('Siguiente: commit + push a main (Gemini lee main), y actualiza el espejo en Drive:')
    print(f'  python3 -I scripts/gemini/bandeja.py pendientes --md   -> Drive create_file (Doc "GEMINI-PENDIENTES", parentId {DRIVE_GEMINI}); mueve a la papelera el Doc anterior del mismo nombre.')


def cmd_pendientes(args):
    if args.md:
        regenerar_pendientes()
        print(open(PENDIENTES, encoding='utf-8').read())
        return
    filas = [r for r in leer_registro() if r['estado'] == 'pendiente']
    if not filas:
        print('Sin tareas pendientes.')
        return
    for r in filas:
        dias = (datetime.date.today() - datetime.date.fromisoformat(r['pedido'])).days
        print(f'{r["id"]}  {r["pedido"]} ({dias} d)  {r["herramienta"]:<13} {r["titulo"]}  [{r["hilo"]}]')


def cmd_recibir(args):
    filas = leer_registro()
    fila = next((r for r in filas if r['id'] == args.id), None)
    if not fila:
        sys.exit(f'ERROR: {args.id} no está en registro.csv')
    if fila['estado'] != 'pendiente':
        sys.exit(f'ERROR: {args.id} ya está {fila["estado"]}')
    texto = leer_texto(args).strip()
    if not texto:
        sys.exit('ERROR: respuesta vacía')
    estado = args.estado
    m = re.match(r'^\s*estado\s*:\s*(hecho|parcial|no-puedo)', texto, re.I)
    if not estado:
        estado = m.group(1).lower() if m else 'hecho'
    mm = re.search(r'^\s*modelo\s*:\s*(.+)$', texto, re.I | re.M)
    modelo = args.modelo or (mm.group(1).strip() if mm else '')
    if not modelo:
        print('AVISO: la respuesta no dice qué modelo la escribió; pide `modelo:` en la línea 3 (regla de Cris: siempre un modelo fuerte).')
    os.makedirs(OUTBOX, exist_ok=True); os.makedirs(DONE, exist_ok=True)
    salida = os.path.join(OUTBOX, f'{args.id}.md')
    meta = [f'id: {args.id}', f'titulo: {fila["titulo"]}', f'pedido: {fila["pedido"]}', f'recibido: {hoy()}',
            f'estado: {estado}', f'hilo: {fila["hilo"]}']
    if args.doc:
        meta.append(f'doc: {args.doc}')
    if modelo:
        meta.append(f'modelo: {modelo}')
    with open(salida, 'w', encoding='utf-8') as f:
        f.write('---\n' + '\n'.join(meta) + '\n---\n' + texto + '\n')
    origen = archivo_de(args.id, INBOX)
    if origen:
        shutil.move(origen, os.path.join(DONE, os.path.basename(origen)))
    fila.update({'estado': estado, 'respondido': hoy(), 'doc': args.doc or '', 'modelo': modelo})
    escribir_registro(filas)
    n = regenerar_pendientes()
    print(f'{args.id} recibida ({estado}): {os.path.relpath(salida, RAIZ)}; tarea movida a gemini/done/. {n} abiertas.')
    print('Siguiente: usa la respuesta en tu trabajo, commit + push, y actualiza el espejo GEMINI-PENDIENTES en Drive.')


def cmd_cerrar(args):
    filas = leer_registro()
    fila = next((r for r in filas if r['id'] == args.id), None)
    if not fila or fila['estado'] != 'pendiente':
        sys.exit(f'ERROR: {args.id} no está pendiente')
    origen = archivo_de(args.id, INBOX)
    if origen:
        os.makedirs(DONE, exist_ok=True)
        with open(origen, 'a', encoding='utf-8') as f:
            f.write(f'\n\n> Cerrada sin respuesta el {hoy()}: {args.motivo}\n')
        shutil.move(origen, os.path.join(DONE, os.path.basename(origen)))
    fila.update({'estado': 'cancelada', 'respondido': hoy()})
    escribir_registro(filas)
    regenerar_pendientes()
    print(f'{args.id} cancelada.')


def cmd_mostrar(args):
    for carpeta in (INBOX, DONE):
        r = archivo_de(args.id, carpeta)
        if r:
            print(f'## Tarea ({os.path.relpath(r, RAIZ)})\n' + open(r, encoding='utf-8').read())
    r = os.path.join(OUTBOX, f'{args.id}.md')
    if os.path.exists(r):
        print(f'## Respuesta ({os.path.relpath(r, RAIZ)})\n' + open(r, encoding='utf-8').read())


def cmd_estado(args):
    filas = leer_registro()
    pend = [r for r in filas if r['estado'] == 'pendiente']
    print(f'Tareas: {len(filas)} en total, {len(pend)} pendientes, '
          f'{sum(r["estado"] == "hecho" for r in filas)} hechas, {sum(r["estado"] == "parcial" for r in filas)} parciales, '
          f'{sum(r["estado"] == "no-puedo" for r in filas)} no-puedo, {sum(r["estado"] == "cancelada" for r in filas)} canceladas.')
    for r in pend:
        dias = (datetime.date.today() - datetime.date.fromisoformat(r['pedido'])).days
        aviso = '  <- lleva más de 2 días: ¿corrió la tarea programada de Gemini?' if dias > 2 else ''
        print(f'  {r["id"]} pendiente desde {r["pedido"]} ({dias} d): {r["titulo"]}{aviso}')
    if len(pend) < 3:
        print('  AVISO: menos de 3 tareas en cola. Gemini corre cada hora: deja siempre trabajo útil (skill gemini-canal, "Cola permanente").')
    if pend:
        ids = ' or '.join(f"title contains '{r['id']}'" for r in pend)
        print('\nPara recoger respuestas, con el conector de Google Drive:')
        print(f"  search_files: parentId = '{DRIVE_RESPUESTAS}' and ({ids})")
        print('  read_file_content de cada Doc encontrado -> guardar el texto en un archivo -> `bandeja.py recibir <ID> --archivo <txt> --doc <viewUrl>`')
        print(f"  Archivos adjuntos: search_files parentId = '{DRIVE_ENTREGAS}'")
    print(f'\nPENDIENTES.md público: {URL_PENDIENTES}')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('pedir'); a.add_argument('--titulo', required=True); a.add_argument('--hilo', required=True)
    a.add_argument('--herramienta', choices=HERRAMIENTAS, default='texto'); a.add_argument('--entrega', choices=ENTREGAS, default='doc')
    a.add_argument('--vence'); a.add_argument('--prioridad', choices=['alta', 'normal', 'baja'])
    a.add_argument('--archivo'); a.add_argument('--texto'); a.set_defaults(f=cmd_pedir)
    a = sub.add_parser('pendientes'); a.add_argument('--md', action='store_true'); a.set_defaults(f=cmd_pendientes)
    a = sub.add_parser('recibir'); a.add_argument('id'); a.add_argument('--archivo'); a.add_argument('--texto')
    a.add_argument('--doc'); a.add_argument('--estado', choices=ESTADOS_RESP); a.add_argument('--modelo'); a.set_defaults(f=cmd_recibir)
    a = sub.add_parser('cerrar'); a.add_argument('id'); a.add_argument('--motivo', required=True); a.set_defaults(f=cmd_cerrar)
    a = sub.add_parser('mostrar'); a.add_argument('id'); a.set_defaults(f=cmd_mostrar)
    a = sub.add_parser('estado'); a.set_defaults(f=cmd_estado)
    args = p.parse_args()
    args.f(args)


if __name__ == '__main__':
    main()
