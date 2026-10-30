# NLPAGE: videos de SheetSmithChile (proyecto "AI Side Hustle")

Repo de redes sociales de la tienda Etsy **SheetSmithChile**: YouTube Shorts de los
productos y videos en bucle para los listings de Etsy. Remotion + herramientas gratis,
sin cuentas. Es de Claude (Cris, 2026-10-30): se puede reorganizar entero.

La memoria del proyecto vive fuera del repo: lee `/mnt/project-files/CLAUDE.md`,
`memoria/ESTADO.md` y `memoria/EXPERIMENTOS.md` antes de empezar, y al terminar pasa
la skill de cierre `ai-side-hustle-cierre-de-tarea` (repo cdevidts/etsy-bridge).

El oficio (cómo se arma un Short que funciona, cómo se revisa) está en la skill
`.claude/skills/shorts-sheetsmith`. Léela antes de tocar un plan.

## "Haz el Short de <producto>"

```bash
npm install && npm run setup                   # una vez por contenedor
npm run producto -- 56-cold-case-01            # fotos + páginas del PDF; mira out/productos/<p>/HOJA-*.jpg
# escribe plans/<producto>-<idioma>.json (copia uno de plans/)
npm run short -- --plan plans/<slug>.json      # compuerta, voz, palabras, render, -14 LUFS, revisión
# lee out/watch/<slug>/GUION.md y abre HOJA.jpg
npm run loop  -- --plan plans/<slug>.json      # video 4:3 mudo para el listing de Etsy + GIF
```

## Reglas

1. **Nunca se muestra el PDF de solución** de un juego (`producto` ni lo convierte).
2. **No se inventa nada**: cada dato del guion sale del listing (`LISTING.txt` o
   `listing_data.py` del producto). Números y años en letras en `dice` (la voz lee mal "2013").
3. Todo copy de YouTube (título, descripción, tags) sigue la skill `ai-side-hustle-seo-copy`
   (frase principal de `plan/seo/mapa.json`; título = frase + "flip-through") y la prosa
   pasa por `no-ai-slop`. Ambas viven en el repo etsy-bridge.
4. **Plata**: solo herramientas gratis. Nada que cobre sin el OK de Cris.
5. Música con licencia clara: Kevin MacLeod (incompetech, CC BY 4.0, el crédito lo pone
   `short` en la ficha) o audio propio del producto. Nada comercial (Content ID).
6. Los renders van a `renders/` con su ficha `<slug>.youtube.md`. Se commitean.
7. Antes de entregar: `GUION.md` leído de corrido (lo que se ESCUCHA en cada segundo),
   loudness -14 LUFS y pico bajo -1 dBTP, `npx tsc --noEmit` limpio.
8. Publicar: YouTube vía el conector Metricool (canal conectado el 30-oct; receta en la skill).
   El video de Etsy se sube por el puente de etsy-bridge (op `multipart`, campo `video`).

## Entorno

Nada que pagar ni cuentas: Chromium en `/opt/pw-browsers` (nunca `playwright install`),
ffmpeg de sistema, Python 3 con piper-tts y faster-whisper (`npm run setup` los instala).
Modelos de voz y whisper se bajan de Hugging Face la primera vez a `.cache/`.
