# G-033 · Certificado de detective (plantilla HTML + sello)

Entregado por Gemini (app, Argon) el 2026-11-05 y verificado acá el 2026-11-06.

- `certificado-detective.html`: carta apaisada 279 × 216 mm, marcadores `{{IDIOMA}} {{TITULO}} {{NOMBRE}} {{CASO}} {{FECHA}} {{FIRMA_CARGO}} {{TEXTO}} {{SELLO}}`. `{{NOMBRE}}` vacío deja el renglón para escribir a mano. Los rótulos fijos de cabecera y pie están en inglés (FORM 87-CR, HOMICIDE & COLD CASE INVESTIGATION BUREAU, OFFICIAL FILING DATE, firma R. Vance): traducirlos a mano para la versión en español.
- `sello.py`: estampa un sello rojo rotado sobre un PNG. `python3 -I sello.py --input a.png --output b.png --sello "CASO CERRADO" --subtexto "ARCHIVO POLICIAL • 1987" [--angle -13.5 --alpha 0.72 --x 0.76 --y 0.24]`. 2 s.
- `demo-es-sello.png`: demo en español renderizada acá (1054 × 816, revisión); el PDF vectorial sale con Playwright `page.pdf({width:'279mm', height:'216mm', printBackground:true, margin:0})`.

Render: rellenar los marcadores con `re.sub(r'\{\{(\w+)\}\}', ...)` y abrir con Playwright (`chromium.launch()`, viewport 1054 × 816 para revisar; `deviceScaleFactor: 3.125` para 300 DPI). Demos a 300 DPI de Gemini en Drive > Gemini > Entregas (`G-033 certificado-demo-en.png`, `-es.png`, `-en.pdf`).
