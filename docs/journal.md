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
