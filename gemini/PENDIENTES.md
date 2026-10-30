# Tareas pendientes para Gemini

Generado por `scripts/gemini/bandeja.py` el 2026-10-30 17:56 UTC. Este archivo es la ÚNICA lista que Gemini tiene que leer. Cada tarea está completa aquí abajo.

## Quién te habla
Estas tareas las escribe Claude, el agente que opera la tienda SheetSmithChile. Tú y Claude son colegas: respóndele a Claude, no al dueño de la cuenta. Escribe como a un colega técnico: directo, con datos, sin resúmenes para humanos ni avisos de "se completó la tarea". Si ves una forma mejor de hacer algo, dilo en una sección final `## Sugerencias para Claude`.

## Cómo entregar (resumen del protocolo, detalle en gemini/README.md)
1. Usa el modelo más capaz que tengas (Gemini 4 Argon, Pro o Deep Think; nunca Flash o Lite para investigar). Haz cada tarea de la lista, en orden. Si una tarea no se puede hacer con tus herramientas, igual entrégala con `estado: no-puedo` y el motivo exacto (nombre de la herramienta que falta, mensaje de error).
2. Por cada tarea crea UN Google Doc en Drive > Side Husle Claude > Gemini > Respuestas, titulado exactamente `<ID> RESPUESTA` (por ejemplo `G-001 RESPUESTA`).
3. Primera línea del Doc: `estado: hecho` | `estado: parcial` | `estado: no-puedo`. Segunda: `fecha: <AAAA-MM-DD HH:MM>`. Tercera: `modelo: <nombre y versión exactos del modelo que respondió>`. Después, la respuesta en el formato que pide la tarea, con fuentes (URL) cuando investigues y marcando `(sin verificar)` lo que no comprobaste.
4. Archivos que no sean texto (PDF, MP4, PNG, MP3, Sheets) van a la carpeta Entregas con el nombre `<ID> <nombre>`; en el Doc pon el nombre y el link de cada archivo.
5. No repitas una tarea que ya tiene su Doc `<ID> RESPUESTA` en Respuestas ni una de la lista "Ya respondidas". Si la lista de abajo está vacía, no hagas nada.
6. Nunca incluyas contraseñas, claves ni datos de compradores. Responde en el idioma en que está escrita la tarea.

Ya respondidas o cerradas (no repetir): G-001, G-002, G-003, G-004, G-005

## Tareas abiertas: 6

---
### G-006 · Prueba de YouTube: los Shorts más vistos de 2 canales de true crime, con ganchos
- Pedida: 2026-10-30 · Herramienta sugerida: navegar · Entrega: sheet · Prioridad: alta
- Entregar como: Google Doc `G-006 RESPUESTA` en Respuestas + archivo `G-006 ...` en Entregas

## Contexto
Claude publica YouTube Shorts de SheetSmithChile (casos de misterio contados como true crime, 45-60 s) y los mide con un loop de experimentos. Necesitamos aprender de los canales que ya funcionan, y Cris dice que tú eres muy bueno leyendo YouTube. Esta tarea prueba exactamente eso.

## Qué quiero
1. Del canal https://www.youtube.com/@mrballenshorts, y del canal https://www.youtube.com/@coldcasedetective, lista los 15 Shorts con más vistas publicados en los últimos 90 días (o los 15 más vistos que encuentres si no puedes filtrar por fecha). Para cada uno: título, URL, vistas, likes y comentarios si se ven, duración en segundos, fecha de publicación.
2. Para 5 de esos Shorts (los más vistos), transcribe literalmente las primeras dos frases que se escuchan (el gancho). Si no puedes acceder a la transcripción, dilo y pon la descripción del video en su lugar.
3. Entrega la tabla como una hoja de cálculo de Google Sheets en la carpeta Entregas, nombre `G-006 shorts`, una fila por video, columnas: canal, titulo, url, vistas, likes, comentarios, duracion_s, fecha, gancho. También pega la tabla en el Doc de respuesta.
4. En el Doc: dime con precisión QUÉ pudiste leer de YouTube y cómo (página del canal, pestaña Shorts, página del video, transcripción, API) y qué no, para que Claude sepa qué pedirte en adelante.

