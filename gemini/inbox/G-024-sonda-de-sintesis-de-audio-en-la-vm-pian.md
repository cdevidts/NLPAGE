---
id: G-024
titulo: Sonda de síntesis de audio en la VM: piano Jingle Bells de 15 s y radio con Morse
pedido: 2026-11-03
hilo: Conversar con Gemini a través del repo
herramienta: texto
entrega: audio
estado: pendiente
prioridad: normal
---
## Contexto
En G-020 propusiste probar síntesis de audio en la VM. Nos sirve para dos cosas: pistas de piano de práctica para los Shorts de partituras y efectos diegéticos para los Cold Cases (radio con estática, Morse). Sin búsqueda web. Nada de solución de ningún caso.

## Qué quiero
1. Inventario: en default_api:execute_bash, di qué hay de ffmpeg, sox, fluidsynth, timidity, lilypond, numpy, scipy, soundfile, pydub, wave. Versión exacta de cada uno o "no está".
2. Genera con Python puro (numpy + wave o scipy.io.wavfile) un WAV de 15 s a 44,1 kHz con la melodía de Jingle Bells (estribillo: E E E · E E E · E G C D E) con envolvente tipo piano (ataque corto, decaimiento exponencial) + acordes simples (C, F, G7) debajo, a 120 BPM. Si hay ffmpeg, conviértelo a MP3 192 kbps. Sube `G-024 jingle-bells-piano.wav` (y .mp3 si se puede) a Entregas.
3. Genera 10 s de "radio policial de 1987": ruido rosa filtrado + un tono Morse a 700 Hz que diga `SOS` tres veces con timing estándar + un chasquido al inicio y al final. Sube `G-024 radio-morse.wav`.
4. Mide con Python: duración, pico en dBFS y RMS en dBFS de cada archivo; en el Doc, tabla con esos datos y el código completo.

## Formato de la respuesta
Español. Doc `G-024 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas. Máximo 1.000 palabras + código.
