# Bitácora de capacidades de la app de Gemini en tareas programadas

Qué probamos, qué pasó y qué pedimos desde entonces. Una fila por prueba; la tabla resumen vive en
`gemini/README.md`. La mantiene el hilo "Conversar con Gemini a través del repo". Regla de Cris
(2026-10-30): Claude debe ir probando qué puede hacer Gemini y hacer que mejore; la tarea corre
cada hora y es "prácticamente ilimitada" (no usa la API).

| Fecha | Tarea | Capacidad probada | Resultado | Qué cambia |
|---|---|---|---|---|
| 2026-10-30 | G-001 | Leer la URL raw de GitHub | NO ("restricciones del sandbox"); leyó el Doc espejo de Drive | El espejo GEMINI-PENDIENTES es obligatorio tras cada cambio |
| 2026-10-30 | G-001 | Crear Google Doc en carpeta de Drive | SÍ (5 Docs bien nombrados, primera línea `estado:` correcta) | Entrega estándar = Doc |
| 2026-10-30 | G-001 | Crear .txt en Entregas | Lo convirtió en Google Doc y lo creó 2 veces | Pedir Docs/Sheets, no .txt; tolerar duplicados |
| 2026-10-30 | G-001 | Deep Research (herramienta) | NO existe en la tarea; investiga con Search + Browse y marca `parcial` | Pedir "investiga en la web con fuentes"; aceptar `parcial` |
| 2026-10-30 | G-002, G-003 | Investigación web con fuentes | SÍ, ~10 KB cada una en 3 min, con URLs; cifras sin verificar | Siempre pedir verificación en página (G-008) antes de actuar |
| 2026-10-30 | G-004 | Video con Veo | NO (sin herramienta de video) | Video sólo por la API (`gemini.py video --pago`) |
| 2026-10-30 | G-005 | NotebookLM crear cuaderno + fuentes | SÍ (cuaderno 94b91608...) | Cuadernos como memoria consultable |
| 2026-10-30 | G-005 | NotebookLM Audio Overview | NO expuesto | Audio a 2 voces por la API (`gemini.py dialogo`) |
| 2026-10-30 | G-001 | Modelo | Se autodeclaró "Gemini 2.5 Pro" | Desde G-006 se exige `modelo:` en la línea 3 y el modelo más capaz |
| 2026-10-30 | G-006 | YouTube: `youtube:get_video_information` | SÍ: con video_id/URL da vistas y likes exactos, fecha, duración, transcripción con marcas cada 5 s y, con `fetch_audio_video_tokens=True`, fotogramas segundo a segundo | Siempre pasar el video_id o la URL del Short; con eso audita hasta uno recién subido |
| 2026-10-30 | G-006 | YouTube: listar los Shorts de un canal | PARCIAL: `youtube:search` no filtra por canal ni ordena por vistas (5 por llamada); la grilla /shorts necesita JS; sin comentarios | Listas de canal = google:search site:youtube.com/shorts + get_video_information; no pedir comentarios |
| 2026-10-30 | G-006, G-008 | Google Sheets en Entregas | SÍ (18 y 12 filas, columnas pedidas) | `entrega: sheet` funciona; llenar antes de gastar búsqueda |
| 2026-10-30 | G-007 | Ver un Short nuestro sin video_id | NO: el canal UCLj5f15NxSLVAr5m6dYtwJA no indexa Shorts recientes y /shorts se bloquea | Pedirlo con URL directa |
| 2026-10-30 | G-008 | Verificar listings de Etsy en página | PARCIAL: Etsy bloquea google:browse (DataDome); precios y títulos salen de snippets indexados; fotos, video y año de apertura no | Pedir solo lo que un snippet trae; fotos/video los vemos por la API del puente |
| 2026-10-30 | G-009 | Pinterest (búsqueda) | NO: requiere sesión + JS; y el cupo de búsqueda se agotó (`THROTTLED_ROLE_LIMIT`, ~10-12 llamadas a google:search/browse por ejecución) | Máximo 2 tareas de búsqueda web por hora (regla 1b del encabezado); reintento G-012 |
| 2026-10-30 | G-010 | Nano Banana / Imagen 3, 4:3, sin texto | SÍ: 2 PNG de 1200x896 subidos como binarios a Entregas, con SynthID | `entrega: imagen` funciona; portadas se componen después con Pillow |
| 2026-10-30 | G-011 | Autocrítica e inventario de herramientas | SÍ: 20 herramientas listadas (Gmail, Calendar, Keep, Slides, Python sin red con Pillow/openpyxl/reportlab, navegador autónomo, datasets) | Sondas en cola: navegador autónomo (G-013), Python→PDF (G-014) |
| 2026-10-30 | G-011 | Elegir el modelo desde dentro de la tarea | NO: el backend fija el modelo antes de entregar el prompt; se autodeclara "Gemini 2.5 Pro" | Solo Cris puede cambiarlo en la app, si la Tarea tiene selector |
| 2026-10-31 | G-012 | Pinterest por google:search | NO: el índice de google:search EXCLUYE pinterest.com (0 resultados con site:) y browse lo bloquea; `pinterest "<frase>"` sí da las páginas de destino (Etsy, blogs) | Pinterest se audita desde nuestro entorno (Playwright); a Gemini se le piden destinos |
| 2026-10-31 | G-012 | CSV generado con Python → Sheet en Entregas | SÍ (Drive lo convirtió a Google Sheet "G-012 pinterest") | Vía sin cuota para tablas |
| 2026-10-31 | G-013 | `web_browser_agent:actuate` en tarea programada | NO: corre 3,5 min y devuelve `<empty>` (sin sesión interactiva) | No pedir navegador autónomo nunca en tareas programadas |
| 2026-10-31 | G-013 | Nuestra tienda vía índice de Google | Solo 4 listings de 40 indexados (Año Nuevo y Thanksgiving, desde 24-oct); los Cold Case no aparecen para el nombre de la tienda | Dato para OPS: visibilidad en Google ≈ 0 |
| 2026-10-31 | G-014 | Python en sandbox + subida binaria | SÍ al 100%: Pillow 11, pypdf, pypdfium2, pdfplumber, Chromium headless+Selenium (HTML→PDF), matplotlib, openpyxl, python-docx/pptx; NO reportlab; fuentes Noto/Liberation/DejaVu/Inter; PDF 812 KB + PNG 4,3 MB subidos sin conversión | Utilería imprimible en serie sin API (G-018); xlsx/csv/pptx también |
| 2026-10-31 | G-015 | YouTube `fetch_audio_video_tokens=True` | SÍ: 180 fotogramas (1/s) + transcripción; tablas segundo a segundo con posición y palabras de subtítulos | Auditoría de nuestros Shorts por URL (G-016) |
| 2026-10-30 | G-011 | `schedules:update_time_based` | SÍ: Gemini puede cambiar el cron de su propia tarea (lo usó para ponerla cada hora) | No pedírselo: la cadencia la decide Cris |
| 2026-11-01 | G-016 | Auditoría fotograma a fotograma de NUESTRO Short (uFgGEGATfA0) | SÍ: plantilla, documentos por segundo, silencios, WPM y notas por regla; vistas/likes exactos | Cada Short nuevo se audita por video_id antes del siguiente |
| 2026-11-01 | G-017 | Leer imágenes de i.etsystatic.com con browse | NO: browse solo acepta texto; sandbox sin internet | Las miniaturas se suben a Drive > Gemini > Miniaturas (G-022) |
| 2026-11-01 | G-018 | Tres piezas de utilería en serie con Python (telegrama, ficha de hotel, informe forense) | SÍ: 3 PDF + 3 PNG carta 300 DPI en Entregas en 4,2 s; código reutilizable en el Doc | Utilería genérica se pide por lotes de 3 con texto exacto |
| 2026-11-01 | G-019 | Snippets de Google de listings de Etsy por frase + año (3 búsquedas) | SÍ: 20 títulos en Sheet, frecuencia de palabras, precios de snippet; nuestro bundle #5 | Investigación de títulos por frase exacta: 1 tarea `navegar` por frase |
| 2026-11-02 | G-020 | Automejora 2: autocrítica de 8 respuestas, reglas de protocolo, inventario sin probar | SÍ: 4 reglas pegables (ya en PENDIENTES 1c), 5 capacidades por probar (audio en VM, image_references, LaTeX, google_finance, Gmail solo Pinterest/Metricool) | Sondas G-024/G-025/G-027 |
| 2026-11-02 | G-021 | Comparar dos Shorts nuestros por API (vistas exactas + fotogramas) | SÍ: 41 vs 1 vistas; hipótesis seed shelf + gancho visual; detectó un fotograma vacío en 00:15 (bug de Remotion) | Cada Short nuevo se compara con el anterior |
| 2026-11-02 | G-022 | Ver imágenes subidas a Drive (view_file) + Pillow para montar grilla 170 px | SÍ: vio las 9, montó `G-022 grilla 170px.png` en Entregas, auditoría con ranking | Imágenes para Gemini: siempre por Drive (Zapier Upload File) |
| 2026-11-02 | G-023 | 3 búsquedas agrupadas con site:etsy.com/listing + Sheet de 2 pestañas | SÍ: 25 fichas reales, frecuencia de palabras, 6 títulos | Patrón de tarea para cualquier frase SEO: 3 queries, site:etsy.com/listing, Sheet primero |
| 2026-11-03 | G-024 | Síntesis de audio en la VM (numpy/scipy/ffmpeg) y subida de WAV/MP3 | SÍ: 3 archivos (piano aditivo 15 s, MP3 192k, radio+Morse 10 s) con pico/RMS medidos; NO hay sox/fluidsynth/lilypond (sin soundfonts) | SFX y pistas sintéticas gratis; el código corre igual en nuestro contenedor |
| 2026-11-03 | G-025 | Nano Banana 1:1 con zona central limpia + `image_references` desde Drive | SÍ 4 PNG 1024×1024 (máximo 1:1); `image_references` NO acepta file_id de Drive (solo adjuntos del turno o imágenes propias); rodeo: medir paleta con NumPy y pasar hex en el prompt | Fondos para miniaturas; "edita nuestra portada" no se pide |
| 2026-11-03 | G-026 | Patrón G-023 aplicado a piano: 1 llamada con 3 queries + site:etsy.com/listing + Sheet | SÍ: 24 fichas, frecuencias, 9 títulos marcando snippet vs inferencia | Patrón consolidado: 1 tarea de búsqueda ⇒ 20+ fichas |
| 2026-11-03 | G-027 | pdflatex/lualatex/weasyprint/Chromium CDP + pypdfium2 en la VM | SÍ: pdflatex y lualatex existen; Chromium solo vía CDP (CLI falla); PDF vectorial de 43 KB vs 54 KB LaTeX vs 255–380 KB Pillow | Utilería de texto: HTML+Chromium; papel viejo: HTML→300 DPI→Pillow |
| 2026-11-04 | G-028 | Patrón G-023 para escape room (3 queries, Sheet) | PARCIAL: la Hoja llegó completa (31 fichas, frecuencias, 3 títulos) pero el Doc RESPUESTA quedó VACÍO (fallo al escribir el Doc) | Si falta el Doc, la Hoja basta; pedir en la próxima automejora que verifique que el Doc tiene texto |
| 2026-11-04 | G-029 | Buscar Shorts por site:youtube.com/shorts + analizar 14 por fotogramas y transcripción | SÍ: 14 Shorts de 14 canales con vistas/fecha de la API, lectura de primeros 3 s, cortes, subtítulos, CTA; el Doc se cortó al final (límite de largo) | Para muestras: pedir la Hoja primero y el Doc corto; dejar los ganchos al principio |
| 2026-11-04 | G-030 | Entregar CÓDIGO (.html y .py) como archivos a Entregas + demo | SÍ: subió .py y .html como archivos (mime text/x-python, text/x-handlebars-template); el código corrió acá sin cambios (verificado 5-nov). El Doc pegó una versión con un bug que el archivo no tiene | Pedir siempre el archivo, no el código pegado; leerlo con download_file_content (read_file_content pierde la indentación) |
| 2026-11-04 | — | Modelo declarado | Desde las 17:34 UTC del 4-nov las respuestas declaran "Argon / Gemini 3.1 Pro" (antes "Gemini 2.5 Pro"): Cris habría cambiado el modelo de la Tarea. Autodeclarado, sin verificar | Seguir exigiendo `modelo:`; comparar calidad G-029/G-030 vs anteriores en la automejora del lunes |
| 2026-11-05 | G-031..G-034 | Cuatro tareas en un lote (1 búsqueda web + 2 YouTube + 1 código) | SÍ: las 4 respondidas en 50 min (16:56-17:47 UTC), Docs con texto y Hojas completas; modelo "Argon / Gemini 3.1 Pro" | Un lote de 4 con 1 sola búsqueda web cabe en una ejecución |
| 2026-11-05 | G-034 | Oír errores de pronunciación de un TTS en español por video_id | SÍ (sin verificar): listó 5 palabras mal pronunciadas con su segundo ("parecina" s 12, "policiga" s 16...) | Auditoría de TTS por Gemini antes de publicar cada Short; comprobar con whisper |
| 2026-11-05 | G-033 | HTML + PDF vectorial + PNG 300 DPI + script Pillow como archivos | SÍ: html (8 KB), pdf (69 KB), 2 png 3296×2550, sello.py; el html corrió acá sin cambios (verificado 6-nov). Subió además copias como Google Docs (ruido) | Ignorar las copias en Doc; usar los archivos binarios/código |
| 2026-11-06 | API | Comparación API gratis vs app: ver YouTube por fotogramas | La API (3.6 Flash, `gemini.py youtube`) da el mismo tipo de tabla por segundo en ~30 s, US$0; la app (Argon) añade más detalle (errores de TTS, diferencias finas) pero tarda hasta 1 h | YouTube urgente → API; análisis fino o con Argon → app. Argon e imágenes solo por la app (en la API son pagados) |

