#!/usr/bin/env python3
"""Estudia los Shorts de creadores parecidos: qué formato les gana a su propio canal.

Gratis y sin cuenta: yt-dlp lee las páginas públicas de listado de YouTube (búsqueda y
pestaña Shorts de cada canal). Las páginas de cada video piden "confirma que no eres un
bot" desde el contenedor: NO se esquiva (sin cookies, sin proxies). Por eso no hay
subtítulos ni duración por Short; sí títulos, vistas, suscriptores y la miniatura.

Método "outlier" (el que usan 1of10 y vidIQ): un Short que hace 3x o más la mediana de
su canal ganó por el formato (tema, gancho, título), no por la audiencia. Esos se miran.

Uso:
  python3 scripts/viral/competencia.py --nicho coldcase
  python3 scripts/viral/competencia.py "jingle bells piano" --canales @PianoVideoLessons
Sale: out/competencia/<fecha>-<nicho>/REPORTE.md + datos.json + miniaturas de los
outliers (abrir con Read para ver el texto en pantalla del primer frame).
Lo que valga se copia a docs/viral/creadores.md (eso sí se commitea).
"""
import argparse, datetime as dt, json, re, statistics, subprocess, sys, urllib.request
from pathlib import Path

# Un canal entra al análisis solo si al menos 1 de cada 4 de sus Shorts habla del nicho
# (la búsqueda trae también canales gigantes de otra cosa: Roblox, MrBeast).
FILTROS = {
    "coldcase": r"murder|case|crime|killer|mystery|unsolved|detective|police|disappear|caso|asesin|crimen",
    "piano": r"piano|chord|song|carol|melod|notes|play|music",
    "juegos": r"game|party|escape|puzzle|play|riddle|juego",
    "sheets": r"budget|sheet|excel|money|debt|spreadsheet|save|saving|finance|planner",
}
NICHOS = {
    "coldcase": ["cold case unsolved mystery shorts", "true crime story shorts", "unsolved murder shorts",
                 "murder mystery game shorts", "caso sin resolver shorts"],
    "piano": ["easy piano tutorial shorts", "christmas song history shorts", "piano letter notes shorts",
              "jingle bells piano shorts"],
    "juegos": ["escape room at home shorts", "christmas party games shorts", "game night ideas shorts"],
    "sheets": ["google sheets budget shorts", "budget with me shorts", "debt payoff shorts", "spreadsheet tips shorts"],
}


def ytdlp_json(args, timeout=150):
    r = subprocess.run(["yt-dlp", "--no-warnings", "--ignore-errors", "--flat-playlist", *args],
                       capture_output=True, text=True, timeout=timeout)
    return r.stdout


def canales_de(q, n):
    """Canales que aparecen en la búsqueda (con su @handle)."""
    out = ytdlp_json(["-j", f"ytsearch{n}:{q}"])
    vistos = {}
    for l in out.splitlines():
        try:
            d = json.loads(l)
        except ValueError:
            continue
        h = d.get("uploader_id") or d.get("channel_id")
        if h and h not in vistos:
            vistos[h] = d.get("channel")
    return list(vistos)


