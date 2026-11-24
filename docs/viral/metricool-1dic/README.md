# Plan B del 1-dic: la cola por Metricool

Si el 1-dic Zapier sigue sin cupo, los Shorts salen por Metricool (marca cdevidts2, blogId 6078519; el plan gratis da 20 publicaciones al mes y los pines ya salen por Make, así que el cupo es para los Shorts). Cada JSON de esta carpeta trae los argumentos listos para `createScheduledPost`: `blogId`, `date` e `info` (pasar `info` como texto JSON). Título, descripción y tags salen tal cual del bloque `youtube` de cada plan; el video es la URL raw fija del commit que ya está en COLA.md. Se generaron el 24-nov.

Reglas: un Short por día a las 16:00 Chile, solo la red `youtube` (nunca `instagram`: en esa marca es de Next Layer), `isAiGeneratedContent` true porque la voz es IA. El orden alterna piano y misterio, con los villancicos antes de mediados de diciembre. Metricool no tiene borrar en el conector: programar de a uno, en el turno de las 14:07 Chile el Short de ese mismo día a las 16:00, para que, si Zapier vuelve, no quede un duplicado agendado. Si la fecha de un JSON ya pasó, cambiar `date` y `publicationDate.dateTime` al día que toque. Tras cada publicación: `experimento.py alta --post metricool`, video_id en shorts.csv (por RSS) y borrar su fila en COLA.md.

| # | Fecha | Plan | Categoría | Archivo |
|---|---|---|---|---|
| 1 | 2026-12-01 16:00 Chile | 62-piano-oda-letras-es | MUSIC | 1-62-piano-oda-letras-es.json |
| 2 | 2026-12-02 16:00 Chile | 60-piano-jingle-letras-es | MUSIC | 2-60-piano-jingle-letras-es.json |
| 3 | 2026-12-03 16:00 Chile | 56-mary-celeste-real-es | ENTERTAINMENT | 3-56-mary-celeste-real-es.json |
| 4 | 2026-12-04 16:00 Chile | 61-piano-noche-paz-colores-es | MUSIC | 4-61-piano-noche-paz-colores-es.json |
| 5 | 2026-12-05 16:00 Chile | 56-faro-flannan-real-es | ENTERTAINMENT | 5-56-faro-flannan-real-es.json |
| 6 | 2026-12-06 16:00 Chile | 62-piano-para-elisa-letras-es | MUSIC | 6-62-piano-para-elisa-letras-es.json |
| 7 | 2026-12-07 16:00 Chile | 62-piano-canon-letras-es | MUSIC | 7-62-piano-canon-letras-es.json |
