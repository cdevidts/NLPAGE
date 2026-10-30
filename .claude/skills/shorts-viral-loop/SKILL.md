---
name: shorts-viral-loop
description: Loop de prueba y retroalimentación para que los YouTube Shorts y pines de video de SheetSmithChile (proyecto AI Side Hustle) se vuelvan virales - hipótesis por video, una variable a la vez, métricas de Metricool, fechas de lectura, bitácora de qué funcionó y qué no, y estudio de creadores parecidos. Úsala antes de planear CADA Short nuevo, al leer sus métricas y en la revisión semanal de contenido. Va junto con shorts-sheetsmith (el oficio del render). No la uses para otras marcas.
---

# Loop viral de Shorts (SheetSmithChile)

`shorts-sheetsmith` dice CÓMO se arma un Short. Esta skill dice QUÉ probar en cada uno,
cómo se mide y qué se aprende. Ningún Short sale sin hipótesis, y ninguno queda sin leer.

Archivos del loop (todos en este repo):
| Archivo | Qué es |
|---|---|
| `docs/viral/BITACORA.md` | Hipótesis (V1, V2...), reglas que ya funcionan, lo descartado y el registro de cada lectura. Es la memoria del loop. |
| `docs/viral/shorts.csv` | Una fila por Short publicado: variables y métricas a 48 h y 7 días. |
| `references/patrones.md` | Lo que hacen los creadores que ganan, por nicho, con evidencia y fecha. |
| `scripts/viral/experimento.py` | `check`, `alta`, `pendientes`, `medir`, `resumen`. |
| `scripts/viral/competencia.py` | Estudio de outliers de otros canales (gratis, sin cuenta). |

## El ciclo de cada día (un Short por día, 16:00 Chile)

1. **Leer lo que venció.** `python3 scripts/viral/experimento.py pendientes`. Si hay
   lecturas de 48 h o 7 días, pide a Metricool las métricas que el comando imprime
   (`getAnalyticsDataByMetrics`, brandId 6078519), guarda el JSON y corre
   `experimento.py medir --metricool <json>`. Anota la conclusión en la bitácora.
2. **Elegir qué probar.** Abre `BITACORA.md`. Regla 70/30: 7 de cada 10 Shorts usan
   las reglas que ya funcionan y cambian solo el tema; 3 de cada 10 prueban la
   hipótesis abierta de más arriba. En los primeros 10 Shorts del canal todos son
   prueba (aún no hay línea base). **Una variable por prueba**: si cambias formato
   y duración a la vez, no sabes cuál funcionó.
3. **Escribir el plan** con `shorts-sheetsmith` y agregarle el bloque `experimento`
   (abajo). `experimento.py check --plan plans/<slug>.json` revisa el bloque y las
   reglas de viralidad. Si da ERROR, no se renderiza.
4. **Render y revisión** (`npm run short`, GUION.md). Al programarlo en Metricool,
   `experimento.py alta --plan plans/<slug>.json --post <id de Metricool> --fecha <AAAA-MM-DD>`.
5. **Commit** de plan, csv y bitácora.

Cada domingo, antes de la retro de operación: `experimento.py resumen` (qué ganó la
semana), una corrida de `competencia.py --nicho <el de la semana>` y copiar a
`references/patrones.md` lo nuevo que valga. De ahí salen hipótesis nuevas.

## El bloque `experimento` del plan

```json
"experimento": {
  "hipotesis": "V2",
  "variable": "formato",
  "variante": "tutorial con letras sobre el teclado",
  "control": "60-piano-villancicos-en (historia del villancico)",
  "formato": "tutorial",
  "gancho_tipo": "dato-imposible",
  "espera": "retención >= 70 % y más vistas a 7 días que el control",
  "listing_id": 4605991888
}
```
- `variable`: formato, gancho, duracion, final, titulo, serie, idioma, cta, voz, musica, hora.
- `formato`: historia, reto, tutorial, pov, confesion, lista, antes-despues.
- `gancho_tipo`: pregunta, dato-imposible, in-medias-res, contradiccion, reto, confesion, pov, superlativo, injusticia.
- `control`: el slug contra el que se compara, o `linea-base`.

## Métricas (todas gratis por el conector Metricool)

