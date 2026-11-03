# Diario de decisiones

## 2026-10-30 · Nace el pipeline (hilo "Montar videos con Remotion para Shorts y Etsy")
- Cris dejó NLPAGE (repo muerto) como repo de redes sociales y Videos-Next-Layer como
  referencia de solo lectura. Aclaró que la marca Next Layer no es la nuestra: se copió
  la técnica (Remotion, efectos medidos con el pico en el corte, ducking, -14 LUFS,
  revisión por GUION, tipografías locales) y se rehízo la parte de marca y de material.
- Diferencia de fondo: Next Layer edita clips de cámara con voz; aquí no hay cámara.
  El material son las páginas del PDF y las fotos del listing, y la voz es IA.
  Por eso se reescribió el pipeline en vez de adaptar buildReel/ingest.
- Decidido: Kokoro (EN) + Piper (ES), faster-whisper para tiempos, incompetech para
  música, audio propio cuando el producto lo trae. Detalle en docs/herramientas.md.
- Primeros videos: Short de Cold Case 01 en inglés y español, Short de partituras de
  piano (EN), y videos de listing 4:3 + GIF de #56 y #60.
- Espera a una persona: que Cris conecte el canal de YouTube en Metricool.

## 2026-10-30 · Videos de listing para el resto del catálogo de juegos y piano
- Pedido del hilo de operación: loops de Etsy para #57, #58, #59, #61, #62 y #55, en ese
  orden. Hechos y dejados en /mnt/project-files/videos/2026-10-30/ (operación los sube).
- Temas nuevos: `clasicos` (azul marino y dorado) para #62 y `navidad` (rojo y dorado,
  el mismo del piano) para #55. El pack #59 mezcla páginas de los tres casos.
- Arreglo: `producto` tomaba el sobre sellado "-EN-ES.pdf" como versión en español y
  pisaba sus páginas; ahora queda con alias `enes`.
- #55: solo páginas de juego; las de pistas y respuestas quedan fuera (regla 1).
- Descartado por ahora: Shorts de estos seis. Primero ver si los de #56 y #60 traen
  vistas cuando el canal esté conectado.
- Espera a una persona: que Cris conecte el canal de YouTube en Metricool.

## 2026-10-30 · YouTube conectado; primeros Shorts programados
- Cris conectó su canal (Cristobal De Vidts) en Metricool. Programados por el conector,
  16:00 hora Chile: #56 EN hoy, #60 EN el 31-oct y #56 ES el 1-nov.
- El MP4 se pasa como URL de raw.githubusercontent fijada a un commit: Metricool la
  aceptó y la copió a su CDN. No hizo falta hosting aparte.
- Declarado como contenido sintético (voz IA) en los tres.
- Espera: ver vistas de los tres antes de hacer Shorts de los otros productos.

## 2026-10-30 · Loop viral de Shorts (hilo "Crear sistema de viralidad para Shorts")
- Pedido de Cris: buscar lo que ayude a la viralidad, anotar lo probado y armar una
  skill del loop de prueba y retroalimentación. Nace `.claude/skills/shorts-viral-loop`,
  `docs/viral/` (BITACORA.md y shorts.csv) y `scripts/viral/` (competencia.py y experimento.py).
- Investigación con `competencia.py` (yt-dlp sobre listados públicos, sin cuenta): en
  piano ganan los tutoriales con letras de notas; en cold case, el documento del
  expediente como gancho; en planillas, confesión y POV (Tiller 600x). Detalle en
  `references/patrones.md`.
