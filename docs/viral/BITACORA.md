# Bitácora del loop viral de Shorts

Regla: cada Short cuelga de una hipótesis de aquí. Se escribe antes qué se espera ver y
cuándo se lee. Al leer: GANA / PIERDE / EMPATE por Short, y CONFIRMADA (2 de 3 ganadas) o
DESCARTADA (2 perdidas) por hipótesis. Skill: `.claude/skills/shorts-viral-loop`.

## Reglas que funcionan (confirmadas con datos propios)
- (ninguna todavía: el canal empezó el 2026-10-30)

## Reglas puestas por Cris (no se prueban)
- 2026-10-30: los Shorts no son anuncios. Historia primero; el producto y el CTA solo al final.
- 2026-10-30: el canal tiene enlaces a la tienda de Etsy y a Gumroad en su cabecera (Cris los puso en YouTube Studio > Personalización). En Shorts el link de la descripción no es clicable, así que el CTA hablado puede decir "el link está en el canal" / "link on the channel". Probarlo contra "búscalo en Etsy" es una variable `cta`.

## Descartado
- (nada todavía)

## Hipótesis abiertas (orden = prioridad)

### V0. Línea base: historia narrada (true crime y "la historia detrás del villancico")
- Los 3 primeros Shorts en formato historia (hilo de videos, 30-oct): 56 Cold Case 01 EN
  (30-oct), 60 piano EN (31-oct), 56 Cold Case 01 ES (1-nov). Sin control: fijan la línea base.
- Lectura: 48 h y 7 días de cada uno. Primer resumen 2026-11-08.
- 2026-11-01, lectura 48 h: Metricool todavía da null en todas las métricas de YouTube (quedan pendientes). Conteo público de la página de YouTube: Cold Case 01 EN (uFgGEGATfA0) **0 vistas a 48 h**; piano Jingle Bells (zrc6EDVDS0A) **40 vistas a ~22 h**. Los dos son públicos, aptos para todo público y reproducibles: el de cold case no recibió reparto inicial. Hipótesis por revisar (sin probar): YouTube reparte menos el true crime a un canal nuevo, o el conteo público de Shorts va atrasado.
- 2026-11-02: Metricool sigue en null (también para el Cold Case ES, _BUAF1B1JXI). Conteo público: Cold Case 01 EN 1 vista a ~72 h; Jingle Bells 41 a 48 h. El piano es el que reparte: el Short del 3-nov (V13) va sobre piano para que la prueba tenga números.
- 2026-11-03 00:24 Chile (captura de Cris del canal, confirmada con la página pública a las 00:30): **Caso archivado ES (_BUAF1B1JXI) 672 vistas y 4 likes a ~35 h**; Jingle Bells 41; The Snow Remembers (V12, 2-nov) 38 a ~8 h; Cold Case 01 EN 1. Metricool sigue en null. El ES es el mismo guion, los mismos documentos, la misma música y el mismo cierre que el EN: cambian el idioma, la voz (Piper es_MX) y el día. Abre V15.
- 2026-11-03 14:10 Chile (conteo público; Metricool sigue en null): Caso archivado ES 676 a ~46 h (672 a ~35 h: se frenó); The Snow Remembers EN (EO-UvYWLfXA) 38 a ~25 h, igual que a ~8 h; Jingle Bells 41; Cold Case 01 EN 1. Patrón: cada Short recibe un solo empujón en las primeras ~12-24 h y después se queda quieto. Lo que se compara es ese empujón.
- 2026-11-04 14:10 Chile (conteo público; Metricool null): caso 02 EN 38 a 48 h (lectura V12/V15 cerrada con conteo público); Beethoven EN (V13, mpTOod1Sxp0) 25 a ~22 h; Caso archivado ES 676; Jingle Bells 41.

