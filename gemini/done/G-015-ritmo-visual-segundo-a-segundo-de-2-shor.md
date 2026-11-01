---
id: G-015
titulo: Ritmo visual segundo a segundo de 2 Shorts de MrBallen (fotogramas)
pedido: 2026-10-31
hilo: Crear sistema de viralidad para Shorts
herramienta: texto
entrega: doc
estado: pendiente
prioridad: alta
---
## Contexto
En G-006 descubriste que con `youtube:get_video_information(..., fetch_audio_video_tokens=True)` ves los fotogramas segundo a segundo. Queremos usar eso para copiar el ritmo visual de los que ganan antes de editar nuestros próximos Shorts. Esta tarea no gasta el cupo de google:search: solo la API de YouTube.

## Qué quiero
Analiza estos 2 Shorts de @mrballenshorts (los más vistos de tu lista G-006):
- https://www.youtube.com/shorts/0273An0eItk ("The Signal", 5,6 M vistas)
- https://www.youtube.com/shorts/2rbGcCtrjQs ("Why You NEVER Camp Alone….", 3,1 M vistas)
Para cada uno:
1. Línea de tiempo de los primeros 30 segundos, segundo a segundo: qué se ve (plano del narrador, foto, mapa, texto en pantalla), cuándo hay corte o punch-in, dónde están los subtítulos en la pantalla (tercio superior/medio/inferior), cuántas palabras por bloque de subtítulo, color y estilo.
2. Del segundo 30 al final: cada cuántos segundos cambia el plano (promedio y máximo sin cambio), y qué pasa en los últimos 5 segundos (cómo cierra, si hay CTA, si corta en seco).
3. Transcripción de los primeros 15 segundos con marcas de tiempo y conteo de palabras por minuto del video completo.
4. En 8 líneas: las 5 reglas de edición que se repiten en los dos y que un editor de Shorts de misterio de 45-60 s debería copiar.
Entrega: Doc con las dos líneas de tiempo en tablas (segundo | se_ve | corte | subtitulo_posicion | subtitulo_palabras) y la sección de reglas.

## Formato de la respuesta
Español (las citas de transcripción en inglés). Doc `G-015 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Máximo 2.000 palabras. Si `fetch_audio_video_tokens` no te entrega fotogramas, dilo y entrega lo que la transcripción permita con `estado: parcial`.
