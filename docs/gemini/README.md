# Gemini (Google AI Studio) en el pipeline

Decidido 2026-10-30, hilo "Usar la cuenta Google AI Pro desde Claude". Cris pidió usar su
Google AI Pro desde Claude.

## Qué se puede y qué no (leído en ai.google.dev el 2026-10-30)

| Herramienta | ¿Desde Claude? | Cómo | Costo |
|---|---|---|---|
| Gemini texto (3.6 Flash por defecto; respaldo 3.8 Flash y 3.5 Flash-Lite) | Sí | API key de AI Studio, `gemini.py texto` | Gratis (free tier, con límite diario por proyecto) |
| Gemini TTS (3.8 Flash TTS, 130+ idiomas, 30 voces, estilo por turno, 2 voces) | Sí | `gemini.py voz` / `dialogo`, o `"voz": "gemini:Charon"` en un plan | Gratis (free tier) |
| Imágenes (Nano Banana 2 Lite, 2.1, Pro) | Sí | `gemini.py imagen --pago` | Pagado: ~US$0,034 por imagen 1K |
| Video (Gemini Omni Flash; Veo 3.1 preview se apagó el 22-oct-2026) | Sí | `gemini.py video --pago` | Pagado: ~US$0,10 por segundo 720p |
| Música (Lyria 3.5) | Sí, no implementado | — | Pagado: US$0,04-0,08 por canción |
| Créditos de Google AI Pro | Sí, si Cris los activa | US$10/mes de Google Cloud, se aplican primero a la API | Gratis mientras no se pasen; piden facturación activa con tarjeta |
| Cuotas altas de AI Pro (Gemini Pro, Nano Banana, Flow, Veo en la app) | No | Solo valen dentro de las apps y de AI Studio web | — |
| NotebookLM (audio y video overviews) | No por vía oficial | La API de NotebookLM Enterprise es de Google Cloud pagado; la de consumo solo con `notebooklm-py` (cookies, riesgo de baneo de la cuenta que entrega las planillas). Se reemplaza con `gemini.py dialogo` (podcast a 2 voces). | — |
| Gemini CLI | Sí, con la misma clave | `npx @google/gemini-cli` con GEMINI_API_KEY | Gratis (free tier) |

Lo que el plan AI Pro NO da: una API key ni cuota de API. Los créditos de US$10 son
la única parte que llega a la API.

## Configuración (una vez)

1. Cris crea la clave con su cuenta de Google AI Pro: https://aistudio.google.com/apikey
   ("Create API key"). Es la vía oficial: no hay riesgo de baneo.
2. La pega como variable de entorno `GEMINI_API_KEY` en la configuración del entorno del
   proyecto (Project settings → Cloud environment → engranaje). No se pega en el chat.
3. Probar: `python3 -I scripts/gemini/gemini.py estado`.

Opcional y con OK de Cris (regla de plata): activar los créditos en
https://developers.google.com/program/my-benefits, activar la facturación del proyecto de
la clave y subir `tope_mes_usd` en `config.json` (máximo 9, para no salir de los US$10).

## Prueba real (2026-10-30, clave de Cris)

- `estado`: 60 modelos visibles; texto, voz, imagen y video del config aparecen.
- Texto: 3.6 Flash y 3.5 Flash-Lite responden en 2-4 s. 3.8 Flash colgó 60 s y luego dio
  503 "high demand": por eso va de respaldo y no de principal. Los 2.5 ya no se abren a
  cuentas nuevas (404).
- Voz: 3.8 Flash TTS, voz Charon con estilo, 6,3 s de audio en ~4 s; faster-whisper la
  transcribió 11/11 palabras (similitud 1,0). Diálogo Kore + Charon: OK.
- Whisper escribe los años en cifras ("1987") aunque la voz los diga bien: baja la
  similitud de la compuerta de `short`; no es un error de la voz.

## Reglas

- Imagen y video solo con `--pago` y si el tope del mes alcanza; cada llamada queda en
  `gasto.csv`. El tope parte en 0.
- Free tier: Google puede usar lo enviado para mejorar sus productos. No mandar datos de
  compradores ni las soluciones de los juegos.
- Una imagen o video de IA en un listing de Etsy o un Short va marcado como contenido IA
  (YouTube: `isAiGeneratedContent`). La foto principal del listing sigue mostrando el
  producto real.
- Los modelos cambian rápido: si un id deja de existir, `estado` lo dice; corregir `config.json`.

## Usos previstos

- Voz ES de mejor calidad que Piper para los Shorts de historia (A/B con el loop viral:
  una variable por vez).
- Segundo modelo que resuelve a ciegas los juegos (regla de calidad) y revisa copy.
- Con créditos: escenas cortas de ambiente (B-roll) para los Shorts de cold case, fondos
  de portada.