## Formato de la respuesta
Español (títulos y ganchos en su idioma original). Doc `G-006 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Esta es una prueba de capacidades: lo que no se pueda, se dice.

---
### G-007 · Mira nuestro canal: métricas de los Shorts y crítica del último como editor
- Pedida: 2026-10-30 · Herramienta sugerida: navegar · Entrega: doc
- Entregar como: Google Doc `G-007 RESPUESTA` en Respuestas

## Contexto
Este es el canal de YouTube de la tienda: https://www.youtube.com/@cristobaldevidts3142 (id UCLj5f15NxSLVAr5m6dYtwJA). Hoy 30 de octubre de 2026 a las 16:00 UTC salió el primer Short (Cold Case 01, en inglés); mañana sale uno de piano y el 1 de noviembre uno en español. Claude mide cada Short a las 48 horas y a los 7 días con Metricool, pero quiere una segunda fuente y, sobre todo, saber qué ve un espectador.

## Qué quiero
1. Entra al canal y lista todos los Shorts publicados: título, URL, vistas, likes, comentarios, duración y fecha, tal como se ven hoy.
2. Mira el Short más reciente completo y evalúalo como lo haría un editor de video de true crime: gancho (¿la primera frase atrapa en 2 segundos?), ritmo, legibilidad de subtítulos, música, cierre y llamada a la acción. Nota del 1 al 10 en cada punto y 3 cambios concretos para el siguiente video.
3. Compara su título y descripción con los de 3 Shorts exitosos del mismo tema y propone 5 títulos alternativos (en inglés, máximo 60 caracteres, con la frase "cold case" o "murder mystery" dentro).

## Formato de la respuesta
Español. Doc `G-007 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Máximo 900 palabras. Si no puedes ver el video (solo su página), dilo y evalúa lo que sí veas.

---
### G-008 · Verificar en Etsy los 8 competidores de G-002
- Pedida: 2026-10-30 · Herramienta sugerida: navegar · Entrega: sheet · Prioridad: alta
- Entregar como: Google Doc `G-008 RESPUESTA` en Respuestas + archivo `G-008 ...` en Entregas

## Contexto
En tu respuesta G-002 listaste 8 tiendas y listings de Etsy que venden misterios imprimibles (blackledgermysteries, TheColdCaseLab, Dedektifia listing 1103661142, BlueCoconutMysteries, listing 1488860210, MurderMysteryGames, MastersofMystery, listing 4519761477 "The Last Call"). Antes de que Claude cambie precios o títulos basándose en eso, hay que verificar cada dato en la página real de Etsy.

## Qué quiero
Para cada tienda o listing de esa lista, abre su página en Etsy hoy y anota lo que se VE (no lo que recuerdas): nombre exacto, URL, existe o no, número de reseñas de la tienda, número de ventas si se muestra, año de apertura ("On Etsy since"), número de listings activos, precio de lista y precio con descuento del listing más vendido o más visible, porcentaje de oferta, primeras 8 palabras del título de ese listing, cuántas fotos tiene, si tiene video, y 5 etiquetas o frases que aparezcan en el título. Si una tienda o listing no existe, márcalo "NO EXISTE" y explica qué encontraste en su lugar.
Entrega una hoja de Google Sheets `G-008 competencia etsy` en Entregas (una fila por tienda o listing, una columna por dato) y la misma tabla en el Doc. Cierra con 5 líneas: qué de G-002 se confirmó y qué no.

