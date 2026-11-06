# Auditoría por fotogramas de nuestros Shorts con la API gratis de Gemini (2026-11-06)

**Según Gemini 3.6 Flash por API (free tier, `gemini.py youtube`), sin verificar a mano.** Hecho en la hora libre que dio Cris el 6-nov (10:59-12:00 UTC). Cada análisis tardó 24-42 s y costó US$0. Mismo prompt para los cuatro: tabla por segundo (voz literal, texto en pantalla, qué se ve, corte), cortes totales y en 10 s, palabras por segundo, segundo probable de abandono marcado "visto" o "supuesto".

## Lo que sale al comparar (mi lectura, no de Gemini)

| Video | Vistas | Duración | Palabras/s | Cortes | Cortes en 10 s | Abandono estimado |
|---|---|---|---|---|---|---|
| `_BUAF1B1JXI` caso 01 ES | 676 | 46 s | 2,26 | 7 | 1 | s 41 (entra el CTA) |
| `uFgGEGATfA0` caso 01 EN | 1 | 46 s | 2,35 | 11 | 4 | s 39-41 (entra el CTA) |
| `EO-UvYWLfXA` caso 02 EN | 38 | 54 s | 2,61 | 9 | 1 | s 7-8 (primer cambio de documento) |
| `A-PErrtdak8` competidor (12,1 M) | 12,1 M | 28 s | 3,4 (3,7 en voz activa) | 14 | 5 | s 8-12 (4 s sin voz) |

1. **El caso 01 en español y en inglés son la misma edición**: mismo documento en cada tramo, mismos rótulos rojos arriba, mismo cierre. Gemini contó 7 cortes en ES y 11 en EN; a 1 fotograma por segundo la cuenta es aproximada, así que no hay una diferencia de edición demostrada. La única diferencia que sale del video es el idioma. Eso apoya la hipótesis del hilo de video (ES > EN por audiencia, no por edición).
2. **El competidor habla un 50 % más rápido (3,4 vs 2,3 palabras/s), dura la mitad (28 vs 46-54 s) y corta el doble (14 cortes, 5 en los primeros 10 s)**. Nuestros tres Shorts tienen 1 corte en los primeros 10 s (salvo la cuenta de 4 en EN). Su subtítulo es UNA palabra por fotograma arriba-centro; el nuestro apila 2-4 líneas abajo más un rótulo arriba.
3. **El competidor no tiene CTA**: termina en "ni qué era" y corta. En los tres nuestros, el modelo ubica el abandono justo donde entra "este caso es ficción... SheetSmithChile en Etsy" (s 41 y s 47): los últimos 5-8 s son los que menos retienen. Coincide con G-029 (10 de 14 ganadores sin CTA comercial).
4. **Caso 02 EN**: el modelo lo ve "estático" (documentos densos) y sitúa el abandono en s 7-8; es el que más texto apila por fotograma (hasta 5 líneas abajo).
5. **Pero el competidor también tiene un hueco**: 4 s sin voz (s 8-12) que el modelo marca como riesgo de abandono. Pausas sí, pero de 1 s, no de 4.

Qué probar en el próximo Short (para el hilo de video, hipótesis de una variable cada una): (a) 30-35 s en vez de 46-54; (b) voz a 3+ palabras/s; (c) subtítulo de una palabra arriba-centro; (d) sin CTA hablado: la voz termina en la última frase del caso y "ficción" + "SheetSmithChile" quedan solo como texto 3 s.

Receta: `python3 -I scripts/gemini/gemini.py youtube <id> --archivo prompt.md --salida out.md` en NLPAGE. Cada Short publicado puede auditarse el mismo día, sin esperar la tarea horaria de la app.

## Caso 01 en español · `_BUAF1B1JXI` (676 vistas)

Aquí tienes el análisis segundo a segundo del video:

### 1. Tabla de desglose segundo a segundo

