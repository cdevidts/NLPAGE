# NLPAGE: videos de SheetSmithChile (proyecto "AI Side Hustle")

Repo de redes sociales de la tienda Etsy **SheetSmithChile**: YouTube Shorts de los
productos y videos en bucle para los listings de Etsy. Remotion + herramientas gratis,
sin cuentas. Es de Claude (Cris, 2026-10-30): se puede reorganizar entero.

La memoria del proyecto vive fuera del repo: lee `/mnt/project-files/CLAUDE.md`,
`memoria/ESTADO.md` y `memoria/EXPERIMENTOS.md` antes de empezar, y al terminar pasa
la skill de cierre `ai-side-hustle-cierre-de-tarea` (repo cdevidts/etsy-bridge).

El oficio (cómo se arma un Short que funciona, cómo se revisa) está en la skill
`.claude/skills/shorts-sheetsmith`. Léela antes de tocar un plan, y antes de cada plan
nuevo pasa por `.claude/skills/shorts-viral-loop` (hipótesis, bloque `experimento`,
medición; bitácora en `docs/viral/BITACORA.md`).

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
2. **Un Short es una historia, no un anuncio** (Cris, 30-oct): el caso contado como true
   crime o la historia real de la pieza, y el producto solo en el cierre. Detalle en la skill.
3. **No se inventa nada**: los hechos salen del expediente (nunca de la solución), del
   listing o de una fuente verificada anotada en el plan. Un caso de ficción se dice
   ficción en el cierre. Números y años en letras en `dice` (la voz lee mal "2013").
4. Todo copy de YouTube (título, descripción, tags) sigue la skill `ai-side-hustle-seo-copy`
   (frase principal de `plan/seo/mapa.json` en descripción y tags; título = gancho con la frase dentro) y la prosa
   pasa por `no-ai-slop`. Ambas viven en el repo etsy-bridge.
5. **Plata**: solo herramientas gratis. Nada que cobre sin el OK de Cris.
6. Música con licencia clara: Kevin MacLeod (incompetech, CC BY 4.0, el crédito lo pone
   `short` en la ficha) o audio propio del producto. Nada comercial (Content ID).
7. Los renders van a `renders/` con su ficha `<slug>.youtube.md`. Se commitean.
8. Antes de entregar: `GUION.md` leído de corrido (lo que se ESCUCHA en cada segundo),
   loudness -14 LUFS y pico bajo -1 dBTP, `npx tsc --noEmit` limpio.
9. Publicar: YouTube vía el conector Metricool (canal conectado el 30-oct; receta en la skill).
   El video de Etsy se sube por el puente de etsy-bridge (op `multipart`, campo `video`).

## Canal con la app de Gemini (cuenta Google AI Pro de Cris)

Para Deep Research, Veo, Nano Banana o NotebookLM, que la API gratis no da: skill
`.claude/skills/gemini-canal` y `gemini/README.md`. Claude deja tareas con
`scripts/gemini/bandeja.py pedir` (van a **main**), Gemini las responde en Google Docs de
Drive y Claude las recoge con `bandeja.py recibir`. Texto y voz siguen por `scripts/gemini/gemini.py`.

## Entorno

Nada que pagar ni cuentas: Chromium en `/opt/pw-browsers` (nunca `playwright install`),
ffmpeg de sistema, Python 3 con piper-tts y faster-whisper (`npm run setup` los instala).
Modelos de voz y whisper se bajan de Hugging Face la primera vez a `.cache/`.
