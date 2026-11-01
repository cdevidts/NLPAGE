# Qué hacen los creadores que ganan (por nicho)

Método: `scripts/viral/competencia.py --nicho <n>`. Un "outlier" es un Short que hizo 3x
o más la mediana de su propio canal: ganó por el formato, no por la audiencia.
Cada entrada lleva fecha y evidencia. Lo que no está medido aquí es opinión de blogs y
se marca así.

## 2026-10-30 · Primera corrida (4 nichos, ~130 canales)

### Cold case / true crime
- Canales chicos y medianos de casos (Criminal Core 243 mil subs, Scary Mysteries 1 M,
  Dark Asia with Megan 1,3 M) tienen medianas de 2-25 mil vistas por Short. Los outliers:
  - "The Tragic Disappearance of Michael Vaughan" (17x, 36 mil): miniatura = el afiche
    real de "MISSING CHILD". El documento ES el gancho.
  - "Two Kids Afraid of the Dark Vanished From an Alaska Cabin — and Were Never Found"
    (5x, 60 mil): título = detalle humano + desaparición + "nunca encontrados".
    Miniatura: dos fotos viejas pegadas en un expediente y un subtítulo amarillo de 3 palabras.
  - "Woman lynched by 150 men...What happened? <nombre> case" (5x): número brutal +
    "What happened?".
  - "...but the police released him🤬" (3x): ángulo de injusticia.
  - Southern Girl Crime Stories: "The Murder of <nombre>" (8x, 141 mil) con la cara de la
    víctima a pantalla completa y "Link to full video in the comments" (el Short es la
    puerta a un video largo).
- Qué copiamos: abrir con un documento del expediente (informe policial, afiche, foto
  vieja) a pantalla completa, subtítulos amarillos de 1-3 palabras, títulos con nombre +
  hecho imposible + pregunta, ángulo de injusticia ("arrestaron al hombre equivocado").
  Nuestros PDF tienen justo ese material.
- Hashtags que aparecen en los outliers: #truecrime, #coldcase (pocos y del nicho).

### Partituras de piano
- Lo que gana es el **tutorial jugable**, no la historia: "Amazing Grace (Easy Piano
  Tutorial - One Hand)" 9,6x; "Do, a deer, a female deer… #easypiano" 18x; "How to find
  what chords to use for a song" 40x; "Golden - KPop Demon Hunters VERY Easy Tutorial" 4,5x.
- Miniaturas: teclado visto de arriba con **las letras de las notas** (CFAFA GFDC) en
  grande, o manos sobre teclas con el nombre de la canción. Es exactamente lo que vende
  nuestro libro (letter notes).
- Títulos: primera línea de la letra de la canción o "Easy Piano Tutorial - One Hand".
- Hipótesis V2: tutorial con letras > historia del villancico.

### Juegos de fiesta y escape room
- Los outliers chicos son el juego **en acción** o un formato de participación:
  "This HALLOWEEN party game is so SCARY FUN!" (20x en un canal de 1.900 subs), "Imagine
  playing tag... but not knowing who the taggers are?" (530x, animado), "If you laugh
  you lose", "Guess The Animal" (MrBeast). El espectador juega desde su teléfono.
- Hipótesis V1: reto ("¿ves la pista?", "¿quién miente?") > historia narrada.

### Planillas y presupuesto
- Tiller (una empresa de planillas de presupuesto, competidor directo) tiene los dos
  outliers más grandes de la corrida: "I've started 47 budgets. This is the one that
  stuck." (602x) y "POV: you don't use Tiller" (556x). Confesión y POV, no tutorial.
- "Work Smarter Not Harder in Google Sheets" (57x, Dean Stokes): un truco en un Short.
- "always all at once 😭 #emergencyfund" (54x, Lunch Money): dolor que todos conocen.
- Hipótesis V6: confesión/POV > tutorial para planillas.

## 2026-10-30 · Gemini G-003 (investigación web de Gemini, SIN VERIFICAR)
Texto completo en `gemini/outbox/G-003.md`; resumen en /mnt/project-files/plan/investigacion/2026-10-30-gemini-G-003-shorts-true-crime.md.
- Primera palabra antes de 0,5 s, sin intro. Shorts de 50-58 s y 130-145 palabras.
- Estructura: 0-3 gancho · 3-15 víctima, lugar, hora · 15-35 sospechosos con coartadas que chocan y un objeto clave · 35-48 quiebre y pregunta central · 48-60 el cierre le pasa la investigación al que mira.
- Estética de expediente sin rostro (corcho, polaroids, informes a máquina, sello rojo), plano nuevo cada 2-3 s, subtítulos palabra a palabra amarillo sobre negro. Música baja (-18 a -22 dB) y efectos de papel y obturador.
- Pasó a hipótesis V4 (duración), V9 (cierre), V10 (gancho) y V11 (ritmo). Más pedidos a Gemini: `scripts/gemini/bandeja.py pedir` (corre cada 6 h).