| Segundo | Lo que se oye (literal) | Texto en pantalla (literal, posición, estilo) | Qué se ve | Corte (Sí/No) |
| :--- | :--- | :--- | :--- | :--- |
| **00:00** | El dueño de un teatro... | "MUERTO" (centro-arriba, caja roja, grande) / "EL DUEÑO DE" (abajo, blanco/rojo, grande) | Periódico *The Port Merrow Courier* con noticia de la muerte. | No |
| **00:01-00:02** | ...muerto en la última función. | "MUERTO EN LA / ÚLTIMA FUNCIÓN" (abajo, grande) | Zoom al titular del periódico. | No |
| **00:03-00:07** | Desmond Ashcombe, 64 años, al pie de su escalera de biblioteca... | "SEIS LIBROS" (arriba, caja roja) / "DESMOND ASHCOMBE / 64 AÑOS / SU ESCALERA DE / BIBLIOTECA" (abajo) | Documento "Croquis de la escena del crimen" (plano de la oficina y cuerpo). | **Sí** (en 00:03) |
| **00:08-00:11** | ...seis libros en el suelo, sus lentes rotos. | "SEIS LIBROS EN EL / SUELO / SUS LENTES / ROTOS" (abajo, grande) | Acercamiento en el croquis a la zona del cuerpo y la escalera. | No |
| **00:12-00:15** | Parecía una caída, la médica forense dijo que no. | "¿UNA CAÍDA?" (arriba, caja roja) / "PARECÍA UNA / CAÍDA / LA MÉDICA / FORENSE" (abajo) | Documento "Informe de incidente" con sello rojo "HOMICIDIO". | **Sí** (en 00:12) |
| **00:16-00:21** | La policía detuvo al dramaturgo, dos días después lo soltó. El caso quedó archivado. | "CASO ARCHIVADO" (arriba, caja roja) / "LA POLICÍA / DETUVO / AL DRAMATURGO / LO SOLTÓ / EL CASO / ARCHIVADO" (abajo) | Documento "Personas de interés" mostrando sospechosos numerados. | **Sí** (en 00:16) |
| **00:22-00:27** | Trece años después, unos obreros que remodelan el teatro vacío encuentran su libreta perdida... | "13 AÑOS DESPUÉS" (arriba, caja roja) / "TRECE AÑOS / DESPUÉS / UNOS OBREROS QUE / REMODELAN EL / TEATRO / VACÍO / ENCUENTRAN SU" (abajo) | Documento "Libreta de bolsillo" con notas a mano y código gráfico. | **Sí** (en 00:22) |
| **00:28-00:32** | ...y dos hojas a medio quemar escondidas detrás de un panel suelto. | "HOJAS QUEMADAS" (arriba, caja roja) / "LIBRETA PERDIDA / Y DOS / HOJAS / A MEDIO / QUEMAR / ESCONDIDAS DETRÁS DE / UN PANEL SUELTO" (abajo) | Documento "Dos páginas impresas, parcialmente quemadas". | **Sí** (en 00:28) |
| **00:33-00:37** | Su teléfono sigue bloqueado. Cinco personas tenían motivos para matarlo. | "5 SOSPECHOSOS" (arriba, caja roja) / "SU TELÉFONO / SIGUE / BLOQUEADO / CINCO PERSONAS / TENÍAN" (abajo) | Retorno al documento de "Personas de interés" (sospechosos). | **Sí** (en 00:33) |
| **00:38-00:40** | Una de ellas lo hizo. ¿Lo resuelves? | "MOTIVOS PARA / MATARLO / UNA LO HIZO / ¿LO RESUELVES?" (abajo, grande) | Portada del expediente del juego "El Último Telón". | **Sí** (en 00:38) |
| **00:41-00:46** | Este caso es ficción, pero lo puedes resolver tú. Lo encuentras en nuestra tienda de Etsy. | "¿LO RESUELVES?" (arriba) / "Caso Archivado N.º 01 · El Último Telón" / "SheetSmithChile en Etsy" (abajo, blanco/pequeño) | Muestra de la carpeta del caso e información de compra. | No |

---

### 2. Cortes totales y en los primeros 10 segundos
* **Cortes totales:** 7 cortes de escena (en 00:03, 00:12, 00:16, 00:22, 00:28, 00:33 y 00:38).
* **Cortes en los primeros 10 segundos:** 1 corte (en el segundo 00:03).