### V15. El mismo Short en español gana al inglés (abierta 2026-11-03, prioridad 1)
- Evidencia: par limpio V0. Cold Case 01 ES 672 vistas a ~35 h contra 1 vista del EN a 72 h; mismo video salvo idioma, voz y día de publicación. Un solo par: puede ser azar del reparto inicial, el país del canal (Chile) o menos competencia en true crime en español.
- Prueba: el caso 02 (The Snow Remembers) en español, con el mismo guion, documentos, gancho (fecha + edad + nombre + lugar), música y cierre que el EN del 2-nov (control, 38 vistas a ~8 h). Si el ES vuelve a ganar por 1,5x o más, se confirma con 2 de 3 en la tercera (caso 03 ES contra EN, o piano ES contra EN).
- Si se confirma: todos los Shorts salen primero en español, y el inglés pasa a ser la prueba.
- Pruebas en curso: caso 02 ES (4-nov, post 414802164) contra caso 02 EN (38 a 48 h); Beethoven ES (5-nov, post 416793981) contra Beethoven EN (25 a ~22 h). Se leen el 6 y el 7-nov.
- Hipótesis rival (G-021, según Gemini, sin verificar): el cold case EN no recibió muestra semilla por título sin entidades conocidas y "killed" al inicio. V15 la debilita: el ES tiene el mismo nombre ficticio y "¿quién mató...?" y sacó 672. Si el caso 02 EN (fecha + lugar en el gancho) sube y el ES no, revisar.

### V1. Cold case: el reto interactivo gana a la historia narrada
- Evidencia: outliers de participación ("If you laugh you lose", "Guess the Animal",
  "Imagine playing tag... but not knowing who the taggers are?" 530x). El producto es un juego.
- Prueba: el mismo caso en formato reto: muestra 2-3 documentos reales del expediente y
  pregunta "una de estas declaraciones es mentira: ¿cuál?". La respuesta no se da (va
  en el juego, o en un Short "parte 2" al día siguiente). Nunca la solución del PDF.
- Se espera: más comentarios por 1.000 vistas y retención > 100 % (la gente mira de nuevo).
- Control: el Short de historia del mismo caso.

### V2. Piano: el tutorial con letras gana a la historia del villancico
- Evidencia: en piano, todos los outliers son tutoriales fáciles con las letras de las
  notas en pantalla (Amazing Grace 9,6x, Do-Re-Mi 18x). Es lo que vende el libro.
- Prueba: teclado de arriba, notas que caen con su letra, la melodía de la pista de
  práctica del libro; título = primera línea de la canción + "easy piano letter notes".
- Control: 60 piano EN (historia de Jingle Bells).

### V3. Serie en 2 partes (cliffhanger) gana a la historia completa
- Evidencia: guías de true crime; el corte deja un bucle abierto que trae a la parte 2.
- Prueba: caso 02 o 03 contado en parte 1 (hasta el giro) y parte 2 al día siguiente.
- Métrica: vistas de la parte 2 / parte 1 y suscriptores ganados esos 2 días.

### V4. Duración: 45-75 s gana a 25-35 s en historias
- Evidencia nueva 2026-10-31 (Gemini G-006, cifras de la API de YouTube): los 15 Shorts más vistos de @mrballenshorts (231 mil a 6,36 M) duran TODOS 152-180 s. Siguiente escalón a probar si 45-75 s gana: 120-170 s.
- Evidencia: Shorts pueden durar hasta 3 min; el tiempo total visto suma. Sin dato propio.
- Prueba: misma estructura con más hechos. Métrica: duración media vista (s) y vistas.
- Requiere subir la compuerta de 58 s de `short` (avisar al hilo de videos).

