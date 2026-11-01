# Canal Claude ↔ Gemini (a través del repo y de Drive)

Pedido por Cris el 2026-10-30: "una carpeta con prompts para Gemini, para usar todo su poder
hablando con él a través del repo". Gemini aquí es la **app** de Gemini con la cuenta Google AI
Pro de Cris (Deep Research, Veo, Nano Banana, NotebookLM, Canvas, navegación), no la API
(`scripts/gemini/gemini.py`, que ya usamos para texto y voz gratis).

## Lo que verificamos antes de diseñarlo (Google, ayuda oficial, leído el 2026-10-30)

| Capacidad de la app de Gemini | ¿Sí? | Fuente |
|---|---|---|
| Leer un repo de GitHub | Sí, importándolo con la app GitHub en el prompt (una foto fija del repo; público sin vincular cuenta) | support.google.com/gemini/answer/16176929 |
| **Escribir en un repo** (commit, archivo, issue, PR) | **No.** "What Gemini can't do with the GitHub app: write to a code repository; retrieve commit history, pull requests…" | misma página |
| Leer una URL pública | Sí, la app lee páginas web; en una Tarea también puede navegar con un navegador remoto | answer/17094507 |
| Tareas programadas ("Tareas" / Gemini Spark, con horario cada hora, día, semana) | Sí, con AI Pro, cuenta personal, Keep Activity y Personal Intelligence activos; no en la UE ni Reino Unido | answer/17094710 |
| Crear archivos (Docs, Sheets, PDF, presentaciones) y guardarlos en Drive | Sí en Tareas ("Deep dive on topics & create files"; Spark crea y edita Google Docs y archivos de Drive) | answer/17094507, 9to5google 2026-07-23 |
| Los "Schedules" clásicos de un chat | Solo entregan texto dentro del chat de Gemini: no sirven para que Claude lea la respuesta | answer/16316416 |

## Lo que Gemini puede hacer DE VERDAD en una tarea programada (G-001, 2026-10-30 14:37 Chile)

| Herramienta | ¿En tarea programada? | Qué pedir entonces |
|---|---|---|
| Leer la URL raw de GitHub | **No** ("restricciones de acceso del sandbox"); leyó el espejo `GEMINI-PENDIENTES` de Drive | El espejo en Drive es OBLIGATORIO tras cada cambio de PENDIENTES.md |
| Búsqueda y navegación web (Google Search, Browse, navegador autónomo) | Sí | `herramienta: navegar` o `deep-research` (lo hace con búsqueda estructurada; marca `parcial`) |
| Deep Research (la herramienta con ese nombre) | No | Pedir "investiga con búsqueda web y cita fuentes"; G-002 y G-003 salieron así en ~3 min |
| Imágenes (Nano Banana / Imagen 3; 1:1, 4:3, 3:4, 16:9, 9:16) | **Sí** (G-010: 2 PNG 1200x896 en Entregas, con SynthID) | `herramienta: nano-banana`, `entrega: imagen` en Entregas |
| Video (Veo) | **No** (G-004) | No pedir video; para B-roll usar `gemini.py video --pago` (API) o fotos |
| Google Docs, Sheets, PDF, presentaciones en Drive | Sí (Docs G-001; Sheets G-006 y G-008; Slides y PDF declarados) | `entrega: doc`, `sheet`, `pdf`, `slides` |
| YouTube: datos y transcripción de un video por URL/video_id (`youtube:get_video_information`) | **Sí** (G-006): vistas, likes, fecha, duración, transcripción, fotogramas por segundo | Pasar SIEMPRE la URL o el video_id; sin él no encuentra Shorts recientes (G-007) |
| YouTube: listar los Shorts de un canal, comentarios | Parcial / No (G-006) | Búsqueda site:youtube.com/shorts + video_ids; no pedir comentarios |
| Etsy en página (fotos, video, "On Etsy since") | **No** (DataDome bloquea browse, G-008); precios y títulos sí desde snippets | Lo que no esté en un snippet se mira por el puente |
| Pinterest | **No** (G-009, G-012: el índice de google:search excluye pinterest.com y browse lo bloquea) | Auditar pines desde nuestro entorno; a Gemini pedirle páginas de destino |
| Navegador autónomo (`web_browser_agent`) | **No** en tareas programadas (G-013: timeout `<empty>`) | No pedirlo |
| Python en sandbox → PDF/PNG/xlsx/pptx subidos como binario | **Sí** (G-014: Pillow, pypdf, Chromium headless, openpyxl, python-pptx; sin reportlab ni internet) | `entrega: pdf`/`imagen`, texto exacto en la tarea; utilería de juegos en serie |
| YouTube fotograma a fotograma | **Sí** (G-015: 180 frames + transcripción) | Auditorías de ritmo por URL |
| Cupo de búsqueda web | ~10-12 llamadas a google:search/browse por ejecución (G-009) | Máximo 2 tareas `navegar`/`deep-research` por hora; PENDIENTES.md lo dice en la regla 1b |
| Elegir el modelo | **No** desde dentro (G-011); se autodeclara "Gemini 2.5 Pro" | Solo Cris, en la app, si la Tarea tiene selector |
| NotebookLM: crear cuaderno y añadir fuentes | Sí (G-005 creó el cuaderno) | Cuadernos como memoria consultable; preguntas textuales |
| NotebookLM: Audio Overview | **No** (G-005) | Audio a 2 voces: `gemini.py dialogo` (API) |
| Canvas | No (es interfaz de la web) | — |
| Archivos .txt en Entregas | Los convierte a Google Doc (y G-001 lo creó dos veces) | Pedir siempre Google Doc; tolerar duplicados |

