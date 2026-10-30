# SheetSmithChile · videos

YouTube Shorts y videos de listing para la tienda Etsy [SheetSmithChile](https://sheetsmithchile.etsy.com),
hechos con [Remotion](https://www.remotion.dev) y herramientas gratis que corren en local.

| Pieza | Herramienta | Licencia / costo |
|---|---|---|
| Video | Remotion 4 (composiciones `Short` 1080x1920 y `EtsyLoop` 1920x1440) | Gratis para personas y equipos de hasta 3 |
| Voz en inglés | Kokoro-82M vía `kokoro-js` (local, CPU) | Apache 2.0 |
| Voz en español | Piper `es_MX-claude-high` (local, CPU) | dataset Apache 2.0 |
| Subtítulos palabra a palabra | faster-whisper (local) + alineación con el guion | MIT |
| Música | Kevin MacLeod, incompetech.com (1.443 piezas con ánimo y bpm) | CC BY 4.0, crédito en la descripción |
| Efectos | Catálogo medido de Mixkit (heredado de Videos-Next-Layer) | Licencia Mixkit, sin atribución |
| Íconos | Iconify (Phosphor y otros) | MIT / Apache |
| Tipografías | Google Fonts: Oswald, Special Elite, Playfair Display, Inter | OFL |
| Material | Fotos de listing y páginas de los PDF del propio producto | Propio |

Comandos y reglas: [CLAUDE.md](CLAUDE.md). Por qué se eligió cada herramienta y qué se descartó:
[docs/herramientas.md](docs/herramientas.md). Decisiones: [docs/journal.md](docs/journal.md).

## Estructura

```
src/                Short.tsx, EtsyLoop.tsx, components/ (Fondo, Texto, Visual, Efecto), lib/ (temas, tipos)
scripts/            producto, short, loop, watch, musica, setup, sfxCatalog; tts/ (Piper, palabras, oír)
plans/              un JSON por video: escenas (lo que se dice, qué se ve), cierre, ficha de YouTube, loop
renders/            los MP4/GIF terminados y su ficha .youtube.md
public/assets/      efectos (catálogo), música propia, íconos; public/productos y public/voz se regeneran
```