---

### 3. Ritmo de locución (Palabras por segundo)
* **Total de palabras habladas:** 104 palabras.
* **Duración total:** 46 segundos.
* **Promedio:** ~2.26 palabras por segundo (locución rápida y continua).

---

### 4. Punto estimado de abandono de audiencia
* **Segundo estimado:** 00:41.
* **Qué pasa en pantalla:** La voz narrativa pasa de contar el misterio a revelar la naturaleza comercial ("Este caso es ficción, pero lo puedes resolver tú... SheetSmithChile en Etsy"). En pantalla aparece el texto promocional con el enlace de la tienda.
* **Clasificación:** 
  * *Visto en el video:* Aparición del texto "SheetSmithChile en Etsy" y la portada comercial del producto.
  * *Supuesto:* El espectador abandona al identificar que el misterio no es un crimen real, sino una llamada a la acción publicitaria.

## Caso 01 en inglés · `uFgGEGATfA0` (1 vista)

Aquí tienes el análisis segundo a segundo del Short de YouTube:

### 1. Tabla de análisis (1 fotograma por segundo)

| Segundo | Lo que se oye (literal) | Texto en pantalla (literal, posición, tamaño) | Qué se ve | Corte |
| :--- | :--- | :--- | :--- | :--- |
| **00:00-00:01** | "A theater owner..." | Sup: SHEETSMITHCHILE (centro, peq), FOUND DEAD (centro, med). Inf: A THEATER OWNER (centro, grande, rojo/blanco). | Recorte de periódico antiguo sobre la muerte del dueño del teatro. Fondo oscuro. | No |
| **00:01-00:03** | "...found dead on closing night." | Sup: Mismo header. Inf: FOUND DEAD ON CLOSING NIGHT (centro, grande). | Zoom al artículo de prensa con el titular "Theater owner found dead on closing night". | Sí (00:01) |
| **00:04-00:05** | "Desmond Ashcombe, 64..." | Sup: SIX BOOKS (arriba, med). Inf: DESMOND ASHCOMBE SIXTY-FOUR (abajo, grande). | Boceto de la escena del crimen (plano de la oficina con la víctima marcada). | Sí (00:04) |
| **00:06-00:11** | "...at the foot of his library ladder, six books on the floor. His glasses were broken." | Sup: SIX BOOKS. Inf: AT THE FOOT / LADDER / SIX BOOKS ON THE FLOOR / BROKEN (abajo, grande, dinámico). | Acercamiento progresivo a los detalles del plano (escalera, libros, víctima). | Sí (00:07, 00:09) |
| **00:12-00:15** | "It looked like a fall. The medical examiner said it wasn't." | Sup: NOT A FALL (arriba, med). Inf: A FALL / THE MEDICAL EXAMINER / SAID IT WASN'T (abajo, grande). | Informe policial de incidentes. Aparece un sello rojo de "HOMICIDE". | Sí (00:12) |
| **00:16-00:21** | "Police arrested the playwright. Two days later they let him go. The case went cold." | Sup: COLD CASE (arriba, med). Inf: POLICE ARRESTED THE PLAYWRIGHT / TWO DAYS LATER / GO / COLD (abajo, grande). | Documento "Persons of Interest" con fichas de sospechosos. Zoom al sospechoso #5. | Sí (00:16, 00:18) |
| **00:22-00:27** | "Thirteen years later, builders renovating the empty theater find his missing notebook..." | Sup: 13 YEARS LATER (arriba, med). Inf: THIRTEEN YEARS LATER / BUILDERS RENOVATING THE EMPTY THEATER FIND / HIS MISSING NOTEBOOK (abajo, grande). | Documento de evidencia "Pocket Notebook" con notas escritas a mano y código cifrado. | Sí (00:22) |
| **00:28-00:31** | "...and two half-burned pages hidden behind a loose panel." | Sup: HALF-BURNED PAGES (arriba, med). Inf: AND TWO HALF-BURNED PAGES / HIDDEN BEHIND A LOOSE PANEL (abajo, grande). | Hoja de evidencia con páginas parcialmente quemadas. | Sí (00:28) |
| **00:32-00:36** | "His phone is still locked. Five people had a reason to want him dead." | Sup: 5 SUSPECTS (arriba, med). Inf: HIS PHONE IS STILL LOCKED / FIVE PEOPLE HAD / WANT HIM DEAD (abajo, grande). | Ficha policial con la lista completa de los 5 sospechosos. | Sí (00:32) |
| **00:37-00:46** | "One of them did it. This case is fiction, but you can solve it yourself. Find it on Etsy at SheetSmithChile." | Sup: ONE OF THEM DID IT -> CAN YOU SOLVE IT? (arriba). Inf: Cold Case File No. 01 / SheetSmithChile on Etsy (botón rojo, grande). | Portada del expediente de juego "The Final Curtain" y anuncio del producto impreso en Etsy. | Sí (00:37, 00:39) |

