---
id: G-014
titulo: Sonda: Python en tu sandbox, recorte de periódico 1987 en PDF
pedido: 2026-10-31
hilo: Conversar con Gemini a través del repo
herramienta: texto
entrega: pdf
estado: pendiente
---
## Contexto
Sonda de capacidad propuesta en G-011: Python en tu sandbox (reportlab / Pillow) y subida de un binario con `drive:create_file(base64_content="file:///...")`. Si funciona, podremos pedirte accesorios imprimibles para los juegos de misterio sin gastar la API. No usa google:search.

## Qué quiero
Genera con Python un PDF tamaño carta (US Letter, 1 página) que imite un recorte de periódico envejecido de 1987, para un caso de FICCIÓN. Texto exacto que debe llevar (no inventes nombres ni hechos distintos; es un accesorio genérico):
- Cabecera del diario: "THE ALPINE GAZETTE" — "Thursday, February 12, 1987" — "25 cents".
- Titular: "BODY FOUND AT MOUNTAIN LODGE AFTER STORM".
- Subtítulo: "Sheriff's office asks guests to remain in the area; roads reopen Friday".
- Cuerpo: 3 párrafos cortos en inglés, sin nombres propios de personas (usa "the lodge owner", "a guest", "the night clerk"), con tono de periódico local: la tormenta cortó la carretera, el cuerpo fue hallado en la madrugada del miércoles cerca de la sala de calderas, la oficina del sheriff no confirma la causa.
- Un recuadro lateral: "WEATHER: Heavy snow continues through Saturday".
Estética: papel amarillento con manchas, tipografía serif de periódico, columnas, bordes irregulares (recorte), ligero ruido/grano. Sin marcas de agua visibles ni texto fuera del indicado.
Sube el PDF a Entregas como `G-014 recorte-1987.pdf` y también un PNG de vista previa `G-014 recorte-1987.png` (300 dpi aprox., 2550x3300 o proporcional). En el Doc pega el código Python completo que usaste (para que podamos repetirlo nosotros) y di qué librerías había disponibles.

## Formato de la respuesta
Español. Doc `G-014 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Si la subida binaria falla, dilo con el error exacto y sube al menos el PNG.
