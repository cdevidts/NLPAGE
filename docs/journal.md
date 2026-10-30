# Diario de decisiones

## 2026-10-30 · Nace el pipeline (hilo "Montar videos con Remotion para Shorts y Etsy")
- Cris dejó NLPAGE (repo muerto) como repo de redes sociales y Videos-Next-Layer como
  referencia de solo lectura. Aclaró que la marca Next Layer no es la nuestra: se copió
  la técnica (Remotion, efectos medidos con el pico en el corte, ducking, -14 LUFS,
  revisión por GUION, tipografías locales) y se rehízo la parte de marca y de material.
- Diferencia de fondo: Next Layer edita clips de cámara con voz; aquí no hay cámara.
  El material son las páginas del PDF y las fotos del listing, y la voz es IA.
  Por eso se reescribió el pipeline en vez de adaptar buildReel/ingest.
- Decidido: Kokoro (EN) + Piper (ES), faster-whisper para tiempos, incompetech para
  música, audio propio cuando el producto lo trae. Detalle en docs/herramientas.md.
- Primeros videos: Short de Cold Case 01 en inglés y español, Short de partituras de
  piano (EN), y videos de listing 4:3 + GIF de #56 y #60.
- Espera a una persona: que Cris conecte el canal de YouTube en Metricool.

## 2026-10-30 · Videos de listing para el resto del catálogo de juegos y piano
- Pedido del hilo de operación: loops de Etsy para #57, #58, #59, #61, #62 y #55, en ese
  orden. Hechos y dejados en /mnt/project-files/videos/2026-10-30/ (operación los sube).
- Temas nuevos: `clasicos` (azul marino y dorado) para #62 y `navidad` (rojo y dorado,
  el mismo del piano) para #55. El pack #59 mezcla páginas de los tres casos.
- Arreglo: `producto` tomaba el sobre sellado "-EN-ES.pdf" como versión en español y
  pisaba sus páginas; ahora queda con alias `enes`.
- #55: solo páginas de juego; las de pistas y respuestas quedan fuera (regla 1).
- Descartado por ahora: Shorts de estos seis. Primero ver si los de #56 y #60 traen
  vistas cuando el canal esté conectado.
- Espera a una persona: que Cris conecte el canal de YouTube en Metricool.

## 2026-10-30 · YouTube conectado; primeros Shorts programados
- Cris conectó su canal (Cristobal De Vidts) en Metricool. Programados por el conector,
  16:00 hora Chile: #56 EN hoy, #60 EN el 31-oct y #56 ES el 1-nov.
- El MP4 se pasa como URL de raw.githubusercontent fijada a un commit: Metricool la
  aceptó y la copió a su CDN. No hizo falta hosting aparte.
- Declarado como contenido sintético (voz IA) en los tres.
- Espera: ver vistas de los tres antes de hacer Shorts de los otros productos.