---

### 2. Conteo de cortes
* **Cortes totales:** 11 cortes de edición.
* **Cortes en los primeros 10 segundos:** 4 cortes (en 00:01, 00:04, 00:07 y 00:09).

---

### 3. Ritmo de locución (Palabras por segundo)
* **Total de palabras habladas:** 108 palabras.
* **Duración total:** 46 segundos.
* **Velocidad promedio:** **2.35 palabras por segundo (WPS)**.

---

### 4. Estimación de abandono de audiencia
* **Segundo de posible abandono:** Entre **00:39 y 00:41**.
* **Qué pasa en pantalla:** La narrativa del crimen termina y cambia abruptamente a la promoción comercial del producto digital ("Can you solve it? SheetSmithChile on Etsy"). *(Supuesto)*.

## Caso 02 en inglés · `EO-UvYWLfXA` (38 vistas)

Aquí tienes el análisis detallado del Short de YouTube:

### 1. Tabla de análisis fotograma a fotograma

| Segundo | Lo que se oye (literal) | Texto en pantalla (literal, posición, tamaño) | Qué se ve | Corte (Sí/No) |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:02** | "Nineteen eighty-nine. Greyhorn Mountain..." | `SHEETSMITHCHILE` (arriba, pequeño) / `GREYHORN, 1989` (arriba, mediano) / `NINETEEN EIGHTY-NINE` (abajo, grande) | Ficha policial/caso no resuelto "The Snow Remembers". | No |
| **00:03 - 00:06** | "...Elsa Brandvold, 54, walks into a snowstorm..." | `GREYHORN MOUNTAIN` / `ELSA BRANDVOLD` / `WALKS INTO A SNOWSTORM` (abajo, grande) | Acercamiento a los datos de la víctima en el documento. | No |
| **00:07 - 00:12** | "It's the night of the winter carnival gala at her own ski lodge. She never comes back." | `NEVER CAME BACK` (arriba, grande) / `CARNIVAL GALA AT LODGE` / `SHE NEVER COMES BACK` (abajo, grande) | Transición a folleto informativo "Greyhorn Lodge". | **Sí** (00:07) |
| **00:13 - 00:19** | "Next morning, they find her at the bottom of Hollow Gully, 9 meters below the footbridge to her chalet." | `9 METERS DOWN` (arriba, grande) / `NEXT MORNING` / `AT THE BOTTOM` / `NINE METERS BELOW` / `FOOTBRIDGE TO HER CHALET` (abajo, grande) | Croquis de la escena del crimen "Scene Sketch - Footbridge". | **Sí** (00:13) |
| **00:20 - 00:26** | "The sheriff calls it an accident: an icy bridge, house slippers, one glass of wine too many." | `AN ACCIDENT?` (arriba, grande) / `THE SHERIFF CALLS` / `AN ICY BRIDGE` / `HOUSE SLIPPERS` / `ONE GLASS OF WINE TOO MANY` (abajo, grande) | Informe oficial del Sheriff ("Larch County Sheriff's Office"). | **Sí** (00:20) |
| **00:27 - 00:33** | "Thirty-seven years later, the mountain gives back three things: a roll of film nobody ever developed..." | `UNDEVELOPED FILM` (arriba, grande) / `THIRTY-SEVEN YEARS LATER` / `FILM NOBODY EVER DEVELOPED` (abajo, grande) | Hoja de contactos de fotos "The Gala Roll". | **Sí** (00:27) |
| **00:34 - 00:36** | "...her green notebook melting out of the snow..." | `THE NOTEBOOK` (arriba, grande) / `HER GREEN NOTEBOOK` / `MELTING OUT OF THE SNOW` (abajo, grande) | Artículos de periódico sobre el hallazgo del cuaderno. | **Sí** (00:34) |
| **00:37 - 00:40** | "...and her strongbox. Nobody has ever opened it." | `LOCKED BOX` (arriba, grande) / `AND HER STRONGBOX` / `NOBODY HAS EVER OPENED IT` (abajo, grande) | Sobre de evidencia "Evidence Envelope A". | **Sí** (00:37) |
| **00:41 - 00:44** | "Five people at the lodge had a reason to want her gone." | `5 SUSPECTS` (arriba, grande) / `FIVE PEOPLE AT THE LODGE HAD` / `WANT HER GONE` (abajo, grande) | Documento con lista de sospechosos "Persons of Interest". | **Sí** (00:41) |
| **00:45 - 00:46** | "One of them did it." | `ONE OF THEM DID IT` (arriba/centro, grande) | Regreso a la portada del archivo del caso. | **Sí** (00:45) |
| **00:47 - 00:54** | "This case is fiction, but you can solve it yourself. Find it on Etsy at SheetSmithChile." | `CAN YOU SOLVE IT?` (centro, grande) / `SheetSmithChile on Etsy` (botón abajo, mediano) / `Cold Case File No. 02` (abajo, pequeño) | Plantilla promocional del juego imprimible y llamada a la acción. | **Sí** (00:47) |

