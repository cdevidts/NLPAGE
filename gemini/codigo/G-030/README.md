# G-030 · Recorte de prensa 1987 (plantilla HTML + envejecido Pillow)

Entregado por Gemini el 2026-11-04 (tarea G-030) y verificado acá el 2026-11-05. Solo marcadores: sin texto de ningún caso.

```bash
# 1. Llenar {{DIARIO}} {{FECHA}} {{CIUDAD}} {{TITULAR}} {{BAJADA}} {{CUERPO}} {{PIE_FOTO}} {{PAGINA}} (CUERPO = párrafos <p>)
# 2. Render a 300 DPI con Playwright (150 mm = 567 px CSS; x3.125 = 1772 px)
node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:567,height:813},deviceScaleFactor:3.125});await p.goto('file://'+process.argv[1]);await p.screenshot({path:process.argv[2],fullPage:true});await b.close();})()" relleno.html limpio.png
# 3. Envejecer (valores por defecto = 1987; ver --help; receta 1936 en plan/investigacion/2026-11-05-gemini-G-030-*)
python3 envejecer.py limpio.png demo.png
```
