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

## 2026-11-04 · Canal Gemini: G-024..G-027 hechas; audio, fondos 1:1, títulos de piano y PDF vectorial
- Las 4 llegaron en ~25 min (12:53–13:17 del 3-nov), todas "hecho", modelo declarado 2.5 Pro. G-024: la VM
  sintetiza audio (numpy/scipy/ffmpeg; sin soundfonts) y subió piano 15 s + radio con Morse; G-025: 4 fondos
  1:1 a 1024 px con zona central limpia declarada; `image_references` no toma fotos de Drive (rodeo: hex de la
  paleta en el prompt); G-026: 24 fichas de piano por snippets y 9 títulos → OPS tras el 5-nov; G-027: pdflatex
  y Chromium por CDP; recomienda HTML+Chromium para texto y HTML→300 DPI→Pillow para papel viejo.
- Nada de lo entregado se ha mirado ni escuchado desde acá (bajar binarios por el conector es caro): quien lo
  use lo baja de Drive y lo revisa. Resúmenes: plan/investigacion/2026-11-04-gemini-G-024..G-027-*.
- Cola nueva: G-028 títulos de escape room de Navidad (búsqueda, alta), G-029 diez Shorts de true crime en
  español por fotogramas (búsqueda, para el hilo de videos), G-030 plantilla HTML de recorte de prensa 1987 +
  script de envejecido (sin texto de casos). Espera a una persona: nada.

## 2026-11-04 (turno diario) · Beethoven en español para el 5-nov
- Lecturas: caso 02 EN 38 a 48 h; Beethoven EN 25 a ~22 h; Metricool sigue en null.
- Short del 5-nov: Beethoven en español (`plans/62-piano-clasicos-historia-es.json`). Es la tercera prueba de V15: misma historia, imagen, música propia y ritmo continuo que el EN, con voz Piper es_MX y el libro Do Re Mi. Va programado en Metricool (post 416793981).
- Piper leía "Beethoven" de forma que whisper oía "Bambé Tobén". Agregué `"pronuncia"` al plan: cambia lo que lee la voz ("Bitóven") sin tocar el subtítulo, una palabra por una palabra. Después de eso whisper oyó "van Beethoven".
- copy_check.py marca errores de Etsy (tags de 20 caracteres, frase al inicio, frase repetida con la ficha). Para YouTube no aplican; el título sigue la regla de la skill: gancho con la frase principal ES dentro.
- El mp4 pesa 53 MB, más que los anteriores. GitHub avisa desde 50 MB y rechaza desde 100 MB. Si sigue creciendo, bajar el bitrate del render.

## 2026-11-06 · Canal Gemini: G-031..G-034 en 50 min; certificado verificado; cola G-035..G-038

- Las 4 tareas del 5-nov llegaron entre 16:56 y 17:47 UTC con "Argon / Gemini 3.1 Pro" y Docs con texto.
  G-031 (35 fichas de trivia, 3 títulos de 134-139 car.) → OPS. G-032 (desglose por segundo de los dos
  Shorts ganadores + esqueleto de 45 s) y G-034 (auditoría de nuestros 3 Shorts: 5 errores de TTS en el
  caso 01 ES, cierre comercial en s 40/39/47, croquis fijo 8 s, propuesta de últimos 8 s sin CTA) → hilo
  de videos. G-033 certificado de detective: html + sello.py bajados a `gemini/codigo/G-033/` y probados
  acá (Playwright 3 s, sello 2 s; demo ES en el README); rótulos fijos de cabecera en inglés → traducir.
- Cola: G-035 bingo navideño (búsqueda + 4 ilustraciones de prueba estilo libro infantil años 60, para
  saber si "huelen a IA"), G-036 guion 45/30 s del caso 02 con hechos públicos, G-037 auditoría de
  pronunciación del TTS con reescrituras para "pronuncia", G-038 sonda de traducción DE/FR/IT/PT-BR.
- Espera a una persona: nada.

## 2026-11-06 · API de Gemini: Argon e imágenes son pagados; YouTube por fotogramas gratis y al instante

