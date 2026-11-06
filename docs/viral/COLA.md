# Cola de Shorts sin publicar

Desde el 4-nov a las 20:45, Metricool no publica nada: el plan gratis trae 20 publicaciones por mes, sumando YouTube y Pinterest, y el cupo vuelve el 1-dic. Mientras tanto los Shorts salen por Zapier YouTube (YouTubeV4CLIAPI), conectado por Cris el 5-nov (conexión 02a955fd-378a-82f8-8741-787af2820624). La acción es `upload_video`: la URL raw del commit va en `video`, y además se pasan title, description, tags, privacy_status public, made_for_kids false, category_id (10 música, 24 entretenimiento) y default_language. Zapier sube de inmediato: `publish_at` es solo para cuentas Partner. Se sube de arriba hacia abajo y, al subir cada uno, se borra su línea y se registra con `experimento.py alta`.

| # | Plan | Render (URL raw fija) | Hipótesis | Nota |
|---|---|---|---|---|
(vacía: el Beethoven ES salió el 5-nov a las 17:21 Chile por Zapier, 6TOTGMLBNLc)

## Pendientes para los próximos Shorts (6-nov)
- G-034 (según Gemini, sin verificar) oye 5 errores de pronunciación de Piper en el caso 01 ES: "parecina" (s 12), "policiga" (s 16), "didas" (s 18), "basilo" por vacío (s 26), "lizó" por hizo (s 39). Comprobar con whisper sobre el render y, si son reales, meterlos en "pronuncia" o cambiar la palabra.
- G-032: esqueleto de 45 s con [HECHO 1] [HECHO 2] [GIRO] y cierre sin CTA hablado (texto fijo "Caso de ficción en SheetSmithChile (Etsy)"). G-036 (guion del caso 02 ES) y G-037 (pronunciación) llegan el 7-nov por el hilo Gemini.
- Para V16: `"llenar": "pantalla"` con fotos de buena resolución.
- Video IA pagado (6-nov, hilo "Conectar Google Flow para videos"): Google Flow descartado (sin API; los MCP no oficiales piden la sesión de Google de Cris + reCAPTCHA). Pendiente que Cris decida activar los US$10/mes de créditos Cloud de AI Pro para `gemini.py video --pago` (Omni Flash, tope US$9, ~11-16 tomas de 8 s). Hasta que ese hilo avise del OK: nada de video pagado. Si llega: B-roll en un Short, medido como hipótesis V16 (dinamismo visual). Detalle: /mnt/project-files/plan/investigacion/2026-11-06-google-flow.md.
