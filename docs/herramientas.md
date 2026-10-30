# Herramientas gratis: qué se probó y qué quedó (2026-10-30)

Criterio de Cris: gratis, como máximo una cuenta nueva, nada en su computador ni su
Chrome. Todo lo adoptado corre en el contenedor sin cuenta.

## Adoptadas

| Necesidad | Herramienta | Prueba | Nota |
|---|---|---|---|
| Voz IA inglés | **Kokoro-82M** (`kokoro-js`, ONNX q8, CPU) | 6,3 s de voz en ~6 s; whisper la transcribe palabra por palabra | Apache 2.0. Voz `af_heart` (nota A en su tabla). Solo inglés en la versión JS. |
| Voz IA español | **Piper** `es_MX-claude-high` (pip `piper-tts`) | Whisper la transcribe completa; `es_MX-ald-medium` se equivocó en "culpable" | Voz entrenada con dataset Apache 2.0. Modelo 63 MB desde Hugging Face. |
| Tiempos de palabra / revisión | **faster-whisper** (`base.en`, `small`) | Tiempos por palabra para los subtítulos y GUION.md de cada render | MIT. Ojo: PyAV del sistema no acepta archivos; se le pasa el audio ya decodificado. |
| Música | **incompetech.com** (Kevin MacLeod) | `pieces.json` con 1.443 piezas, ánimo y bpm; MP3 directos | CC BY 4.0: el crédito va en la descripción (lo escribe `short`). |
| Música propia | Pistas de práctica del producto (piano) | Jingle Bells del libro #60 de cama del Short de piano | Nuestra: sin Content ID. |
| Efectos | Catálogo medido de **Mixkit** (de Videos-Next-Layer) | 253 efectos con pico, ataque, nivel y brillo; MP3 de assets.mixkit.co bajan bien | Licencia Mixkit, sin atribución. |
| Íconos | **Iconify** API | SVG por URL, sin llave | Sets MIT/Apache (Phosphor por defecto). |
| Tipografías | **Google Fonts** CSS2 → woff2 en el repo | Oswald, Special Elite, Playfair Display, Inter | OFL. En el repo porque el Chrome del render puede no tener red. |
| Video | **Remotion 4** + Chromium del entorno | Short de 35 s en ~90 s de render | Licencia gratis para personas y empresas de hasta 3 personas. |

## Probadas y descartadas (por ahora)

| Herramienta | Por qué no |
|---|---|
| Pollinations (imágenes IA sin cuenta) | El plan anónimo usa un modelo chico, pone marca de agua y responde 503 por límite. La imagen de prueba no servía. |
| Páginas de mixkit.co (buscar música/efectos nuevos) | Cloudflare responde 429 "Just a moment" al contenedor. Los MP3 sí bajan, así que se usa el catálogo ya medido. |
| FreePD | Sitio cerrado. |
| Pixabay música, Chosic | 403 desde el contenedor; Pixabay además pide llave. |
| Freesound | 403, y la API pide cuenta. |
| Openverse audio | Sin respuesta (timeout) desde el contenedor. |
| edge-tts (voces de Microsoft) | No probado a propósito: usa un endpoint privado del navegador Edge; los términos no lo cubren para uso comercial. Kokoro y Piper alcanzan. |
| Coqui XTTS | Licencia no comercial. |

## Pendientes de probar
- Imágenes IA en Spaces de Hugging Face (FLUX.1-schnell por gradio_client, cuota anónima chica) si un video pide una imagen que el producto no tiene.
- Lottie animados (LottieFiles GraphQL y Noto Emoji animado), ya implementado en Videos-Next-Layer: sumar como `sticker` cuando un video lo pida.
- Publicar en YouTube: conector Metricool (falta que Cris conecte el canal). Alternativa sin Metricool: YouTube Data API, que pide un proyecto de Google Cloud y OAuth de Cris.

## Agregada 2026-10-30: Gemini API (cuenta Google AI Pro de Cris)

`scripts/gemini/gemini.py`: texto y voz gratis (free tier), imagen y video pagados con tope
mensual en `docs/gemini/config.json` (parte en 0). Necesita `GEMINI_API_KEY` en el entorno.
Probado contra un servidor falso con las formas de respuesta de la documentación; falta la
prueba real cuando esté la clave. Detalle y decisiones en `docs/gemini/README.md`.