- Cris dio una hora libre (10:59-12:00 UTC) y pidió probar la API (GEMINI_API_KEY) en vez del canal por
  Drive, sin agregar facturación. Leído ai.google.dev/gemini-api/docs/pricing: `gemini-4-argon`,
  `gemini-3.1-pro-preview` y TODOS los modelos de imagen (Nano Banana 2 Lite/2.1/Pro, 2.5 Flash Image)
  tienen "Free Tier: Not available". No se llamó a ninguno (countTokens no gasta y no distingue tier).
  Los US$10/mes de AI Pro exigen activar Cloud Billing con tarjeta: no se toca.
- Lo que sí es gratis y nuevo: `gemini.py youtube <id>` (generateContent con file_data de YouTube).
  3.6 Flash audita un Short de 46 s en 24-42 s con tabla por segundo, cortes, palabras/s y punto de
  abandono. Hecho con los 3 Shorts nuestros y el competidor de 12,1 M: docs/viral/2026-11-06-gemini-api-
  youtube-auditoria-shorts.md (copia en plan/investigacion/). 3.8 Flash dio 503 (alta demanda) y
  2.5 Pro ya no existe para cuentas nuevas (404): la cadena de respaldo sigue valiendo.
- Reparto de roles desde hoy: app de Gemini (canal por Drive, cada hora) para Argon, Nano Banana, búsqueda
  web y entregas en Drive; API para ver videos de YouTube al instante, texto y voz.
- Espera a una persona: nada.

## 2026-11-05 · Metricool sin cupo
- El hilo de canales avisó, y lo comprobé en getScheduledPosts, que el plan gratis de Metricool trae 20 publicaciones por mes. Desde el 4-nov 20:45 todo falla con "account limit". El caso 02 ES alcanzó a salir (7CZBpp1r4kU); el Beethoven ES del 5-nov va a fallar.
- Ruta nueva: Zapier YouTube. Hoy no tiene conexión y Cris tiene que conectarla una vez; ese pedido lo hace canales. Hasta entonces el turno diario solo mide y deja a lo más un Short en `docs/viral/COLA.md`. El prompt del turno ya está actualizado.
- G-029 (true crime en español) pasó a patrones.md y a V14. Pedí a Gemini G-034, la auditoría del Caso archivado ES contra los EN.

## 2026-11-05 · Canal Gemini: G-028..G-030; el modelo ya se declara Argon; el recorte de prensa corre acá
- G-028 (escape room de Navidad): el Doc llegó vacío pero la Hoja trae 31 fichas, frecuencias y 3 títulos
  de 133 car. → OPS (es de temporada; nadie del mercado dice "bilingüe"). G-029: 14 Shorts de true crime
  en español por fotogramas; los ganadores no tienen CTA comercial, subtítulo de una palabra gigante arriba,
  15–62 s → hilo de videos. G-030: plantilla HTML de recorte 1987 + envejecer.py; bajados con
  download_file_content y probados acá (Playwright 3 s + Pillow 4 s): `gemini/codigo/G-030/`.
- Desde el 4-nov 17:34 UTC las respuestas declaran "Argon / Gemini 3.1 Pro" (autodeclarado).
- Cola nueva: G-031 títulos de trivia navideña (búsqueda), G-032 desglose segundo a segundo de los dos
  Shorts ganadores (YouTube por id), G-033 certificado de detective bilingüe en HTML (sin texto de casos),
  y G-034 (prioridad alta, pedida por el hilo de videos a las 15:21 UTC): auditoría por segundo de nuestros
  tres Shorts (_BUAF1B1JXI 676 vistas vs uFgGEGATfA0 1 vs EO-UvYWLfXA 38), solo evidencia del video, más
  un cierre de 45 s sin CTA hablado con "ficción" en pantalla. PR #28 fusionado (squash) con todo esto.
- Espera a una persona: nada.

## 2026-11-05 (turno diario) · Solo medir
- YouTube todavía no está conectado en Zapier y Metricool no tiene cupo, así que no hubo Short nuevo. Beethoven ES sigue primero en `docs/viral/COLA.md`.
- V13: Beethoven EN 26 a 48 h contra 41 del control. Por regla es PIERDE, pero hay confusor (otra pieza, sin Navidad).
- V15: la primera señal va en contra. Caso 02 ES 7 a ~25 h, contra 38 del EN. Se lee mañana a 48 h.

