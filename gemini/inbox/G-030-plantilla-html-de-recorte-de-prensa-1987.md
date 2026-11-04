---
id: G-030
titulo: Plantilla HTML de recorte de prensa 1987 + script Pillow de envejecido (solo marcadores, sin texto de casos)
pedido: 2026-11-04
hilo: Conversar con Gemini a través del repo
herramienta: texto
entrega: imagen
estado: pendiente
vence: 2026-11-06
prioridad: normal
---
## Contexto
En G-027 recomendaste HTML/CSS + Chromium para texto y un híbrido con Pillow para papel envejecido. Lo queremos como plantilla reutilizable para los próximos Cold Cases: un recorte de periódico de 1987. Sin texto real de ningún caso: SOLO marcadores de posición. Nada de solución de ningún juego. Sin búsqueda web.

## Qué quiero
1. `G-030 recorte-1987.html`: plantilla de recorte de prensa (ancho 150 mm, alto libre) con cabecera de diario ficticio ("The Ridgeline Courier" o similar, inventado), fecha y ciudad, titular a dos líneas, bajada, cuerpo a dos columnas con separador fino, un pie de foto con un recuadro gris donde iría la foto, y un pequeño número de página. Tipografía serif del sistema (tipo Times/Noto Serif), interletrado y justificado de diario de los 80. Todos los textos son marcadores entre dobles llaves: {{DIARIO}}, {{FECHA}}, {{CIUDAD}}, {{TITULAR}}, {{BAJADA}}, {{CUERPO}} (párrafos separados por líneas en blanco), {{PIE_FOTO}}, {{PAGINA}}. Súbelo como archivo a Entregas; si la herramienta no deja subir .html, pégalo completo en el Doc.
2. `G-030 envejecer.py`: script Python (Pillow + NumPy, sin otras dependencias) que recibe un PNG a 300 DPI y devuelve otro envejecido con parámetros por línea de comandos: amarilleo (0-1), grano, viñeteado, 1-3 manchas de café con borde, un doblez horizontal con sombra, bordes rasgados o recortados con tijera, y desaturación leve de la tinta. Que cada parámetro tenga un valor por defecto que se vea bien. Súbelo (o pégalo).
3. Demostración: llena la plantilla con texto de relleno en inglés que no cuente ningún hecho (lorem ipsum está bien), renderízala a 300 DPI por Chromium (CDP) + pypdfium2 y pásala por el script con los valores por defecto. Sube `G-030 recorte-1987-demo.png` (envejecido) y `G-030 recorte-1987-limpio.png` (sin envejecer).
4. En el Doc: cómo se corre cada paso (comandos exactos), cuánto tarda, el peso de cada archivo, y qué parámetros cambiarías para un diario de 1936 en lugar de 1987.

## Formato de la respuesta
Español. Doc `G-030 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas; archivos en Entregas. Máximo 800 palabras + código.
