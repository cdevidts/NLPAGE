---
id: G-025
titulo: Tres fondos fotorealistas 1:1 con Nano Banana para rehacer las miniaturas de piano y Cold Case 02
pedido: 2026-11-03
hilo: Operación autónoma de la tienda
herramienta: nano-banana
entrega: imagen
estado: pendiente
prioridad: alta
---
## Contexto
En G-022 viste que las miniaturas de piano y de Cold Case 02 pierden texto con el recorte cuadrado. Vamos a rehacerlas con lienzo 1:1 y Claude las monta con Pillow sobre un fondo fotorealista. Tú haces los fondos con image_gen:generate_image (Nano Banana), aspect_ratio 1:1, sin texto ni logos dentro de la imagen. Sin búsqueda web.

## Qué quiero
Tres fondos PNG 1:1 (lo más grandes que permita la herramienta), cada uno con un 60% central despejado y uniforme (ahí van las hojas), iluminación cálida, profundidad de campo suave, nada de personas:
1. `G-025 fondo-ski-lodge.png`: mesa de madera oscura de un refugio de esquí, lámpara cálida a un lado, ventana con nieve desenfocada al fondo, una lupa y un lápiz en una esquina (para Cold Case 02, 4605211787).
2. `G-025 fondo-piano.png`: teclado de piano vertical visto en diagonal desde arriba, luz de tarde, superficie lisa oscura al centro donde apoyar una partitura (para 4605991888 y 4605998382).
3. `G-025 fondo-piano-kids.png`: igual que el anterior pero más luminoso, con lápices de colores (rojo, naranja, amarillo, verde, azul) en una esquina y un adorno navideño pequeño (para 4605993316).
En el Doc: para cada imagen el prompt exacto que usaste, tamaño en px, y una línea diciendo qué cuadrante quedó limpio. Si image_references permite tomar como referencia una de nuestras fotos de Drive > Miniaturas (por ejemplo 1uJP_ZOjcPzBNxIspKqmEyiDhd3r3exxZ), haz una cuarta variante "fondo-ski-lodge-ref" y di si respetó la paleta.

## Formato de la respuesta
Español. Doc `G-025 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas; los PNG en Entregas. Máximo 800 palabras.