## 2026-11-05 (tarde) · Primer Short por Zapier
- Cris conectó YouTube en Zapier. Beethoven ES salió a las 17:21 Chile (6TOTGMLBNLc) con `upload_video`, usando la URL raw fija del commit como archivo. Fue más tarde que las 16:00 de los anteriores: es un confusor menor que queda anotado en shorts.csv.
- Zapier no tiene el campo de "contenido alterado o sintético" que mandaba Metricool. La voz es TTS sobre un grabado, no una persona realista, así que no aplica.
- Desde ahora el turno diario sube el Short al terminar (~14:30 Chile) en vez de programarlo a las 16:00.

## 2026-11-05 (noche) · V15 confirmada
- Captura de Cris a las 20:25 Chile: Beethoven ES 148 vistas en ~3 h, contra 26 del EN a 48 h. Con eso V15 queda en 2 de 3 (caso 01 gana, caso 02 pierde, Beethoven gana) y se confirma. Los Shorts salen en español por defecto. El confusor es que el ES se subió por Zapier, con idioma es y aviso a suscriptores.

## 2026-11-05 21:15 Chile: ¿sesgo latinoamericano? y sticker de producto (preguntas de Cris)
- YouTube Analytics se puede leer por Zapier (GET crudo a youtubeanalytics v2 con la conexión YouTube de Cris). Receta en la skill shorts-viral-loop. Reemplaza a Metricool para YouTube, que devuelve vacío.
- País: solo el caso 01 ES tiene filas (Bolivia 119, Argentina 69 de 686). Los EN no tienen ninguna. Canal "SheetsmithChile", de 2020, sin país, sin descripción, 0 suscriptores. Idioma declarado correcto en los 7 videos. El listing del caso 01 siguió en 2 vistas. V15 queda confirmada para vistas y no para ventas; abrí V18 (el público ES no llega a Etsy).
- Retención (Analytics, 28-oct a 5-nov): Beethoven EN 41 % (la mejor), caso 01 ES 25 %, villancicos EN 26 %, caso 02 EN 19 %. Beethoven ES va en 215 vistas y 12 likes a ~3,5 h (sin Analytics aún).
- Sticker de producto (YouTube Shopping): pide estar en el Programa de Socios (el canal tiene 0 suscriptores) y una tienda de Shopify, Fourthwall, Spreadshop u otra compatible. Etsy y Gumroad no lo son, y el programa de afiliados no incluye Chile. La API de YouTube no etiqueta productos y Make tampoco. Queda para cuando el canal entre al programa.
- Descarté poner el país del canal en EE. UU.: tiene que ser el real (impuestos y pagos).
- Pendiente: el canal no tiene descripción; escribirla con la skill SEO en un turno próximo.

