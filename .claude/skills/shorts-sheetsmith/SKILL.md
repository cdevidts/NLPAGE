---
name: shorts-sheetsmith
description: Oficio para armar, revisar y corregir los YouTube Shorts y los videos de listing de Etsy de la tienda SheetSmithChile (proyecto AI Side Hustle) con el pipeline Remotion de este repo. Úsala siempre que la tarea toque un video de esa tienda - un Short nuevo, cambiar el guion de uno, revisar un render, el video en bucle de un listing o un GIF. No la uses para otras marcas.
---

# Shorts y videos de Etsy de SheetSmithChile

SheetSmithChile vende descargas digitales en Etsy: planillas de Google Sheets, juegos
imprimibles (cold case, escape room, fiestas) y partituras fáciles de piano. No hay
cámara ni persona: **el material es el producto mismo** (las páginas del PDF y las
fotos del listing). Un Short muestra lo que el comprador va a tener en la mano.

Las lecciones pagadas, por tema, están en `references/lecciones.md`. Muchas vienen
del repo Videos-Next-Layer (otra marca, otro pipeline): se copió la técnica, no la
identidad.

## El orden de trabajo

1. **`npm run producto -- <carpeta>`** y abre **cada** `out/productos/<p>/HOJA-*.jpg`.
   Elige páginas mirando. En juegos, nunca la solución (el script no la convierte).
2. **Lee el listing** (`/mnt/project-files/etsy/<p>/LISTING.txt` o `listing_data.py`)
   y, en juegos, los primeros documentos del expediente (carta, sospechosos, informe):
   de ahí sale la historia. Datos del producto (jugadores, horas, idiomas) del listing.
3. **Escribe el plan** copiando uno de `plans/`. Una escena = una frase dicha + una
   cosa que se ve. El copy de YouTube sigue `ai-side-hustle-seo-copy` y `no-ai-slop`.
4. **`npm run short -- --plan ... --solo-check`** (2 s) y después sin la bandera.
   La compuerta corta si falta una imagen, si pasa de 58 s o si whisper no oye lo
   que la voz debía decir.
5. **Revisa**: `out/watch/<slug>/GUION.md` de corrido (lo que se ESCUCHA cada segundo,
   loudness, silencios) y `HOJA.jpg` (un frame por segundo). Un error de pronunciación
   solo se ve en el GUION.
6. **`npm run loop -- --plan ...`** para el video del listing (4:3, 10 s, mudo) y el GIF.
7. Commit, entrada en `docs/journal.md`, y la ficha `renders/<slug>.youtube.md` lista
   para publicar.

## Regla de fondo: un Short es una historia, no un anuncio (Cris, 2026-10-30)

Los primeros Shorts eran anuncios ("39 documents, 1-6 players, it's on Etsy") y Cris
los rechazó: sirven para la portada de Etsy, no para que se compartan. Desde ahora:

- **Se cuenta una historia que engancha por sí sola** y el producto aparece recién
  en el cierre. Si sacas el cierre, el video tiene que seguir valiendo la pena.
- **Juegos de misterio (cold case, escape room, fiesta):** se narra el caso como
  true crime, como si fuera real: gancho (el muerto, el lugar, la noche), los hechos
  raros, el error de la policía, el giro (lo que apareció después), y la pregunta
  abierta ("One of them did it."). En el cierre, y solo ahí: "Este caso es ficción,
  pero lo puedes resolver tú. Enlace en la descripción." Decir que es ficción es
  obligatorio (honestidad y normas de YouTube) y va al final para no matar el gancho.
  Los hechos salen de los documentos del expediente, nunca de la solución, y nunca
  se muestra un acertijo resuelto (patrón del teléfono, cifrados).
- **Partituras y otros productos:** la historia real detrás de la pieza (Jingle
  Bells fue la primera canción tocada en el espacio y no se escribió para Navidad).
  Dato histórico = dato verificado con fuente, anotada en `notas` del plan y en la
  descripción. Las fotos de apoyo, de dominio público (NASA, Wikimedia PD) en
  `public/assets/media/<fuente>/` con su `CREDITOS.md`.
