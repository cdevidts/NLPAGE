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
| 2026-10-30 | G-006..G-011 | YouTube (listados, vistas, transcripciones), Sheets, Pinterest, Nano Banana, autocrítica | pendiente | — |

## Pendiente de probar
Gmail (leer el correo de Etsy cdevidts2 para avisos de venta), Google Calendar, Slides, ejecución
de código en su sandbox (sin red), navegador autónomo en Etsy con sesión (NO: nunca con la cuenta de
Cris), Google Maps, lectura de PDFs de Drive (nuestros expedientes, nunca las soluciones), Deep
Think, traducción de listings DE/FR/IT/NL/PT con revisión de SEO.
