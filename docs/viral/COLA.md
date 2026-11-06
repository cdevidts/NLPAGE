# Cola de Shorts sin publicar

Desde el 4-nov a las 20:45, Metricool no publica nada: el plan gratis trae 20 publicaciones por mes, sumando YouTube y Pinterest, y el cupo vuelve el 1-dic. Mientras tanto los Shorts salen por Zapier YouTube (YouTubeV4CLIAPI), conectado por Cris el 5-nov (conexión 02a955fd-378a-82f8-8741-787af2820624). La acción es `upload_video`: la URL raw del commit va en `video`, y además se pasan title, description, tags, privacy_status public, made_for_kids false, category_id (10 música, 24 entretenimiento) y default_language. Zapier sube de inmediato: `publish_at` es solo para cuentas Partner. Se sube de arriba hacia abajo y, al subir cada uno, se borra su línea y se registra con `experimento.py alta`.

| # | Plan | Render (URL raw fija) | Hipótesis | Nota |
|---|---|---|---|---|
(vacía: el Beethoven ES salió el 5-nov a las 17:21 Chile por Zapier, 6TOTGMLBNLc)

## Pendientes para los próximos Shorts (6-nov)
- G-034 (según Gemini, sin verificar) oye 5 errores de pronunciación de Piper en el caso 01 ES: "parecina" (s 12), "policiga" (s 16), "didas" (s 18), "basilo" por vacío (s 26), "lizó" por hizo (s 39). Comprobar con whisper sobre el render y, si son reales, meterlos en "pronuncia" o cambiar la palabra.
- G-032: esqueleto de 45 s con [HECHO 1] [HECHO 2] [GIRO] y cierre sin CTA hablado (texto fijo "Caso de ficción en SheetSmithChile (Etsy)"). G-036 (guion del caso 02 ES) y G-037 (pronunciación) llegan el 7-nov por el hilo Gemini.
- Para V16: `"llenar": "pantalla"` con fotos de buena resolución.
- Video IA pagado ACTIVO (6-nov 22:05 UTC, hilo "Conectar Google Flow para videos"): Cris ligó la facturación (pagó US$30 de saldo + créditos AI Pro US$10/mes). `gemini.py video --pago` con gemini-omni-1.2-flash (~US$0.07/s 720p, 10 s por toma, tope US$9/mes en docs/gemini/config.json). Tomas para el Short del caso 02 ES: public/ia/57-caso02-es-1.mp4 (8 s, 3 tomas: hotel en ventisca 0-2,5 s, mesa de la gala 2,5-5,5 s, ventana escarchada 5,5-8 s; ficha docs/video-ia/fichas/57-caso02-es-1.json; escalar 104% la toma 1) y public/ia/caso02-lodge-noche.mp4 (10 s, una toma, hecha sin ficha: cabaña chica, no es el hotel del caso; usar solo de relleno). Toda toma nueva: skill video-ia-prompteo. Medir como V16 (dinamismo visual): 2-3 tomas IA por Short vs fotos con zoom. Cada peso tiene que verse en vistas: Cris lo exigió.
