#!/usr/bin/env python3
"""Loop viral de Shorts: revisa el experimento de un plan, registra lo publicado,
dice qué lecturas vencen y guarda las métricas de Metricool. Skill: shorts-viral-loop.

  experimento.py check      --plan plans/<slug>.json
  experimento.py alta       --plan plans/<slug>.json --post <id Metricool> --fecha AAAA-MM-DD [--hora 16:00]
  experimento.py pendientes [--hoy AAAA-MM-DD]
  experimento.py medir      --metricool respuesta.json [--hoy AAAA-MM-DD]
  experimento.py resumen

Las métricas las trae el conector Metricool (no hay API desde Python): `pendientes`
imprime la llamada exacta, se guarda su respuesta JSON y `medir` la cruza con el registro.
"""
import argparse, csv, datetime as dt, json, re, statistics, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CSV = RAIZ / "docs/viral/shorts.csv"
BITACORA = RAIZ / "docs/viral/BITACORA.md"
ETSY = Path("/mnt/project-files/plan/metricas/serie/etsy.csv")
BRAND = "6078519"
# Orden fijo: `medir` lee las filas de Metricool en este orden.
METRICAS = ["YTVP01", "YTVP04", "YTVP06", "YTVP08", "YTVP09", "YTVP11", "YTVP12", "YTVP17"]
VARIABLES = {"formato", "gancho", "duracion", "final", "titulo", "serie", "idioma", "cta", "voz", "musica", "hora", "tema"}
FORMATOS = {"historia", "reto", "tutorial", "pov", "confesion", "lista", "antes-despues"}
GANCHOS = {"pregunta", "dato-imposible", "in-medias-res", "contradiccion", "reto", "confesion", "pov",
           "superlativo", "injusticia", "fecha-edad-nombre"}
CAMPOS = ["slug", "producto", "idioma", "fecha", "hora", "metricool_post", "video_id", "listing_id",
          "hipotesis", "variable", "variante", "control", "formato", "gancho_tipo", "duracion_s", "titulo",
          "v48", "ret48", "likes48", "com48", "shares48",
          "v7", "ret7", "likes7", "com7", "shares7", "etsy_antes", "etsy_despues", "veredicto"]
TIENDA = re.compile(r"\b(etsy|sheetsmith\w*|link|shop|store|buy|download|tienda|compra\w*|descarga\w*|enlace)\b", re.I)
FICCION = re.compile(r"fiction|fictional|ficci[oó]n|ficticio|made[- ]up|invented|inventado", re.I)


def leer():
    if not CSV.exists():
        return []
    with CSV.open(newline="") as f:
        return list(csv.DictReader(f))


def guardar(filas):
    with CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for r in filas:
            w.writerow({k: r.get(k, "") for k in CAMPOS})


def hipotesis_abiertas():
    return set(re.findall(r"^### (V\d+)\.", BITACORA.read_text(), re.M)) if BITACORA.exists() else set()


def check(plan_path):
    p = json.loads(Path(plan_path).read_text())
    err, avi = [], []
    ex = p.get("experimento")
    if not ex:
        err.append('falta el bloque "experimento" (ver la skill shorts-viral-loop)')
        ex = {}
    else:
        if ex.get("hipotesis") not in hipotesis_abiertas():
            err.append(f'experimento.hipotesis "{ex.get("hipotesis")}" no está en docs/viral/BITACORA.md')
        if ex.get("variable") not in VARIABLES:
            err.append(f"experimento.variable debe ser una de {sorted(VARIABLES)}")
        if ex.get("formato") not in FORMATOS:
            err.append(f"experimento.formato debe ser uno de {sorted(FORMATOS)}")
        if ex.get("gancho_tipo") not in GANCHOS:
            err.append(f"experimento.gancho_tipo debe ser uno de {sorted(GANCHOS)}")
        for k in ("variante", "control", "espera"):
            if not ex.get(k):
                err.append(f"experimento.{k} vacío: escribe antes qué esperas ver")
    esc = p.get("escenas", [])
    if esc:
        n1 = len(esc[0].get("dice", "").split())
        if n1 > 12:
            err.append(f"gancho de {n1} palabras: máximo 12 (se tiene que oír en 1-2 s)")
        if TIENDA.search(esc[0].get("dice", "") + " " + esc[0].get("texto", "")):
            err.append("la primera escena nombra la tienda o el link: eso es un anuncio")
        corte = max(1, int(len(esc) * 0.7))
        for i, e in enumerate(esc[:corte]):
            if TIENDA.search(e.get("dice", "")):
                err.append(f"escena {i + 1} habla de tienda/compra antes del final (regla de Cris: CTA solo al cierre)")
    cierre = (p.get("cierre") or {}).get("dice", "")
    if not re.search(r"etsy|sheetsmith", cierre, re.I):
        avi.append("el cierre no dice dónde se consigue (p. ej. 'busca SheetSmithChile en Etsy')")
    if re.search(r"link in the description|link en la descripci", cierre, re.I):
        avi.append("en Shorts el link de la descripción no es clicable: mejor 'busca SheetSmithChile en Etsy'")
    if p.get("tema") == "coldcase" or str(p.get("producto", "")).startswith(("56", "57", "58", "59")):
        todo = cierre + " " + " ".join(e.get("dice", "") for e in esc[-2:])
        if not FICCION.search(todo):
            err.append("cold case sin aviso de ficción al final: nunca presentar el caso como real")
    tit = (p.get("youtube") or {}).get("titulo", "")
    if re.search(r"flip-?through|walkthrough|template|printable", tit, re.I):
        avi.append(f'título con lenguaje de anuncio ("{tit}"): el título es gancho con la frase de búsqueda dentro')
    for a in avi:
        print(f"⚠️  {a}")
    for e in err:
        print(f"❌ {e}")
    if err:
        sys.exit(1)
    print(f"✓ experimento {ex.get('hipotesis')}: {ex.get('variable')} = {ex.get('variante')}")


