---
name: gemini-canal
description: SOLO para el proyecto AI Side Hustle (SheetSmithChile). Cómo un hilo de Claude le pide trabajo a la app de Gemini (Deep Research, Veo, Nano Banana, NotebookLM, Canvas, cuenta Google AI Pro de Cris) a través de gemini/ de este repo y de Drive, y cómo recoge y usa las respuestas. Úsala cuando necesites investigación profunda, video, imagen o audio que la API gratis de Gemini no da, y al despertar si pediste algo antes.
---

# Canal con Gemini (repo NLPAGE + Drive)

Protocolo completo: `gemini/README.md`. Herramienta: `python3 -I scripts/gemini/bandeja.py`.
La app de Gemini NO escribe en GitHub: lee las tareas en `gemini/PENDIENTES.md` (main) y deja
las respuestas como Google Docs en Drive > Side Husle Claude > Gemini > Respuestas.

## Cuándo usarlo (y cuándo no)
- Sí: Deep Research con fuentes (competencia, tendencias, patrones de creadores), video Veo,
  imagen Nano Banana, Audio Overview de NotebookLM, documentos largos con Canvas, navegar
  páginas que el contenedor no puede leer.
- No: texto corto o voz (eso es `scripts/gemini/gemini.py`, gratis y al instante), nada con
  datos de compradores, claves ni soluciones de los juegos, nada urgente (la tarea programada
  corre cada 6 horas).

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

## Reglas
- Lo que Gemini afirme se verifica antes de actuar sobre dinero o listings (es investigación,
  no verdad); cita siempre "según Gemini (G-NNN)".
- Máximo 2-3 Deep Research por día (cupo de AI Pro). Una tarea, un resultado.
- Fechas absolutas; español o inglés según lo que vaya a usar el resultado.
