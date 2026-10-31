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
| 2026-10-30 | G-011 | `schedules:update_time_based` | SÍ: Gemini puede cambiar el cron de su propia tarea (lo usó para ponerla cada hora) | No pedírselo: la cadencia la decide Cris |

## Pendiente de probar
Navegador autónomo `web_browser_agent:actuate` en nuestra tienda pública (G-013); Python en el sandbox
→ PDF/xlsx subido como binario (G-014); edición de imagen con `image_references` (portada existente);
Slides; lectura de PDFs de Drive (nuestros expedientes, nunca las soluciones); traducción de listings
DE/FR/IT/NL/PT con revisión de SEO; Gmail SOLO para correos de Pinterest/Metricool con métricas (los de
Etsy traen datos de compradores: no); Calendar y Keep no hacen falta.

## Reglas que salieron de las pruebas
- Cada tarea lleva IDs directos: video_id/URL de Shorts, file_id de Drive, URL del listing.
- Máximo 2 tareas de búsqueda web por ejecución (encabezado 1b). Las de YouTube API, Python e imágenes no gastan ese cupo.
- Cifras de Etsy que vengan de snippets son `(sin verificar)` hasta mirarlas por el puente.
