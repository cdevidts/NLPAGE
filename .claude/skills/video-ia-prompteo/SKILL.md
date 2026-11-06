---
name: video-ia-prompteo
description: Cómo se escribe, revisa y paga cada toma de video con IA (Gemini Omni Flash por la API) para los Shorts de SheetSmithChile. Úsala SIEMPRE antes de llamar a `gemini.py video`, al planear B-roll con IA para un Short, o al revisar una toma generada. Cada toma cuesta plata real de Cris.
---

# Video con IA: prompteo sin azar

Regla de Cris (2026-11-06): **nada al azar**. Cada segundo de video con IA se paga con la
plata de Cris (prepago y créditos de AI Pro, tope de US$9 al mes en `docs/gemini/config.json`).
Una toma que hay que repetir es plata perdida. Por eso:

- Ninguna toma se genera sin una **ficha** (`docs/video-ia/fichas/<short>-<n>.json`).
  `gemini.py video` rechaza los prompts sueltos y las fichas incompletas.
- Ninguna toma se genera sin un **Short concreto** que la use y un **momento** del guion
  (lo que dice la voz en esos segundos).
- Un clip de 8 s trae **3 tomas distintas** (lo normal) con cortes en tiempos fijos: rinde
  tres planos por el precio de uno.

## El orden de trabajo (no se salta ningún paso)

1. **Guion primero.** El Short ya tiene plan o guion (skills `shorts-sheetsmith` y
   `shorts-viral-loop`). Decide en qué segundos va la toma y qué dice la voz encima. La toma
   ilustra esa frase, no otra cosa.
2. **Hechos del expediente.** Lugar, año, estación, clima y objetos salen del expediente
   del juego (nunca de la solución) o del listing. Anota la página en `fuente`. Si el caso
   dice "condado de Larch, sheriff, 1989", la toma no puede ser en los Alpes.
3. **Escribe la ficha** copiando `docs/video-ia/fichas/_plantilla.json`. Todos los campos son
   obligatorios (ver abajo). Texto de la ficha en inglés: el modelo solo está evaluado en inglés.
4. **Ensayo** (gratis): `python3 -I scripts/gemini/gemini.py video --ficha <f> --ensayo`.
   Lee el prompt armado de corrido, como si fueras el modelo: ¿hay algo que pueda entender de
   dos maneras?
5. **Revisión** (centavos): `... --revisar`. Un modelo de texto revisa el prompt contra esta
   skill. Corrige todo lo que tenga sentido y vuelve al paso 4. "SIN PROBLEMAS" o problemas
   descartados con razón escrita en `notas` de la ficha antes de pagar.
6. **Checklist antes de pagar** (abajo). Si un punto falla, no se paga.
7. **Generar**: `... --ficha <f> --salida public/ia/<short>-<n>.mp4 --pago`. Deja al lado
   `<n>.prompt.txt` y `<n>.tira.jpg` (2 fotogramas por segundo).
8. **Revisar la tira entera** (abre la imagen). ¿Están las 3 tomas, en sus tiempos? ¿Hay
   texto, caras raras, manos deformes, gente que no se pidió, saltos de luz? Escribe el
   resultado en `resultado` de la ficha: `usable`, `usable con recorte (segundos)` o `falla`.
9. **Si falla:** nada de reintentar a ciegas. Escribe el diagnóstico (qué palabra del prompt
   causó qué) en *Lecciones* de esta skill, corrige la ficha y recién ahí se vuelve a pagar.
   Dos fallas seguidas con la misma ficha = se para y se cambia el enfoque.
10. **Medir.** El Short que la usa se registra en el loop viral como prueba V16 (dinamismo
    visual). Si las tomas con IA no suben la retención o las vistas frente a fotos con zoom,
    se deja de gastar y se avisa a Cris.

## Campos de la ficha