---

### 2. Conteo de cortes totales y en los primeros 10 segundos
* **Cortes totales:** 9 cortes.
* **Cortes en los primeros 10 segundos:** 1 corte (en el segundo 00:07).

---

### 3. Palabras por segundo (WPS) de la locución
* **Total de palabras habladas:** 141 palabras.
* **Duración total:** 54 segundos.
* **Velocidad:** **2.61 palabras por segundo**.

---

### 4. Punto estimado de abandono de espectadores
* **Segundo de abandono estimado:** **00:07 - 00:08**
* **Qué pasa en pantalla ahí (visto en el video):** En el segundo 00:07 ocurre el primer cambio brusco de documento (pasa de la portada del expediente al folleto "Greyhorn Lodge") y entra el rótulo en rojo `NEVER CAME BACK`.
* **Razón del abandono (supuesto):** Tras los primeros 6 segundos de introducción narrativa, el espectador nota que el contenido es la presentación estática de un documento de lectura/juego impreso. Quienes no buscan juegos de rol/misterio en formato papel suelen hacer *scroll* al ver el primer cambio hacia textos densos.

## Competidor · `A-PErrtdak8` (12,1 M vistas, jessus_20)

Aquí tienes el análisis detallado del Short de YouTube:

### 1. Análisis segundo a segundo (1 fotograma por segundo)

