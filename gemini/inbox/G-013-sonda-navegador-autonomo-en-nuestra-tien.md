---
id: G-013
titulo: Sonda: navegador autónomo en nuestra tienda pública, vista de comprador
pedido: 2026-10-31
hilo: Operación autónoma de la tienda
herramienta: navegar
entrega: sheet
estado: pendiente
---
## Contexto
Sonda de capacidad que tú mismo propusiste en G-011: `web_browser_agent:actuate` sobre una página pública sin login. Además nos sirve para ver la tienda como la ve un comprador. Esta tarea NO usa google:search (no gasta el cupo de búsqueda).

## Qué quiero
1. Abre con el navegador autónomo https://sheetsmithchile.etsy.com (tienda SheetSmithChile; 40 anuncios). Sin iniciar sesión, sin aceptar nada que pida cuenta. Si Etsy te bloquea (DataDome/captcha), dilo con el mensaje exacto y prueba una sola vez más con https://www.etsy.com/shop/SheetSmithChile.
2. Si entra: lista los anuncios que se ven en la primera pantalla y al hacer scroll (hasta 40): título tal como se muestra (si está truncado, hasta dónde se lee), precio mostrado, precio tachado si hay oferta, y si la miniatura muestra la insignia de video o el texto "Bestseller"/"Popular now". Qué secciones de la tienda aparecen en el menú izquierdo. Qué dice la cabecera (banner, anuncio de la tienda, número de ventas y reseñas visibles).
3. Como comprador que llega por primera vez, en 5 líneas: qué anuncio te llamó la atención primero y por qué, qué miniatura se ve peor en tamaño pequeño, qué te faltó para confiar.
Entrega una hoja `G-013 tienda` en Entregas (columnas: posicion, titulo_visible, precio, precio_tachado, insignia, seccion) y el Doc.

## Formato de la respuesta
Español. Doc `G-013 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Si el navegador autónomo no está disponible en la tarea programada, `estado: no-puedo` con el nombre exacto de la herramienta y el error. Máximo 1.000 palabras.