## 2026-11-06 08:15 Chile · Short de la tregua de Navidad (V16), en la hora libre que dio Cris
- Short ES 60-piano-villancicos-historia-es publicado por Zapier: https://youtube.com/shorts/oRX2V9bh0rw (46,9 s, -14,0 LUFS, pico -2,0 dBTP). Historia real de Noche de paz en la tregua de 1914; el libro de villancicos solo en el cierre.
- V16: seis recursos distintos (4 fotos de archivo de dominio público y 2 cortes de la página de Noche de paz) y fotos a escenario completo con la opción nueva `"llenar": true` de Visual.tsx. El primer render dejaba las fotos horizontales como franjas de ~560 px; con `llenar` ocupan los 900 px del escenario.
- Wikimedia respondió 429 a todo (API, REST y upload). Openverse con `license=pdm,cc0` trajo fotos de Flickr Commons que sí se bajan. Créditos en public/assets/media/archivo/CREDITOS.md. Descarté la foto del partido de fútbol (no está claro que sea de 1914) y una de soldados alemanes con casco de 1916.
- Whisper oye "Celca de Hibres" en vez de "cerca de Ypres" y "de si" en vez de "de Etsy"; en el audio se entiende. La compuerta pasó en las 7 voces.
- Agregué `visual` a las variables de experimento.py. Abrí V19 (30-35 s y voz más rápida) con la auditoría por la API de Gemini del hilo Gemini.
- Lecturas: 8-nov (48 h) y 13-nov (7 días), contra el Beethoven ES (296 vistas, 15 likes y 1 comentario a ~15 h).
- 11:25 Chile: canales advirtió que "paró una guerra" exagera (la tregua fue local y de pocos días). Corregí la descripción en YouTube por la API (videos.update vía Zapier, mismo título) y en el plan: "la tregua fue local y duró poco, pero en varios tramos del frente...". El título queda como gancho; el cuerpo dice el alcance. Para los próximos: el gancho puede ser fuerte, pero el guion o la descripción tienen que decir el alcance real.
- 08:52 Chile: video de listing del #64 Claude Memory Kit (Etsy 4611164570), pedido del hilo de producto. Las fotos son 4:3 y con texto propio, así que tapaban el título del loop; agregué `"alto"` al loop (690 px para fotos 4:3, centradas). Subido con swap_video.py: borró el provisorio (204) y subió el nuevo (201, video_id 852473017). El Short de la historia del kit queda para un turno próximo.

## 2026-11-06 (noche) — Short multifacético del caso 02 ES (pedido de Cris)
- Cris (22:27 UTC): mezclar Remotion con video IA (personas, escenas tensas, personajes), CTA que invite a comentar hecho para el producto, y la voz Piper "es muy mala".
- Voz: probé 6 voces Gemini TTS contra Piper con la misma frase; whisper oyó a Piper "tormenta de Miebe", "plena cala"; Sulafat y Algieba al 100 %. Voz ES por defecto: `gemini:Sulafat`, velocidad 1.15. gemini.py reintenta los 429 (tope de 10 pedidos por minuto del TTS en el nivel pagado).
- Nuevo visual `"tipo": "video"` (Visual.tsx): tramo desde-hasta de un clip a pantalla completa, 0,6x-1,3x, congela el último fotograma si falta.
- 3 clips IA míos con ficha (deshielo; sobrino, gerente, antorchas; rival, teleférico, pasarela), revisados con --revisar hasta "SIN PROBLEMAS", los 3 usables a la primera. Más 3 del hilo de Google Flow (sospechosos, gala, hallazgo). Nos cruzamos y los dos pagamos tomas: acordado que este hilo pide las tomas de los Shorts. Gasto de noviembre US$5,18 de US$9.
- gemini.py: la frase fija "same place, same moment" chocaba con fichas de varios sitios; ahora remite a la continuidad de la ficha y el campo `detalle` reemplaza la frase de época.
- CTA: los cinco sospechosos numerados, cada cara con su número y nombre, y "deja su número en los comentarios".
- Render 49,5 s, -14,0 LUFS, pico -1,4 dBTP. Se mide como V16 (paquete) contra el caso 02 ES del 4-nov.

## 2026-11-07 · Canal Gemini, turno diario