def shorts_de(handle, n):
    base = f"https://www.youtube.com/{handle}" if handle.startswith("@") else f"https://www.youtube.com/channel/{handle}"
    out = ytdlp_json(["-J", "--playlist-end", str(n), base + "/shorts"])
    try:
        d = json.loads(out)
    except ValueError:
        return None
    if not isinstance(d, dict):
        return None
    vids = [{"id": e["id"], "titulo": e.get("title") or "", "vistas": e.get("view_count") or 0}
            for e in d.get("entries") or [] if e and e.get("id")]
    return {"canal": d.get("channel") or handle, "handle": handle,
            "suscriptores": d.get("channel_follower_count") or 0, "shorts": vids}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("busquedas", nargs="*")
    ap.add_argument("--nicho", choices=NICHOS)
    ap.add_argument("--canales", nargs="*", default=[], help="@handles a sumar")
    ap.add_argument("--por-busqueda", type=int, default=12, help="resultados de búsqueda a mirar")
    ap.add_argument("--shorts", type=int, default=30, help="últimos Shorts por canal")
    ap.add_argument("--umbral", type=float, default=3.0, help="veces la mediana del canal")
    ap.add_argument("--min-vistas", type=int, default=20000)
    ap.add_argument("--filtro", help="regex de títulos del nicho (por defecto el del --nicho)")
    a = ap.parse_args()
    qs = a.busquedas or NICHOS.get(a.nicho or "", [])
    nombre = a.nicho or re.sub(r"[^a-z0-9]+", "-", " ".join(qs or a.canales).lower())[:40]
    dest = Path("out/competencia") / f"{dt.date.today()}-{nombre}"
    (dest / "miniaturas").mkdir(parents=True, exist_ok=True)

    handles = list(dict.fromkeys(a.canales + [h for q in qs for h in canales_de(q, a.por_busqueda)]))
    print(f"{len(handles)} canales", file=sys.stderr)
    canales, outliers = [], []
    for h in handles:
        c = shorts_de(h, a.shorts)
        if not c or len(c["shorts"]) < 5:
            continue
        filtro = a.filtro or FILTROS.get(a.nicho or "")
        if filtro:
            hits = sum(bool(re.search(filtro, v["titulo"], re.I)) for v in c["shorts"])
            if hits < len(c["shorts"]) / 4:
                continue
        med = statistics.median(v["vistas"] for v in c["shorts"]) or 1
        c["mediana"] = med
        canales.append(c)
        for v in c["shorts"]:
            x = v["vistas"] / med
            if x >= a.umbral and v["vistas"] >= a.min_vistas:
                outliers.append({**v, "canal": c["canal"], "handle": h, "suscriptores": c["suscriptores"],
                                 "mediana_canal": med, "x_mediana": round(x, 1),
                                 "url": f"https://www.youtube.com/shorts/{v['id']}"})
    hashtags = {}
    for o in outliers:
        for h in re.findall(r"#\w+", o["titulo"].lower()):
            hashtags[h] = hashtags.get(h, 0) + 1
    outliers.sort(key=lambda o: (o["x_mediana"], o["vistas"]), reverse=True)
    for o in outliers[:15]:
        p = dest / "miniaturas" / f"{o['id']}.jpg"
        for nombre in ("oardefault", "hqdefault"):  # oardefault es la vertical; no siempre existe
            try:
                img = urllib.request.urlopen(f"https://i.ytimg.com/vi/{o['id']}/{nombre}.jpg", timeout=20).read()
            except Exception:
                continue
            if len(img) > 2000:  # 1 KB = imagen gris de "no hay"
                p.write_bytes(img)
                o["miniatura"] = str(p)
                break
    (dest / "datos.json").write_text(json.dumps({"busquedas": qs, "canales": canales, "outliers": outliers},
                                                ensure_ascii=False, indent=1))
    canales.sort(key=lambda c: c["mediana"], reverse=True)
    r = [f"# Competencia {dt.date.today()} · {nombre}", "", f"Búsquedas: {', '.join(qs) or '-'}", "",
         "## Canales (mediana de vistas de sus últimos Shorts)", "", "| canal | subs | mediana | Shorts |", "|---|---|---|---|"]
    r += [f"| {c['canal']} ({c['handle']}) | {c['suscriptores']:,} | {int(c['mediana']):,} | {len(c['shorts'])} |" for c in canales]
    r += ["", f"## Outliers (>= {a.umbral}x la mediana de su canal y >= {a.min_vistas:,} vistas)", "",
          "| x mediana | vistas | canal | título | miniatura |", "|---|---|---|---|---|"]
    r += [f"| {o['x_mediana']} | {o['vistas']:,} | {o['canal']} | [{o['titulo'][:90]}]({o['url']}) | {o.get('miniatura', '-')} |"
          for o in outliers[:40]]
    top_h = sorted(hashtags.items(), key=lambda kv: -kv[1])[:15]
    r += ["", "## Hashtags en los títulos de los outliers", "", ", ".join(f"{h} ({n})" for h, n in top_h) or "-"]
    (dest / "REPORTE.md").write_text("\n".join(r) + "\n")
    print(dest / "REPORTE.md")


if __name__ == "__main__":
    main()
