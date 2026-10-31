---
name: gemini-canal
description: SOLO para el proyecto AI Side Hustle (SheetSmithChile). Cómo un hilo de Claude le pide trabajo a la app de Gemini (Deep Research, Veo, Nano Banana, NotebookLM, Canvas, cuenta Google AI Pro de Cris) a través de gemini/ de este repo y de Drive, y cómo recoge y usa las respuestas. Úsala cuando necesites investigación profunda, video, imagen o audio que la API gratis de Gemini no da, y al despertar si pediste algo antes.
---

# Canal con Gemini (repo NLPAGE + Drive)

Protocolo completo: `gemini/README.md`. Herramienta: `python3 -I scripts/gemini/bandeja.py`.
La app de Gemini NO escribe en GitHub: lee las tareas en `gemini/PENDIENTES.md` (main) y deja
las respuestas como Google Docs en Drive > Side Husle Claude > Gemini > Respuestas.

## Qué puede y qué no (probado el 2026-10-30, tabla completa en gemini/README.md)
Sí: búsqueda y navegación web con fuentes (no es la herramienta "Deep Research", pero investiga
bien: G-002, G-003), imágenes Nano Banana, Google Docs/Sheets/PDF/Slides en Drive, crear cuadernos
de NotebookLM. No: Veo, Audio Overview, Canvas, y NO lee la URL raw de GitHub: el espejo
`GEMINI-PENDIENTES` en Drive es el camino real, actualízalo siempre.

## Cuándo usarlo (y cuándo no)
- Sí: investigación web con fuentes (competencia, tendencias, patrones de creadores), imagen
  Nano Banana, hojas de cálculo o PDF armados por Gemini, cuadernos de NotebookLM, navegar
  páginas que el contenedor no puede leer (YouTube, Etsy sin API).
- No: texto corto o voz (eso es `scripts/gemini/gemini.py`, gratis y al instante), nada con
  datos de compradores, claves ni soluciones de los juegos, nada urgente (la tarea programada
  corre cada hora: la respuesta llega en menos de 60 min).

## Pedir
1. Escribe la tarea en un archivo del scratchpad con tres secciones: `## Contexto`,
   `## Qué quiero`, `## Formato de la respuesta`. Concreta, con fuentes pedidas y la frase
   "si no puedes hacerlo desde una tarea programada, responde `estado: no-puedo` y el motivo".
2. `python3 -I scripts/gemini/bandeja.py pedir --titulo "..." --hilo "<título de tu hilo>" --herramienta deep-research --entrega doc --archivo tarea.md`
   (herramientas: texto, deep-research, navegar, nano-banana, veo, notebooklm, canvas, sheets;
   entregas: doc, pdf, sheet, imagen, video, audio, slides; opcional `--vence`, `--prioridad`).
3. Commit y **push a main** (`git push origin HEAD:main` desde una rama al día, o PR con merge
   inmediato): Gemini lee `raw.githubusercontent.com/cdevidts/NLPAGE/main/gemini/PENDIENTES.md`.
4. Espejo en Drive: `bandeja.py pendientes --md` imprime el texto; con el conector de Drive,
   `create_file` título `GEMINI-PENDIENTES`, `parentId` `1-mAs2etmZt8fH7-YIlH9aEDJRfbBB73-`,
   `contentMimeType` `text/markdown` (se convierte a Google Doc) y `trash_file` del
   `GEMINI-PENDIENTES` anterior (búscalo con `search_files title = 'GEMINI-PENDIENTES'`).
5. Anota en tu journal/ESTADO que esperas `G-NNN`, y qué harás con la respuesta.

## Recoger (al despertar, y siempre antes de volver a pedir lo mismo)
1. `python3 -I scripts/gemini/bandeja.py estado` lista lo pendiente y la consulta exacta de Drive.
2. Drive `search_files`: `parentId = '1WqcooCtde-MUKygT4aLB5Uhdk7Vf3-ax' and title contains 'G-NNN'`.
   Si hay Doc: `read_file_content`, guarda el texto en un archivo y
   `bandeja.py recibir G-NNN --archivo resp.txt --doc <viewUrl>` (lee `estado:` de la primera línea).
   Archivos adjuntos: `search_files parentId = '1GyhIPtv-6WICQJoRhmdzzAnVZt5V1Xh1'`; bájalos con
   `download_file_content` solo si los vas a usar.
3. Commit, push a main y espejo en Drive (paso 4 de "Pedir") para que Gemini no repita la tarea.
4. Usa la respuesta: una investigación va a `/mnt/project-files/plan/investigacion/<fecha>-<tema>.md`
   con la fuente "Gemini Deep Research, G-NNN"; un video/imagen va a `public/` o `assets/`
   según el pipeline. Si `estado: no-puedo`, anota en `gemini/README.md` (tabla de capacidades)
   qué no se puede, para no volver a pedirlo.
5. Si una tarea lleva más de 2 días sin respuesta, dile a Cris en una línea que revise que la
   tarea programada de Gemini siga activa (Google las pausa por inactividad). Nada más que eso.

## Cola permanente (regla de Cris, 2026-10-30: "úsalo bastante, es prácticamente ilimitado")
Gemini corre cada hora. Nunca dejes la cola con menos de 3 tareas útiles. Fuentes de tareas que
siempre sirven: YouTube (Shorts más vistos de un nicho con ganchos transcritos, métricas de nuestro
canal, crítica de un Short), Etsy (verificar competidores en página, títulos y precios de un nicho,
reseñas de un producto), Pinterest (pines que ganan por búsqueda), Sheets con datos tabulados,
imágenes de fondo (Nano Banana), traducciones revisadas, resúmenes de fuentes largas. Cada hilo pide
lo suyo con `pedir`; el turno diario de este canal (12:07 Chile) rellena la cola si nadie lo hizo.
Cada lunes se pide una tarea de automejora (modelo G-011: autocrítica de sus respuestas, inventario
de herramientas, mejoras al protocolo) y lo útil se aplica en `gemini/README.md` y aquí.

## Reglas
- Lo que Gemini afirme se verifica antes de actuar sobre dinero o listings (es investigación,
  no verdad); cita siempre "según Gemini (G-NNN)". Pide la verificación al propio Gemini
  ("abre la página y anota lo que VES", como G-008) antes de tocar precios o títulos.
- Cada tarea lleva IDs directos (URL o video_id del Short, file_id de Drive, URL del listing): sin ellos Gemini no encuentra lo reciente (G-007).
- Solo 2 tareas de búsqueda web (`navegar`, `deep-research`) por hora: PENDIENTES.md ya se lo dice a Gemini (regla 1b); si pides varias, ordénalas por prioridad porque hará las 2 primeras.
- Etsy y Pinterest no se dejan navegar (antibot / sesión): a Gemini se le pide lo que sale en snippets de Google; fotos, video y precios exactos se miran por el puente.
- Cada respuesta debe traer `modelo:` (línea 3). Si falta o es Flash/Lite, vuelve a pedir la tarea
  indicando que use el modelo más capaz (Gemini 4 Argon / Pro / Deep Think).
- Gemini le habla a Claude, no a Cris: nunca le pidas a Cris que le transmita algo a Gemini; lo que
  Gemini deba saber va en la tarea o en el encabezado de PENDIENTES.md (`bandeja.py`).
- Una tarea, un resultado. Sin tope de tareas (no usa la API), pero cada una con un uso concreto.
- Fechas absolutas; español o inglés según lo que vaya a usar el resultado.