def duracion(slug):
    mp4 = RAIZ / "renders" / f"{slug}.mp4"
    if not mp4.exists():
        return ""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                       capture_output=True, text=True)
    return f"{float(r.stdout.strip()):.1f}" if r.stdout.strip() else ""


def alta(plan_path, post, fecha, hora):
    p = json.loads(Path(plan_path).read_text())
    ex = p.get("experimento") or {}
    filas = [r for r in leer() if r["slug"] != p["slug"]]
    filas.append({
        "slug": p["slug"], "producto": p.get("producto", ""), "idioma": p.get("idioma", ""),
        "fecha": fecha, "hora": hora, "metricool_post": post, "listing_id": ex.get("listing_id", ""),
        "hipotesis": ex.get("hipotesis", ""), "variable": ex.get("variable", ""), "variante": ex.get("variante", ""),
        "control": ex.get("control", ""), "formato": ex.get("formato", ""), "gancho_tipo": ex.get("gancho_tipo", ""),
        "duracion_s": duracion(p["slug"]), "titulo": (p.get("youtube") or {}).get("titulo", ""),
    })
    filas.sort(key=lambda r: (r["fecha"], r["hora"]))
    guardar(filas)
    print(f"✓ {p['slug']} registrado para {fecha} {hora} (lecturas {d(fecha, 2)} y {d(fecha, 7)})")


def d(fecha, dias):
    return (dt.date.fromisoformat(fecha) + dt.timedelta(days=dias)).isoformat()


def vencidas(filas, hoy):
    out = []
    for r in filas:
        if not r["fecha"]:
            continue
        if not r["v48"] and d(r["fecha"], 2) <= hoy:
            out.append((r, "48h"))
        if not r["v7"] and d(r["fecha"], 7) <= hoy:
            out.append((r, "7d"))
    return out


def pendientes(hoy):
    filas = leer()
    v = vencidas(filas, hoy)
    if not v:
        prox = sorted({d(r["fecha"], 2) for r in filas if not r["v48"]} | {d(r["fecha"], 7) for r in filas if not r["v7"]})
        print(f"Nada vence hoy ({hoy}). Próxima lectura: {prox[0] if prox else '-'}")
        return
    for r, k in v:
        print(f"- {r['slug']} ({r['fecha']}): lectura {k}")
    desde = min(r["fecha"] for r, _ in v)
    print("\nPide a Metricool (getAnalyticsDataByMetrics) y guarda la respuesta JSON:")
    print(json.dumps({"brandId": BRAND, "from": f"{desde}T00:00:00-03:00", "to": f"{hoy}T23:59:59-03:00",
                      "metrics": METRICAS}))
    print("Luego: python3 scripts/viral/experimento.py medir --metricool <archivo>")


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def etsy_vistas(listing, desde, hasta):
    """Vistas que sumó el listing entre dos fechas según la serie diaria de operación."""
    if not listing or not ETSY.exists():
        return ""
    puntos = []
    with ETSY.open(newline="") as f:
        for r in csv.DictReader(f):
            if r["listing_id"] == str(listing):
                puntos.append((r["fecha"][:10], int(float(r["vistas"] or 0))))
    antes = [v for f, v in puntos if f <= desde]
    despues = [v for f, v in puntos if f <= hasta]
    if not antes or not despues:
        return ""
    return str(despues[-1] - antes[-1])