- Descartado: bajar la página de cada video o sus subtítulos (YouTube pide "no soy un
  bot" desde el contenedor; no se esquiva), YouTube Analytics API (OAuth de Cris),
  y las cifras sin fuente de skills ajenas como reglas.
- Espera a una persona: nada. El hilo de videos registra cada Short con `experimento.py alta`.

## 2026-10-30 · Los Shorts pasan a ser historias (pedido de Cris)
- Cris: los Shorts eran anuncios; sirven para Etsy, no para viralizar. Rehechos los tres
  como historia: el Cold Case 01 contado como true crime (EN y ES), con "este caso es
  ficción, pero lo puedes resolver tú" solo en el cierre; el de piano cuenta que Jingle
  Bells fue la primera canción tocada en el espacio (Gemini 6A, 1965) y que no se
  escribió para Navidad, con fotos de NASA (dominio público).
- Los anuncios quedaron en renders/ como referencia; no se publican.
- Cierre sin "link in the description" (en Shorts no es clicable): "Find it on Etsy,
  at SheetSmithChile".
- Titulares de 1 línea y sin rótulos encima: los de 2 líneas chocaban con la etiqueta.
- El cierre ES usa la portada en español (antes salía la foto en inglés).
- Entra el loop viral del hilo de viralidad (skill shorts-viral-loop); estos tres son V0.

## 2026-10-30 · Gemini desde el contenedor (cuenta Google AI Pro de Cris)
- El plan AI Pro no trae API: sus cuotas valen en las apps y en AI Studio web. Lo que sí
  llega a la API son US$10/mes de créditos de Google Cloud (hay que activarlos).
- Adoptado: API key de AI Studio + `scripts/gemini/gemini.py` (texto, voz, diálogo gratis;
  imagen y video con `--pago` y tope mensual). Voz `gemini:<Voz>` opcional en los planes.
- Descartado: notebooklm-py (cookies de la cuenta que entrega las planillas) y Veo 3.1
  preview (apagado el 22-oct; lo reemplaza Gemini Omni Flash).
- Espera a una persona: Cris crea la clave y la deja como GEMINI_API_KEY en el entorno.

## 2026-10-30 · Canal con la app de Gemini a través del repo (pedido de Cris)
- Cris quiere darle a Gemini una tarea programada que revise el repo y hacer "una carpeta con
  prompts" para usar su poder (Deep Research, Veo, NotebookLM) desde Claude.
- Verificado en la ayuda oficial de Google: la app de Gemini lee repos de GitHub pero NO escribe
  en ellos; sí crea Google Docs y archivos en Drive desde una Tarea programada (AI Pro). Por eso
  el canal es mixto: `gemini/inbox` + `PENDIENTES.md` en main (lo que lee Gemini) y respuestas
  como Docs en Drive > Side Husle Claude > Gemini > Respuestas, que Claude copia a `gemini/outbox`.
- Hecho: `scripts/gemini/bandeja.py` (pedir, pendientes, recibir, cerrar, mostrar, estado), skill
  `gemini-canal`, protocolo en `gemini/README.md`, prompt de la tarea para Cris en
  `gemini/PROMPT-TAREA-GEMINI.md`, 5 tareas iniciales (G-001 sonda de capacidades, G-002 y G-003
  Deep Research de competencia Etsy y de canales de Shorts, G-004 Veo, G-005 NotebookLM).
- Descartado: pedirle a Gemini que haga commits o issues (no puede); schedules clásicos de chat
  (solo dejan texto en el chat); Gmail (Gemini no envía correos).
- Espera a una persona: Cris pega el texto de `gemini/PROMPT-TAREA-GEMINI.md` en una Tarea de
  Gemini (una vez). La primera respuesta (G-001) dirá qué herramientas funcionan de verdad.

## 2026-10-30 · Gemini respondió las 5 tareas: qué puede y qué no
- Cris activó la Tarea ~16:30 UTC; Gemini corrió a las 17:37-17:43 UTC y dejó los 5 Docs en
  Respuestas. Recogidos con `bandeja.py recibir` a `gemini/outbox/`.
- Aprendido (G-001): NO lee la URL raw de GitHub (usó el espejo de Drive: ahora es obligatorio);
  sí navega y busca en la web, crea Docs/Sheets/PDF en Drive, genera imágenes (Nano Banana) y
  cuadernos de NotebookLM. NO tiene Veo (G-004), Audio Overview (G-005) ni Canvas; "Deep
  Research" como herramienta no existe en la tarea, pero investiga con búsqueda (G-002, G-003
  salieron como `parcial` y son útiles).
- G-002 (competencia Etsy en misterios): los líderes venden a US$4.50-6 con oferta permanente
  del 40-55%, títulos que abren con "Printable Murder Mystery Game" / "Printable Cold Case File",
  foto 1 flat-lay con badges, tags "date night" y "solo", micro-casos a US$3. Pasa a OPS como
  hipótesis (sin verificar).
