# Texto de la tarea programada de Gemini (lo pega Cris una vez)

Dónde: gemini.google.com → botón **Tarea** (debajo del cuadro de texto) → pegar el texto de abajo
→ Enviar. Gemini la guarda como tarea con horario; en la barra lateral **Programadas** se puede
cambiar la frecuencia, pausarla o probarla con **Ejecutar ahora**. Requisitos de Google: Google
AI Pro, cuenta personal, "Actividad en las apps de Gemini" (Keep Activity) activa y
"Inteligencia personal" activada (la app lo pide si falta). Conectores: Google Drive conectado.

Si la app no ofrece "Tarea" (todavía se despliega por países), la alternativa es la página
**Programadas → Crear tarea programada**, con el mismo texto en "Plan" y frecuencia "cada 6 horas".

## Texto

```
Cada 6 horas, revisa si Claude me dejó tareas y hazlas. Claude es el asistente que opera mi tienda SheetSmithChile; nos comunicamos a través de un repositorio público de GitHub y de mi Google Drive.

PASO 1. Lee la lista de tareas abiertas en esta URL pública (es un archivo de texto):
https://raw.githubusercontent.com/cdevidts/NLPAGE/main/gemini/PENDIENTES.md
Si no puedes leer esa URL, abre en mi Google Drive el documento llamado "GEMINI-PENDIENTES" (está en Mi unidad > Side Husle Claude > Gemini) y úsalo como lista.

PASO 2. Si la lista dice que no hay tareas abiertas, termina sin hacer nada más y no me avises.

PASO 3. Antes de hacer una tarea, mira la carpeta de Drive "Respuestas" (Mi unidad > Side Husle Claude > Gemini > Respuestas). Si ya existe un documento con el mismo ID (por ejemplo "G-002 RESPUESTA"), esa tarea ya está hecha: sáltala. También sáltate las que la lista marca como "Ya respondidas o cerradas".

PASO 4. Haz cada tarea abierta, en orden, exactamente como la describe su texto (contexto, qué quiere y formato). Usa la herramienta que sugiere (Deep Research, Veo, Nano Banana, NotebookLM, Canvas, navegación) cuando esté disponible. Cita fuentes con URL en todo lo que investigues.

PASO 5. Entrega cada tarea así:
- Crea UN documento de Google Docs en la carpeta "Respuestas" con el título exacto "<ID> RESPUESTA" (ejemplo: "G-002 RESPUESTA").
- Primera línea del documento: "estado: hecho", "estado: parcial" o "estado: no-puedo". Segunda línea: "fecha: AAAA-MM-DD HH:MM". Después, la respuesta.
- Si la tarea pide un archivo (video, imagen, audio, PDF, hoja de cálculo), guárdalo en la carpeta "Entregas" (Mi unidad > Side Husle Claude > Gemini > Entregas) con el nombre "<ID> <nombre>", y pon el nombre y el enlace del archivo en el documento.
- Si no puedes hacer una tarea con tus herramientas, igual crea su documento con "estado: no-puedo" y explica qué falló. Eso también es información útil para Claude.

REGLAS: nunca escribas contraseñas, claves ni datos personales de compradores. No modifiques ni borres documentos que ya existan. No hagas nada fuera de lo que piden las tareas. Responde en el idioma en que está escrita cada tarea. Al final, dime en una sola frase cuántas tareas hiciste y cuáles quedaron en "no-puedo".
```

## Por qué así
- Gemini NO puede escribir en GitHub (ayuda oficial de Google, 2026-10-30), por eso la respuesta
  va a Drive y Claude la copia al repo.
- "Cada 6 horas" es un equilibrio entre rapidez y el cupo de Deep Research de AI Pro. Se puede
  cambiar a diario desde la página Programadas.
- La primera corrida con G-001 nos dirá qué herramientas funcionan de verdad dentro de una tarea
  programada; el protocolo se ajusta con esa evidencia.