## 2026-10-31 · Gemini G-006 y G-007
Resumen en /mnt/project-files/plan/investigacion/2026-10-31-gemini-G-006-G-007-shorts-youtube.md; texto en `gemini/outbox/G-006.md` y `G-007.md`.
- Dato (API de YouTube): los 15 Shorts más vistos de @mrballenshorts duran 152-180 s. Los ganchos abren con fecha + edad + nombre + lugar (85 %), no con pregunta → V4 y V12.
- @coldcasedetective NO tiene Shorts (G-003 se equivocó): fuera como referencia de formato.
- Crítica de editor a nuestra estructura (sin verificar): nada de carátula en 0:00-0:02, primera palabra en el fotograma 1; plano o punch-in cada 2,5-3,5 s (V11); subtítulos ~25 % más arriba del borde, 2-3 palabras; voz -6 dB y cama -20 dB; cerrar con reto + bucle (V5, V9), no con "buy it on Etsy". 5 títulos propuestos en el resumen: pasan por `ai-side-hustle-seo-copy` antes de usarse.
- Para auditar un Short nuestro, la tarea a Gemini lleva su URL (`https://www.youtube.com/shorts/<video_id>` de `docs/viral/shorts.csv`): con ella da vistas, likes, transcripción y fotogramas aunque YouTube aún no lo indexe.

## 2026-11-01 · Corrida semanal cold case (competencia.py, 40 canales)
Reporte en `out/competencia/2026-11-01-coldcase/REPORTE.md` (no se commitea).
- Outliers reales del nicho: "The Tragic Disappearance of Michael Vaughan" (Criminal Core, 17x su mediana) y "Two Kids Afraid of the Dark Vanished From an Alaska Cabin — and Were Never Found" (Scary Mysteries, 5x). Confirma el título nombre/quiénes + lugar + "never found/came back" de la primera corrida; el Short del caso 02 (V12) ya lo usa.
- La búsqueda "murder mystery game shorts" trae Roblox Murder Mystery 2 (3 de 5 outliers): ruido. Se cambió por "printable murder mystery game" en `competencia.py`.
- Medianas: canales de true crime de 240 k-1 M subs rondan 2-12 mil vistas por Short; un canal chico de casos sin resolver (Unsolved Case Files, 7,9 k subs) tiene mediana 87. Nuestra vara realista los primeros meses: decenas a cientos.

## 2026-11-01 · Gemini G-015: ritmo segundo a segundo de MrBallen (SIN VERIFICAR)
Resumen en /mnt/project-files/plan/investigacion/2026-11-01-gemini-G-013-G-014-G-015-sondas.md; texto en `gemini/outbox/G-015.md`. 180 fotogramas de "The Signal" (5,66 M) y "Why You NEVER Camp Alone" (3,12 M).
- Gancho (V12): fecha + edad + nombre, y la primera prueba visual con rótulo entre 0:02 y 0:08.
- Voz: ~172 palabras/min, 188-196 en el gancho, sin silencios de más de 0,25 s (nuestra cola entre escenas es 0,3 s + whoosh: revisar si se prueba V11).
- Subtítulos: 1-4 palabras al 52 % de la altura, MAYÚSCULAS, blanco con borde negro; ámbar solo para nombres, fechas y peligro. Nunca abajo.
- Ritmo (V11): corte o punch-in cada 4,5-4,8 s de promedio, máximo 7-12 s sin corte, planos de 2-6 s en el último tercio. Choca con G-007 (2,5-3,5 s): medir, no elegir.
- Final (V5): corte en seco en la última sílaba, sin CTA ni pantalla final. Choca con nuestra regla de decir "ficción" y dónde encontrarlo: **no quitar el cierre** hasta que llegue G-016 (auditoría de uFgGEGATfA0 y cómo decir "juego imprimible" sin sonar a anuncio).

## Lo que dicen las guías (sin medir por nosotros: tratarlo como hipótesis)
- Shorts pueden durar hasta 3 minutos desde el 15-oct-2024; la compuerta de 58 s de
  `short` es por costumbre, no por regla de YouTube.
- Desde el 31-mar-2025 cada inicio o repetición cuenta como vista; "visto vs deslizado"
  solo está en YouTube Studio. Benchmarks de "viewed" (70-85 %) son de blogs, sin fuente oficial.
- Bucle: si el último frame empalma con el primero, la gente lo ve dos veces (vidIQ y otros;
  cifras como "2,7x vistas" no traen método).
- Series en partes con cliffhanger hacen seguir al canal (guías de true crime).
- Links en descripción y comentarios de Shorts no son clicables desde ago-2023; el link
  de "video relacionado" solo apunta a otro video del mismo canal y se pone desde
  YouTube Studio en escritorio.
- Política "inauthentic content" (15-jul-2025): castiga plantillas repetidas con voz IA
  y poco aporte humano; no prohíbe la voz IA.

Fuentes: tubefilter.com/2023/08/10/youtube-shorts-comments-spam,
vidiq.com/blog/post/youtube-related-links-connect-shorts-long-videos,
vidiq.com/blog/post/double-youtube-watch-time-looping-shorts,
creatoressentials.com/glossary/viewed-vs-swiped-away,
gulfnews.com (política de monetización 15-jul-2025),
fluxnote.io/guides/youtube-shorts-unsolved-cases-strategy.