- G-003 (Shorts true crime): primera palabra antes de 0,5 s, 50-58 s y 130-145 palabras,
  estética de expediente sin rostro, CTA como continuación del juego. Pasa al loop viral.
- Descartado: pedirle video o audio a la app de Gemini. Espera a una persona: nada.

## 2026-10-30 · Gemini cada hora y reglas de Cris para el canal
- Cris (17:53 UTC) puso la tarea de Gemini cada hora y pidió: usarla bastante (sin la API es casi
  ilimitada), exigir siempre un modelo fuerte (Gemini 4 Argon), que Gemini converse con Claude y no
  le reporte a Cris, que Claude haga que Gemini mejore y siga probando capacidades, y explotar su
  lectura de YouTube.
- Hecho: encabezado de PENDIENTES.md con "quién te habla", modelo más capaz, `modelo:` en la línea 3
  y sección "Sugerencias para Claude"; `recibir` guarda el modelo en registro.csv; aviso si la cola
  baja de 3; `gemini/CAPACIDADES.md`; reglas en README y skill; 6 tareas nuevas en cola: G-006
  YouTube (Shorts más vistos de MrBallen Shorts y Cold Case Detective, ganchos, Sheet), G-007 nuestro
  canal y crítica del Short, G-008 verificar en página los 8 competidores de G-002, G-009 Pinterest,
  G-010 imágenes flat-lay (Nano Banana), G-011 automejora semanal.
- Turno diario del canal (12:07 Chile) en el hilo "Conversar con Gemini a través del repo": recoger,
  repartir, rellenar la cola, automejora los lunes.
- Descartado: pedirle a Cris que vuelva a pegar la tarea (las reglas van en PENDIENTES.md).
- Espera a una persona: nada.

## 2026-10-31 · Turno diario del canal Gemini: 6 respuestas, protocolo con cupo de búsqueda
- Llegaron las 6 (G-006..G-011) en la ejecución de las 18:08-18:30 UTC del 30-oct, todas con `modelo:`
  ("Gemini 2.5 Pro, entorno programado"; dice que no puede elegir Argon/Deep Think desde dentro).
  Recogidas a `gemini/outbox/`, resúmenes en plan/investigacion/2026-10-31-gemini-G-006-G-007-* y
  G-008-*; G-009 quedó `no-puedo` (Pinterest pide sesión + se agotó el cupo de búsqueda).
- Aprendido: ~10-12 llamadas a google:search/browse por ejecución (THROTTLED_ROLE_LIMIT); YouTube por
  URL/video_id da vistas, likes, transcripción y fotogramas; Etsy y Pinterest bloquean browse; Nano Banana
  sí (2 PNG 4:3 en Entregas); Python sin red con Pillow/reportlab/openpyxl; puede subir binarios.
- Hecho: regla 1b en PENDIENTES.md (máx. 2 tareas de búsqueda web por hora, marca `Búsqueda web: sí/no`
  por tarea), CAPACIDADES.md y README al día, skill: IDs directos en cada tarea. Cola: G-012 Pinterest
  (sola), G-013 navegador autónomo en la tienda, G-014 PDF de recorte 1987 con Python, G-015 ritmo visual
  de 2 Shorts de MrBallen.
- Descartado: pedir Gmail de Etsy (datos de compradores); Calendar/Keep. Gemini relevó una "nota de
  Cris" sobre recursos de diseño de Apple: va al coordinador como dato sin verificar, no es de esta tienda.
- Espera a una persona: si Cris quiere otro modelo que "2.5 Pro", es en la app (la tarea no lo elige).

## 2026-11-01 · Canal Gemini: 4 respuestas en 45 min; Pinterest y navegador descartados, Python y fotogramas confirmados
- G-012: el índice de google:search excluye pinterest.com (no era cuota): Pinterest queda fuera de Gemini;
  trajo 24 páginas de destino y 3 reglas de pines (a Canales). G-013: navegador autónomo devuelve `<empty>`
  en tareas programadas; solo 4 de 40 listings indexados en Google. G-014: Python en sandbox + subida
  binaria funcionan (recorte 1987 en PDF/PNG verificado); sin reportlab. G-015: 180 fotogramas por Short,
  5 reglas de edición de MrBallen (al loop viral).
