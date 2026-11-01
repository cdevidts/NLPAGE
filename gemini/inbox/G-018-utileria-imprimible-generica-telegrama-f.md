---
id: G-018
titulo: Utilería imprimible genérica: telegrama, ficha de hotel e informe forense (Python)
pedido: 2026-11-01
hilo: Crear juegos de misterio imprimibles
herramienta: texto
entrega: pdf
estado: pendiente
---
## Contexto
G-014 demostró que puedes fabricar utilería imprimible con Python y subirla como binario. Queremos un juego de 3 plantillas GENÉRICAS reutilizables para expedientes de misterio de ficción (sin nombres de personas, sin lugares reales, campos en blanco o con "____" donde iría el dato). Sin google:search.

## Qué quiero
Tres PDF US Letter de 1 página cada uno, estética de 1985-1990, generados con Pillow o HTML+Chromium (lo que dé mejor tipografía), más un PNG de vista previa de cada uno (300 DPI):
1. `G-018 telegrama.pdf`: formulario de telegrama de la "WESTERN UNION"-style pero con nombre inventado "CONTINENTAL TELEGRAPH CO.", con campos: DATE, FROM, TO, y un cuerpo de 4 líneas en mayúsculas con STOP entre frases: "ARRIVING FRIDAY NIGHT STOP DO NOT SPEAK TO ANYONE ABOUT THE LEDGER STOP BURN THIS STOP". Textura de papel amarillo pálido, tipografía monoespaciada de teletipo, sello de recepción rectangular con hora "RECD 11:42 PM".
2. `G-018 ficha-hotel.pdf`: tarjeta de registro de hotel "MOUNTAIN LODGE — GUEST REGISTRATION", con campos: Name, Address, Room No., Arrival, Departure, Automobile / License, Signature; líneas manuscritas vacías; una nota al pie "Guests are requested to deposit valuables at the front desk". Papel crema con esquinas gastadas y un sello circular "PAID".
3. `G-018 informe-forense.pdf`: formulario "COUNTY CORONER — PRELIMINARY EXAMINATION REPORT", casillas: Case No., Date/Time, Location Found, Apparent Cause (checkboxes: Blunt force / Sharp force / Asphyxia / Toxic / Undetermined), Body Temperature, Rigor, Lividity, Notes (6 líneas vacías), Examiner signature. Papel blanco envejecido con sello "COPY" en rojo diagonal, tipografía de máquina de escribir.
Reglas: ningún texto fuera de lo indicado, sin nombres reales ni marcas registradas. Sube los 6 archivos a Entregas con esos nombres. En el Doc: qué librería usaste para cada uno, el código completo de UNO de los tres (el más complejo), y los problemas que encontraste.

## Formato de la respuesta
Español. Doc `G-018 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas.