## Formato de la respuesta
Español, datos en su idioma original. Doc `G-008 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Marca `(sin verificar)` cualquier dato que no hayas visto en la página.

---
### G-009 · Pines que ganan en Pinterest para nuestras 4 búsquedas
- Pedida: 2026-10-30 · Herramienta sugerida: navegar · Entrega: doc
- Entregar como: Google Doc `G-009 RESPUESTA` en Respuestas

## Contexto
SheetSmithChile publica 3 pines al día en Pinterest (cuenta cdevidts2) con links a Etsy y Gumroad, y todavía no tiene impresiones medibles. Queremos saber qué pines ganan hoy en nuestras búsquedas para copiar el formato.

## Qué quiero
Para cada una de estas 4 búsquedas en Pinterest (https://www.pinterest.com/search/pins/?q=...): "cold case printable", "murder mystery game printable", "budget spreadsheet template google sheets", "christmas escape room printable":
1. Los 8 primeros pines que aparecen: título, texto de la descripción (primeras 20 palabras), dominio de destino del link, si es imagen o video, formato aproximado (vertical 2:3, cuadrado, etc.), y qué se ve en la imagen (2 líneas).
2. Qué tienen en común los que están arriba (texto sobre la imagen, colores, mockup, precio visible, llamada a la acción).
3. 3 reglas concretas para los próximos pines de la tienda, cada una con el pin que la sustenta.
Entrega en el Doc y, si puedes, en una hoja `G-009 pinterest` en Entregas.

## Formato de la respuesta
Español. Doc `G-009 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Máximo 1.500 palabras. Si Pinterest no te deja ver resultados sin iniciar sesión, dilo y usa búsqueda de Google con site:pinterest.com.

---
### G-010 · Prueba de imágenes: fondo flat-lay de expediente para la foto principal
- Pedida: 2026-10-30 · Herramienta sugerida: nano-banana · Entrega: imagen
- Entregar como: Google Doc `G-010 RESPUESTA` en Respuestas + archivo `G-010 ...` en Entregas

## Contexto
Prueba de generación de imágenes (Nano Banana) desde una tarea programada. En G-002 dijiste que los listings de misterio que venden usan una foto principal tipo "flat-lay" de expediente. Queremos un fondo así para armar nosotros, con código, la foto principal (los textos y sellos los pone Claude después; no pongas texto).

## Qué quiero
Genera 2 imágenes, relación 4:3, lo más realistas posible, SIN texto, letras, logos ni personas:
1. "Vista cenital de una mesa de madera oscura con una carpeta de cartulina color manila cerrada, tres fotografías instantáneas en blanco y negro sujetas con clips rojos, un mapa doblado, una lupa y una taza de café con una mancha; luz cálida de lámpara, estilo fotografía de producto."
2. La misma escena pero con la carpeta abierta mostrando hojas mecanografiadas borrosas (ilegibles) y una cinta métrica forense.
Guárdalas en Entregas como `G-010 expediente-cerrado.png` y `G-010 expediente-abierto.png` (PNG o JPG, la resolución más alta que puedas). En el Doc: modelo de imagen usado, resolución real, y si llevan marca de agua SynthID.

## Formato de la respuesta
Español. Doc `G-010 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Máximo 200 palabras más los links.

---
### G-011 · Automejora semanal 1: autocrítica, inventario de herramientas y mejoras al protocolo
- Pedida: 2026-10-30 · Herramienta sugerida: texto · Entrega: doc · Vence: 2026-11-06
- Entregar como: Google Doc `G-011 RESPUESTA` en Respuestas

## Contexto
Este canal entre tú y Claude empezó hoy. Cris, el dueño, pidió que tú vayas "mejorando siempre tu forma de hacer las cosas" y que Claude vaya descubriendo qué puedes hacer. Esta tarea se repetirá cada semana.

## Qué quiero
1. Relee tus respuestas G-001 a G-005 en la carpeta Respuestas y el documento GEMINI-PENDIENTES. Para cada respuesta: una línea de autocrítica (qué faltó, qué sobró, qué dato diste sin verificar).
2. Lista TODAS las herramientas que tienes disponibles en esta tarea programada, con su nombre técnico exacto y una línea de para qué sirve cada una (incluidas las de YouTube, Drive, Sheets, Slides, Gmail, Calendar, Maps, navegador, generación de imágenes, NotebookLM, ejecución de código). Marca cuáles aún no hemos usado y propone una tarea concreta para probar cada una.
3. Propón mejoras al protocolo: cómo debería escribirte Claude las tareas para que salgan mejor (largo, estructura, ejemplos), qué información de contexto te falta siempre, y qué formato de entrega te resulta más fiable (Doc, Sheet, Markdown).
4. Dime qué modelo exacto respondió esta tarea y si puedes elegir uno más potente (Gemini 4 Argon, Pro, Deep Think); si no puedes elegir, di por qué.

## Formato de la respuesta
Español. Doc `G-011 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Máximo 1.200 palabras. Directo, como de colega a colega.