## Pendiente de probar
Slides; lectura de PDFs de Drive (nuestros expedientes, nunca las soluciones); traducción de listings
DE/FR/IT/NL/PT con revisión de SEO; Gmail SOLO para correos de Pinterest/Metricool con métricas (los de
Etsy traen datos de compradores: no); google_finance (sin uso claro); Calendar y Keep no hacen falta.
Probado el 3-nov: audio en la VM (G-024 sí), image_references (G-025: no desde Drive), LaTeX (G-027 sí). En cola el 6-nov: traducción DE/FR/IT/PT (G-038).

## Reglas que salieron de las pruebas
- Cada tarea lleva IDs directos: video_id/URL de Shorts, file_id de Drive, URL del listing.
- Máximo 2 tareas de búsqueda web por ejecución (encabezado 1b). Las de YouTube API, Python e imágenes no gastan ese cupo.
- Cifras de Etsy que vengan de snippets son `(sin verificar)` hasta mirarlas por el puente.
- NO existen para Gemini: Pinterest (índice lo excluye), navegador autónomo, Veo, Audio Overview, elegir modelo.
- SÍ y barato (sin cupo): YouTube por URL con fotogramas, Python→PDF/PNG/xlsx/pptx/WAV/MP3 subidos a Entregas, PDF vectorial por HTML+Chromium o pdflatex, imágenes Nano Banana 1024 px (sin referencia a fotos de Drive), Docs/Sheets.
