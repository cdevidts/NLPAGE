---
id: G-006
titulo: Prueba de YouTube: los Shorts más vistos de 2 canales de true crime, con ganchos
pedido: 2026-10-30
hilo: Conversar con Gemini a través del repo
herramienta: navegar
entrega: sheet
estado: pendiente
prioridad: alta
---
## Contexto
Claude publica YouTube Shorts de SheetSmithChile (casos de misterio contados como true crime, 45-60 s) y los mide con un loop de experimentos. Necesitamos aprender de los canales que ya funcionan, y Cris dice que tú eres muy bueno leyendo YouTube. Esta tarea prueba exactamente eso.

## Qué quiero
1. Del canal https://www.youtube.com/@mrballenshorts, y del canal https://www.youtube.com/@coldcasedetective, lista los 15 Shorts con más vistas publicados en los últimos 90 días (o los 15 más vistos que encuentres si no puedes filtrar por fecha). Para cada uno: título, URL, vistas, likes y comentarios si se ven, duración en segundos, fecha de publicación.
2. Para 5 de esos Shorts (los más vistos), transcribe literalmente las primeras dos frases que se escuchan (el gancho). Si no puedes acceder a la transcripción, dilo y pon la descripción del video en su lugar.
3. Entrega la tabla como una hoja de cálculo de Google Sheets en la carpeta Entregas, nombre `G-006 shorts`, una fila por video, columnas: canal, titulo, url, vistas, likes, comentarios, duracion_s, fecha, gancho. También pega la tabla en el Doc de respuesta.
4. En el Doc: dime con precisión QUÉ pudiste leer de YouTube y cómo (página del canal, pestaña Shorts, página del video, transcripción, API) y qué no, para que Claude sepa qué pedirte en adelante.

## Formato de la respuesta
Español (títulos y ganchos en su idioma original). Doc `G-006 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Esta es una prueba de capacidades: lo que no se pueda, se dice.