- Cola: G-016 auditoría de nuestro Short uFgGEGATfA0, G-017 sonda de miniaturas desde i.etsystatic.com,
  G-018 tres props genéricos (telegrama, ficha de hotel, informe forense), G-019 títulos de Año Nuevo en
  Google para H2.
- Resúmenes: plan/investigacion/2026-11-01-gemini-G-012-* y G-013-G-014-G-015-*. CAPACIDADES.md y README al día.
- Descartado: pedir Pinterest o navegador a Gemini. Espera a una persona: nada. Mañana (lunes): automejora 2.

## 2026-11-01 · Turno diario: primera lectura y Short V12

- Lectura 48 h: Metricool sigue en null para YouTube (pendiente). Conteo público: Cold Case 01 EN 0 vistas a 48 h, Jingle Bells 40 a ~22 h. Anotado en V0 de la bitácora.
- Short del 2-nov: caso 02 "The Snow Remembers" (EN), prueba V12 (gancho fecha + edad + nombre + lugar). Misma voz, música y cierre que el control; el confusor es el caso. 54,6 s, -14 LUFS, pico -1,4 dBTP. Metricool post 413095557, 2-nov 16:00 Chile.
- Arreglado: la compuerta de voz castigaba "nineteen eighty-nine" porque whisper escribe "1989"; ahora compara números y años en inglés en letras. setup instala yt-dlp (la corrida de competencia de los domingos fallaba sin él).
- Descartado: repetir el caso 01 con otro gancho (subir dos veces casi el mismo video arriesga "contenido reutilizado").
- Espera a una persona: nada.

## 2026-11-02 · Canal Gemini (lunes): 4 respuestas, miniaturas a Drive por Zapier, automejora 2 en cola
- G-016 (Short Cold Case 01 fotograma a fotograma): 147 WPM por seis silencios de 1 s, subtítulos al 79%,
  último tercio estático y tarjeta muda de 7,5 s; tres cambios y un cierre diegético (al hilo de videos).
  G-017: `no-puedo`, browse no acepta image/jpeg. G-018: telegrama, ficha de hotel e informe forense en
  PDF+PNG 300 DPI (a juegos). G-019: nuestro bundle NYE es #5 en Google con "2027"; frecuencia de
  palabras y 3 títulos para H2 (a OPS, lectura 5-nov).
- Aprendido: para que Gemini vea imágenes hay que subirlas a Drive; la acción de Zapier "Google Drive:
  Upload File" las sube desde la URL pública a resolución completa (9 fotos en Gemini > Miniaturas).
  Pegar base64 por `create_file` corrompió 2 de 5 archivos: descartado.
- Cola: G-020 automejora semanal 2 (autocrítica G-012..G-019, fallos, capacidades sin probar, modelo),
  G-021 auditoría del Short de piano zrc6EDVDS0A vs Cold Case 01 (40 vistas vs 0), G-022 auditoría de
  las 9 miniaturas desde Drive, G-023 títulos "Printable Murder Mystery Game" en Google para retitular
  Cold Case 02/03 tras el 5-nov. Solo G-023 usa búsqueda web.
- Resúmenes: plan/investigacion/2026-11-02-gemini-G-016-*, G-018-*, G-019-*. Espera a una persona: nada.

## 2026-11-02 · Turno diario: G-016, V13 y Short de Beethoven

- G-016 (auditoría de Gemini del Short cold case 01) verificada en lo medible: entre escenas había ~1,1 s de silencio (Kokoro ~0,3 s al inicio y ~0,45 s al final, más 0,45 s del pipeline). Nuevo `"ritmo": "continuo"` en los planes (V13); V14 (cierre diegético) queda anotada.
- Lecturas: Metricool sigue en null para YouTube; conteo público cold case 01 EN 1 vista a ~72 h, Jingle Bells 41 a 48 h.
- Short del 3-nov: #62 partituras clásicas, historia del estreno de la Novena (Viena 1824, Beethoven sordo, Unger lo da vuelta) con ritmo continuo: 40,9 s contra ~47 s con el ritmo viejo. Control: Jingle Bells. Hechos de Wikipedia; grabado de Offterdinger (dominio público). Metricool post 414317939.
- Se eligió piano porque es lo único que YouTube está repartiendo; una prueba sobre cold case con 0-1 vistas no mide nada.
- Wikimedia Commons limita las descargas (429): sale una cada pocos minutos. Espera a una persona: nada.