### V5. Final en bucle gana a final cerrado
- Prueba: la última frase empalma con la primera ("...and that's why nobody believed
  her when she said:" → "Who killed Desmond Ashcombe?"). Métrica: retención > 100 %.
- Variante G-015 (Gemini, 2026-11-01, sin verificar): corte en seco en la última sílaba, sin pantalla final. Choca con decir "ficción" y dónde está el juego: no se quita el cierre hasta la respuesta de G-016.

### V6. Planillas: confesión o POV gana a tutorial
- Evidencia: Tiller "I've started 47 budgets..." 602x y "POV: you don't use Tiller" 556x.
- Prueba: Short de presupuesto o deudas en formato confesión. Control: un tutorial.

### V7. Español rinde distinto que inglés con el mismo guion
- Prueba: ya corre con 56 EN vs 56 ES. Métrica: vistas y retención a 7 días.

### V8. El Short mueve el listing en Etsy
- Métrica: vistas del listing (serie/etsy.csv) 72 h después vs 72 h antes, y clics
  salientes del pin de video del mismo Short. Se lee en cada Short; con tráfico chico,
  se suma por mes.

### V9. Cold case: cierre "el expediente sigue abierto" gana a "puedes resolverlo tú"
- Evidencia: Gemini G-003 (2026-10-30, sin verificar; canales MrBallen Shorts, Explore With Us, Cold Case Detective): el CTA que sigue la historia ("The file remains open... can you solve what detectives missed?") en vez de vender. Detalle en plan/investigacion/2026-10-30-gemini-G-003-shorts-true-crime.md.
- Prueba: misma historia, solo cambia la última frase (sigue el aviso de ficción). Métrica: comentarios/1.000 y vistas del listing en Etsy.

### V10. Gancho de contradicción gana a la pregunta "¿quién lo mató?"
- Evidencia: Gemini G-003 clasifica 10 ganchos; contradicción y "tú eres el detective" arriba. Sin verificar.
- Prueba: primera frase "Everyone had an alibi. One of them was lying." vs la pregunta del V0. Métrica: retención y vistas 48 h.

### V11. Cambio de plano cada 2-3 s gana a escenas de 4-6 s
- Evidencia: Gemini G-003 (ritmo de los canales de expediente). Hoy el pipeline cambia por frase (~4 s).
- Prueba: partir cada escena en 2 planos del mismo documento (foco distinto). Métrica: retención.
- G-015 (Gemini, 2026-11-01, sin verificar) mide otra cosa en MrBallen: corte cada 4,5-4,8 s de promedio, máximo 7-12 s sin corte, 2-6 s en el último tercio, y voz a ~172 palabras/min sin silencios de más de 0,25 s. Si V11 gana a 2-3 s, probar después 4,5 s con subtítulos al 52 % de la altura.

### V12. Gancho "fecha + edad + nombre + lugar" gana a la pregunta
- Evidencia: Gemini G-006 (2026-10-31): el 85 % de los 15 Shorts más vistos de MrBallen abre así ("On July 28th, 1984, 25-year-old Brigitta Fredenhagen arrived at Yellowstone..."), casi nunca con pregunta. Ganchos literales en el Sheet "G-006 shorts" (Drive > Side Husle Claude > Gemini > Entregas).
- Prueba: misma historia, primera frase con fecha (en letras en `dice`), edad, nombre y lugar del expediente vs. la pregunta del V0. Métrica: retención y vistas 48 h. Compite con V10 (contradicción): probar V12 primero, tiene más evidencia.
- G-015 (Gemini, 2026-11-01, sin verificar) suma: la primera prueba visual con rótulo entre 0:02 y 0:08, y el gancho más rápido (188-196 palabras/min).

### V13. Voz continua (huecos de ~0,2 s) gana a escenas con ~1,1 s de silencio
- Evidencia: Gemini G-016 (2-nov, auditoría de uFgGEGATfA0): seis silencios de ~1 s, 147 palabras/min efectivas contra ~172 de MrBallen (G-015). **Verificado por nosotros** (2-nov): Kokoro deja ~0,3 s al inicio y ~0,45 s al final de cada frase, y el pipeline suma 0,15 + 0,3 s: ~1,1 s entre escenas.
- Prueba: `"ritmo": "continuo"` en el plan (recorta la voz y deja ~0,2 s entre escenas); todo lo demás igual a un control ya publicado. Métrica: retención y vistas 48 h.
- Si gana, pasa a ser el default del pipeline.

### V14. Cierre diegético gana a la tarjeta de producto
- Evidencia: Gemini G-016 (sin verificar): la tarjeta final muda de 7,5 s saca a la gente; propone seguir en el expediente hasta el final (sello "FICTIONAL CASE FILE · PRINTABLE GAME", voz "...print the case file from SheetSmithChile on Etsy and tell us who killed <nombre>", corte en seco en el nombre, subtítulos hasta el final). Cumple la regla de decir ficción y dónde está el juego.
- Prueba: mismo formato, cierre diegético contra la tarjeta. Necesita cambiar la escena de cierre de `Short` (todavía no existe). Variante de V5.

## Registro de lecturas
| Fecha | Short | Lectura | Vistas | Retención | Coment./1k | Shares/1k | Veredicto | Nota |
|---|---|---|---|---|---|---|---|---|

