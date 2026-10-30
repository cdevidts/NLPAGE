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
2. **Lee el listing** (`/mnt/project-files/etsy/<p>/LISTING.txt` o `listing_data.py`).
   Todo dato del guion sale de ahí: cuántas páginas, jugadores, horas, idiomas.
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

## Qué hace que un Short de producto funcione

### Gancho en 1,5 s
La primera escena es una pregunta o una promesa concreta del producto, no el nombre
de la tienda: "Who killed Desmond Ashcombe on closing night?", "Can't read music?
You can still play Jingle Bells tonight." El titular de arriba la resume en 2-4
palabras con UNA palabra resaltada (`*así*`).

### Estructura (30-45 s)
`Gancho → el problema o la historia → qué trae (con páginas reales) → cómo se usa →
para quién (jugadores, nivel, idiomas) → cierre con dónde se compra`. Una idea por
escena, 6-14 palabras por escena. A 2,6 palabras/s, 45 s son ~110 palabras.

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
- YouTube: conector Metricool (`createScheduledPost` con el MP4 en una URL pública).
  Falta que Cris conecte el canal en Metricool: pedirlo una vez, con los videos listos.
- Etsy: el `-etsy.mp4` va al listing por el puente de etsy-bridge (copiar a
  `assets/<carpeta>/` de main y op request multipart con `video`). Editar un listing
  activo es gratis.
