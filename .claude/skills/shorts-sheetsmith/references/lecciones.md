# Lecciones (cada una ya costó algo)

## Heredadas de Videos-Next-Layer (otra marca; se copió la técnica)
- **Mira el video, no frames sueltos.** `npm run watch` da lo que se escucha en cada
  segundo. Los errores de sonido y de subtítulo no se ven en un frame.
- **Tipografías con `@font-face` en una hoja de estilo**, desde `public/fonts/`. Con
  `new FontFace()` el render pintó parte del texto con la fuente de respaldo aunque
  `document.fonts.check()` dijera que cargó.
- **El pico del efecto cae en el corte**, no su inicio. Los efectos se eligen medidos
  (duración, ataque, brillo), no por el nombre: muchos "whoosh" duran 6 s.
- **Efectos sintetizados suenan a arena.** Se bajan (Mixkit), no se generan.
- **El mismo efecto repetido suena a máquina**: rotan dentro del video y cambian entre videos (semilla = slug).
- **El silencio digital es un error.** La música de cama sigue sonando entre escenas.
- **Música comercial = Content ID.** Solo CC BY con crédito, o audio propio.
- **Nada de lenguaje de diapositiva**: chips numerados, cajas con barra, barras de
  progreso y cross-fades largos hacían que un reel pareciera PowerPoint.

## De este repo
- 2026-10-30. **La voz lee mal los años en cifras**: Piper dijo "2013" y whisper oyó
  "2003". Números y años en letras en `dice`.
- 2026-10-30. **Whisper con el guion como pista oye lo que espera.** Con
  `initial_prompt` la compuerta daba 13/13 palabras sobre una voz que decía otra cosa.
  `palabras.py` ya no usa pista.
- 2026-10-30. **Loudnorm en una pasada deja el pico en -0,5 dBTP.** Dos pasadas (medir y
  aplicar lineal) lo dejan bajo -1.
- 2026-10-30. **Las páginas a 1500 px se ven blandas con zoom 2x.** `producto` las
  convierte a 2200 px de alto.
- 2026-10-30. **Imágenes con IA gratis sin cuenta (Pollinations) no sirven**: modelo
  chico, marca de agua y límite de uso. El material es el producto.
- 2026-10-30. **mixkit.co (las páginas) bloquea con Cloudflare** desde el contenedor;
  los MP3 de assets.mixkit.co sí bajan. Por eso se usa el catálogo ya medido.
- 2026-10-30. **Piper pronuncia mal "anfitrión"** (whisper oyó "anfitrirón" y "aficirón"
  en tres redacciones). Se reescribe la frase sin esa palabra.
- 2026-10-30. **Whisper escribe los números en cifras** ("de 1 a 6") aunque el guion diga
  "uno a seis": `palabras.py` los pasa a letras (0-20) antes de comparar, y la compuerta
  compara por letras, no por palabras ("Do Re Mi" → "do -remy").
- 2026-10-30. **El zoom a un foco cerca del borde destapaba el fondo** dentro del marco.
  `camara()` limita el corrimiento a (1 - 1/zoom)/2 del tamaño.
