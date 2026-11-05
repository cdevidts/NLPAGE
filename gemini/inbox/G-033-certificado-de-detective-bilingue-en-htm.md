---
id: G-033
titulo: Certificado de detective bilingüe en HTML (plantilla con marcadores) + demos a 300 DPI
pedido: 2026-11-05
hilo: Conversar con Gemini a través del repo
herramienta: texto
entrega: pdf
estado: pendiente
vence: 2026-11-07
prioridad: normal
---
## Contexto
G-030 funcionó: la plantilla y el script corren en nuestro contenedor sin cambios. Siguiente pieza reutilizable para los Cold Cases (listings 4604988351, 4605211787, 4605344156 y el pack): un "Certificado de detective" que el comprador imprime al resolver el caso. Es un extra habitual en los listings de misterio de la competencia y lo podemos añadir gratis a los cuatro. Solo marcadores, sin texto de ningún caso ni solución. Sin búsqueda web.

## Qué quiero
1. `G-033 certificado-detective.html`: hoja carta apaisada (279 × 216 mm, margen 0), estilo documento oficial de 1987 (orla de filete doble, sello circular dibujado en CSS, tipografía serif del sistema, un renglón de firma), con marcadores {{IDIOMA}} (en/es), {{TITULO}}, {{NOMBRE}} (renglón vacío si viene en blanco), {{CASO}}, {{FECHA}}, {{FIRMA_CARGO}}, {{TEXTO}} (un párrafo), {{SELLO}} (texto dentro del sello). Dos juegos de textos de ejemplo en el Doc: inglés y español neutro, sin nombrar ningún caso real ("Case File No. ___").
2. `G-033 certificado-demo-en.png` y `G-033 certificado-demo-es.png` a 300 DPI (render Chromium CDP + pypdfium2 como en G-030), y `G-033 certificado-demo-en.pdf` vectorial.
3. Opcional: una variante `--sello` para el script envejecer.py de G-030 que solo añada un sello de tinta roja semitransparente ligeramente rotado (texto configurable) sin el resto del envejecido; si lo haces, sube `G-033 sello.py` como archivo.
4. En el Doc: comandos exactos, tiempos, pesos, y qué cambiarías para un certificado de 1936.

## Formato de la respuesta
Español. Doc `G-033 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas; archivos en Entregas (como archivos, no pegados: el archivo .py de G-030 estaba bien y el pegado en el Doc tenía un error). Máximo 800 palabras + código.