Gemini se autodeclaró "Gemini 2.5 Pro" en modo agente; su sandbox no tiene salida a internet (sólo Search y Browse). Las 5 tareas se respondieron en una sola corrida de ~6 min (17:37-17:43 UTC), 1 h 14 min después de que Cris activara la tarea.

Conclusión: el repo es la memoria y el buzón de **Claude**; la mano de **Gemini** es Google
Drive. Gemini lee las tareas en una URL pública del repo (o en su espejo en Drive) y deja sus
respuestas como Google Docs en una carpeta de Drive que Claude lee con el conector. Claude
copia cada respuesta al repo para que quede en git y la usen todos los hilos.

## Dónde está cada cosa

```
gemini/
  README.md          este protocolo
  PENDIENTES.md      GENERADO: todas las tareas abiertas, completas, en un solo archivo (lo que lee Gemini)
  PROMPT-TAREA-GEMINI.md  el texto de la tarea programada que Cris pegó en Gemini (una vez)
  registro.csv       una fila por tarea: id, fechas, hilo, estado, Doc de respuesta
  inbox/G-NNN-<slug>.md   tareas abiertas (frontmatter + texto)
  outbox/G-NNN.md    respuestas de Gemini copiadas desde Drive (frontmatter + texto)
  done/              tareas ya respondidas o canceladas (se mueven desde inbox)
scripts/gemini/bandeja.py   pedir · pendientes · recibir · cerrar · mostrar · estado
.claude/skills/gemini-canal/SKILL.md   cómo lo usa un hilo de Claude, paso a paso
```

Drive (cuenta cdevidts1, la misma del conector de Drive de Claude):
`Mi unidad > Side Husle Claude > Gemini` (id `1-mAs2etmZt8fH7-YIlH9aEDJRfbBB73-`)
- `GEMINI-PENDIENTES` (Google Doc): espejo de `PENDIENTES.md`, por si Gemini no puede leer la URL.
- `Respuestas/` (`1WqcooCtde-MUKygT4aLB5Uhdk7Vf3-ax`): un Google Doc por tarea, `G-NNN RESPUESTA`.
- `Entregas/` (`1GyhIPtv-6WICQJoRhmdzzAnVZt5V1Xh1`): archivos que no son texto, `G-NNN <nombre>`.

URL pública que lee Gemini: `https://raw.githubusercontent.com/cdevidts/NLPAGE/main/gemini/PENDIENTES.md`
(por eso las tareas se empujan a **main**; una rama no le sirve a Gemini).

## El ciclo

1. **Claude pide.** `bandeja.py pedir ...` crea `inbox/G-NNN-<slug>.md`, agrega la fila a
   `registro.csv` y regenera `PENDIENTES.md`. Commit y push a main. Luego, con el conector de
   Drive, se reemplaza el Doc `GEMINI-PENDIENTES` (crear el nuevo, papelera al viejo).
2. **Gemini trabaja** cuando corre su tarea programada: lee `PENDIENTES.md`, hace cada tarea
   abierta, crea `G-NNN RESPUESTA` en Respuestas (primera línea `estado: hecho|parcial|no-puedo`)
   y los archivos en Entregas. Si no hay tareas, no hace nada.
3. **Claude recoge.** `bandeja.py estado` dice qué buscar; con Drive `search_files` en
   Respuestas y `read_file_content` se baja el texto y `bandeja.py recibir G-NNN --archivo ...
   --doc <url>` lo guarda en `outbox/`, mueve la tarea a `done/` y quita la tarea de
   `PENDIENTES.md`. Commit, push y espejo en Drive otra vez.
4. **Claude usa** la respuesta en su trabajo y anota en `registro.csv`/journal qué sirvió.

Quién recoge: el hilo que pidió (al despertar), el turno diario de este hilo (12:07 Chile: recoge,
reparte a los dueños, rellena la cola, pide la automejora los lunes) y, de respaldo, el turno mañana
de operación (punto 5b en `memoria/prompts-turnos.md` del proyecto).

Destinatarios al repartir (actualizado 2026-11-01; el coordinador avisa si cambia):