- Recogidas G-035..G-038 (las 4 respondidas entre 15:47 y 16:18 UTC del 6-nov, 30 min después de espejar; modelo "Argon / Gemini 3.1 Pro"). Resúmenes en /mnt/project-files/plan/investigacion/2026-11-07-gemini-G-03*.md.
- G-035: 34 fichas de bingo navideño (estándar 50 cartones, 0 de 34 con emojis, precio mediano US$3,48, "calling cards" como cierre) + 4 ilustraciones Nano Banana de 3 tintas planas y un pipeline Pillow para que parezcan impresas. Las PNG están en Entregas; el enlace público de Drive no se baja por curl desde el contenedor (devuelve HTML), así que OPS las mira desde Drive. Repartido a OPS.
- G-036: guion ES de 45 s y 30 s para el caso 02 con hechos públicos del Short EN, pausa sin voz al estilo A-PErrtdak8 y cierre sin CTA hablado; título «Caso archivado 1989: ¿accidente bajo el puente helado?». Repartido al hilo de videos.
- G-037: auditoría de pronunciación de los 3 Shorts (6 incomprensibles en el caso 01 ES de Piper: hiatos -ía/-ío con consonante parásita y "lo hizo" → "lizó"; Kokoro EN limpio) + 30 palabras con reescritura. Piper ya está descartada (Cris, 6-nov), así que vale como regla general de "números en letras y revisar hiatos" y como lista para probar en Gemini TTS. La VM de Gemini no tiene motor TTS.
- G-038: certificado de detective en DE/FR/IT/PT-BR con terminología policial de 1987 (Urkunde, Dossier d'instruction, Fascicolo d'indagine, Inquérito Policial) y 3 keywords por idioma sin verificar; dos deslices (IT "dei facts", sello FR "affaire classée"). Repartido al hilo de misterio.
- Cola nueva (4, 2 de búsqueda): G-039 keywords DE/FR en SERP y títulos para el Cold Case 01 (OPS), G-040 auditoría por fotogramas de cah0eRHnqTU con voz Sulafat y clips IA contra 7CZBpp1r4kU (video, alta), G-041 tendencias de la semana en Shorts ES de true crime y cuánto IA usan (video), G-042 auditoría del DE/FR del listing 4604988351 + ficha IT y NL (OPS).

## 2026-11-07 (turno diario)
- Lecturas: Beethoven ES 326 vistas a ~45 h (gana a su par EN, 26: V15 3/3 a favor del español); villancicos EN 41 a 7 días (retención 25,8 %). cah0eRHnqTU (IA + Sulafat + CTA de comentar) 121 vistas y 5 likes a ~18 h contra 7 del control a 48 h: la decisión formal de V16 es el 8-nov.
- Short del día: par 1 de V17 (Algieba) con las tomas IA ya pagadas, cero gasto. No salió: el free tier de Gemini TTS tiene tope de 10 voces por día y el Short pide 18. No usé la clave de pago (Cris: solo límites gratuitos). Arreglo: `vozLoteGemini` pide todas las líneas en un solo pedido y las corta por silencios; probado con un lote armado con 3 voces reales (cortes limpios, whisper 100 %). El Short queda para el 8-nov.
- Espera a una persona: nada.

## 2026-11-08 · Canal Gemini, turno diario

- Recogidas G-039..G-042 (las 4 respondidas entre 15:28 y 16:16 UTC del 7-nov, 50 min después de espejar; modelo "Argon / Gemini 3.1 Pro"). Resúmenes en /mnt/project-files/plan/investigacion/2026-11-08-gemini-G-03*/G-04*.md.
- G-039: ~40 fichas DE/FR reales; el 90 % dice "zum Ausdrucken"/"à imprimer" y "(PDF)", el idioma del producto va al final del título ("| English"); SpurlosVerschwunden domina en DE. 3 títulos y 13 tags verificados por idioma para el #56. A OPS.
- G-040: Sulafat sin errores graves (Piper tenía 6), 2,27 pal/s; cah0eRHnqTU 121 vistas contra 7 del control. Tres artefactos de IA con segundo y dos puntos de fuga (arranque s2-4 sin gancho, cierre comercial hablado s44). 5 cambios para el par Algieba. Al hilo de videos.
- G-041: 14 Shorts ES de true crime de la semana; los canales 100 % IA se estancan en 500-1.700 vistas, los que crecen mezclan IA con evidencia real; fórmula de 10 líneas para 35-42 s. Al hilo de videos.
- G-042: 20 correcciones al DE/FR del listing 4604988351 (calco FR "a arrêté le mauvais homme", DE "Cold-Case-Einheit" → Dezernat) y fichas IT/NL completas; longitudes validadas acá. Ojo: cambió "Entsperrmuster" por "Entsperrcode" (mecánica del juego, se mantiene la palabra original) y afirma sin verificar que la app de Etsy no baja PDF. A OPS con esas salvedades.
- Cola nueva (3, 2 de búsqueda): G-043 guion por planos y prompts por clip del caso 01 para la voz Algieba con los arreglos de G-040 (video, alta), G-044 verificación IT/NL en SERP y corrección de título/tags del #56 (OPS), G-045 juegos de misterio en Gumroad: Google + Discover, precios y anzuelos (Canales). El lunes 9 toca la automejora.