| Campo | Qué lleva | Ejemplo bueno | Ejemplo malo |
|---|---|---|---|
| `short` | plan o guion que la usa | `plans/57-cold-case-02-historia-es.json` | "un Short" |
| `momento` | segundos del Short y la frase que suena | "s 0-8: 'Veintiocho de enero de mil novecientos ochenta y nueve...'" | — |
| `fuente` | de dónde salen los hechos | "expediente ES p. 1: Greyhorn Lodge, condado de Larch, 28-ene-1989, tormenta, gala del Carnaval de Invierno" | — |
| `objetivo` | qué tiene que sentir el espectador | "aislamiento y amenaza antes del primer dato" | "que se vea bonito" |
| `duracion` | 3-10 s; 8 s con 3 tomas es el estándar | 8 | — |
| `estilo` | género visual + época + soporte | "Cinematic true-crime documentary re-creation, 1989, shot on 35mm film" | "cool video" |
| `lugar` | sitio exacto con detalles físicos | "a three-story 1980s timber-and-stone mountain hotel on a pine-covered slope" | "a cabin" |
| `luz` | fuentes, dirección, temperatura, contraste | "night; warm tungsten 2700K practicals from windows as key; cold blue 6000K moonlight through snow as fill; high contrast" | "dramatic lighting" |
| `paleta` | 2-3 colores dominantes | "deep navy, amber window glow, desaturated white snow" | — |
| `lente` | focal, profundidad de campo, textura | "35mm and 85mm anamorphic, shallow depth of field, fine film grain, slight halation" | — |
| `continuidad` | lo que se mantiene entre tomas | "same storm, same night, same hotel, snowfall direction left to right in every shot" | — |
| `tomas` | 1-4 tomas contiguas `desde`/`hasta`, mínimo 1,5 s (mejor 2-3 s) | ver plantilla | — |
| `audio` | solo ambiente: la voz y la música las pone Remotion | "howling blizzard wind, creaking timber; no music, no dialogue" | — |
| `evitar` | 3+ negativos concretos | "no people", "no on-screen text", "no modern cars" | — |
| `texto_en_pantalla` | opcional; por defecto ninguno (los textos los pone Remotion) | — | — |
| `imagen` | opcional: foto o imagen de referencia (primer fotograma o estilo) | — | — |

Cada toma: `plano` (tamaño: extreme wide, wide, medium, close-up, extreme close-up, insert),
`camara` (movimiento único y motivado: slow push-in, lateral dolly, crane down, locked-off,
handheld drift; velocidad), `sujeto` y `accion` (concretos, 4+ palabras, algo que se mueve),
`foco` (qué está nítido; rack focus si cambia), y `luz` si cambia respecto de la general.

## Oficio: cómo se piensan 3 tomas en 8 s

- **Gramática clásica**: general que ubica (dónde y cuándo) → plano medio que cuenta (el
  objeto o el lugar del hecho) → detalle que inquieta (un inserto que pide la siguiente
  frase). Variar el tamaño de plano en cada corte; dos tomas del mismo tamaño seguidas se
  ven como un salto.
- **Un movimiento por toma**, lento y con intención. Nada de órbitas y zooms a la vez.
- **Luz motivada**: toda luz sale de una fuente que existe en la escena (ventana, lámpara,
  chimenea, luna, sirena). Misma dirección de luz clave en las 3 tomas.
- **Tiempo de lectura**: una toma de menos de 2 s solo sirve si es un golpe (inserto). Para
  el gancho de un Short (primeros 1,5 s), la primera toma debe ser la más fuerte.
- **Pensar el corte en Remotion**: cada toma debe poder usarse sola. El último fotograma de
  la toma 3 debe ser limpio (sin movimiento brusco) para cortar o congelar.
- **Personas y personajes** (Cris, 6-nov 22:27: "prueba personas, escenas tensas, personajes"):
  se permiten y hay que probarlos. Para que no huela a IA: luz dramática con una fuente clara,
  expresiones contenidas (mirar, girar la cabeza, quedarse quieto), nada de manos haciendo
  cosas finas (escribir, abrir cierres, tocarse la cara), nada de bocas hablando, piel con
  textura natural. Siempre en `evitar`: "no distorted faces or hands, no extra fingers". Nunca
  gente real reconocible ni menores. En la tira se revisa cara por cara.
