---
id: G-027
titulo: Sonda HTML+Chromium y pdflatex para utilería de texto (hoja de respuestas de trivia)
pedido: 2026-11-03
hilo: Conversar con Gemini a través del repo
herramienta: texto
entrega: pdf
estado: pendiente
prioridad: baja
---
## Contexto
En G-020 dijiste que las plantillas de utilería saldrían más nítidas y livianas con HTML/CSS + Chromium headless que con Pillow, y propusiste probar pdflatex. Queremos ver las dos cosas con una pieza genérica (sin datos de ningún caso real). Sin búsqueda web.

## Qué quiero
1. Comprueba si existen pdflatex, xelatex, lualatex, pandoc, wkhtmltopdf y weasyprint en la VM (versión o "no está").
2. Con HTML/CSS + Chromium headless: una hoja carta "Hoja de respuestas · Trivia de películas de Navidad" con 3 bloques de 10 líneas numeradas, cabecera con nombre del equipo y puntaje, pie con "SheetSmithChile · print & play". Tipografía serif del sistema, márgenes 18 mm, dos tonos de rojo (#8B1A1A y #C82323). Exporta `G-027 trivia-respuestas-html.pdf` y, con pypdfium2, una previsualización `G-027 trivia-respuestas-html.png` a 150 DPI.
3. La misma hoja con pdflatex si existe (`G-027 trivia-respuestas-latex.pdf`); si no existe, dilo y salta este punto.
4. Compara: peso en KB, nitidez del texto a 100% (recorte zoom en PNG), tiempo de generación. Recomienda cuál usar para utilería de texto y cuál para papel envejecido (Pillow, como G-018).

## Formato de la respuesta
Español. Doc `G-027 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas; archivos en Entregas; código HTML/CSS completo al final. Máximo 1.000 palabras + código.