- **Título de YouTube:** el gancho como pregunta o dato sorprendente, con la frase
  de búsqueda dentro ("Cold case file: who killed the theater owner on closing
  night?"). La frase principal de `plan/seo/mapa.json` va en la primera línea de la
  descripción y en los tags. 3-4 hashtags al final (#shorts incluido).
- **Antes de cada plan, la skill `shorts-viral-loop`**: qué hipótesis prueba el Short,
  el bloque `experimento` del plan, `scripts/viral/experimento.py check` sin ERROR y
  `alta` al programarlo. Lo medido y aprendido vive en `docs/viral/BITACORA.md`.
- En Shorts el link de la descripción no es clicable: el cierre dice dónde buscar
  ("Find it on Etsy, at Sheet Smith Chile"; en la voz, el nombre separado), no
  "link in the description". Desde el 30-oct el canal tiene en su cabecera los
  enlaces a Etsy y Gumroad: también vale "link on the channel" / "el link está en el canal".
  La descripción lleva, bajo el link de Etsy de la primera línea: "Shop links (Etsy and
  Gumroad) are on the channel page: tap the channel name." (ES: "Los links de la tienda
  (Etsy y Gumroad) están en el canal: toca el nombre del canal.").

## Qué hace que un Short funcione

### Gancho en 1,5 s
La primera frase es el hecho más fuerte de la historia, no el nombre de la tienda
ni del producto: "A theater owner is found dead on the closing night of his own
play." / "December, 1965. Two astronauts in orbit radio Mission Control." El titular
de arriba lo resume en 2-4 palabras con UNA palabra resaltada (`*así*`).

### Estructura (30-45 s)
`Gancho → hechos raros (2-3 escenas) → giro → pregunta abierta o remate → cierre
con el producto y dónde está`. Una idea por escena, 6-16 palabras por escena,
frases cortas. A 2,6 palabras/s, 45 s son ~110 palabras.

### Visuales (tipos en `src/lib/types.ts`)
| tipo | cuándo |
|---|---|
| `pagina` + `foco` | Mostrar un detalle que se nombra: la cámara entra al punto (x, y en 0-1) con ease-in-out. `etiqueta` pone un rótulo tipo ficha. |
| `abanico` | "Trae N cosas": 4-6 páginas que se abren en abanico. |
| `imagen` | Una foto del listing (mockups ya diseñados). |
| `numero` | Un dato duro: "1-6 players", "20". |
| `portada` | La portada entrando en 3D. |
| cierre | Automático: portada, nombre, pastilla "SheetSmithChile on Etsy". |

### Temas (`src/lib/temas.ts`)
Cada línea tiene el mundo visual de sus fotos de Etsy: `coldcase` (madera oscura,
papel crema, rojo sello, Oswald + máquina de escribir), `piano` (rojo navidad, dorado,
Playfair), `sheets` (blanco y verde Sheets, Inter), `fiesta` (azul noche, naranjo).
Lo que une a la tienda es el movimiento y la marca chica arriba, no un color.

### Movimiento
Nada lineal: `spring()` con sobrepaso para lo que llega, ease-in-out para la cámara.
Cortes secos entre escenas con whoosh grave. Nada de lenguaje de presentación: sin
barras de progreso, sin chips numerados, sin disolvencias largas.

### Sonido
- Voz: Kokoro `af_heart` (EN, la de mejor nota) y Piper `es_MX-claude-high` (ES).
  Opción Gemini TTS (gratis, pide `GEMINI_API_KEY`): `"voz": "gemini:Charon"` y
  `"vozEstilo": "narrador de true crime, grave"` en el plan. Probarla como variable de un
  experimento del loop viral, no de golpe en todos. Detalle en `docs/gemini/README.md`.
  Velocidad 1,05-1,08. **Números y años en letras** en `dice`.
- Música: cama que baja al 30 % cuando hay voz (automático). Para piano, la pista de
  práctica del propio producto (`musica.archivo`): el video suena a lo que se compra.
  Para lo demás, `npm run musica -- --buscar "mysterious suspense"` y elegir por ánimo.
- Efectos medidos (Mixkit): whoosh en cada cambio de escena, pop al entrar un ícono,
  golpe en el cierre. El pico cae en el evento.
- Salida a -14 LUFS / pico bajo -1 dBTP (loudnorm en dos pasadas).

### Subtítulos
Dicen exactamente lo que suena, palabra por palabra (faster-whisper sobre la voz,
emparejado con el guion). Hasta 3 palabras por pantalla; la que suena lleva el
resaltador que la barre. Van en y≈1385: sobre la interfaz de YouTube (abajo) y bajo
el visual.

## Zona segura de YouTube Shorts (1080x1920)
Arriba ~120 px (buscar, menú), abajo ~380 px (título, canal, música) y a la derecha
~140 px (botones). Titular en y 200-420, visual 420-1320, subtítulo 1385-1560.

## Publicar
- YouTube: conector Metricool, marca cdevidts2 (blogId 6078519), canal conectado el
  30-oct. `createScheduledPost` con `providers [{network: youtube}]`, `youtubeData`
  {title, type "short", privacy "public", tags, category, madeForKids false,
  isAiGeneratedContent true (la voz es IA)} y el texto de la ficha sin la línea de tags.
  El MP4 va como URL de raw.githubusercontent de este repo (es público) fijada a un
  commit ya empujado; Metricool la copia a su CDN. Hora: 16:00 Chile (la mejor según
  Metricool), un Short por día. Nunca la red Instagram de esa marca (es de Next Layer).
- Etsy: el `-etsy.mp4` se sube con `python3 /mnt/project-files/plan/metricas/swap_video.py
  <listing_id>=<mp4>` (reemplaza el video anterior). Editar un listing activo es gratis.