- **Secuencia rápida**: la guía oficial permite cortes cada 0,5-2 s. Una rueda de 5 caras de
  1,6 s cada una es válida si todas comparten luz, encuadre y fondo (el cambio de persona es el
  corte, no un salto). Hasta 6 tomas por clip.
- **Texto físico en la escena** (una hora en una libreta, un sello de fecha): se define en
  `texto_en_pantalla` y debe ser algo que ya está escrito, nunca escribiéndose.
- **Época correcta**: decir el año y pedir detalle de época ("period-correct 1989"); negar lo
  moderno que suele colarse (celulares, autos modernos, LED).
- **Audio**: solo ambiente. Nada de música ni voces: se pisan con la voz y la música del Short.

## Checklist antes de pagar

1. ¿El Short y el momento existen y la toma ilustra exactamente esa frase?
2. ¿Cada dato físico sale de `fuente` (nunca de la solución)?
3. ¿Las tomas cubren 0 → `duracion` sin huecos, con tamaños de plano distintos?
4. ¿Cada toma tiene un solo movimiento de cámara y una sola acción?
5. ¿La luz tiene fuente, dirección y temperatura, y es la misma lógica en las 3 tomas?
6. ¿`evitar` cubre texto, gente, caras, objetos modernos y música?
7. ¿`--revisar` quedó sin problemas o con cada problema respondido en `notas`?
8. ¿Alcanza el tope del mes? (`--ensayo` lo muestra.)

## Costos (aistudio.google.com/docs/pricing, 2026-11-06)
gemini-omni-1.2-flash ~US$0.07 por segundo a 720p (8 s = US$0.56; 360p ~US$0.023/s). Una
imagen de referencia Nano Banana 2 Lite ~US$0.034. Todo queda en `docs/gemini/gasto.csv`.

## Lecciones (cada falla pagada, con su diagnóstico)
- 2026-11-06, primera toma (`public/ia/caso02-lodge-noche.mp4`, US$0.70, sin ficha): calidad
  visual buena, pero se pidió "ski lodge in the Alps" y el caso 02 ocurre en el condado de
  Larch (sheriff, EE.UU.); salió una cabaña chica y el expediente habla de un hotel de montaña
  con gala. Una sola toma continua de 10 s. Causa: prompt escrito sin leer el expediente ni el
  guion. De ahí nació esta skill.
- 2026-11-06, segunda toma con esta skill (`public/ia/57-caso02-es-1.mp4`, US$0.56, ficha
  `57-caso02-es-1.json`): salió a la primera. 3 tomas con los cortes exactos en 2,5 s y 5,5 s.
  `--revisar` encontró 4 problemas antes de pagar (nieve que "se acumula" en 2,5 s, sujeto y
  acción sin puntuación, rack focus + doble parpadeo en 2,5 s, "paper snowflakes" que llaman
  adornos navideños). Defecto que quedó: "shot on 35mm film" dibujó esquinas redondeadas en
  la toma 1 -> agregar a `evitar`: "no rounded frame corners, no film gate border, no vignette
  frame". Duración: `response_format.duration` va como texto ("8s"), 3s a 15s.
- 2026-11-06, tanda de personajes (fichas 57-caso02-es-2 a 5, 4 x US$0.56): las 4 salieron
  usables a la primera tras 3 rondas de `--revisar`. Funciona: rueda de 5 caras a 1,6 s con la
  misma luz (sin morphing), multitud de gala de época, primer plano emotivo, texto físico
  corto ("07:40", sello "'89 1 28") que sale legible. Falla menor: "unlit torch" salió encendida
  (el modelo asocia antorcha con fuego: si importa, cambiar el objeto). La revisión pide cada
  vez más matices: después de la 3.ª ronda se cierra y se paga. Los negativos se escriben sin
  "no" delante (gemini.py los arma como "Avoid all of the following: ...").