## 2026-11-08 (mañana)
- Salió el par 1 de V17 (Algieba): gow-3CRGpYo, 51 s, -14,1 LUFS. La voz en lote funcionó: 18 líneas en un pedido gratis. Algieba a 1,25 (a 1,15 el Short duraba 64 s y hablaba a 2,66 palabras/s contra 2,93 de Sulafat); guion recortado a la longitud del control.
- Apliqué de G-040 solo lo que no cambia la variable de la prueba: fuera la toma con artefacto. Cierre sin CTA hablado y una cara fija por sospechoso quedan para después de V17 (son V14 y la próxima ficha IA).

## 2026-11-08 (turno diario, domingo)
- V16 paquete GANA en vistas (cah0eRHnqTU 125 contra 7 a 48 h); retención pendiente; 0 comentarios pese al CTA. Se levanta el congelamiento del video IA con tope de 2 clips por Short. Tregua ES 196 contra Beethoven ES 326: no gana. Beethoven ES retiene 79,9 %.
- Competencia piano (competencia.py, out/competencia/2026-11-08-piano/REPORTE.md, no se commitea): los outliers del nicho son lecciones cortas ("cómo...", acordes, tocar con dos manos), no historias de la pieza. Idea para V-piano: un Short que enseñe una frase de Noche de paz con las notas Do Re Mi en pantalla.
- Short de hoy: ya salió en la mañana (gow-3CRGpYo, Algieba).

## 2026-11-08 · Canal Gemini: cupo agotado, canal en pausa

- Cris (20:22 UTC): se le acabó el uso de Gemini. Causa: 45 tareas en 9 días (11 el 30-oct, 3-4 diarias después; 18 con búsqueda web, ~10 de YouTube por fotogramas, 2 de Nano Banana) más la Tarea corriendo cada hora (~215 corridas), que gasta aunque la lista esté vacía. La regla "es prácticamente ilimitado" del 30-oct queda superada.
- Hecho: espejo de Drive reemplazado por un Doc "CANAL EN PAUSA" (cada corrida termina al instante); G-043/G-044/G-045 retiradas del espejo (siguen en inbox/). README, skill y CAPACIDADES actualizados al régimen nuevo: lotes solo lunes y jueves, ≤3 tareas, solo lo que la API gratis no hace; auditorías de YouTube por `gemini.py youtube`. El turno de este hilo pasa de diario a lunes y jueves.
- Espera a una persona: la frecuencia de la Tarea (cada hora) solo la cambia Cris desde su app; se lo dije como información, sin pedírselo.

## 2026-11-09 · Canal Gemini, turno de lunes: lote 0

- Sin respuestas: G-043..G-045 estuvieron en el espejo 5 h el 8-nov y Gemini no produjo nada, señal de que el cupo ya estaba agotado antes de que Cris lo notara. El espejo sigue en "CANAL EN PAUSA".
- Decisión: no espejar nada hoy (un día después de quedarse sin cupo, y Cris querría usar Gemini él). Primer lote del régimen nuevo el jueves 12-nov con G-043, G-044 y G-045 (2 búsquedas). Si el jueves tampoco responde, se le dice a Cris una sola vez.
- Espera a una persona: nada.

## 2026-11-09 (turno diario)
- Retención: cah0eRHnqTU 84,2 % contra 39,9 % del control: el paquete de V16 gana también en retención. Tregua ES 75,3 %, Beethoven ES 79,3 %: los ES con voz Gemini o Piper retienen 75-84 %.
- Short del día: caso 03 ES (uFWsXm89siE), 30 s (V19), Sulafat, CTA "¿culpable o inocente?". Solo páginas: nada pagado (regla de Cris del 8-nov). La voz en lote pidió 9 líneas en un pedido.
- Pendiente de mejora: las páginas siguen ocupando ~40 % de la pantalla; para el próximo, probar zoom más alto o recortes de página a pantalla completa.