| Segundo | Lo que se oye (literal) | Texto en pantalla (literal, posición, tamaño) | Qué se ve | Corte |
| :---: | :--- | :--- | :--- | :---: |
| **00:00** | El | misterio (centro superior, grande) | Creador hablando a cámara en su habitación. | No |
| **00:01** | misterio que nunca se reveló. | reveló (centro superior, grande) | Creador hablando a cámara. | No |
| **00:02** | En 2003 Yang Liwei | *Sin texto* | Astronauta chino (Yang Liwei) en la cápsula espacial. | Sí |
| **00:03** | fue el primer astronauta | el (centro superior, mediano) | Astronauta dentro del traje de astronauta. | No |
| **00:04** | chino en ir al espacio. | chino (centro superior, mediano) | Primer plano de astronauta en la nave. | No |
| **00:05** | Durante su travesía | durante (centro superior, mediano) | Vista de la Tierra y la atmósfera desde la órbita. | Sí |
| **00:06** | espacial escuchó un ruido | espacial (centro superior, mediano) | Toma del horizonte terrestre desde el espacio. | No |
| **00:07** | que no entendía qué era. | *Sin texto* | Rostro del astronauta tras la visera del casco. | Sí |
| **00:08** | *(Efecto de sonido de misterio)* | *Sin texto* | Astronauta reclinado en el interior de la cápsula. | No |
| **00:09** | *(Efecto de sonido de misterio)* | *Sin texto* | Retrato de astronauta mirando a cámara. | Sí |
| **00:10** | *(Efecto de sonido de misterio)* | *Sin texto* | Fotografía oficial del astronauta sonriendo. | Sí |
| **00:11** | *(Efecto de sonido de misterio)* | *Sin texto* | Vista de la Tierra a través de la ventana circular. | Sí |
| **00:12** | *(Música de suspenso)* | *Sin texto* | Vista exterior de la Tierra desde la ventana. | No |
| **00:13** | Según él, el sonido | él (centro superior, mediano) | Astronauta sonriendo con traje espacial. | Sí |
| **00:14** | era como martilleando | un (centro superior, mediano) | Astronauta sentado con el traje oficial. | No |
| **00:15** | un tubo de hierro | tuvo [sic] (centro superior, mediano) | Astronauta saludando con la mano. | Sí |
| **00:16** | con un mazo de madera. | mazo (centro superior, mediano) | Espectrograma/onda de audio animada sobre fondo negro. | Sí |
| **00:17** | El sonido no podía viajar | puede (centro superior, mediano) | Imagen del astronauta con cara de meme (*Trollface*). | Sí |
| **00:18** | en el espacio, por lo que no sabía | *Sin texto* | Astronauta recostado observando instrumentos. | Sí |
| **00:19** | si venía de fuera | venía (centro superior, mediano) | Astronauta en el interior del módulo. | No |
| **00:20** | o de dentro. | dentro (centro superior, mediano) | Rostro del astronauta mirando hacia arriba. | No |
| **00:21** | Miró por una ventana | ventana (centro superior, mediano) | Vista de la Tierra desde el tragaluz de la nave. | Sí |
| **00:22** | y no vio nada ni fuera | ni (centro superior, mediano) | Curvatura de la Tierra desde la escotilla. | No |
| **00:23** | ni dentro. | y (centro superior, mediano) | Astronauta rodeado de fotógrafos tras su regreso. | Sí |
| **00:24** | Y hasta el día de hoy no se sabe | sabe (centro superior, mediano) | Astronauta atendiendo a los medios. | No |
| **00:25** | qué golpeó su nave | nave (centro superior, mediano) | Vista del espacio exterior por la ventana circular. | Sí |
| **00:26** | ni qué era. | era (centro superior, mediano) | Vista de la Tierra en silencio. | No |
| **00:27** | *(Fondeo de tono dramático final)* | *Sin texto* | Toma final de la ventana mirando a la Tierra. | No |

---

### 2. Conteo de cortes
* **Cortes totales:** 14 cortes.
* **Cortes en los primeros 10 segundos (00:00 - 00:10):** 5 cortes (en los segundos 00:02, 00:05, 00:07, 00:09 y 00:10).

---

### 3. Palabras por segundo de la voz
* **Total de palabras habladas:** 96 palabras.
* **Duración total:** 28 segundos.
* **Promedio:** **3.43 palabras por segundo** (~3.7 palabras/segundo considerando únicamente los 26 segundos de locución activa).

---

### 4. Punto de abandono de audiencia
* **Segundo estimado:** **00:08 - 00:12**.
* **Qué pasa en pantalla (*visto en el video*):** La locución del narrador se detiene por completo durante 4 segundos. En pantalla se suceden imágenes fijas y clips breves del astronauta y la Tierra acompañados solo por un efecto de sonido misterioso.
* **Razón del abandono (*supuesto*):** El cese repentino de la voz explicativa interrumpe el ritmo del relato (*retención pasiva*), haciendo que el espectador pierda el hilo narrativo inicial y continúe desplazándose (*scrolling*) antes de que se reanude la explicación en el segundo 00:13.