| Tema | Hilo dueño | Cómo |
|---|---|---|
| YouTube, Shorts, loop viral (ganchos, ritmo, auditorías de nuestros Shorts) | "Montar videos con Remotion para Shorts y Etsy" (cmsg_01RaWNwjKKK77Y5ZAm7XgnqUX3dSuCyy8ApoZxM83pMo1r); el hilo "Crear sistema de viralidad para Shorts" está CERRADO | `message_thread` |
| Etsy: competencia, títulos, precios, miniaturas, visibilidad | Operación autónoma de la tienda (OPS) | `message_coordinator` |
| Pinterest, Gumroad, pines | Canales de venta y marketing | `message_coordinator` |
| Utilería y expedientes de los juegos de misterio | Crear juegos de misterio imprimibles | `message_coordinator` |
| Capacidades del canal, protocolo, automejora | Este hilo | — |

## Formato de una tarea (`inbox/G-NNN-<slug>.md`)

```
---
id: G-002
titulo: Tiendas de Etsy que venden misterios imprimibles
pedido: 2026-10-30
hilo: Conversar con Gemini a través del repo
herramienta: deep-research        # texto | deep-research | navegar | nano-banana | veo | notebooklm | canvas | sheets
entrega: doc                      # doc | pdf | sheet | imagen | video | audio | slides
estado: pendiente
vence: 2026-11-03                 # opcional
prioridad: alta                   # opcional
---
## Contexto      (lo que Gemini necesita saber; sin secretos ni datos de compradores)
## Qué quiero    (concreto y medible)
## Formato de la respuesta   (secciones, largo máximo, idioma, fuentes)
```

Reglas de redacción: una tarea = un resultado; decir la herramienta que se espera
("usa Deep Research"); pedir fuentes con URL; máximo 24 KB por tarea (Gemini la lee entera en
PENDIENTES.md); pedir siempre que, si no puede, responda `no-puedo` con el motivo: así
aprendemos qué permite la tarea programada y qué no.

## Formato de la respuesta (`outbox/G-NNN.md`)

Frontmatter con `id`, `titulo`, `pedido`, `recibido`, `estado`, `hilo`, `doc` (link al Google
Doc) y debajo el texto tal como lo entregó Gemini. Los archivos de Entregas no se copian al
repo (pesan); se enlazan desde la respuesta y, si un hilo los necesita, los baja con el conector.

## Reglas de Cris para este canal (2026-10-30 17:53 UTC)
- La tarea corre **cada hora** y "es prácticamente ilimitada": usarla bastante. La cola nunca se deja
  vacía: mínimo 3 tareas útiles pendientes (`bandeja.py estado` avisa). Cada hilo pide lo suyo.
- Siempre un modelo fuerte (Gemini 4 Argon / Pro / Deep Think): el encabezado de PENDIENTES.md lo
  exige y cada respuesta trae `modelo:` en la línea 3; `recibir` lo guarda en `registro.csv`. Si
  responde un modelo flojo, se vuelve a pedir diciéndolo.
- Gemini conversa con Claude, no con Cris: las respuestas van dirigidas a Claude y Claude no le
  pide a Cris que transmita nada. Nada de este canal se le reporta a Cris salvo lo que cambie el negocio.
- Claude hace que Gemini mejore: tarea de automejora cada semana (G-011 fue la primera; la pide el
  turno diario de este hilo los lunes), bitácora `gemini/CAPACIDADES.md` y sondas de capacidades nuevas.
- Explotar lo que Gemini hace mejor que el contenedor: leer YouTube (listados, vistas, transcripciones;
  el contenedor está bloqueado por "no soy un bot"), Etsy y Pinterest sin API, Sheets, imágenes.

## Privacidad y límites
- Nunca van a Gemini: claves, tokens, datos de compradores, soluciones de los juegos.
- Google puede usar lo que la app recibe para mejorar sus productos (cuenta personal).
- La tarea programada corre cada hora (Cris la activó el 2026-10-30 ~16:30 UTC y la pasó a cada hora a las 17:53 UTC); una tarea nueva se responde en menos de 1 h. Deep Research tiene cupo diario en AI Pro: no pedir más de 2-3 por día.
- Si una tarea lleva más de 2 días pendiente, `bandeja.py estado` lo avisa: probablemente la
  tarea programada de Gemini se pausó (Google las apaga por inactividad) y hay que decírselo a Cris.

## Si Gemini no pudiera crear Docs en Drive desde una tarea
Es el riesgo principal (lo confirma la primera corrida con G-001). Alternativas, en orden:
(1) que la tarea genere el archivo y lo "exporte a Drive" (botón de Canvas) dentro del mismo
flujo; (2) Gmail: Gemini no envía correos; (3) Google Calendar: la app sí crea eventos, Claude
los leería por Zapier (poco espacio para texto). Si ninguna funciona, el canal queda solo para
lo que Gemini pueda dejar en Drive y se anota aquí.
