---
id: G-012
titulo: Pinterest, segundo intento: pines que ganan en nuestras 4 búsquedas (sola en su hora)
pedido: 2026-10-31
hilo: Canales de venta y marketing
herramienta: navegar
entrega: sheet
estado: pendiente
prioridad: alta
---
## Contexto
Reintento de G-009 (quedó `no-puedo` porque el cupo de búsqueda se agotó con G-006 y G-008 en la misma hora). Ahora es la ÚNICA tarea de búsqueda web de este lote: tienes el cupo completo (~10 llamadas). Pinterest no se deja navegar sin sesión, así que usa `google:search` con `site:pinterest.com/pin <frase>` y lee lo que traigan los snippets y, si abre, `google:browse` de cada pin individual (las páginas /pin/<id>/ a veces sí cargan sin sesión).

## Qué quiero
Para cada una de estas 4 frases (2 llamadas de búsqueda por frase como máximo): "cold case printable", "murder mystery game printable", "budget spreadsheet template google sheets", "christmas escape room printable":
1. Los 6 primeros pines que encuentres: título, primeras 20 palabras de la descripción, dominio de destino (etsy.com, gumroad.com, blog propio...), y si el snippet o la página dice que es video o imagen.
2. Qué tienen en común los títulos y descripciones que aparecen arriba (palabras que se repiten, longitud, si nombran el precio, si tienen llamada a la acción).
3. 3 reglas concretas para los próximos pines de SheetSmithChile, cada una con el pin que la sustenta (URL).
Pobla la hoja que ya existe en Entregas: `G-009 pinterest` (ID 1Zv7x1iweD2EYU51WfV-GPsur2McZ-GGG5UOihsXsn7o), columnas: frase, posicion, titulo, descripcion_20_palabras, dominio_destino, tipo, url_pin. Llénala ANTES de agotar el cupo, o genera un .csv con Python y súbelo como `G-012 pinterest.csv`.

## Formato de la respuesta
Español. Doc `G-012 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Máximo 1.200 palabras. Si vuelve a saltar el límite de búsqueda, entrega lo que alcanzaste con `estado: parcial` y di en qué llamada saltó.