## 2026-11-03 · El Short en español ganó: V15

- Captura de Cris (3-nov 00:24 Chile), confirmada en la página pública: Caso Archivado ES 672 vistas y 4 likes a ~35 h; el mismo video en inglés, 1 vista. Jingle Bells 41, The Snow Remembers EN 38 a ~8 h. Metricool sigue en null para YouTube.
- Nueva V15 (español gana a inglés), prioridad 1. Short del 4-nov: el caso 02 en español, mismo video que el EN del 2-nov (control). El gancho ES deja edad y lugar para la escena 2 porque los números en letras pasan las 12 palabras. Metricool post 414802164.
- La compuerta de voz ahora pasa números y años en español a letras.
- Descartado por ahora: rehacer el Beethoven (3-nov) en español; sale como está y se compara después.
- Espera a una persona: nada.

## 2026-11-03 · Canal Gemini: G-020..G-023 en una hora; Gemini ya ve imágenes desde Drive
- G-020 (automejora 2): autocrítica útil y 4 reglas de protocolo, ahora en PENDIENTES.md como 1c
  (agrupar hasta 4 queries por llamada, site:etsy.com/listing, nada de browser agent ni browse sobre
  imágenes/Etsy/Pinterest). Modelo sigue "2.5 Pro". G-021: piano 41 vistas vs cold case 1; hipótesis
  seed shelf + gancho visual; detectó un fotograma vacío en 00:15 (hueco entre Sequences) → hilo de videos.
  G-022: vio las 9 miniaturas desde Drive y montó la grilla 170 px; con recorte cuadrado 7 de 9 pierden
  texto; ranking y 3 cambios (lienzo 1:1) → OPS. G-023: 25 fichas reales con site:etsy.com/listing,
  frecuencia de palabras y 6 títulos para Cold Case 02/03 → OPS (H8 tras el 5-nov).
- Cola: G-024 audio en la VM (piano + Morse), G-025 fondos 1:1 Nano Banana para rehacer miniaturas,
  G-026 títulos de piano por snippets (única de búsqueda), G-027 HTML+Chromium vs pdflatex.
- Resúmenes: plan/investigacion/2026-11-02-gemini-G-021-*, G-022-*, G-023-*. Espera a una persona: nada.

## 2026-11-03 (tarde) · G-021: frame vacío arreglado
- Llegó G-021 de Gemini (piano contra Cold Case 01 EN). Verifiqué su hallazgo concreto: a los 15,5 s del Short de piano había un frame vacío, porque la imagen nueva entraba con opacidad 0 justo después de un corte seco. En `src/components/Visual.tsx` las imágenes y portadas ahora entran desde 0,55; revisé con `remotion still` los frames 464-466 y la imagen ya se ve desde el primero. Vale desde el próximo render; los Shorts ya programados (3 y 4-nov) quedan como están.
- Su hipótesis de "muestra semilla por entidad en el título" la anoté como rival de V15, pero el ES del caso 01 (mismo título traducido, mismo nombre ficticio) la debilita.
- Las otras ideas (una página distinta por escena, cierre de ~3,5 s) van al próximo Short de piano. Las pausas largas ya las prueba V13.

## 2026-11-03 (turno diario) · Solo medir
- El 4-nov ya tiene Short (caso 02 ES, post 414802164), así que hoy no se hizo otro. Lecturas públicas: Caso archivado ES 676 (se frenó después de las ~35 h), caso 02 EN 38 a ~25 h (igual que a ~8 h), Jingle Bells 41, Cold Case 01 EN 1. Metricool sigue en null.
- Cada Short recibe un solo empujón en sus primeras horas. Mañana, con el caso 02 ES, se compara ese empujón contra los 38 del EN.