| Qué | Métrica Metricool | Para qué |
|---|---|---|
| Vistas | YTVP06 | Distribución. Desde marzo de 2025 cada inicio o repetición cuenta como vista. |
| Duración media vista | YTVP08 (s) | **Retención = YTVP08 / duración del Short.** Sobre 100 % = la gente lo repite (bucle). |
| Likes, comentarios, shares | YTVP09, YTVP11, YTVP12 | Por cada 1.000 vistas. Shares y comentarios pesan más que likes. |
| Suscriptores ganados | YTEV05 (día) | ¿El formato crea audiencia? |
| Fuentes de tráfico | YTTS01, YTTS02 | Si "SHORTS" domina, el feed lo está empujando; si es "YT_SEARCH", vive del título. |
| Pin de video | PIPO08, PIPO11, PIPO12, PIPO13 | Impresiones, clics salientes, vistas y segundos vistos. |
| Venta | `plan/metricas/serie/etsy.csv` | Vistas del listing 72 h antes vs 72 h después del Short. |

YouTube no da por API el "visto vs deslizado" ni el CTR del feed: no se inventan.
Los links en la descripción de un Short NO son clicables (YouTube, desde ago-2023). Los
clics a la tienda salen del perfil del canal y de los pines de video de Pinterest, que
sí llevan link. Por eso cada Short ganador se reusa como pin de video (hilo de canales).

**Lecturas**: a las 48 h (primer grupo de prueba del feed) y a los 7 días (final). Un
Short se compara contra la **mediana del canal** de los últimos 10 Shorts:
- GANA: vistas 7 d >= 1,5x la mediana y retención >= la mediana.
- PIERDE: vistas 7 d <= 0,67x la mediana.
- Lo demás, EMPATE. Con menos de 5 Shorts previos, solo se anota (línea base).
Una hipótesis queda **CONFIRMADA** con 2 victorias en 3 pruebas y pasa a "Reglas que
funcionan" (y a `shorts-sheetsmith` si cambia el oficio). **DESCARTADA** con 2 derrotas.
Con números chicos todo es ruido: nunca concluir con un solo video.

## Reglas de viralidad que ya rigen (las revisa `check`)

1. **No es un anuncio** (Cris, 2026-10-30). Historia real o curiosidad primero; la
   tienda, el producto y el CTA solo en la última escena / el cierre.
2. **Honestidad**: un cold case nuestro es ficción. Se cuenta como true crime, pero el
   cierre dice que es un caso para resolver ("este caso es ficción: lo puedes resolver
   tú"). Nunca afirmar que pasó de verdad. Los datos históricos (piano) deben ser ciertos y
   verificados en 2 fuentes.
3. **Gancho en 1-2 s**: primera frase de 12 palabras o menos, con algo concreto (un
   nombre, un número, un objeto). El primer frame ya tiene texto grande y una imagen
   que se entiende sola (documento, cara, teclado). Nada de logo ni nombre de tienda al inicio.
4. **Un bucle abierto antes de los 3 s** (una pregunta que el video responde tarde) y
   el pago al final. Un cold case puede terminar con la pregunta abierta: invita a comentar.
5. **CTA hablado** que no dependa de un link: "busca SheetSmithChile en Etsy".
6. **Variedad**: cada Short con guion propio. YouTube desmonetiza y frena el contenido
   "inauthentic" (plantilla repetida con voz IA, política de jul-2025). La voz IA se declara.

## Hipótesis abiertas y su orden
Ver `docs/viral/BITACORA.md`. Si se acaban: correr `competencia.py`, mirar los outliers
(título y miniatura) y escribir la nueva hipótesis con su evidencia antes de probarla.

## Herramientas: qué se probó
- `competencia.py` usa yt-dlp sobre los listados públicos (búsqueda y pestaña Shorts de
  cada canal): títulos, vistas, suscriptores, miniatura. La página de cada video pide
  "confirma que no eres un bot" desde el contenedor: **no se esquiva** (sin cookies ni
  proxies), así que no hay subtítulos ni duración de Shorts ajenos.
- Lo que el contenedor no puede ver (subtítulos y ganchos de Shorts ajenos, crítica de nuestros
  Shorts, Deep Research) se le pide a la app de Gemini por el canal del repo:
  `scripts/gemini/bandeja.py pedir` (skill `gemini-canal`, respuesta en ~1 h en Drive). Ya
  pedidos: G-006 (15 Shorts más vistos de MrBallen y Cold Case Detective con ganchos
  transcritos) y G-007 (crítica de nuestro canal). Todo lo de Gemini entra como hipótesis
  "según Gemini, sin verificar", nunca como regla.
- Métricas propias: solo Metricool. YouTube Analytics API pediría OAuth de Cris: no hace falta.
- Skills ajenas revisadas (2026-10-30): `viral-video-master` (josiahsiegel/claude-plugin-marketplace)
  trae cifras sin fuente (p. ej. "55 s da 3x vistas"); se tomaron solo las ideas
  cualitativas (bucle, serie, CTA de comentario) y quedaron como hipótesis, no como reglas.