def medir(archivo, hoy):
    data = json.loads(Path(archivo).read_text())
    rows = data.get("rows", data) if isinstance(data, dict) else data
    filas = leer()
    por_id = {r["video_id"]: r for r in filas if r["video_id"]}
    por_titulo = {r["titulo"].strip().lower(): r for r in filas}
    lecturas = []
    sin_datos = False
    for row in rows:
        m = dict(zip(METRICAS, row))
        vid, tit = str(m.get("YTVP04") or ""), str(m.get("YTVP17") or "").strip().lower()
        r = por_id.get(vid) or por_titulo.get(tit)
        if not r:
            continue
        r["video_id"] = r["video_id"] or vid
        if m.get("YTVP06") is None:
            # Metricool tarda ~1 día en traer números: null no es cero. Se reintenta mañana.
            print(f"{r['slug']}: Metricool aún sin métricas (null); queda pendiente")
            sin_datos = True
            continue
        dur = num(r["duracion_s"]) or 1
        vistas = num(m.get("YTVP06"))
        base = {"v": int(vistas), "ret": f"{num(m.get('YTVP08')) / dur * 100:.0f}", "likes": int(num(m.get("YTVP09"))),
                "com": int(num(m.get("YTVP11"))), "shares": int(num(m.get("YTVP12")))}
        if not r["v48"] and d(r["fecha"], 7) <= hoy:
            r["v48"] = "-"  # se pasó la lectura de 48 h: un número de 7 días ahí engañaría
        for k, sufijo in (("48h", "48"), ("7d", "7")):
            dias = 2 if sufijo == "48" else 7
            if not r[f"v{sufijo}"] and d(r["fecha"], dias) <= hoy:
                for c, val in base.items():
                    r[f"{c}{sufijo}"] = str(val)
                if sufijo == "7":
                    r["etsy_antes"] = etsy_vistas(r["listing_id"], d(r["fecha"], -3), r["fecha"])
                    r["etsy_despues"] = etsy_vistas(r["listing_id"], r["fecha"], d(r["fecha"], 3))
                    r["veredicto"] = veredicto(r, filas)
                lecturas.append((r, k, base))
    guardar(filas)
    if not lecturas and sin_datos:
        guardar(filas)
        print("✓ video_id anotado; las lecturas quedan para cuando Metricool traiga números.")
        return
    if not lecturas:
        print("Ninguna lectura vencida coincidió con las filas de Metricool (¿el título cambió? pon video_id a mano).")
        return
    lineas = []
    for r, k, b in lecturas:
        por_mil = lambda x: f"{x / b['v'] * 1000:.1f}" if b["v"] else "-"
        ver = r["veredicto"] if k == "7d" else ""
        lineas.append(f"| {hoy} | {r['slug']} | {k} | {b['v']} | {b['ret']} % | {por_mil(b['com'])} | "
                      f"{por_mil(b['shares'])} | {ver} | {r['hipotesis']} {r['variable']}={r['variante']} |")
        print(f"{r['slug']} {k}: {b['v']} vistas, retención {b['ret']} %, veredicto {ver or '(48 h, solo se anota)'}")
    texto = BITACORA.read_text().rstrip("\n") + "\n" + "\n".join(lineas) + "\n"
    BITACORA.write_text(texto)
    print("✓ shorts.csv y BITACORA.md al día. Escribe la conclusión en la hipótesis.")


def veredicto(r, filas):
    previos = [num(x["v7"]) for x in filas if x["v7"] and x["fecha"] < r["fecha"]][-10:]
    if len(previos) < 5:
        return "LINEA-BASE"
    med = statistics.median(previos) or 1
    rets = [num(x["ret7"]) for x in filas if x["ret7"] and x["fecha"] < r["fecha"]][-10:]
    v = num(r["v7"])
    if v >= 1.5 * med and num(r["ret7"]) >= statistics.median(rets):
        return "GANA"
    if v <= 0.67 * med:
        return "PIERDE"
    return "EMPATE"


def resumen():
    filas = leer()
    if not filas:
        print("Sin Shorts registrados.")
        return
    print("| Short | fecha | hip. | variable=variante | v48 | v7 | ret7 | veredicto |\n|---|---|---|---|---|---|---|---|")
    for r in filas:
        print(f"| {r['slug']} | {r['fecha']} | {r['hipotesis']} | {r['variable']}={r['variante']} | {r['v48'] or '-'} | "
              f"{r['v7'] or '-'} | {r['ret7'] or '-'} | {r['veredicto'] or '-'} |")
    cuenta = {}
    for r in filas:
        if r["veredicto"] in ("GANA", "PIERDE", "EMPATE"):
            cuenta.setdefault(r["hipotesis"], []).append(r["veredicto"])
    for h, vs in sorted(cuenta.items()):
        g, p = vs.count("GANA"), vs.count("PIERDE")
        estado = "CONFIRMADA" if g >= 2 else "DESCARTADA" if p >= 2 else "abierta"
        print(f"{h}: {g} ganadas, {p} perdidas, {len(vs) - g - p} empates → {estado}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("--plan", required=True)
    a = sub.add_parser("alta"); a.add_argument("--plan", required=True); a.add_argument("--post", default="")
    a.add_argument("--fecha", required=True); a.add_argument("--hora", default="16:00")
    hoy = dt.date.today().isoformat()
    pe = sub.add_parser("pendientes"); pe.add_argument("--hoy", default=hoy)
    m = sub.add_parser("medir"); m.add_argument("--metricool", required=True); m.add_argument("--hoy", default=hoy)
    sub.add_parser("resumen")
    x = ap.parse_args()
    if x.cmd == "check":
        check(x.plan)
    elif x.cmd == "alta":
        alta(x.plan, x.post, x.fecha, x.hora)
    elif x.cmd == "pendientes":
        pendientes(x.hoy)
    elif x.cmd == "medir":
        medir(x.metricool, x.hoy)
    else:
        resumen()


if __name__ == "__main__":
    main()
